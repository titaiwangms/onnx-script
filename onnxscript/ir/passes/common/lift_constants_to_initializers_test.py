# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from __future__ import annotations

import unittest

import numpy as np

from onnxscript import ir
from onnxscript.ir.passes.common import lift_constants_to_initializers


class TestLiftConstantsToInitializersPass(unittest.TestCase):
    def test_pass_with_lifting_constants_to_initializers(self):
        inputs = [
            ir.Value(
                name="input_a", type=ir.TensorType(ir.DataType.FLOAT), shape=ir.Shape((2, 3))
            ),
            ir.Value(
                name="input_b",
                type=ir.TensorType(ir.DataType.FLOAT),
                shape=ir.Shape((2, 3)),
            ),
        ]

        constant_tensor = ir.tensor(np.random.rand(2, 3).astype(np.float32))
        attribute = ir.convenience.convert_attributes({"value": constant_tensor})
        const_node = ir.Node("", "Constant", inputs=[], attributes=attribute, num_outputs=1)
        add_node = ir.Node("", "Add", inputs=[inputs[0], const_node.outputs[0]])
        mul_node = ir.Node("", "Mul", inputs=[add_node.outputs[0], inputs[1]])

        model = ir.Model(
            graph=ir.Graph(
                inputs=inputs,
                outputs=mul_node.outputs,
                nodes=[const_node, add_node, mul_node],
                opset_imports={"": 20},
            ),
            ir_version=10,
        )

        # Check that the initializer is not in the graph yet
        self.assertEqual(len(model.graph.initializers), 0)
        # And 1 constant node
        self.assertEqual(len([node for node in model.graph if node.op_type == "Constant"]), 1)

        # Perform lift constants to initializers
        result = lift_constants_to_initializers.LiftConstantsToInitializersPass()(model)
        self.assertTrue(result.modified)
        # Check that the constant node is lifted to an initializer
        self.assertEqual(len(result.model.graph.initializers), 1)
        # And 0 constant node
        self.assertEqual(
            len([node for node in result.model.graph if node.op_type == "Constant"]), 0
        )
