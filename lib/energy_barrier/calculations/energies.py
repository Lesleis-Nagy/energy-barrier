r"""
A collection of routines to calculate structure energies.
"""

from energy_barrier.materials import saturation_magnetization
from energy_barrier.conversion import field_to_tesla

import numpy as np


def integrate_vector(f0, f1, f2, f3, v0, v1, v2, v3):
    r"""
    Integrate a (linearly varying) field over a tetrahedron defined by four vertices
    v0, v1, v3 & v3.
    :param f0: the field quantity at the first vertex v0
    :param f1: the field quantity at the second vertex v1
    :param f2: the field quantity at the third vertex v2
    :param f3: the field quantity at the fourth vertex v3
    :param v0: the first vertex of the tetrahedron
    :param v1: the second vertex of the tetrahedron
    :param v2: the third vertex of the tetrahedron
    :param v3: the fourth vertex of the tetrahedron
    :return: the linearly varying integral of the vector field (defined at four points of
             a tetrahedron) over the tetrahedron of vertices v0, v1, v2 & v3.
    """
    # Tetrahedral volume.
    dxdydz = abs(np.linalg.det(
        np.array([
            [v0[0], v0[1], v0[2], 1.0],
            [v1[0], v1[1], v1[2], 1.0],
            [v2[0], v2[1], v2[2], 1.0],
            [v3[0], v3[1], v3[2], 1.0],
        ])
    ) / 6.0)

    Sfx = ((f0[0] + f1[0] + f2[0] + f3[0]) / 4.0) * dxdydz
    Sfy = ((f0[1] + f1[1] + f2[1] + f3[1]) / 4.0) * dxdydz
    Sfz = ((f0[2] + f1[2] + f2[2] + f3[2]) / 4.0) * dxdydz

    return [Sfx, Sfy, Sfz]


def compute_field_integrals(dom_structs):
    r"""
    For each domain structure of a path, compute Sm_dv - the integral of the (small m) magnetization field over the
    magnetic region.
    :param Hx: the x component of the direction of the applied field
    :param Hy: the y component of the direction of the applied field
    :param Hz: the z component of the direction of the applied field
    :param H: the strength of the applied field
    :param unit: the unit of the applied field.
    :param dom_structs: the domain structures.
    :return: a list of path energies.
    """
    vertices = dom_structs["vertices"]
    elements = dom_structs["elements"]

    fields = dom_structs["fields"]
    field_titles = dom_structs["field_titles"]

    field_integrals = {}
    for field_idx, field in enumerate(fields):
        Sfx = 0.0
        Sfy = 0.0
        Sfz = 0.0
        for elem_idx, elem in enumerate(elements):
            # Vertices at the corners of the element.
            v0 = vertices[elem[0]]
            v1 = vertices[elem[1]]
            v2 = vertices[elem[2]]
            v3 = vertices[elem[3]]

            # Field values at the corners of the element.
            f0 = field[elem[0]]
            f1 = field[elem[1]]
            f2 = field[elem[2]]
            f3 = field[elem[3]]

            Sf = integrate_vector(f0, f1, f2, f3, v0, v1, v2, v3)
            Sfx += Sf[0]
            Sfy += Sf[1]
            Sfz += Sf[2]

        field_title = field_titles[field_idx]
        sf = 1E-18
        field_integrals[field_title] = [sf*Sfx, sf*Sfy, sf*Sfz]

    return field_integrals


def path_energies(T, hx, hy, hz, H, unit, field_integrals, material="magnetite"):
    r"""
    :param T: temperature (associated with field_integrals).
    :param hx:
    :param hy:
    :param hz:
    :param H: field strength
    :param unit:
    :param field_integrals:
    :return:
    """
    mu0 = 1.25663706E-6  # (m kg) / (s^2 A^2)
    Ms = saturation_magnetization(T, material=material)
    H_T = field_to_tesla(H, unit)

    path_energies = {}
    for field_title, Sm_dv in field_integrals.items():
        m_dot_h = Sm_dv[0] * hx + Sm_dv[1] * hy + Sm_dv[2] * hz
        path_energies[field_title] = Ms * H_T * m_dot_h + mu0 * Ms * Ms * m_dot_h

    return path_energies
