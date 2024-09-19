# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""openvino module namespace, exposing factory functions for all ops and other classes."""
# noqa: F401

from openvino._pyopenvino import get_version

__version__ = get_version()

# Openvino pybind bindings and python extended classes
from openvino._pyopenvino import Symbol
from openvino._pyopenvino import Dimension
from openvino._pyopenvino import Input
from openvino._pyopenvino import Output
from openvino._pyopenvino import Node
from openvino._pyopenvino import Type
from openvino._pyopenvino import PartialShape
from openvino._pyopenvino import Shape
from openvino._pyopenvino import Strides
from openvino._pyopenvino import CoordinateDiff
from openvino._pyopenvino import DiscreteTypeInfo
from openvino._pyopenvino import AxisSet
from openvino._pyopenvino import AxisVector
from openvino._pyopenvino import Coordinate
from openvino._pyopenvino import Layout
from openvino._pyopenvino import ConstOutput
from openvino._pyopenvino import layout_helpers
from openvino._pyopenvino import OVAny
from openvino._pyopenvino import RTMap
from openvino.runtime.ie_api import Core
from openvino.runtime.ie_api import CompiledModel
from openvino.runtime.ie_api import InferRequest
from openvino.runtime.ie_api import Model
from openvino.runtime.ie_api import AsyncInferQueue
from openvino._pyopenvino import Version
from openvino._pyopenvino import Tensor
from openvino._pyopenvino import Extension
from openvino._pyopenvino import ProfilingInfo
from openvino._pyopenvino import get_batch
from openvino._pyopenvino import set_batch
from openvino._pyopenvino import serialize
from openvino._pyopenvino import save_model
from openvino._pyopenvino import shutdown

# Import opsets
from openvino.runtime import opset1
from openvino.runtime import opset2
from openvino.runtime import opset3
from openvino.runtime import opset4
from openvino.runtime import opset5
from openvino.runtime import opset6
from openvino.runtime import opset7
from openvino.runtime import opset8
from openvino.runtime import opset9
from openvino.runtime import opset10
from openvino.runtime import opset11
from openvino.runtime import opset12
from openvino.runtime import opset13

# Import properties API
from openvino.runtime import properties

# Helper functions for openvino module
from openvino.runtime.ie_api import tensor_from_file
from openvino.runtime.ie_api import compile_model

# Extend Node class to support binary operators
Node.__add__ = opset13.add
Node.__sub__ = opset13.subtract
Node.__mul__ = opset13.multiply
Node.__div__ = opset13.divide
Node.__truediv__ = opset13.divide
Node.__radd__ = lambda left, right: opset13.add(right, left)
Node.__rsub__ = lambda left, right: opset13.subtract(right, left)
Node.__rmul__ = lambda left, right: opset13.multiply(right, left)
Node.__rdiv__ = lambda left, right: opset13.divide(right, left)
Node.__rtruediv__ = lambda left, right: opset13.divide(right, left)
Node.__eq__ = opset13.equal
Node.__ne__ = opset13.not_equal
Node.__lt__ = opset13.less
Node.__le__ = opset13.less_equal
Node.__gt__ = opset13.greater
Node.__ge__ = opset13.greater_equal
