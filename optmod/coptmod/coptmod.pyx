import numpy as np
cimport numpy as np

cimport node

include "manager.pyx"

NODE_TYPE_UNKNOWN = node.NODE_TYPE_UNKNOWN
NODE_TYPE_CONSTANT = node.NODE_TYPE_CONSTANT
NODE_TYPE_VARIABLE = node.NODE_TYPE_VARIABLE
NODE_TYPE_ADD = node.NODE_TYPE_ADD
NODE_TYPE_SUBTRACT = node.NODE_TYPE_SUBTRACT
NODE_TYPE_NEGATE = node.NODE_TYPE_NEGATE
NODE_TYPE_MULTIPLY = node.NODE_TYPE_MULTIPLY
NODE_TYPE_SIN = node.NODE_TYPE_SIN
NODE_TYPE_COS = node.NODE_TYPE_COS


