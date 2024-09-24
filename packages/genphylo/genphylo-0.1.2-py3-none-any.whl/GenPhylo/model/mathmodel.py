# Required packages
from Bio import Phylo
from io import StringIO
from scipy.linalg import expm
from sympy import symbols, Eq, solve
import numpy as np
import sympy as sp

from GenPhylo.utils.generate_sequences import generate_sequences
from GenPhylo.utils.get_matrix_from_dict import get_matrix_from_dict

class Edge:
    def __init__(self, edge, transition_matrix=None):
        self.edge = edge
        self.transition_matrix = transition_matrix

class MM:
    def __init__(self, source, target, matrix):
        self.source = source
        self.target = target
        self.matrix = matrix

def generate_alignment(length, distribution):
    """
    Generates an alignment of length `length` using a given `distribution`.
    """
    nucleotides = np.array(['A', 'G', 'C', 'T'])
    seq = np.random.choice(nucleotides, size=length, p=distribution)
    return ''.join(seq)

def alpha(new_distribution, Q, i, k):
    """
    Returns the parameter alpha of the Metropolis - Hastings algorithm
    """
    ratio = new_distribution[k] * Q[k, i] / (new_distribution[i] * Q[i, k])
    return min(1, ratio)

def get_M2(new_distribution,d2, l, dir_constant):
    """
    Metropolis - Hastings implementation to get M2
    """
    #print("Computing M2")
    P = np.zeros((4,4))
    iteration = 0
    iter = True

    while iter and iteration < 50:
        # Random Markov matrix generation
        Q = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                Q[i,:] = R
                i = i + 1

        # Time reversible matrix generation
        for i in range(4):
            for j in range(4):
                if i == j:
                    sum = 0
                    for k in range(4):
                        if k != i:
                            sum += (Q[i,k] * (1 - alpha(new_distribution,Q,i,k)))
                    P[i,j] = Q[i,i] + sum
                else:
                    P[i,j] = Q[i,j]*alpha(new_distribution,Q,i,j)

        assert (np.abs(np.sum(new_distribution - np.matmul(new_distribution,P)))) < 10**-6
        
        # Adjust the matrix diagonalising (ensure matrix with determinant d2)
        vaps, _ = np.linalg.eig(P)
        vaps = sorted(vaps, reverse=True)
        A = symbols('A')
        eq = Eq(-d2+(((1-A)*vaps[1]+A)*((1-A)*vaps[2]+A)*((1-A)*vaps[3]+A)),0)
        #print("Before solving")
        sol = solve(eq, A)
        #print("Solved")
        # We only want the real solution between 0 and 1
        #print(sol)
        for s in sol:
            if s.is_real and 0 <= s <= 1:
                a = np.float64(s)
                M2 = (1-a)*P + a*np.identity(4)
                iter = False
                break
            elif s.is_complex: #If imaginary part is negligible
                if np.abs(np.imag(s)) < 10**-9 and 0 <= sp.re(s) <= 1:
                    a = np.float64(sp.re(s))
                    M2 = (1-a)*P + a*np.identity(4)
                    iter = False
                    break
        iteration += 1
    
    if iteration == 50:
        return 0
    else: 
        return M2

def find_k(distribution, l, sq_det_D, exp_minus_l):
    """
    Finds a suitable value of k to satisfy the condition
    detM1 > np.exp(-l)*np.sqrt(np.linalg.det(D_))/np.sqrt(np.linalg.det(D)).
    """
    epsilon = 1e-3  # Desired precision
    lower_bound = 2.5
    upper_bound = 25  # Adjust upper bound as needed
    
    while upper_bound - lower_bound > epsilon:
        M1 = np.zeros((4,4))
        mid = (lower_bound + upper_bound) / 2
        dir_constant_mid = (mid*np.exp(-l/4))/(np.sqrt(l/4))
        i = 0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant_mid
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                M1[i,:] = R
                i = i + 1
        
        new_distribution = np.matmul(distribution, M1)
        D_ = np.diag(new_distribution)
        detM1 = np.linalg.det(M1)
        sq_det_D_ = np.sqrt(np.linalg.det(D_))
        res = exp_minus_l * sq_det_D_ / sq_det_D

        if detM1 > res:
            upper_bound = mid
        else:
            lower_bound = mid

    return (lower_bound + upper_bound) / 2

def generate_random_matrix(distribution, l):
    """
    Returns the transition matrix M=M1M2 given a branch length
    and the distribution at the ancestor node.
    """

    #print("Computing M1")
    D = np.diag(distribution)
    sq_det_D = np.sqrt(np.linalg.det(D))
    exp_minus_l = np.exp(-l)
    k = find_k(distribution, l, sq_det_D, exp_minus_l)
    dir_constant = (k*np.exp(-l/4))/(np.sqrt(l/4))
    
    res = 1
    iteration = 1

    # Compute M1
    while res >= 1 and iteration < 50:
        M1 = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                M1[i,:] = R
                i = i + 1

        new_distribution = np.matmul(distribution,M1)
        D_ = np.diag(new_distribution)
        sq_det_D_ = np.sqrt(np.linalg.det(D_))
        res = exp_minus_l * sq_det_D_ / sq_det_D
        detM1 = np.linalg.det(M1)

        #If detM1 > res and res < 1, conditions are met. Otherwise, a new iteration.
        if detM1 <= res:
            res = 1
        
        iteration += 1

    #print("M1 got")
    d2 = res * (1 / detM1)
    M2 = get_M2(new_distribution,d2,l,dir_constant)

    if not isinstance(M2, np.ndarray) and M2 == 0:
        return np.zeros((4,4))
    else:
        detM2 = np.linalg.det(M2)
        assert(np.abs(detM2 - d2) < 10**-6)
        M = np.matmul(M1,M2)
        #print("M computed")
        return M

