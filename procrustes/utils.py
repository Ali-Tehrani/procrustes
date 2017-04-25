"""
Utility Module.
"""


import numpy as np


def zero_padding(x1, x2, row=False, column=False, square=False):
    """
    Match the number of rows and/or columns of arrays x1 and x2 by
    padding zero rows and/or columns to the array with the smaller dimensions.

    Parameters
    ----------
    x1 : ndarray
        A 2D array
    x2 : ndarray
        A 2D array
    row : bool
        Set to True to match the number of rows by zero-padding; default=True.
    column : bool
        Set to True to match the number of columns by zero-padding; default=False.
    square: bool
        Set to True to zero pad the input arrays such that the inputs become square
        arrays of the same size
    Returns
    -------
    If row = True and Column = False:

         Returns the input arrays, x1 and x2, where the array with the fewer number
         of rows has been padded with zeros to match the number of rows of the other array

    if row = False and column = True

         Returns the input arrays, x1 and x2, where the array with the fewer number
         of columns has been padded with zeros to match the number of columns of the other array

    if row = True and column = True

         Returns the input arrays, x1 and x2, where the array with the fewer rows has been row-padded
         with zeros, and the array with the fewer number of columns has been column-padded with zeros
         in order to match the row/column number of the array with the greatest number of rows/columns.
         The outputs have the same size, and need not be square.

    if squre = True
         Returns the input arrays x1 and x2 zero padded such that both arrays are square and of the same size.
    """
    # Confirm the input arrays are 2d arrays
    # Assertions are a systematic way to check that the internal state of a program is as the
    # programmer expected, with the goal of catching bugs
    # Assertions are a systematic way to check that the internal state of a
    # program is as the programmer expected, with the goal of catching bugs
    assert isinstance(x1, np.ndarray) and isinstance(x2, np.ndarray)
    assert isinstance(x1, np.ndarray) and isinstance(x2, np.ndarray)
    assert x1.ndim == 2 and x2.ndim == 2
    if square:
        if (x1.shape == x2.shape) and (x1.shape[0] == x1.shape[1]):
            print "The arrays are already square and of the same size."
        n_1, m_1 = x1.shape
        n_2, m_2 = x2.shape
        new_dimension = max(n_1, n_2, m_1, m_2)
        # Row pad
        if n_1 < new_dimension:
            pad = np.zeros((new_dimension - n_1, x1.shape[1]))
            x1 = np.concatenate((x1, pad), axis=0)
        if n_2 < new_dimension:
            pad = np.zeros((new_dimension - n_2, x2.shape[1]))
            x2 = np.concatenate((x2, pad), axis=0)
        # Column Pad
        if m_1 < new_dimension:
            pad = np.zeros((new_dimension, new_dimension - m_1))
            x1 = np.concatenate((x1, pad), axis=1)
        if m_2 < new_dimension:
            pad = np.zeros((new_dimension, new_dimension - m_2))
            x2 = np.concatenate((x2, pad), axis=1)

    if x1.shape == x2.shape:
        pass
    else:
        if row and column:
            # operations on rows
            if x1.shape[0] < x2.shape[0]:
                # padding x1 with zero rows
                pad = np.zeros((x2.shape[0] - x1.shape[0], x1.shape[1]))
                x1 = np.concatenate((x1, pad), axis=0)
            elif x1.shape[0] > x2.shape[0]:
                # padding x2 with zero rows
                pad = np.zeros((x1.shape[0] - x2.shape[0], x2.shape[1]))
                x2 = np.concatenate((x2, pad), axis=0)

            # operaations on columns
            if x1.shape[1] < x2.shape[1]:
                # padding x1 with zero columns
                pad = np.zeros((x1.shape[0], x2.shape[1] - x1.shape[1]))
                x1 = np.concatenate((x1, pad), axis=1)
            elif x1.shape[1] > x2.shape[1]:
                # padding x2 with zero columns
                pad = np.zeros((x2.shape[0], x1.shape[1] - x2.shape[1]))
                x2 = np.concatenate((x2, pad), axis=1)

        elif row:
            if x1.shape[0] < x2.shape[0]:
                # padding x1 with zero rows
                pad = np.zeros((x2.shape[0] - x1.shape[0], x1.shape[1]))
                x1 = np.concatenate((x1, pad), axis=0)
            elif x1.shape[0] > x2.shape[0]:
                # padding x2 with zero rows
                pad = np.zeros((x1.shape[0] - x2.shape[0], x2.shape[1]))
                x2 = np.concatenate((x2, pad), axis=0)

        elif column:
            if x1.shape[1] < x2.shape[1]:
                # padding x1 with zero columns
                pad = np.zeros((x1.shape[0], x2.shape[1] - x1.shape[1]))
                x1 = np.concatenate((x1, pad), axis=1)
            elif x1.shape[1] > x2.shape[1]:
                # padding x2 with zero columns
                pad = np.zeros((x2.shape[0], x1.shape[1] - x2.shape[1]))
                x2 = np.concatenate((x2, pad), axis=1)

        else:
            raise ValueError('Either row or column arguments should be set to True for '
                             'the padding to be meaningful.')

    return x1, x2


