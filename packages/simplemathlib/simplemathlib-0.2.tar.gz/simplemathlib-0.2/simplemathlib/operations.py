# simplemathlib/operations.py

import numpy as np
import math


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    """Performs element-wise multiplication"""
    return np.multiply(a, b)


def matrix_multiply(a, b):
    """Performs matrix multiplication"""
    return np.matmul(a, b)


def svd(matrix):
    """Performs Singular Value Decomposition on a matrix"""
    u, s, vh = np.linalg.svd(matrix)
    return u, s, vh


def log(value, base=math.e):
    """Returns the logarithm of a number"""
    return math.log(value, base)


def dot_product(vector_a, vector_b):
    """Calculates the dot product of two vectors"""
    return np.dot(vector_a, vector_b)


def transpose(matrix):
    """Returns the transpose of a matrix"""
    return np.transpose(matrix)


def inverse(matrix):
    """Returns the inverse of a matrix"""
    return np.linalg.inv(matrix)


def determinant(matrix):
    """Returns the determinant of a matrix"""
    return np.linalg.det(matrix)


def norm(vector, order=2):
    """Returns the norm of a vector or matrix (default is 2-norm)"""
    return np.linalg.norm(vector, ord=order)


def eigenvalues(matrix):
    """Returns the eigenvalues of a matrix"""
    return np.linalg.eigvals(matrix)


def eigenvectors(matrix):
    """Returns the eigenvalues and eigenvectors of a matrix"""
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors
