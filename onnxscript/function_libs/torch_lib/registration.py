"""Registry for aten functions."""

from __future__ import annotations

from types import FunctionType
from typing import Any, Callable, Optional

import onnxscript


class OverloadedFunction:
    """Overloaded function.

    Attributes:
        name: Name of the op. E.g. "aten::add".
        overloads: Overloads function.
        privates: Private functions not exposed to users.
    """

    def __init__(self, name: str):
        self.name = name
        self.overloads: list[Any] = []
        self.privates: list[Any] = []


class Registry:
    """Registry for aten functions."""

    def __init__(self):
        self._registry: dict[str, OverloadedFunction] = {}

    def register(self, func: Any, name: str, *, private: bool = False) -> None:
        """Register a function."""

        if private:
            self._registry.setdefault(name, OverloadedFunction(name)).privates.append(func)
        else:
            self._registry.setdefault(name, OverloadedFunction(name)).overloads.append(func)

    def __getitem__(self, name):
        return self._registry[name]

    def get_functions(self, name: str):
        return self._registry.get(name, None)

    def is_registered(self, name: str):
        overloads = self.get_functions(name)
        return overloads is not None

    def __contains__(self, name):
        return name in self._registry

    def __iter__(self):
        return iter(self._registry)

    def __repr__(self):
        return repr(self._registry)


# Default registry
default_registry = Registry()


def torch_op(
    name,
    *,
    registry: Optional[Registry] = None,
    trace_only: bool = False,
    private: bool = False,
) -> Callable[[FunctionType], onnxscript.OnnxFunction | onnxscript.values.TracedOnnxFunction]:
    """Register a torch op.

    Args:
        name: ATen name of the function. E.g. "aten::add".
        registry: Registry to register the function to. If None, the default registry is used.
        trace_only: Whether the function should only be traced and not compiled.
        private: Whether the function is private (not directly exposed). It should
            be true for all functions with names starting with "_".
    """
    if registry is None:
        registry = default_registry

    def wrapper(
        func: FunctionType,
    ) -> onnxscript.OnnxFunction | onnxscript.values.TracedOnnxFunction:
        # Compile the function
        custom_opset = onnxscript.values.Opset(domain="pkg.onnxscript.torch_lib", version=1)

        processed_func: onnxscript.OnnxFunction | onnxscript.values.TracedOnnxFunction
        if trace_only:
            processed_func = onnxscript.values.TracedOnnxFunction(custom_opset, func)
        else:
            assert isinstance(func, FunctionType)
            processed_func = onnxscript.script(opset=custom_opset)(func)

        assert registry is not None
        registry.register(processed_func, name, private=private)
        return processed_func

    return wrapper
