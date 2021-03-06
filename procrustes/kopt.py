# -*- coding: utf-8 -*-
# The Procrustes library provides a set of functions for transforming
# a matrix to make it as similar as possible to a target matrix.
#
# Copyright (C) 2017-2021 The QC-Devs Community
#
# This file is part of Procrustes.
#
# Procrustes is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Procrustes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
"""Kopt Module."""

from copy import deepcopy
import itertools as it

import numpy as np
from procrustes.utils import compute_error

__all__ = [
    "kopt_heuristic_single",
    "kopt_heuristic_double",
]


def kopt_heuristic_single(a, b, p=None, k=3, tol=1.0e-8):
    r"""Compute locally optimal permutation matrix and its error using k-opt heuristic.

    Perform k-opt local search with every possible valid combination of the swapping mechanism.

    Parameters
    ----------
    a : ndarray
        The 2D-array :math:`\mathbf{A}` which is going to be transformed.
    b : ndarray
        The 2D-array :math:`\mathbf{B}` representing the reference matrix.
    p : ndarray, optional
        The 2D-array :math:`\mathbf{P}` representing the initial permutation matrix. If `None`, the
        identity matrix is used.
    k : int, optional
        The order of the permutation. For example, `k=3` swaps all possible 3-permutations of the
        given p matrix.
    tol : float, optional
        Convergence threshold of the heuristic algorithm.

    Returns
    -------
    perm : ndarray
        The permutation array after optimal heuristic search.
    error : float
        The error distance of two arrays with the updated permutation array.
    """
    if k < 2 or not isinstance(k, int):
        raise ValueError(f"Argument k must be a integer greater than 2. Given k={k}")
    # assign p to be an identity array, if not specified
    if p is None:
        p = np.identity(np.shape(a)[0])
    num_row = p.shape[0]
    error = compute_error(a, b, p, p)
    # all the possible row-wise permutations
    for comb in it.combinations(np.arange(num_row), r=k):
        for comb_perm in it.permutations(comb, r=k):
            if comb_perm != comb:
                p_new = deepcopy(p)
                p_new[comb, :] = p_new[comb_perm, :]
                error_new = compute_error(a, b, p_new, p_new)
                if error_new < error:
                    p, error = p_new, error_new
                    if error <= tol:
                        break
    return p, error


def kopt_heuristic_double(a, b, p=None, q=None, k=3, tol=1.0e-8):
    r"""
    K-opt kopt for regular two-sided permutation Procrustes to improve the accuracy.

    Perform k-opt local search with every possible valid combination of the swapping mechanism for
    regular 2-sided permutation Procrustes.

    Parameters
    ----------
    a : ndarray
        The 2D-array :math:`\mathbf{A}` which is going to be transformed.
    b : ndarray
        The 2D-array :math:`\mathbf{B}` representing the reference matrix.
    p : ndarray, optional
        The left permutation array which remains to be processed with k-opt local search. Default
        is the identity matrix with the same shape of array_m.
    q : ndarray, optional
        The right permutation array which remains to be processed with k-opt local search. Default
        is the identity matrix with the same shape of array_m.
    k : int, optional
        Defines the oder of k-opt heuristic local search. For example, k=3 leads to a local
        search of 3 items and k=2 only searches for two items locally.
    tol : float, optional
        Tolerance value to check if k-opt heuristic converges.

    Returns
    -------
    perm_kopt_p : ndarray
        The left permutation array after optimal heuristic search.
    perm_kopt_q : ndarray
        The right permutation array after optimal heuristic search.
    kopt_error : float
        The error distance of two arrays with the updated permutation array.
    """
    if k < 2 or not isinstance(k, int):
        raise ValueError(f"Argument k must be a integer greater than 2. Given k={k}")
    # assign p & q to be an identity arrays, if not specified
    if p is None:
        p = np.identity(np.shape(a)[0])
    if q is None:
        q = np.identity(np.shape(a)[0])

    num_row_left = p.shape[0]
    num_row_right = q.shape[0]
    kopt_error = compute_error(a, b, p, q)
    # the left hand side permutation
    # pylint: disable=too-many-nested-blocks
    for comb_left in it.combinations(np.arange(num_row_left), r=k):
        for comb_perm_left in it.permutations(comb_left, r=k):
            if comb_perm_left != comb_left:
                perm_kopt_left = deepcopy(p)
                # the right hand side permutation
                for comb_right in it.combinations(np.arange(num_row_right), r=k):
                    for comb_perm_right in it.permutations(comb_right, r=k):
                        if comb_perm_right != comb_right:
                            perm_kopt_right = deepcopy(q)
                            perm_kopt_right[comb_right, :] = perm_kopt_right[comb_perm_right, :]
                            e_kopt_new_right = compute_error(b, a, p.T,
                                                             perm_kopt_right)
                            if e_kopt_new_right < kopt_error:
                                q = perm_kopt_right
                                kopt_error = e_kopt_new_right
                                if kopt_error <= tol:
                                    break

                perm_kopt_left[comb_left, :] = perm_kopt_left[comb_perm_left, :]
                e_kopt_new_left = compute_error(b, a, perm_kopt_left.T, q)
                if e_kopt_new_left < kopt_error:
                    p = perm_kopt_left
                    kopt_error = e_kopt_new_left
                    if kopt_error <= tol:
                        break

    return p, q, kopt_error
