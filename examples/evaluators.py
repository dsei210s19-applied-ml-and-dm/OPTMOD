import time
import numpy as np
from optmod import Variable, sin, cos, sum

x = Variable(name='x', value=np.random.randn(4,3))
y = Variable(name='y', value=10.)

f = sin(3*x+10.)*cos(y-sum(x*y))

vars = list(x.get_variables())+[y]

e = f.get_fast_evaluator(vars)
var_values = np.array([v.get_value() for v in vars])
e.eval(var_values)

print('same value:', np.all(e.get_value() == f.get_value()))

t0 = time.time()
for i in range(500):
    f.get_value()
t1 = time.time()
for i in range(500):
    e.eval(var_values)
t2 = time.time()
print('speedup:', (t1-t0)/(t2-t1))

