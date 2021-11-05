import unittest

from energy_barrier.file_io.tecplot import read_tecplot
from energy_barrier.calculations.energies import compute_field_integrals
from energy_barrier.calculations.energies import path_energies


class Test_compute_field_integrals(unittest.TestCase):
    def test_one(self):
        field_data = read_tecplot("/data/Dropbox/MyPapers/trm_paper/cubo030/100nm/magnetite_20C/cde6aa20-79b6-4d54-aca7-de73c02c7180.tec")
        field_integrals = compute_field_integrals(field_data)
        print(field_integrals)


class Test_compute_path_energies(unittest.TestCase):
    def test_one(self):
        field_data = read_tecplot("/data/Dropbox/MyPapers/trm_paper/cubo030/100nm/magnetite_20C/cde6aa20-79b6-4d54-aca7-de73c02c7180.tec")
        field_integrals = compute_field_integrals(field_data)
        path = path_energies(20, 1.0, 1.0, 1.0, 0.0, "mT", field_integrals)

        for key, value in path.items():
            print(f"{key}\t{value}")
