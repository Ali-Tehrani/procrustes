# -*- coding: utf-8 -*-
# Procrustes is a collection of interpretive chemical tools for
# analyzing outputs of the quantum chemistry calculations.
#
# Copyright (C) 2017-2018 The Procrustes Development Team
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


import numpy as np
from procrustes import PermutationProcrustes
from numpy.testing import assert_almost_equal


def test_permutation_identical():
    # square array
    array_a = np.arange(25).reshape(5, 5)
    # permutation matrix for identical arrays is identity
    perm = PermutationProcrustes(array_a, array_a)
    assert_almost_equal(perm.array_a, array_a, decimal=6)
    assert_almost_equal(perm.array_b, array_a, decimal=6)
    assert_almost_equal(perm.array_p, np.eye(5), decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)
    # rectangular array
    array_a = np.array([[3, 5, 4, 3], [1, 6, 5, 4], [1, 6, 4, 2]])
    # procrustes with no scale and translate
    perm = PermutationProcrustes(array_a, array_a)
    # permutation matrix for identical arrays is identity
    assert_almost_equal(perm.array_a, array_a, decimal=6)
    assert_almost_equal(perm.array_b, array_a, decimal=6)
    assert_almost_equal(perm.array_p, np.eye(4), decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)


def test_permutation_columns():
    # square array
    array_a = np.array([[1, 5, 8, 4], [1, 5, 7, 2], [1, 6, 9, 3], [2, 7, 9, 4]])
    # permutate columns of array a
    array_b = np.array([[8, 4, 5, 1], [7, 2, 5, 1], [9, 3, 6, 1], [9, 4, 7, 2]])
    # corresponding permutation
    permutation = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]])
    # procrustes with no translate and scale
    perm = PermutationProcrustes(array_a, array_b, False, False)
    assert_almost_equal(perm.array_a, array_a, decimal=6)
    assert_almost_equal(perm.array_b, array_b, decimal=6)
    assert_almost_equal(perm.array_p, permutation, decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)
    # padd arrays with zero row and columns
    array_a = np.concatenate((array_a, np.array([[0], [0], [0], [0]])), axis=1)
    array_b = np.concatenate((array_b, np.array([[0, 0, 0, 0]])), axis=0)
    # procrustes with no translate and scale
    perm = PermutationProcrustes(array_a, array_b, False, False)
    assert_almost_equal(perm.array_a, array_a[:, :-1], decimal=6)
    assert_almost_equal(perm.array_b, array_b[:-1, :], decimal=6)
    assert_almost_equal(perm.array_p, permutation, decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)


def test_permutation_translate_scale():
    # square array
    array_a = np.array([[1, 5, 8, 4], [1, 5, 7, 2], [1, 6, 9, 3], [2, 7, 9, 4]])
    # permutation matrix for identical arrays is identity
    perm = PermutationProcrustes(array_a, array_a)
    assert_almost_equal(perm.array_a, array_a, decimal=6)
    assert_almost_equal(perm.array_b, array_a, decimal=6)
    assert_almost_equal(perm.array_p, np.eye(4), decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)
    # array_b is scaled and translated array_a
    array_b = 3.78 * array_a + np.array([6, 1, 5, 3])
    perm = PermutationProcrustes(array_a, array_b, translate=True, scale=True)
    assert_almost_equal(perm.array_a, perm.array_b, decimal=6)
    assert_almost_equal(perm.array_p, np.eye(4), decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)
    # array_b is scaled, translated, and permuted array_a
    permute = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])
    array_b = np.dot(array_b, permute)
    perm = PermutationProcrustes(array_a, array_b, translate=True, scale=True)
    assert_almost_equal(perm.array_p, permute, decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)
    # rectangular array
    array_a = np.array([[118.51, 515.27, 831.61, 431.62], [161.61, 535.13, 763.16, 261.63],
                        [116.31, 661.34, 961.31, 363.15], [236.16, 751.36, 913.51, 451.22]])
    # array_b is scaled, translated, and permuted array_a
    array_b = 51.63 * array_a + np.array([56.24, 79.32, 26.15, 49.52])
    permute = np.array([[0., 0., 0., 1.], [0., 1., 0., 0.], [0., 0., 1., 0.], [1., 0., 0., 0.]])
    array_b = np.dot(array_b, permute)
    # procrustes with translate and scale
    perm = PermutationProcrustes(array_a, array_b, translate=True, scale=True)
    assert_almost_equal(perm.array_p, permute, decimal=6)
    assert_almost_equal(perm.error, 0., decimal=6)