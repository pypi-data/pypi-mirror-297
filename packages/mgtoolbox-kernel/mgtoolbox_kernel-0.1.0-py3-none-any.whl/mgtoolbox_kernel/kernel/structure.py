# -*- encoding: utf-8 -*-
"""
    @File    :   structure.py
    @Time    :   2021/04/30 15:49:14
    @Author  :   何冰 
    @Email   :   shhebing@qq.com
    @WebSite :   https://mgtoolbox.cn
    @Desc    :   材料结构相关类。
"""
import re
from typing import Dict, List, Union
from pathlib import Path

import numpy as np
import scipy.spatial
from mgtoolbox_kernel.io import read_structure_file, read_structure_data
from .mgclass import MGobject
from .atom import Atom
from .cell import Cell
from .site import Site


class Structure(MGobject):
    def __init__(self, sites: List[Site], cell: Cell, attributes=None):
        if attributes is None:
            attributes = {}
        super().__init__(attributes)
        self.sites: List[Site] = sites
        self.cell: Cell = cell

    def __repr__(self) -> str:
        sstring = str({"cell": self.cell, "sites": self.sites})
        return sstring

    def add_site(self, site: Site):
        self.sites.append(site)

    def add_sites(self, sites: List[Site]):
        self.sites += sites

    def remove_sites(self, sites: List[Site]):
        for site in sites:
            self.sites.remove(site)

    def set_cell(self, cell: Cell):
        self.cell = cell

    @property
    def is_ordered(self):
        """是否为有序结构

        Returns
        -------
        bool
            是否有序
        """
        return all((site.is_ordered for site in self.sites))

    @staticmethod
    def from_file(filename: Union[str, Path]) -> Union["Structure", List["Structure"]]:
        structs_mode = read_structure_file(filename)
        structs = []
        for struct_mode in structs_mode:
            struct = Structure.from_struct_model(struct_mode)
            structs.append(struct)
        if len(structs) == 1:
            return structs[0]
        else:
            return structs

    @staticmethod
    def from_data(file_data: str):
        # 默认cif格式文件数据
        structs_mode = read_structure_data(file_data)
        structs = []
        for struct_mode in structs_mode:
            struct = Structure.from_struct_model(struct_mode)
            structs.append(struct)
        if len(structs) == 1:
            return structs[0]
        else:
            return structs

    @staticmethod
    def merge_eq_coords(coords):
        Structure.adjust_coords(coords)
        dm = scipy.spatial.distance_matrix(coords, coords)
        type_list = list(range(dm.shape[0]))
        for row in range(dm.shape[0]):
            for col in range(row + 1, dm.shape[1]):
                if dm[row][col] < 0.003:
                    type_list[col] = type_list[row]
        unique_ids = set(type_list)
        ucoords = coords[list(unique_ids)]
        return ucoords

    @staticmethod
    def adjust_coords(coords):
        """调整分数坐标值
        使得分数坐标值在0.999-1.001范围的坐标更改为0.0
        Parameters
        ----------
        coords : _type_
            _description_
        """
        abs_value = np.abs(coords - 1.0)
        coords[abs_value < 0.001] = 0.0

    @staticmethod
    def from_struct_model(struct_mode: Dict):
        lattice_paramteters = struct_mode["lattice_parameters"]
        cell = Cell(
            lattice_paramteters[0],
            lattice_paramteters[1],
            lattice_paramteters[2],
            lattice_paramteters[3],
            lattice_paramteters[4],
            lattice_paramteters[5],
        )
        attributes = struct_mode['attributes']
        sites = []
        for struct_site in struct_mode["sites"]:
            coords = np.mod(
                np.dot(struct_mode["symm_ops"][0], struct_site["coord"])
                + struct_mode["symm_ops"][1],
                1.0,
            )
            # 合并等价位点中坐标相同位点
            # Merge the points with the same coordinates in the equivalent points
            ucoords = Structure.merge_eq_coords(coords)
            for i, coord in enumerate(ucoords):
                occupier = {}
                for symbol, occupy in struct_site["occupancy"].items():
                    if occupy < 0.0:
                        raise ValueError("Structure file site occupy value error")
                    sym = re.findall(r"[A-Z][a-z]?", symbol)
                    if struct_mode["oxidation_state"]:
                        atom = Atom(sym[0], struct_mode["oxidation_state"][symbol])
                        occupier[atom] = occupy
                    else:
                        # -16 表示该离子化合价无法确定。
                        atom = Atom(sym[0], -16)
                        occupier[atom] = occupy
                site = Site(coord, occupier)
                site.label = struct_site["label"] + "_" + str(i)
                site.type = struct_site["site_type"]
                sites.append(site)
        unique_sites = Structure.remove_duplicates_sites(sites)
        return Structure(unique_sites, cell, attributes)

    @staticmethod
    def remove_duplicates_sites(sites: List[Site]):
        result = []
        for item in sites:
            if item not in result:
                result.append(item)
            else:
                result[result.index(item)].assign_occupier_by_dict(item.occupier)
        return result

    def write_to_cif(self, filename: str):
        with Path(filename).open("+w") as f:
            f.write(f"data_{Path(filename).stem}\n")

            f.write("_cell_length_a       {}\n".format(self.cell.abc[0]))
            f.write("_cell_length_b       {}\n".format(self.cell.abc[1]))
            f.write("_cell_length_c       {}\n".format(self.cell.abc[2]))

            f.write("_cell_angle_alpha    {}\n".format(self.cell.angles[0]))
            f.write("_cell_angle_beta     {}\n".format(self.cell.angles[1]))
            f.write("_cell_angle_gamma    {}\n".format(self.cell.angles[2]))

            f.write("_symmetry_space_group_name_H-M    'P 1'\n")
            f.write("_symmetry_Int_Tables_number        1\n")

            f.write("loop_\n")
            f.write("_symmetry_equiv_pos_site_id\n")
            f.write("_symmetry_equiv_pos_as_xyz\n")
            f.write("1        'x, y, z'\n")

            f.write("loop_\n")
            f.write("_atom_site_label\n")
            f.write("_atom_site_type_symbol\n")
            f.write("_atom_site_fract_x\n")
            f.write("_atom_site_fract_y\n")
            f.write("_atom_site_fract_z\n")
            f.write("_atom_site_occupancy\n")
            for site in self.sites:
                for occupier, occupy in site.occupier.items():
                    f.write(
                        f"{site.label} {occupier.symbol} {site.x} {site.y} {site.z} {occupy}\n"
                    )

            f.write(f"#End of data_{Path(filename).stem}")
