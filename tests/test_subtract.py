import optmod
import unittest
import numpy as np
import networkx as nx

class TestSubtract(unittest.TestCase):

    def test_contruction(self):
        
        x = optmod.variable.VariableScalar(name='x')

        f = optmod.function.subtract([x, 1.])
        self.assertEqual(f.name, 'subtract')
        self.assertEqual(len(f.arguments), 2)
        self.assertTrue(f.arguments[0] is x)
        self.assertTrue(isinstance(f.arguments[1], optmod.constant.Constant))
        self.assertEqual(f.arguments[1].value, 1.)

        self.assertRaises(AssertionError, optmod.function.subtract, [x, 1., 2.])

    def test_constant_constant(self):

        a = optmod.constant.Constant(4.)
        b = optmod.constant.Constant(5.)

        f = a - b
        self.assertTrue(f.is_constant())
        self.assertEqual(f.get_value(), -1)

    def test_scalar_scalar(self):

        x = optmod.variable.VariableScalar(name='x', value=2.)
        y = optmod.variable.VariableScalar(name='y', value=3.)

        f = x - 1.
        self.assertTrue(isinstance(f, optmod.function.subtract))
        self.assertTrue(f.arguments[0] is x)
        self.assertTrue(isinstance(f.arguments[1], optmod.constant.Constant))
        self.assertEqual(f.arguments[1].value, 1.)
        self.assertEqual(f.get_value(), 1.)
        self.assertEqual(str(f), 'x - %s' %optmod.utils.repr_number(1.))
        
        f = 1. - x
        self.assertTrue(isinstance(f, optmod.function.subtract))
        self.assertTrue(f.arguments[1] is x)
        self.assertTrue(isinstance(f.arguments[0], optmod.constant.Constant))
        self.assertEqual(f.arguments[0].value, 1.)
        self.assertEqual(f.get_value(), -1.)
        self.assertEqual(str(f), '%s - x' %optmod.utils.repr_number(1.))

        f = x - y
        self.assertTrue(isinstance(f, optmod.function.subtract))
        self.assertTrue(f.arguments[0] is x)
        self.assertTrue(f.arguments[1] is y)
        self.assertEqual(f.get_value(), -1.)
        self.assertEqual(str(f), 'x - y')

        f = 3. - x - y
        self.assertTrue(isinstance(f, optmod.function.subtract))
        self.assertTrue(isinstance(f.arguments[0], optmod.function.subtract))
        self.assertTrue(f.arguments[0].arguments[1] is x)
        self.assertTrue(isinstance(f.arguments[0].arguments[0], optmod.constant.Constant))
        self.assertEqual(f.arguments[0].arguments[0].value, 3)
        self.assertTrue(f.arguments[1] is y)
        self.assertEqual(f.get_value(), -2.)
        self.assertEqual(str(f), '%s - x - y' %optmod.utils.repr_number(3.))

    def test_scalar_matrix(self):

        rn = optmod.utils.repr_number
        
        value = [[1., 2., 3.], [4., 5., 6.]]
        x = optmod.variable.VariableScalar(name='x', value=2.)
        y = optmod.variable.VariableMatrix(name='y', value=value)
        r = np.random.random((2,3))
        
        f = x - r
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
                self.assertTrue(fij.arguments[0] is x)
                self.assertEqual(fij.arguments[1].value, r[i,j])
        self.assertTrue(isinstance(f.get_value(), np.matrix))
        self.assertTrue(np.all(f.get_value() == 2. - r))
        self.assertEqual(str(f),
                         ('[ x - %s, x - %s, x - %s ]\n' %(rn(r[0,0]), rn(r[0,1]), rn(r[0,2])) +
                          '[ x - %s, x - %s, x - %s ]\n' %(rn(r[1,0]), rn(r[1,1]), rn(r[1,2]))))

        f = r - x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
                self.assertTrue(fij.arguments[1] is x)
                self.assertEqual(fij.arguments[0].value, r[i,j])
        self.assertTrue(isinstance(f.get_value(), np.matrix))
        self.assertTrue(np.all(f.get_value() == r - 2.))
        self.assertEqual(str(f),
                         ('[ %s - x, %s - x, %s - x ]\n' %(rn(r[0,0]), rn(r[0,1]), rn(r[0,2])) +
                          '[ %s - x, %s - x, %s - x ]\n' %(rn(r[1,0]), rn(r[1,1]), rn(r[1,2]))))

        f = x - np.matrix(r)
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTrue(np.all(f.get_value() == 2. - r))
        self.assertEqual(str(f),
                         ('[ x - %s, x - %s, x - %s ]\n' %(rn(r[0,0]), rn(r[0,1]), rn(r[0,2])) +
                          '[ x - %s, x - %s, x - %s ]\n' %(rn(r[1,0]), rn(r[1,1]), rn(r[1,2]))))

        f = np.matrix(r) - x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTrue(np.all(f.get_value() == r - 2.))
        self.assertEqual(str(f),
                         ('[ %s - x, %s - x, %s - x ]\n' %(rn(r[0,0]), rn(r[0,1]), rn(r[0,2])) +
                          '[ %s - x, %s - x, %s - x ]\n' %(rn(r[1,0]), rn(r[1,1]), rn(r[1,2]))))

        f = y - 1
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
                self.assertTrue(fij.arguments[0] is y[i,j])
                self.assertEqual(fij.arguments[1].value, 1.)
        self.assertTrue(isinstance(f.get_value(), np.matrix))
        self.assertTrue(np.all(f.get_value() == np.array(value) - 1))
        self.assertEqual(str(f),
                         ('[ y[0,0] - %s, y[0,1] - %s, y[0,2] - %s ]\n' %(rn(1), rn(1), rn(1)) +
                          '[ y[1,0] - %s, y[1,1] - %s, y[1,2] - %s ]\n' %(rn(1), rn(1), rn(1))))

        f = 1 - y
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTrue(np.all(f.get_value() == 1. - np.array(value)))
        self.assertEqual(str(f),
                         ('[ %s - y[0,0], %s - y[0,1], %s - y[0,2] ]\n' %(rn(1), rn(1), rn(1)) +
                          '[ %s - y[1,0], %s - y[1,1], %s - y[1,2] ]\n' %(rn(1), rn(1), rn(1))))

        f = x - y
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
                self.assertTrue(fij.arguments[1] is y[i,j])
                self.assertTrue(fij.arguments[0] is x)
        self.assertTrue(isinstance(f.get_value(), np.matrix))
        self.assertTrue(np.all(f.get_value() == 2. - np.array(value)))
        self.assertEqual(str(f),
                         ('[ x - y[0,0], x - y[0,1], x - y[0,2] ]\n' +
                          '[ x - y[1,0], x - y[1,1], x - y[1,2] ]\n'))

        f = y - x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.subtract))
                self.assertTrue(fij.arguments[0] is y[i,j])
                self.assertTrue(fij.arguments[1] is x)
        self.assertTrue(isinstance(f.get_value(), np.matrix))
        self.assertTrue(np.all(f.get_value() == np.array(value) - 2.))
        self.assertEqual(str(f),
                         ('[ y[0,0] - x, y[0,1] - x, y[0,2] - x ]\n' +
                          '[ y[1,0] - x, y[1,1] - x, y[1,2] - x ]\n'))

        f = (y - 1) - (3 - x)
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                self.assertEqual(str(f[i,j]), 'y[%d,%d] - %s - (%s - x)' %(i, j, rn(1), rn(3)))
                self.assertTrue(isinstance(f[i,j].arguments[0], optmod.function.subtract))
                self.assertTrue(isinstance(f[i,j].arguments[1], optmod.function.subtract))
        self.assertTrue(np.all(f.get_value() == (np.array(value) - 1.) - (3. - 2.)))

    def test_matrix_matrix(self):

        rn = optmod.utils.repr_number
        
        value1 = [[1., 2., 3.], [4., 5., 6.]]
        value2 = np.random.random((2,3))
        x = optmod.variable.VariableMatrix(name='x', value=value1)
        y = optmod.variable.VariableMatrix(name='y', value=value2)

        f = x - value2
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTupleEqual(f.shape, (2,3))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertEqual(str(fij), 'x[%d,%d] - %s' %(i, j, rn(value2[i,j])))
        self.assertTrue(np.all(f.get_value() == np.matrix(value1) - value2))
                
        f = value2 - x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTupleEqual(f.shape, (2,3))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertEqual(str(fij), '%s - x[%d,%d]' %(rn(value2[i,j]), i, j))
        self.assertTrue(np.all(f.get_value() == value2 - np.matrix(value1)))

        f = x - y
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTupleEqual(f.shape, (2,3))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertEqual(str(fij), 'x[%d,%d] - y[%d,%d]' %(i, j, i, j))
        self.assertTrue(np.all(f.get_value() == np.matrix(value1) - value2))

        f = y - x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        self.assertTupleEqual(f.shape, (2,3))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertEqual(str(fij), 'y[%d,%d] - x[%d,%d]' %(i, j, i, j))
        self.assertTrue(np.all(f.get_value() == value2 - np.matrix(value1)))

    def test_zero(self):

        x = optmod.variable.VariableScalar(name='x', value=3.)
        
        f = x - 0
        self.assertTrue(f is x)

        f = 0 - x
        self.assertTrue(isinstance(f, optmod.function.negate))
        self.assertEqual(str(f), '-x')

    def test_analyze(self):

        x = optmod.variable.VariableScalar('x')
        y = optmod.variable.VariableScalar('y')

        f = x - 1
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], -1.)
        self.assertEqual(len(prop['a']), 1)
        self.assertEqual(prop['a'][x], 1.)

        f = 2 - x
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], 2.)
        self.assertEqual(len(prop['a']), 1)
        self.assertEqual(prop['a'][x], -1.)

        f = x - y - x
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], 0.)
        self.assertEqual(len(prop['a']), 2)
        self.assertEqual(prop['a'][x], 0.)
        self.assertEqual(prop['a'][y], -1.)

        f = x - y - 10. - x
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], -10.)
        self.assertEqual(len(prop['a']), 2)
        self.assertEqual(prop['a'][x], 0.)
        self.assertEqual(prop['a'][y], -1.)

    def test_derivative(self):

        x = optmod.variable.VariableScalar(name='x', value=3.)
        y = optmod.variable.VariableScalar(name='y', value=4.)

        f = x - 1
        fx = f.get_derivative(x)
        fy = f.get_derivative(y)
        self.assertTrue(isinstance(fx, optmod.constant.Constant))
        self.assertEqual(fx.value, 1.)
        self.assertTrue(isinstance(fy, optmod.constant.Constant))
        self.assertEqual(fy.value, 0.)
        
        f = x - y
        fx = f.get_derivative(x)
        fy = f.get_derivative(y)
        self.assertTrue(isinstance(fx, optmod.constant.Constant))
        self.assertEqual(fx.value, 1.)
        self.assertTrue(isinstance(fy, optmod.constant.Constant))
        self.assertEqual(fy.value, -1.)

        f = (x - 1) - (x - 3) - (y - (x - 5.))
        fx = f.get_derivative(x)
        fy = f.get_derivative(y)        
        self.assertTrue(isinstance(fx, optmod.constant.Constant))
        self.assertEqual(fx.value, 1.)
        self.assertTrue(isinstance(fy, optmod.constant.Constant))
        self.assertEqual(fy.value, -1.)        