def translate_array(array_a, array_b=None):
    """
    Return translated array_a and translation vector.

    Parameters
    ----------
    array_a : ndarray
        The 2D array to translate.
    array_b : ndarray
        The 2D array to translate array_a based on (default=None).

    Returns
    -------
    ndarray, ndarray
        If array_b is None, array_a is translated to origin using its centroid.
        If array_b is given, array_a is translated to centroid of array_b (the centroid of
        translated array_a will centroid with the centroid array_b).
     """
    # The mean is strongly affected by outliers and is not a robust estimator for central location
    # see https://docs.python.org/3.6/library/statistics.html?highlight=mean#statistics.mean
    centroid = compute_centroid(array_a)
    if array_b is not None:
            centroid -= compute_centroid(array_b)
    return array_a - centroid, -centroid


def scale_array(array_a, array_b=None):
    """
    Uniform scaling of the input (m x n) array.

    Scales the arrays so that each array corresponds to a point on the unit sphere
    in R^(m x n). The required operation is Frobenius normalization.

    Parameters
    ----------
    array_a : ndarray
        A 2D array

    array_b : ndarray
        A 2D array

    show_scaling : bool
        A boolean value specifying whether or not the scaling factor is returned.

    keep_centroid : bool
        A boolean value specifying whether or not the centroid of the input array should be kept and not translated
        to the origin.

    Returns
    -------
    if array_b = None and show_scaling = True :
        returns the Frobenius normalized array_a and the scaling factor, s=1 / Frobenius_norm.

    if array_b = None and show_scaling = False :
        returns the Frobenius normalized array_a.

    if array_b is not none :
        returns the optimal scaling factor for array_a which brings the frobenius norm of array_a
        to that of array_b\'s.
    """
    if array_b is not None:
        print 'When array_b is supplied, this function returns the optimal scaling factor bringing the scale' \
              ' of array_a to that of array_b\'s.'
    if array_b is not None:
        # Calculate Frobenius norm of array a
        fna = frobenius_norm(array_a)
        # Calculate Frobenius norm of array b
        fnb = frobenius_norm(array_b)
        # Bring the scale of array a to the scale of array b's
        scale_a_to_b = fnb / fna
        # Compute the rescaled array a
        array_a_rescaled = scale_a_to_b * array_a
        return array_a_rescaled, scale_a_to_b

    else:
        # Centre array by normalizing by the Frobenius norm
        # Calculate Frobenius norm
        fn = frobenius_norm(array_a)
        # Scale array to lie on unit sphere
        array = array_a / fn
        scaling = 1. / fn
        return array, scaling


def translate_scale_array(array_a, array_b=None):
    """
    Translation of one object (array_a) to coincide with either the origin, or the
    centroid of another object (array_b). After translational components has been removed,
    Frobenius scaling is applied. The array_a is Frobenius normalized (if array_b is None),
    or, if array_b is not None, array_a is optimally scaled to array_b such that the Frobenius
    norm of the new array_a is equal to that of array_b's.

    Parameters
    ----------
    array_a : ndarray
        A 2D array

    array_b : ndarray
        A 2D array

    show_scaling : bool
        A boolean value specifying whether or not the tranlation vector and scaling factor is returned.

    Returns
    ----------
    if array_b = None and show_scaling = True :
        returns the origin-centred and Frobenius normalized array_a, as well as the corresponding
         translation vector and the scaling factor.

    if array_b = None and show_scaling = False :
        returns the origin-centred and Frobenius normalized array_a.

    if array_b is not None :
        returns the translated and optimally scaled array_a with respect to array_b. i.e. array_a\'s centroid
        is first translated to coincide with array_b's, and then the updated array_a is scaled such that its
        Frobenius norm is equal to array_b's.
     """

    if array_b is not None:
        print 'When array_b is supplied, this function returns the translation/scaling which bring the ' \
              'centroid and scale of array_a to that of array_b\'s. '

    if array_b is not None:
        # Origin-centre each input array
        at, translate_vec1 = translate_array(array_a)
        bt, unused_translate_vec = translate_array(array_b)
        # Compute the scaling factor between the two arrays
        scale_a_to_b = frobenius_norm(at) / frobenius_norm(bt)
        # Scale the original array by the scaling factor
        scaled_original = at * scale_a_to_b
        # Calculate the required translation
        translate_vec2 = array_b - scaled_original
        scaled_translated_original = scaled_original + translate_vec2
        """
        array_a is first origin_translated, scaled to array_b's scaling, then centroid translated to array_b's
        centroid. The net translation and scaling are described below.
        """
        net_translation = translate_vec1 * scale_a_to_b + translate_vec2
        scaling = scale_a_to_b
        return scaled_translated_original, net_translation, scaling
    else:
        # Translate array_a's centroid to that of array_b's
        array_translated, t_vec = translate_array(array_a)
        # Scale by Frobenius norm
        array_translated_scaled, scaling = scale_array(array_translated)
        return array_translated_scaled, t_vec, scaling


