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


from procrustes.base import Procrustes
from procrustes.utils import eigenvalue_decomposition, singular_value_decomposition
from procrustes.procrustes_orthogonal import OrthogonalProcrustes
import numpy as np
from itertools import product


class TwoSidedOrthogonalSingleTransformationProcrustes(Procrustes):

    r"""
    This method deals with the two-sided orthogonal Procrustes problem limited to
    a single transformation. Given a symmetric :math: `n \times n` matrix :math:`A`
    and a reference :math:`n \times n` math:`A^0`, find two unitary\orthogonal transformation
    of :math:`A` that makes it as close as possible to :math:`A^0`. I.e.,

    .. math::
       \begin{array}{c}
       \underbrace {\min }_{\left\{ {{\bf{U}}\left| {{\bf{U}}_{}^{ - 1} =
       {\bf{U}}_{}^\dagger } \right.}
       \right\}}\left\| {{\bf{U}}_{}^\dagger {\bf{A}}{{\bf{U}}_{}} - {{\bf{A}}^0}} \right\|_F^2 =
       \underbrace {\min        }_{\left\{ {{\bf{U}}\left| {{\bf{U}}_{}^{ - 1} =
       {\bf{U}}_{}^\dagger } \right.}        \right\}}{\mathop{\rm Tr}\nolimits} \left[
       {\left( {{\bf{U}}_{}^\dagger {\bf{AU}}        - {{\bf{A}}^0}} \right)_{}^\dagger \left(
       {{\bf{U}}_{}^\dagger {\bf{A}}{{\bf{U}}_{}}        - {{\bf{A}}^0}} \right)} \right]\\
       = \underbrace {\max }_{\left\{ {{\bf{U}}\left| {{{\bf{U}}^{ - 1}} =
       {\bf{U}}_{}^\dagger } \right.} \right\}}{\mathop{\rm Tr}\nolimits}
       \left[{{\bf{U}}_{}^\dagger{\bf{A}}_{}^\dagger{{\bf{U}}_{}}{{\bf{A}}^0}} \right]
       \end{array}

    The solution is obtained by taking the eigenvalue decomposition of the matrices

    .. math::
       {\bf{A}} = {{\bf{U}}_A}{\Lambda _A}{\bf{U}}_A^\dagger \\
       {{\bf{A}}^0} = {{\bf{U}}_{{A^0}}}{\Lambda _{{A^0}}}{\bf{U}}_{{A^0}}^\dagger\\
       {\bf{U}} = {\bf{U}}_A^{}{\bf{SU}}_{{A^0}}^\dagger

    where :math:`S` is a diagonal matrix for which every diagonal element is :math:`\pm{1}`,

    .. math::
       {\bf{S}} = \left[ {\begin{array}{*{20}{c}}
       { \pm 1}&0& \cdots &0\\
       0&{ \pm 1}& \ddots & \vdots \\
       \vdots & \ddots & \ddots &0\\
       0& \cdots &0&{ \pm 1}
       \end{array}} \right]

    Choose the choce of :math:`S` required :math:`2^n` trial-and-error tests.

    A heuristic, due to Umeyama, is to take the element-wise absolute value of the elements
    of the unitary transformations,

    .. math::
       {{\bf{U}}_{{\rm{Umeyama}}}} = {\rm{abs}}\left( {{\bf{U}}_A^{}} \right) \cdot
       {\rm{abs}}\left( {{\bf{U}}_{{A^0}}^\dagger } \right)

    This is not actually a unitary matrix. But we can use the orthogonal procrustes problem
    to find the closest unitray matrix (i.e., the closest matrix that is unitarily equivalent
    to the identity matrix),

    .. math::
       \begin{array}{c}
       \underbrace {\min }_{\left\{ {{\bf{U}}\left| {{{\bf{U}}^{ - 1}} =
       {\bf{U}}_{}^\dagger } \right.}  \right\}}\left\| {{\bf{IU}} -
       {{\bf{U}}_{{\rm{Umeyama}}}}} \right\|_F^2 = \underbrace {\min }_{\left\{{{\bf{U}}\left|
       {{{\bf{U}}^{ - 1}} = {\bf{U}}_{}^\dagger } \right.}\right\}}{\mathop{\rm Tr}\nolimits}
       \left[ {\left( {{\bf{U}} -{{\bf{U}}_{{\rm{Umeyama}}}}} \right)_{}^\dagger
       \left( {{\bf{U}} - {{\bf{U}}_{{\rm{Umeyama}}}}} \right)} \right]\\
       = \underbrace {\max }_{\left\{ {{\bf{U}}\left| {{{\bf{U}}^{ - 1}} =
       {\bf{U}}_{}^\dagger } \right.} \right\}}{\mathop{\rm Tr}\nolimits}
       \left[{{\bf{U}}_{}^\dagger {{\bf{U}}_{{\rm{Umeyama}}}}} \right]
       \end{array}

    with solution given by Eqs.(2)-(3). I.e.m making the singular value decomposition of
    :math:`{U}_{Umeyama}` ,

    .. math::
       {{\bf{U}}_{{\rm{Umeyama}}}} = {\bf{\tilde U}}\tilde \Sigma {\bf{\tilde V}}_{}^\dagger
       {\bf{U}}_{{\rm{Umeyama}}}^{\left( {{\rm{approx}}{\rm{.}}} \right)} =
       {\bf{\tilde U\tilde V}}_{}^\dagger

    **Note**

    Map_a_to_b is set to True by default. For the two-sided single transformation procrustes
    analyses, this is crucial
    for accuracy. When set to False, the input arrays both undergo centroid translation to
    the origin and Frobenius normalization, prior to further analysis. Something about
    this transformation skews the accuracy of the results.
    """

    def __init__(self, array_a, array_b, translate=False, scale=False):

        Procrustes.__init__(self, array_a, array_b,
                            translate=translate, scale=scale)

        if (abs(self.array_a - self.array_a.T) > 1.e-10).all() or
            (abs(self.array_b - self.array_b.T) > 1.e-10).all():
            raise ValueError(
                'Arrays array_a and array_b must both be symmetric for this analysis.')

    def calculate(self, return_u_approx=False, return_u_best=True, tol=1.e-12):
        """
        Calculates the single optimum two-sided orthogonal transformation matrix in the
        double-sided procrustes problem

        Parameters
        ----------
        array_a : ndarray
            A 2D array representing the array to be transformed (as close as possible to array_b)

        array_b : ndarray
            A 2D array representing the reference array

        Returns
        ----------
        u_umeyama_approx, array_transformed, error
        u_umeyama_approx = the optimum orthogonal transformation array satisfying the double
             sided procrustes problem. Array represents the closest orthogonal array to
             u_umeyama given by the orthogonal procrustes problem
        array_transformed = the transformed input array after transformation by u_umeyama_approx
        error = the error as described by the double-sided procrustes problem
        """
        if return_u_approx:
            # Calculate the eigenvalue decomposition of array_a and array_b
            sigma_a, u_a = eigenvalue_decomposition(
                self.array_a, two_sided_single=True)
            sigma_a0, u_a0 = eigenvalue_decomposition(
                self.array_b, two_sided_single=True)
            # Compute u_umeyama
            u_umeyama = np.multiply(abs(u_a), abs(u_a0).T)
            # Compute u_umeyama_approx using orthogonal procrustes analysis
            n, m = u_umeyama.shape
            ortho = OrthogonalProcrustes(np.eye(n), u_umeyama)
            # u_approx, array_transformed_ortho, error_ortho = ortho.calculate()
            ortho.array_u[abs(ortho.array_u) < 1.e-8] = 0
            # Calculate the error
            error_approx = self.double_sided_error(
                ortho.array_u, ortho.array_u)
            # Calculate the transformed input array
            array_transformed_approx = np.dot(self.array_a, ortho.array_u)

        if return_u_best:
            # svd of each array
            u_a, sigma_a, v_trans_a = singular_value_decomposition(
                self.array_a)
            u_a0, sigma_a0, v_trans_a0 = singular_value_decomposition(
                self.array_b)
            n, m = self.array_a.shape
            assert(n == m)
            # Compute all 2^n combinations of diagonal n x n matrices where diagonal elements are
            # from the set {-1,1}
            diag_vec_list = list(product((-1., 1.), repeat=n))
            error_best = 1.e5  # Arbitrarily initialize best error
            """
            Iterate until all possible combinations have been checked, and choose trial with the
            least error. If any iteration produces error less than the tolerance, stop the loop
            and choose this trial.
            """
            for i in range(2**n):
                # Compute the trial's optimum transformation array
                u_trial = np.dot(
                    np.dot(u_a, np.diag(diag_vec_list[i])), u_a0.T)
                # And the trial's corresponding error:
                error = self.double_sided_error(u_trial, u_trial)
                if error < tol:
                    u_best = u_trial
                    error_best = error
                    break
                if error < error_best:
                    u_best = u_trial
                    error_best = error
                else:
                    continue
            array_transformed_best = np.dot(
                np.dot(u_best.T, self.array_a), u_best)

        if return_u_approx and return_u_best:
            if error_approx >= error_best:
                u_best = u_best
                error_best = error_best
            else:
                u_best = ortho.array_u
                error_best = error_approx
            print " You've selected both the Umeyaman and exact transformations."
            print "Output order: u_approx, u_best, array_transformation_approx_exact,"
            print "array_transformation_exact, error_approx, error_best, translate_and_or_scaling:"
            return ortho.array_u, u_best, array_transformed_approx, array_transformed_best,
                   error_approx, error_best

        elif return_u_approx:
            print "You've selected the Umeyaman approximation."
            print 'The input 2D arrays are {0} and {1}.\n'.format(self.array_a.shape, self.array_b.shape)
            return ortho.array_u, array_transformed_approx, error_approx

        elif return_u_best:
            print "You've selected the best transformation. "
            print 'The input 2D arrays are {0} and {1}.\n'.format(self.array_a.shape, self.array_b.shape)
            return u_best, array_transformed_best, error_best

        else:
            print "Cannot complete analysis. You must select at least one transformation."
