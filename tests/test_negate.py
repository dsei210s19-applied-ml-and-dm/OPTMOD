import optmod
import unittest
import numpy as np
import networkx as nx

class TestNegate(unittest.TestCase):

    def test_contruction(self):

        x = optmod.variable.VariableScalar(name='x')
        f = optmod.function.negate(x)
        self.assertTrue(isinstance(f, optmod.function.negate))
        self.assertEqual(f.name, 'negate')
        self.assertEqual(len(f.arguments), 1)
        self.assertTrue(f.arguments[0] is x)

        self.assertRaises(AssertionError, optmod.function.negate, [x, 1., 2.])

    def test_constant(self):

        a = optmod.constant.Constant(4.)
        
        f = -a
        self.assertTrue(f.is_constant())
        self.assertEqual(f.get_value(), -4)

    def test_scalar(self):

        x = optmod.variable.VariableScalar(name='x', value=2.)

        f = -x
        self.assertTrue(isinstance(f, optmod.function.negate))
        self.assertEqual(f.name, 'negate')
        self.assertEqual(len(f.arguments), 1)
        self.assertTrue(f.arguments[0] is x)
        
        self.assertEqual(f.get_value(), -2.)
        self.assertEqual(str(f), '-x')

    def test_matrix(self):

        value = np.random.randn(2,3)
        x = optmod.variable.VariableMatrix(name='x', value=value)

        f = -x
        self.assertTrue(isinstance(f, optmod.expression.ExpressionMatrix))
        for i in range(2):
            for j in range(3):
                fij = f[i,j]
                self.assertTrue(isinstance(fij, optmod.function.negate))
                self.assertEqual(len(fij.arguments), 1)
                self.assertTrue(fij.arguments[0] is x[i,j])
                self.assertEqual(fij.get_value(), -value[i,j])
                self.assertEqual(str(fij), '-x[%d,%d]' %(i,j))

    def test_function(self):

        rn = optmod.utils.repr_number

        x = optmod.variable.VariableScalar(name='x', value=3.)

        f = -optmod.sin(x)
        self.assertEqual(f.get_value(), -np.sin(3.))

        f = -(x + 1)
        self.assertEqual(f.get_value(), -(3.+1.))
        self.assertEqual(str(f), '-(x + %s)' %rn(1.))

        f = -(1 - x)
        self.assertEqual(f.get_value(), -(1.-3.))
        self.assertEqual(str(f), '-(%s - x)' %rn(1.))

        f = -(-x)
        self.assertEqual(f.get_value(), 3.)
        self.assertTrue(f is x)

        f = --x
        self.assertEqual(f.get_value(), 3.)
        self.assertTrue(f is x)

    def test_analyze(self):

        x = optmod.variable.VariableScalar(name='x')
        y = optmod.variable.VariableScalar(name='y')

        f = -x
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], 0.)
        self.assertEqual(len(prop['a']), 1.)
        self.assertEqual(prop['a'][x], -1.)

        f = -4.*(-y+3*x-2)
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertTrue(prop['affine'])
        self.assertEqual(prop['b'], 8.)
        self.assertEqual(len(prop['a']), 2.)
        self.assertEqual(prop['a'][x], -12.)
        self.assertEqual(prop['a'][y], 4.)

        f = -(4.+x)*(-y+3*x-2)
        prop = f.__analyze__(nx.MultiDiGraph(), '')
        self.assertFalse(prop['affine'])
        self.assertEqual(prop['b'], 8.)
        self.assertEqual(len(prop['a']), 2.)
        self.assertTrue(x in prop['a'])
        self.assertTrue(y in prop['a'])

    def test_derivative(self):

        x = optmod.variable.VariableScalar(name='x', value=2.)
        y = optmod.variable.VariableScalar(name='y', value=3.)
        
        f = -x
        fx = f.get_derivative(x)
        fy = f.get_derivative(y)

        self.assertTrue(isinstance(fx, optmod.constant.Constant))
        self.assertEqual(fx.get_value(), -1.)
        self.assertTrue(isinstance(fy, optmod.constant.Constant))
        self.assertEqual(fy.get_value(), 0.)