def singular_value_decomposition(array):
    """
    Return Singular Value Decomposition of an array.

    Decomposes an math:`m \times n` array math:`A` such that math:`A = U*S*V.T`

    Parameters
    -----------

    array: ndarray
    A 2D array who's singular value decomposition is to be calculated.

    Returns
    --------------
    u = a unitary matrix.
    s = diagonal matrix of singular values, sorting from greatest to least.
    v = a unitary matrix.
    """
    return np.linalg.svd(array)


def eigenvalue_decomposition(array, two_sided_single=False):
    """
    Computes the eigenvalue decomposition of array
    Decomposes array A such that A = U*S*U.T

    Parameters
    ------------
    array: ndarray
       A 2D array who's eigenvalue decomposition is to be calculated.

    two_sided_single : bool
        Set to True when dealing with two-sided single transformation procrustes problems,
        such as two_sided single transformation orthogonal / permutation. When true, array of
        eigenvectors is rearranged according to rows rather than columns, allowing the analysis
        to proceed.

    Returns
    ------------
    s = 1D array of the eigenvalues of array, sorted from greatest to least.
    v = 2D array of eigenvectors of array, sorted according to S.
    """
    # Test whether eigenvalue decomposition is possible on the input array
    if is_diagonalizable(array) is False:
        raise ValueError('The input array is not diagonalizable. The analysis cannot continue.')

    # Find eigenvalues and array of eigenvectors
    s, v = np.linalg.eigh(array)
    # Sort the eigenvalues from greatest to least
    idx = s.argsort()[::-1]

    s = s[idx]
    if two_sided_single:
        # For the two-sided single-transformation problems, we permute rows by idx
        v = v[idx]
    else:
        # For all other given problems, we permute columns by idx
        v = v[:, idx]

    return s, v


def hide_zero_padding(array, tol=1.e-8):
    """
    Removes any zero-padding that may be on the array.

    Parameters
    ------------
    array: An array that may or may not contain zero-padding, where all important information
    is contained in upper-left block of array.

    tol: Tolerance for which is sum(row/column) < tol, then the row/col will be removed.

    Returns
    ----------
    Returns the input array with any zero-padding removed.
    All zero padding is assumed to be such that all relevant information is contained
    within upper-left most array block
    """
    m, n = array.shape
    for i in range(m)[::-1]:
        # If the sum of array elements across given row is less than tol..
        if sum(np.absolute(array[i, :])) < tol:
            array = np.delete(array, i, 0)

    # If the sum of array elements down given col is less than tol..
    for j in range(n)[::-1]:
        if sum(np.absolute(array[:, j])) < tol:
            array = np.delete(array, j, 1)
    return array


def is_diagonalizable(array):
    """
    Check if the given array is diagonalizable or not.

    Parameters
    ------------
    array: A square array for which the diagonalizability is of interest

    Returns
    ---------
    Returns a boolean value dictating whether or not the input array is diagonalizable
    """
    array = hide_zero_padding(array)
    m, n = array.shape
    if m != n:
        raise ValueError('The input array must be square.')
    u, s, vt = np.linalg.svd(array)
    rank_u = np.linalg.matrix_rank(u)
    rank_array = np.linalg.matrix_rank(array)
    if rank_u != rank_array:
        # The eigenvectors cannot span the dimension of the vector space
        # The array cannot be diagonalizable
        return False
    else:
        # The eigenvectors span the dimension of the vector space and therefore
        # the array is diagonalizable
        return True


def compute_centroid(array):
    """
    """
    centroid = array.mean(0)
    return centroid


def frobenius_norm(array):
    """Return the Forbenius norm of array."""
    return np.sqrt((array ** 2.).sum())
