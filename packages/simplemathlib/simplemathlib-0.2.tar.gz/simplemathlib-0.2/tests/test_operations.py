# tests/test_operations.py

import unittest
import numpy as np
import math
from simplemathlib import (
    add,
    subtract,
    multiply,
    matrix_multiply,
    svd,
    log,
    dot_product,
    transpose,
    inverse,
    determinant,
    norm,
    eigenvalues,
    eigenvectors,
)


class TestOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertTrue(np.array_equal(multiply([1, 2, 3], [4, 5, 6]), [4, 10, 18]))

    def test_matrix_multiply(self):
        a = np.array([[1, 2], [3, 4]])
        b = np.array([[5, 6], [7, 8]])
        result = matrix_multiply(a, b)
        self.assertTrue(np.array_equal(result, np.array([[19, 22], [43, 50]])))

    def test_svd(self):
        matrix = np.array([[1, 2], [3, 4]])
        u, s, vh = svd(matrix)
        self.assertEqual(u.shape, (2, 2))
        self.assertEqual(len(s), 2)
        self.assertEqual(vh.shape, (2, 2))

    def test_log(self):
        self.assertAlmostEqual(log(math.e), 1)
        self.assertAlmostEqual(log(100, 10), 2)

    def test_dot_product(self):
        v1 = np.array([1, 2, 3])
        v2 = np.array([4, 5, 6])
        self.assertEqual(dot_product(v1, v2), 32)

    def test_transpose(self):
        matrix = np.array([[1, 2, 3], [4, 5, 6]])
        result = transpose(matrix)
        expected = np.array([[1, 4], [2, 5], [3, 6]])
        self.assertTrue(np.array_equal(result, expected))

    def test_inverse(self):
        matrix = np.array([[1, 2], [3, 4]])
        result = inverse(matrix)
        expected = np.array([[-2.0, 1.0], [1.5, -0.5]])
        self.assertTrue(np.allclose(result, expected))

    def test_determinant(self):
        matrix = np.array([[1, 2], [3, 4]])
        result = determinant(matrix)
        self.assertAlmostEqual(result, -2.0)

    def test_norm(self):
        vector = np.array([1, 2, 3])
        result = norm(vector)
        self.assertAlmostEqual(result, 3.7416573867739413)

    def test_eigenvalues(self):
        matrix = np.array([[1, 2], [3, 4]])
        result = eigenvalues(matrix)
        expected = np.array([-0.37228132, 5.37228132])
        self.assertTrue(np.allclose(result, expected))

    def test_eigenvectors(self):
        matrix = np.array([[1, 2], [3, 4]])
        values, vectors = eigenvectors(matrix)
        self.assertTrue(np.allclose(values, [-0.37228132, 5.37228132]))
        self.assertTrue(
            np.allclose(
                vectors, [[-0.82456484, -0.41597356], [0.56576746, -0.90937671]]
            )
        )


if __name__ == "__main__":
    unittest.main()
