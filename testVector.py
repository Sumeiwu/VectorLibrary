import unittest

import mpivecpy
import scalar_proxy
import plus_proxy1
import diff_proxy1
import matrixmul_proxy
from mpivecpy import mpiInit, mpiFinialize, isMaster, Vec
import numpy as np
import math

class TestVector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mpiInit()

    @classmethod
    def tearDownClass(cls):
        mpiFinialize()

    def test_Abs(self):
        vec = Vec( [-1, -2, -3, 4, 5, 6], 3, 2)
        result = mpivecpy.abs(vec)

        correctResult = [1, 2, 3, 4, 5, 6]
        matInResult = result.matrix
        if isMaster():
            self.assertListEqual(correctResult, matInResult)

    def test_log2(self):
        l = [1, 4, 8, 16, 1024, 2048]
        vec = Vec(l, 6, 1)

        result = mpivecpy.log2(vec)
        correctResult =    [math.log(e, 2) for e in l ]
        if isMaster():
            self.assertListEqual(result.matrix, correctResult)

    def test_divide_scalar(self):
        l = [1, 4, 8, 16, 1024, 2048]
        vec = Vec(l, 6, 1)

        result = vec / 2

        correctResult =    [e/2.0 for e in l ]

        if isMaster():
            self.assertListEqual(result.matrix, correctResult)


    def test_Add_Scalar(self):
        l  = [1, 2,3, 4, 5, 6, 7, 8]
        vec = Vec(l, 2, 4)

        result = vec + 100.0
        correctResult =  [l[i] + 100 for i in range(len(l))]

        if isMaster():
            self.assertListEqual(correctResult, result.matrix)


    def test_Add_matrix(self):
        l  = [1, 2, 3, 4, 5, 6, 7, 8]
        l2  = [1, 2, 3, 4, 5, 6, 7, 8]
        vec = Vec(l, 2, 4)
        vec2 = Vec(l2, 2, 4)

        result = vec + vec2
        correctResult =  [l[i] + l2[i] for i in range(len(l))]

        if isMaster():
            self.assertListEqual(correctResult, result.matrix)

    def test_Sub_matrix(self):
        l  = [1, 2, 3, 4, 5, 6, 7, 8]
        l2  = [1, 2, 3, 4, 5, 6, 7, 8]
        vec = Vec(l, 2, 4)
        vec2 = Vec(l2, 2, 4)

        result = vec - vec2
        correctResult =  [l[i] - l2[i] for i in range(len(l))]

        if isMaster():
            self.assertListEqual(correctResult, result.matrix)

    def test_Sub_Scalar(self):
        pass

    def test_Mul_matrix(self):
        #l  = np.array([1,2,3])
        #l2  = np.array([4,5,6])
        l = [1,2,3]
        l2 = [4,5,6]
        vec = Vec(l, 3, 1)
        vec2 = Vec(l2, 1, 3)

        result = vec * vec2

        n1 = np.array([[1],[2],[3]])
        n2 = np.array([4,5,6])
        res = n1 * n2
        res1 = list(np.array(res).flatten())

        correctResult =  res1

        if isMaster():
            self.assertListEqual(correctResult, result.matrix)

    def test_sqrt_matrix(self) :
        l = [1, 4, 9, 100, 2500]
        vec = Vec(l, 5, 1)

        result = mpivecpy.sqrt(vec)

        correctResult =    [math.sqrt(e) for e in l ]
        if isMaster():
            self.assertListEqual(result.matrix, correctResult)

    def test_power_matrix(self):
        l = [1, 4, 9, 100, 2500]
        vec = Vec(l, 5, 1)

        result = vec ** 2

        correctResult =    [e ** 2 for e in l ]
        if isMaster():
            self.assertListEqual(result.matrix, correctResult)

    def test_sum(self):
        l = [1, 4, 9, 100, 2500]
        v = Vec(l, 5, 1)

        result = mpivecpy.sum(v)

        correctResult =  sum(l)
        if isMaster():
            print(result)
            print(correctResult)
            self.assertEqual(result, correctResult)

  
    def test_getitem(self):
        X = [10, 11, 12, 13, 14, 15]
        vecX = Vec(X, 3, 2)

        if isMaster():
            self.assertEqual(vecX[0, 0], 10)
            self.assertEqual(vecX[2, 1], 15)

            self.assertEqual(vecX[1, 1], 13)
        
        a =  vecX[2, :]
        b = vecX[0, :]
        if isMaster():
            self.assertTrue(isinstance(a, Vec))
            self.assertListEqual([14, 15], a.matrix)
            self.assertListEqual([10, 11], b.matrix) 

    def test_setitem(self) :
        X = [10, 11, 12, 13, 14, 15]
        vecX = Vec(X, 3, 2)

        Y = [1, 2, 3, 4, 5, 6]
        vecY = Vec(Y, 3, 2)

        vecX[0, :] = vecY[2, :]
        if isMaster():
            self.assertListEqual([5, 6, 12, 13, 14, 15], vecX.matrix)
        
        vecX[1, :] = vecY[1, :]
        if isMaster():
            self.assertListEqual([5, 6, 3, 4, 14, 15], vecX.matrix)
    
    def test_minimum(self):
        X = [10, 11, 12, 13, 14, 15]
        vecX = Vec(X, 3, 2)

        Y = [20, 10, 15, 4, 5, 21]
        vecY = Vec(Y, 3, 2)

        result = mpivecpy.minimum(vecX, vecY)

        correct = [x if x < y else y for x, y in zip(X, Y)]
        if isMaster():
            self.assertListEqual(correct, result.matrix)


    def test_floyd_mpivecpyization(self):
        inf = 1000000
        X = [  0,  inf,  -2,  inf,
               4,   0,   3,  inf,
             inf,  inf,   0,   2,
             inf,  -1,  inf,   0] 
        vecX = Vec(X, 4, 4)

        result = self.floyd_warshall_faster(vecX, 4)
        correctResult = [0.0, -1.0, -2.0, 0.0, 4.0, 0.0, 2.0, 4.0, 5.0, 1.0, 0.0, 2.0, 3.0, -1.0, 1.0, 0.0]

        if isMaster():
            print(result.matrix, correctResult)

    def floyd_warshall_faster(self, mat, n):
        for k in xrange(n):
            for i in xrange(n):
                mat[i,:] = mpivecpy.minimum(mat[i,:], mat[k,:] + mat[i, k]) 

        return mat

    def test_euclidean_distance(self):
        X = [10, 11, 12, 13, 14, 15]
        Y = [20, 19, 18, 17, 16, 15]
        vecX = Vec(X, 6, 1)
        vecY = Vec(Y, 6, 1)
        
        result =  math.sqrt(mpivecpy.sum((vecX - vecY) ** 2))

        correctReuslt = math.sqrt(sum( (x - y) ** 2 for x, y in zip(X, Y)))

        if isMaster():
            print(result)
            print(correctReuslt)

            self.assertEqual(result, correctReuslt)
  
if __name__ == "__main__":
    unittest.main()
