.. include:: defs.hrst

.. _reference:

*************
API Reference
*************

.. _ref_constant:

Constant
========

.. autoclass:: optmod.constant.Constant

.. _ref_variable:

Variable Types
==============

.. autoclass:: optmod.variable.VariableScalar
.. autoclass:: optmod.variable.VariableMatrix
.. autoclass:: optmod.variable.VariableDict

.. _ref_expression:

Expression
==========

.. autoclass:: optmod.expression.Expression
.. autoclass:: optmod.expression.ExpressionMatrix
.. autoclass:: optmod.expression.SparseExpressionMatrix
.. autofunction:: optmod.expression.make_Expression

.. _ref_function:

Function
========

.. autoclass:: optmod.function.Function
.. autoclass:: optmod.function.ElementWiseFunction
.. autoclass:: optmod.function.add
.. autoclass:: optmod.function.multiply
.. autoclass:: optmod.function.sin
.. autoclass:: optmod.function.cos

.. _ref_constraint:

Constraint
==========

.. autoclass:: optmod.constraint.Constraint
.. autoclass:: optmod.constraint.ConstraintArray

.. _ref_problem:

Problem
=======

.. autoclass:: optmod.problem.Objective
.. autoclass:: optmod.problem.minimize
.. autoclass:: optmod.problem.maximize
.. autoclass:: optmod.problem.EmptyObjective
.. autoclass:: optmod.problem.Problem

.. _ref_evaluator:

Evaluator
=========

.. autoclass:: optmod.coptmod.Evaluator
   :members:

.. _ref_utils:

Utilities
=========

.. autofunction:: optmod.utils.sum
