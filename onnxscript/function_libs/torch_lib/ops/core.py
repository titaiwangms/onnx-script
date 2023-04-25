# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
# mypy: disable-error-code="misc,arg-type,type-arg,valid-type,assignment,return-value"
"""torch.ops.aten operators under the `core` module.

- No inplace operators.
- All functions should not have the script() decorator. This is because
    we want to delay the compilation of the function.
"""
from __future__ import annotations

from typing import Any, Optional, Sequence, Tuple, Union

from onnxscript import BOOL, DOUBLE, FLOAT, INT8, INT16, INT32, INT64
from onnxscript.function_libs.torch_lib.registration import torch_op
from onnxscript.function_libs.torch_lib.tensor_typing import (
    IntType,
    RealType,
    TFloat,
    TFloatOrBFloat16,
    TInt,
    TReal,
    TrealOrUInt8,
    TRealUnlessFloat16OrInt8,
    TRealUnlessInt16OrInt8,
    TTensor,
    TTensorOrString,
)
from onnxscript.onnx_opset import opset18 as op
from onnxscript.onnx_types import TensorType

_INT64_MAX = 9223372036854775807
_INT64_MIN = -9223372036854775808


@torch_op("aten::abs")
def aten_abs(self: TReal) -> TReal:
    """abs(Tensor self) -> Tensor"""

    return op.Abs(self)


@torch_op("aten::acos")
def aten_acos(self: TFloat) -> TFloat:
    """acos(Tensor self) -> Tensor"""

    return op.Acos(self)


@torch_op("aten::acosh")
def aten_acosh(self: TFloat) -> TFloat:
    """acosh(Tensor self) -> Tensor"""

    return op.Acosh(self)


@torch_op("aten::add")
def aten_add(self: TReal, other: TReal, alpha: float = 1.0) -> TReal:
    """add.Tensor(Tensor self, Tensor other, *, Scalar alpha=1) -> Tensor"""
    # FIXME(titaiwang): get rid of this when we have type_promotion
    other = op.CastLike(other, self)
    alpha = op.CastLike(alpha, other)
    other = op.Mul(other, alpha)
    return op.Add(self, other)


def aten_addbmm(
    self: TensorType,
    batch1: TensorType,
    batch2: TensorType,
    beta: float = 1.0,
    alpha: float = 1.0,
) -> TensorType:
    """addbmm(Tensor self, Tensor batch1, Tensor batch2, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


def aten_addcdiv(
    self: TensorType, tensor1: TensorType, tensor2: TensorType, value: float = 1.0
) -> TensorType:
    """addcdiv(Tensor self, Tensor tensor1, Tensor tensor2, *, Scalar value=1) -> Tensor"""

    raise NotImplementedError()


def aten_addcmul(
    self: TensorType, tensor1: TensorType, tensor2: TensorType, value: float = 1.0
) -> TensorType:
    """addcmul(Tensor self, Tensor tensor1, Tensor tensor2, *, Scalar value=1) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::addmm")
def aten_addmm(
    self: TFloat, mat1: TFloat, mat2: TFloat, beta: float = 1.0, alpha: float = 1.0
) -> TFloat:
    """addmm(Tensor self, Tensor mat1, Tensor mat2, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""

    mat1_mat2 = op.MatMul(mat1, mat2)
    scaled_mat1_mat2 = op.Mul(mat1_mat2, alpha)
    scaled_self = op.Mul(self, beta)
    return op.Add(scaled_self, scaled_mat1_mat2)


def aten_addmv(
    self: TensorType, mat: TensorType, vec: TensorType, beta: float = 1.0, alpha: float = 1.0
) -> TensorType:
    """addmv(Tensor self, Tensor mat, Tensor vec, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


def aten_addr(
    self: TensorType, vec1: TensorType, vec2: TensorType, beta: float = 1.0, alpha: float = 1.0
) -> TensorType:
    """addr(Tensor self, Tensor vec1, Tensor vec2, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


def aten_adjoint(self: TensorType) -> TensorType:
    """adjoint(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_affine_grid_generator(
    theta: TensorType, size: Sequence[int], align_corners: bool
) -> TensorType:
    """affine_grid_generator(Tensor theta, int[] size, bool align_corners) -> Tensor"""

    raise NotImplementedError()


def aten_affine_grid_generator_backward(
    grad: TensorType, size: Sequence[int], align_corners: bool
) -> TensorType:
    """affine_grid_generator_backward(Tensor grad, int[] size, bool align_corners) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::alias")
def aten_alias(self: TTensor) -> TTensor:
    """alias(Tensor(a) self) -> Tensor(a)"""

    return op.Identity(self)


def aten_alias_copy(self: TensorType) -> TensorType:
    """alias_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_align_as(self: TensorType, other: TensorType) -> TensorType:
    """align_as(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_align_tensors(tensors: Sequence[TensorType]) -> TensorType:
    """align_tensors(Tensor[] tensors) -> Tensor[]"""

    raise NotImplementedError()


def aten_align_to(self: TensorType, names: Sequence[str]) -> TensorType:
    """align_to(Tensor(a) self, Dimname[] names) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::all")
def aten_all(self: TTensor) -> BOOL:
    """all(Tensor self) -> Tensor"""

    if op.Size(op.Shape(self)) == 0:
        result = op.Cast(self, to=BOOL.dtype)
    else:
        self_bool = op.Cast(self, to=BOOL.dtype)
        self_int = op.Cast(self_bool, to=INT64.dtype)
        result_int = op.ReduceMin(self_int, keepdims=0)
        result = op.Cast(result_int, to=BOOL.dtype)

    return result


@torch_op("aten::all", overload=True)
def aten_all_dim(self: TTensor, dim: int, keepdim: bool = False) -> BOOL:
    """all(Tensor self) -> Tensor"""

    if op.Size(op.Shape(self)) == 0:
        result = op.Cast(self, to=BOOL.dtype)
    else:
        self_bool = op.Cast(self, to=BOOL.dtype)
        self_int = op.Cast(self_bool, to=INT64.dtype)
        dims = op.Reshape(dim, op.Constant(value_ints=[-1]))
        result_int = op.ReduceMin(self_int, dims, keepdims=keepdim)
        result = op.Cast(result_int, to=BOOL.dtype)

    return result


@torch_op("aten::allclose")
def aten_allclose(
    self: TReal,
    other: TReal,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,  # pylint: disable=unused-argument
) -> BOOL:
    """allclose(Tensor self, Tensor other, float rtol=1e-05, float atol=1e-08, bool equal_nan=False) -> bool"""

    # FIXME: check equal_nan when self and other are all NaN
    # |input - other| <= atol + rtol x |other|
    left_part = op.Abs(op.Sub(self, other))
    right_part = op.Add(atol, op.Mul(rtol, op.Abs(other)))
    is_close = op.LessOrEqual(left_part, right_part)
    is_close_int = op.Cast(is_close, to=INT8.dtype)

    # If min is 0, some elements are not close -> allclose is False
    # If min is 1, all elements are close -> allclose is True
    return op.Cast(op.ReduceMin(is_close_int, keepdims=0), to=BOOL.dtype)


def aten_alpha_dropout(input: TensorType, p: float, train: bool) -> TensorType:
    """alpha_dropout(Tensor input, float p, bool train) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::amax")
def aten_amax(self: TReal, dim: INT64, keepdim: bool = False) -> TReal:
    """amax(Tensor self, int[1] dim=[], bool keepdim=False) -> Tensor"""

    # ReduceMax reduces all dimensions when dim is empty
    return op.ReduceMax(self, dim, keepdims=keepdim)


@torch_op("aten::amin")
def aten_amin(self: TReal, dim: INT64, keepdim: bool = False) -> TReal:
    """amin(Tensor self, int[1] dim=[], bool keepdim=False) -> Tensor"""

    # ReduceMin reduces all dimensions when dim is empty
    return op.ReduceMin(self, dim, keepdims=keepdim)


def aten_aminmax(
    self: TensorType, dim: Optional[int] = None, keepdim: bool = False
) -> tuple[TensorType, TensorType]:
    """aminmax(Tensor self, *, int? dim=None, bool keepdim=False) -> (Tensor min, Tensor max)"""

    raise NotImplementedError()


def aten_and(self: TensorType, other: TensorType) -> TensorType:
    """__and__.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_angle(self: TensorType) -> TensorType:
    """angle(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::any", trace_only=True)
def aten_any(self: TTensor, dim: Optional[int] = None, keepdim: bool = True) -> BOOL:
    """any(Tensor self) -> Tensor"""

    negative_one = op.Constant(value_ints=[-1])
    self_rank = op.Size(op.Shape(self))
    if self_rank == 0:
        self = op.Reshape(self, negative_one)

    # cannot cast to INT64 because 0.1 will be cast to 0, then convert to false
    self_bool = op.Cast(self, to=BOOL.dtype)
    # op.ReduceMax() in next step cannot calculate BOOL value, so convert to INT64
    self_int = op.Cast(self_bool, to=INT64.dtype)

    if op.OptionalHasElement(dim):
        dim = op.Reshape(dim, negative_one)
        dims = op.Cast(dim, to=INT64.dtype)
        result_max = op.ReduceMax(self_int, dims, keepdims=keepdim, noop_with_empty_axes=0)
    else:
        result_max = op.ReduceMax(self_int, keepdims=0, noop_with_empty_axes=0)

    result = op.Greater(result_max, op.Constant(value_int=0))
    if self_rank == 0:
        result = op.Squeeze(result)

    return result


def _range_supported(dtype: int) -> bool:
    """Returns true if the dtype is supported by the ONNX Range op."""
    return dtype in {
        DOUBLE.dtype,
        FLOAT.dtype,
        INT16.dtype,
        INT32.dtype,
        INT64.dtype,
    }


@torch_op("aten::arange", trace_only=True)
def aten_arange(end: Union[DOUBLE, FLOAT, INT16, INT32, INT64], dtype: int = -1) -> TensorType:
    """arange(Scalar end, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        zero = op.CastLike(0.0, end)
        one = op.CastLike(1.0, end)
        result = op.Range(zero, end, one)
    elif _range_supported(dtype):
        end = op.Cast(end, to=dtype)
        zero = op.Cast(0, to=dtype)
        one = op.Cast(1, to=dtype)
        result = op.Range(zero, end, one)
    else:
        # Cast input to float if dtype is not supported by Range,
        # because the input dtype may be e.g. bfloat16 / int8 etc.
        # which Range does not support. The output type is ensured because the output
        # is casted to the specified dtype.
        end = op.Cast(end, to=FLOAT.dtype)
        zero = op.Constant(value_float=0.0)
        one = op.Constant(value_float=1.0)
        result = op.Cast(op.Range(zero, end, one), to=dtype)

    return result


@torch_op("aten::arange", overload=True, trace_only=True)
def aten_arange_start(
    start: TRealUnlessFloat16OrInt8, end: TRealUnlessFloat16OrInt8, dtype: int = -1
) -> TensorType:
    """arange.start(Scalar start, Scalar end, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        one = op.CastLike(1.0, end)
        result = op.Range(start, end, one)
    elif _range_supported(dtype):
        end = op.Cast(end, to=dtype)
        start = op.Cast(start, to=dtype)
        one = op.Cast(1, to=dtype)
        result = op.Range(start, end, one)
    else:
        # Cast input to float if dtype is not supported by Range,
        # because the input dtype may be e.g. bfloat16 / int8 etc.
        # which Range does not support. The output type is ensured because the output
        # is casted to the specified dtype.
        end = op.Cast(end, to=FLOAT.dtype)
        start = op.Cast(start, to=FLOAT.dtype)
        one = op.Constant(value_float=1.0)
        result = op.Cast(op.Range(start, end, one), to=dtype)

    return result


@torch_op("aten::arange", overload=True, trace_only=True)
def aten_arange_start_step(
    start: TRealUnlessFloat16OrInt8,
    end: TRealUnlessFloat16OrInt8,
    step: TRealUnlessFloat16OrInt8,
    dtype: int = -1,
) -> TensorType:
    """arange.start_step(Scalar start, Scalar end, Scalar step=1, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        result = op.Range(start, end, step)
    elif _range_supported(dtype):
        end = op.Cast(end, to=dtype)
        start = op.Cast(start, to=dtype)
        step = op.Cast(step, to=dtype)
        result = op.Range(start, end, step)
    else:
        # Cast input to float if dtype is not supported by Range,
        # because the input dtype may be e.g. bfloat16 / int8 etc.
        # which Range does not support. The output type is ensured because the output
        # is casted to the specified dtype.
        end = op.Cast(end, to=FLOAT.dtype)
        start = op.Cast(start, to=FLOAT.dtype)
        step = op.Cast(step, to=FLOAT.dtype)
        result = op.Cast(op.Range(start, end, step), to=dtype)

    return result


def aten_arccos(self: TensorType) -> TensorType:
    """arccos(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_arccosh(self: TensorType) -> TensorType:
    """arccosh(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_arcsin(self: TensorType) -> TensorType:
    """arcsin(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_arcsinh(self: TensorType) -> TensorType:
    """arcsinh(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_arctan(self: TensorType) -> TensorType:
    """arctan(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_arctan2(self: TensorType, other: TensorType) -> TensorType:
    """arctan2(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_arctanh(self: TensorType) -> TensorType:
    """arctanh(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::argmax", trace_only=True)
def aten_argmax(self: TReal, dim: Optional[int] = None, keepdim: bool = False) -> TReal:
    """argmax(Tensor self, int? dim=None, bool keepdim=False) -> Tensor"""

    if dim is None:  # TODO: use OptionalHasElement(dim)
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    return aten_argmax_dim(self, dim=dim, keepdim=keepdim)


@torch_op("aten::argmax", overload=True)
def aten_argmax_dim(self: TReal, dim: int, keepdim: bool = False) -> TReal:
    """argmax(Tensor self, int? dim=None, bool keepdim=False) -> Tensor"""

    self_is_scaler = op.Size(op.Shape(self)) == 0
    if self_is_scaler:
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    result = op.ArgMax(self, axis=dim, keepdims=keepdim)
    if self_is_scaler:
        result = op.Squeeze(result)

    return result


@torch_op("aten::argmin", trace_only=True)
def aten_argmin(self: TReal, dim: Optional[int] = None, keepdim: bool = False) -> TReal:
    """argmin(Tensor self, int? dim=None, bool keepdim=False) -> Tensor"""

    if dim is None:  # TODO: use OptionalHasElement(dim)
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    return aten_argmin_dim(self, dim=dim, keepdim=keepdim)


@torch_op("aten::argmin", overload=True)
def aten_argmin_dim(self: TReal, dim: int, keepdim: bool = False) -> TReal:
    """argmin(Tensor self, int? dim=None, bool keepdim=False) -> Tensor"""

    self_is_scaler = op.Size(op.Shape(self)) == 0
    if self_is_scaler:
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    result = op.ArgMin(self, axis=dim, keepdims=keepdim)
    if self_is_scaler:
        result = op.Squeeze(result)

    return result


def aten_argsort(self: TensorType, dim: int = -1, descending: bool = False) -> TensorType:
    """argsort(Tensor self, int dim=-1, bool descending=False) -> Tensor"""

    raise NotImplementedError()


def aten_argwhere(self: TensorType) -> TensorType:
    """argwhere(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::as_strided", trace_only=True)
def aten_as_strided(
    self: TTensor, size: INT64, stride: INT64, storage_offset: int = 0
) -> TTensor:
    """as_strided(Tensor(a) self, SymInt[] size, SymInt[] stride, SymInt? storage_offset=None) -> Tensor(a)"""

    rank = len(stride)
    return _aten_as_strided_onnx(self, size, stride, storage_offset, rank)


@torch_op("aten::as_strided", private=True)
def _aten_as_strided_onnx(
    self: TTensor, size: INT64, stride: INT64, storage_offset: int = 0, rank: int = 0
) -> TTensor:
    # e.g. when size=[2,3,4], stride=[2,1,3], indices=[0]
    # i = 0
    # indices=[0], add_value=[0,3,6,9]
    # expand(shape=[4]) to [0,0,0,0]
    # then + add_value = [0,3,6,9]
    # i = 1
    # indices=[0,3,6,9], add_value=[0,1,2]
    # expand(shape=[3,4] to [[0,3,6,9],[0,3,6,9],[0,3,6,9]]
    # indices + add_value = [[0,3,6,9],[1,3,7,10],[2,5,8,11]]
    # i = 2
    # indices = [[0,3,6,9],[1,3,7,10],[2,5,8,11]], add_value=[0,2]
    # expand(shape=[2,3,4]) to [[[0,3,6,9],[1,3,7,10],[2,5,8,11]]],[[0,3,6,9],[1,3,7,10],[2,5,8,11]]]
    # indices + add_value = [[[0,3,6,9],[1,3,7,10],[2,5,8,11]]],[[2,5,8,11],[3,5,9,12],[4,7,10,13]]]
    neg_1 = op.Constant(value_ints=[-1])
    rank_tensor = op.Reshape(rank, neg_1)  # should be 3
    # The final indices for op.Gather(data, indices), will be continually changed during the loop
    indices = op.Constant(value_int=0)
    one_seq = op.SequenceEmpty()
    for i in range(rank):
        # Get the index from back to front, should be 2,1,0 when to i=0,1,2
        j = rank - i - 1
        j_tensor = op.Reshape(j, neg_1)
        # Get size according to index_j, should be 4,3,2 when i=0,1,2
        size_dim_j = op.Gather(size, j_tensor, axis=0)
        # Get right size according to index_j, should be [4],[3,4],[2,3,4] when i=0,1,2
        size_after_j = op.Slice(size, j_tensor, rank_tensor)
        # Get stride according to index_j, should be 3,1,2 when i=0,1,2
        stride_dim_j = op.Gather(stride, j_tensor, axis=0)
        indices = op.Expand(indices, size_after_j)
        # When size[j]=4, stride[j]=3, then add_value = [0,1,2,3] * 3 = [0,3,6,9]
        # When size[j]=3, stride[j]=1, then add_value = [0,1,2] * 1 = [0,1,2]
        # When size[j]=2, stride[j]=2, then add_value = [0,1] * 2 = [0,2]
        add_value = op.Range(0, size_dim_j, 1) * stride_dim_j
        # Compute the shape for add_value for correct broadcasting
        if i == 0:
            # shape = [dim_size]
            shape = size_dim_j
        else:
            # shape = [dim_size, 1, 1, ...], the count of 1 euqal to i
            ones = op.ConcatFromSequence(one_seq, axis=0)
            shape = op.Concat(op.Cast(size_dim_j, to=FLOAT.dtype), ones, axis=0)
            shape = op.Cast(shape, to=INT64.dtype)

        add_value = op.Reshape(add_value, shape)
        # Broadcasting add value to indices according to size and stride value
        indices = indices + add_value
        # Dims after dim_size to reshape(add_value), should be [1],[1,1],[1,1,1] when i=0,1,2
        one_seq = op.SequenceInsert(one_seq, op.Constant(value_floats=[1.0]))

    self_flatten = op.Reshape(self, op.Constant(value_ints=[-1]))
    indices = op.Add(indices, storage_offset)
    result = op.Gather(self_flatten, indices)

    return result


def aten_as_strided_copy(
    self: TensorType, size: INT64, stride: INT64, storage_offset: Optional[INT64] = None
) -> TensorType:
    """as_strided_copy(Tensor self, SymInt[] size, SymInt[] stride, SymInt? storage_offset=None) -> Tensor"""

    raise NotImplementedError()


def aten_as_strided_scatter(
    self: TensorType,
    src: TensorType,
    size: INT64,
    stride: INT64,
    storage_offset: Optional[INT64] = None,
) -> TensorType:
    """as_strided_scatter(Tensor self, Tensor src, SymInt[] size, SymInt[] stride, SymInt? storage_offset=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::asin")
def aten_asin(self: TFloat) -> TFloat:
    """asin(Tensor self) -> Tensor"""

    return op.Asin(self)


@torch_op("aten::asinh")
def aten_asinh(self: TFloat) -> TFloat:
    """asinh(Tensor self) -> Tensor"""

    return op.Asinh(self)


@torch_op("aten::atan")
def aten_atan(self: TFloat) -> TFloat:
    """atan(Tensor self) -> Tensor"""

    return op.Atan(self)


def aten_atan2(self: TensorType, other: TensorType) -> TensorType:
    """atan2(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::atanh")
def aten_atanh(self: TFloat) -> TFloat:
    """atanh(Tensor self) -> Tensor"""

    return op.Atanh(self)


def aten_atleast_1d(self: TensorType) -> TensorType:
    """atleast_1d(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_atleast_2d(self: TensorType) -> TensorType:
    """atleast_2d(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_atleast_3d(self: TensorType) -> TensorType:
    """atleast_3d(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_avg_pool1d(
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0,),
    ceil_mode: bool = False,
    count_include_pad: bool = True,
) -> TensorType:
    """avg_pool1d(Tensor self, int[1] kernel_size, int[1] stride=[], int[1] padding=0, bool ceil_mode=False, bool count_include_pad=True) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::baddbmm")
def aten_baddbmm(
    self: TrealOrUInt8,
    batch1: TRealUnlessInt16OrInt8,
    batch2: TRealUnlessInt16OrInt8,
    beta: float = 1.0,
    alpha: float = 1.0,
) -> TRealUnlessInt16OrInt8:
    """baddbmm(Tensor self, Tensor batch1, Tensor batch2, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""
    batch_mul = op.MatMul(batch1, batch2)
    alpha_cast = op.CastLike(alpha, self)
    mul_a = op.Mul(batch_mul, alpha_cast)
    beta_cast = op.CastLike(beta, self)
    mul_b = op.Mul(self, beta_cast)
    return op.Add(mul_a, mul_b)


def aten_bartlett_window(window_length: int) -> TensorType:
    """bartlett_window(int window_length, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_batch_norm(
    input: TensorType,
    weight: Optional[TensorType],
    bias: Optional[TensorType],
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    training: bool,
    momentum: float,
    eps: float,
    cudnn_enabled: bool,
) -> TensorType:
    """batch_norm(Tensor input, Tensor? weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool training, float momentum, float eps, bool cudnn_enabled) -> Tensor"""

    raise NotImplementedError()


def aten_batch_norm_backward_elemt(
    grad_out: TensorType,
    input: TensorType,
    mean: TensorType,
    invstd: TensorType,
    weight: Optional[TensorType],
    mean_dy: TensorType,
    mean_dy_xmu: TensorType,
    count: TensorType,
) -> TensorType:
    """batch_norm_backward_elemt(Tensor grad_out, Tensor input, Tensor mean, Tensor invstd, Tensor? weight, Tensor mean_dy, Tensor mean_dy_xmu, Tensor count) -> Tensor"""

    raise NotImplementedError()


def aten_batch_norm_backward_reduce(
    grad_out: TensorType,
    input: TensorType,
    mean: TensorType,
    invstd: TensorType,
    weight: Optional[TensorType],
    input_g: bool,
    weight_g: bool,
    bias_g: bool,
) -> tuple[TensorType, TensorType, TensorType, TensorType]:
    """batch_norm_backward_reduce(Tensor grad_out, Tensor input, Tensor mean, Tensor invstd, Tensor? weight, bool input_g, bool weight_g, bool bias_g) -> (Tensor, Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_batch_norm_elemt(
    input: TensorType,
    weight: Optional[TensorType],
    bias: Optional[TensorType],
    mean: TensorType,
    invstd: TensorType,
    eps: float,
) -> TensorType:
    """batch_norm_elemt(Tensor input, Tensor? weight, Tensor? bias, Tensor mean, Tensor invstd, float eps) -> Tensor"""

    raise NotImplementedError()


def aten_batch_norm_gather_stats(
    input: TensorType,
    mean: TensorType,
    invstd: TensorType,
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    momentum: float,
    eps: float,
    count: int,
) -> tuple[TensorType, TensorType]:
    """batch_norm_gather_stats(Tensor input, Tensor mean, Tensor invstd, Tensor? running_mean, Tensor? running_var, float momentum, float eps, int count) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_batch_norm_gather_stats_with_counts(
    input: TensorType,
    mean: TensorType,
    invstd: TensorType,
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    momentum: float,
    eps: float,
    counts: TensorType,
) -> tuple[TensorType, TensorType]:
    """batch_norm_gather_stats_with_counts(Tensor input, Tensor mean, Tensor invstd, Tensor? running_mean, Tensor? running_var, float momentum, float eps, Tensor counts) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_batch_norm_stats(input: TensorType, eps: float) -> tuple[TensorType, TensorType]:
    """batch_norm_stats(Tensor input, float eps) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_batch_norm_update_stats(
    input: TensorType,
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    momentum: float,
) -> tuple[TensorType, TensorType]:
    """batch_norm_update_stats(Tensor input, Tensor? running_mean, Tensor? running_var, float momentum) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_bernoulli(self: TensorType, generator: Optional[str] = None) -> TensorType:
    """bernoulli(Tensor self, *, Generator? generator=None) -> Tensor"""

    raise NotImplementedError()


def aten_bilinear(
    input1: TensorType,
    input2: TensorType,
    weight: TensorType,
    bias: Optional[TensorType] = None,
) -> TensorType:
    """bilinear(Tensor input1, Tensor input2, Tensor weight, Tensor? bias=None) -> Tensor"""

    raise NotImplementedError()


def aten_binary_cross_entropy_with_logits(
    self: TensorType,
    target: TensorType,
    weight: Optional[TensorType] = None,
    pos_weight: Optional[TensorType] = None,
    reduction: int = 1,
) -> TensorType:
    """binary_cross_entropy_with_logits(Tensor self, Tensor target, Tensor? weight=None, Tensor? pos_weight=None, int reduction=Mean) -> Tensor"""

    raise NotImplementedError()


def aten_bincount(
    self: TensorType, weights: Optional[TensorType] = None, minlength: int = 0
) -> TensorType:
    """bincount(Tensor self, Tensor? weights=None, int minlength=0) -> Tensor"""

    raise NotImplementedError()


def aten_binomial(
    count: TensorType, prob: TensorType, generator: Optional[str] = None
) -> TensorType:
    """binomial(Tensor count, Tensor prob, Generator? generator=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::bitwise_and")
def aten_bitwise_and(self: TInt, other: TInt) -> TInt:
    """bitwise_and.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.BitwiseAnd(self, other)


@torch_op("aten::bitwise_left_shift")
def aten_bitwise_left_shift(self: TInt, other: TInt) -> TInt:
    """bitwise_left_shift.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.BitShift(self, other, direction="LEFT")


@torch_op("aten::bitwise_not")
def aten_bitwise_not(self: TInt) -> TInt:
    """bitwise_not(Tensor self) -> Tensor"""

    return op.BitwiseNot(self)


@torch_op("aten::bitwise_not", overload=True)
def aten_bitwise_not_bool(self: BOOL) -> BOOL:
    """bitwise_not(Tensor self) -> Tensor"""
    return op.Not(self)


@torch_op("aten::bitwise_or")
def aten_bitwise_or(self: TInt, other: TInt) -> TInt:
    """bitwise_or.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.BitwiseOr(self, other)


@torch_op("aten::bitwise_right_shift")
def aten_bitwise_right_shift(self: TInt, other: TInt) -> TInt:
    """bitwise_right_shift.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.BitShift(self, other, direction="RIGHT")


@torch_op("aten::bitwise_xor")
def aten_bitwise_xor(self: TInt, other: TInt) -> TInt:
    """bitwise_xor.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.BitwiseXor(self, other)


def aten_blackman_window(window_length: int) -> TensorType:
    """blackman_window(int window_length, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_block_diag(tensors: Sequence[TensorType]) -> TensorType:
    """block_diag(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::bmm")
def aten_bmm(self: TFloat, mat2: TFloat) -> TFloat:
    """bmm(Tensor self, Tensor mat2) -> Tensor"""

    return op.MatMul(self, mat2)


def aten_broadcast_tensors(tensors: Sequence[TensorType]) -> TensorType:
    """broadcast_tensors(Tensor[] tensors) -> Tensor[]"""

    raise NotImplementedError()


@torch_op("aten::broadcast_to")
def aten_broadcast_to(self: TTensor, size: INT64) -> TTensor:
    """broadcast_to(Tensor(a) self, SymInt[] size) -> Tensor(a)"""

    return op.Expand(self, size)


def aten_bucketize(
    self: TensorType, boundaries: TensorType, out_int32: bool = False, right: bool = False
) -> TensorType:
    """bucketize.Tensor(Tensor self, Tensor boundaries, *, bool out_int32=False, bool right=False) -> Tensor"""

    raise NotImplementedError()


def aten_can_cast(from_: int, to: int) -> bool:
    """can_cast(ScalarType from, ScalarType to) -> bool"""

    raise NotImplementedError()


def aten_cartesian_prod(tensors: Sequence[TensorType]) -> TensorType:
    """cartesian_prod(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::cat")
def aten_cat(tensors: Sequence[TTensor], dim: int = 0) -> TTensor:
    """cat(Tensor[] tensors, int dim=0) -> Tensor"""

    # NOTE: Having empty tensors when concatenating along non-zero dimension
    # is not supported.
    # TODO(justinchuby): Filter these tensors out with Sequence ops before
    # calling ConcatFromSequence.
    return op.ConcatFromSequence(tensors, axis=dim)


def aten_ccol_indices(self: TensorType) -> TensorType:
    """ccol_indices(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_ccol_indices_copy(self: TensorType) -> TensorType:
    """ccol_indices_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_cdist(
    x1: TensorType, x2: TensorType, p: float = 2.0, compute_mode: Optional[int] = None
) -> TensorType:
    """cdist(Tensor x1, Tensor x2, float p=2, int? compute_mode=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::ceil")
def aten_ceil(self: TFloat) -> TFloat:
    """ceil(Tensor self) -> Tensor"""

    return op.Ceil(self)


def aten_chain_matmul(matrices: Sequence[TensorType]) -> TensorType:
    """chain_matmul(Tensor[] matrices) -> Tensor"""

    raise NotImplementedError()


def aten_chalf(self: TensorType, memory_format: Optional[str] = None) -> TensorType:
    """chalf(Tensor self, *, MemoryFormat? memory_format=None) -> Tensor"""

    raise NotImplementedError()


def aten_channel_shuffle(self: TensorType, groups: int) -> TensorType:
    """channel_shuffle(Tensor self, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_cholesky(self: TensorType, upper: bool = False) -> TensorType:
    """cholesky(Tensor self, bool upper=False) -> Tensor"""

    raise NotImplementedError()


def aten_cholesky_inverse(self: TensorType, upper: bool = False) -> TensorType:
    """cholesky_inverse(Tensor self, bool upper=False) -> Tensor"""

    raise NotImplementedError()


def aten_cholesky_solve(
    self: TensorType, input2: TensorType, upper: bool = False
) -> TensorType:
    """cholesky_solve(Tensor self, Tensor input2, bool upper=False) -> Tensor"""

    raise NotImplementedError()


def aten_choose_qparams_optimized(
    input: TensorType, numel: int, n_bins: int, ratio: float, bit_width: int
) -> tuple[TensorType, TensorType]:
    """choose_qparams_optimized(Tensor input, int numel, int n_bins, float ratio, int bit_width) -> (Tensor, Tensor)"""

    raise NotImplementedError()


@torch_op("aten::chunk")
def aten_chunk(self: TTensor, chunks: INT64, dim: int = 0) -> TTensor:
    """chunk(Tensor(a -> *) self, int chunks, int dim=0) -> Tensor(a)[]"""

    neg_1 = op.Constant(value_ints=[-1])
    # Get size of specified dim
    self_shape = op.Shape(self)
    dim_size = op.Gather(self_shape, dim, axis=0)
    # Compute size/chunk to get the number of data in one chunk
    num_per_chunk = op.Div(dim_size, chunks)
    num_per_chunk = op.Cast(op.Mod(dim_size, chunks) > 0, to=INT64.dtype) + num_per_chunk  # type: ignore[operator]

    # Compute real chunk number
    num_chunk = op.Div(dim_size, num_per_chunk)
    # Get something like [n, n, n, n, ...], total num_chunk
    list_split = op.Expand(num_per_chunk, op.Reshape(num_chunk, neg_1))

    remainder = op.Mod(dim_size, num_per_chunk)
    if remainder > 0:  # type: ignore[operator]
        # Append the remainder to the [n, n, n, n, ..., r]
        list_split = op.Concat(list_split, op.Reshape(remainder, neg_1), axis=0)
    return op.Split(self, list_split, axis=dim)


@torch_op("aten::clamp", trace_only=True)
def aten_clamp(self: TReal, min: Optional[TReal] = None, max: Optional[TReal] = None) -> TReal:
    """clamp(Tensor self, Tensor? min=None, Tensor? max=None) -> Tensor"""
    clamped = self

    if min is None and max is None:
        return clamped

    # If min is greater than max torch.clamp(..., min, max)
    # sets all elements in input to the value of max.
    # So this order is important.
    if min is not None:
        min_clamp = op.CastLike(min, self)
        clamped = op.Max(clamped, min_clamp)

    if max is not None:
        max_clamp = op.CastLike(max, self)
        clamped = op.Min(clamped, max_clamp)

    return clamped


@torch_op("aten::clamp_max")
def aten_clamp_max(self: TReal, max_: TReal) -> TReal:
    """clamp_max(Tensor self, Tensor max) -> Tensor"""

    self_size = op.Size(self)
    max_shape = op.Shape(max_)
    max_rank = op.Size(max_shape)
    if self_size == 0:
        result = op.Expand(self, max_shape)
    else:
        if max_rank == 0:
            max_ = op.CastLike(max_, self)
            result = op.Clip(self, None, max_)
        else:
            result = op.Min(self, max_)

    return result


@torch_op("aten::clamp_min")
def aten_clamp_min(self: TReal, min_: TReal) -> TReal:
    """clamp_min(Tensor self, Tensor min) -> Tensor"""

    self_size = op.Size(self)
    min_shape = op.Shape(min_)
    min_rank = op.Size(min_shape)
    if self_size == 0:
        result = op.Expand(self, min_shape)
    else:
        if min_rank == 0:
            min_ = op.CastLike(min_, self)
            result = op.Clip(self, min_, None)
        else:
            result = op.Max(self, min_)

    return result


@torch_op("aten::clone")
def aten_clone(
    self: TTensor, memory_format: str = ""  # pylint: disable=unused-argument
) -> TTensor:
    """clone(Tensor self, *, MemoryFormat? memory_format=None) -> Tensor"""

    return op.Identity(self)


def aten_coalesce(self: TensorType) -> TensorType:
    """coalesce(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_col_indices(self: TensorType) -> TensorType:
    """col_indices(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_col_indices_copy(self: TensorType) -> TensorType:
    """col_indices_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_column_stack(tensors: Sequence[TensorType]) -> TensorType:
    """column_stack(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


def aten_combinations(
    self: TensorType, r: int = 2, with_replacement: bool = False
) -> TensorType:
    """combinations(Tensor self, int r=2, bool with_replacement=False) -> Tensor"""

    raise NotImplementedError()


def aten_complex(real: TensorType, imag: TensorType) -> TensorType:
    """complex(Tensor real, Tensor imag) -> Tensor"""

    raise NotImplementedError()


def aten_concat(tensors: Sequence[TensorType], dim: int = 0) -> TensorType:
    """concat(Tensor[] tensors, int dim=0) -> Tensor"""

    raise NotImplementedError()


def aten_concatenate(tensors: Sequence[TensorType], dim: int = 0) -> TensorType:
    """concatenate(Tensor[] tensors, int dim=0) -> Tensor"""

    raise NotImplementedError()


def aten_conj(self: TensorType) -> TensorType:
    """conj(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_conj_physical(self: TensorType) -> TensorType:
    """conj_physical(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::constant_pad_nd")
def aten_constant_pad_nd(self: TTensor, pad: INT64, value: float = 0.0) -> TTensor:
    """constant_pad_nd(Tensor self, SymInt[] pad, Scalar value=0) -> Tensor"""

    # The desired order of paddings is
    # dim_0_begin, dim_1_begin, ... , dim_0_end, ..., dim_n_end.
    # n is the dimension of input.
    # assume zero-dimensions in the beginning
    # rank = len(self.shape)  # rank must be scalar
    # paddings = list(pad[:]) + [0] * (rank * 2 - len(pad))
    # reverse order and collate first beginnings and then ends
    # paddings = paddings[-2::-2] + paddings[-1::-2]

    neg_1 = op.Constant(value_ints=[-1])

    rank = op.Size(op.Shape(self))
    zero_count = op.Sub(op.Mul(rank, 2), op.Size(pad))
    zero_count = op.Reshape(zero_count, neg_1)
    zero = op.Constant(value_ints=[0])
    zeros = op.Expand(zero, zero_count)
    torch_paddings = op.Concat(pad, zeros, axis=0)
    size_d = op.Size(torch_paddings)
    steps = op.Constant(value_ints=[-2])

    starts = steps
    ends = op.Sub(starts, size_d)
    odd_elements = op.Slice(torch_paddings, starts, ends, zero, steps)

    starts = neg_1
    ends = op.Sub(starts, size_d)
    even_elements = op.Slice(torch_paddings, starts, ends, zero, steps)

    onnx_padding = op.Concat(odd_elements, even_elements, axis=0)
    return op.Pad(self, onnx_padding, value)


@torch_op("aten::contiguous", trace_only=True)
def aten_contiguous(self: TTensor, memory_format: str = "contiguous_format") -> TTensor:
    """contiguous(Tensor(a) self, *, MemoryFormat memory_format=contiguous_format) -> Tensor(a)"""

    if memory_format in ["contiguous_format", "preserve_format"]:
        return op.Identity(self)
    else:
        # TODO: Find out a way to annotate constraints for argument, as part of the function meta data structure.
        raise NotImplementedError(
            "memory_format value supports 'contiguous_format' or 'preserve_format' only."
        )


@torch_op("aten::conv1d", trace_only=True)
def aten_conv1d(
    input: TFloat,
    weight: TFloat,
    bias: Optional[TFloat] = None,
    stride: Sequence[int] = (1,),
    padding: Sequence[int] = (0,),
    dilation: Sequence[int] = (1,),
    groups: int = 1,
) -> TFloat:
    """conv1d(Tensor input, Tensor weight, Tensor? bias=None, int[1] stride=1, int[1] padding=0, int[1] dilation=1, int groups=1) -> Tensor"""

    # Attributes need to be manipulated in Python to match ONNX's conv1d
    if not isinstance(padding, Sequence):
        padding = (padding,)
    pads = [*padding, *padding]

    if not isinstance(dilation, Sequence):
        dilation = (dilation,)
    dilations = list(dilation)

    if not isinstance(stride, Sequence):
        stride = (stride,)
    strides = list(stride)

    if bias is None:
        weight_dim_0 = op.Shape(weight, start=0, end=1)
        bias_shape = op.Expand(weight_dim_0, op.Constant(value_ints=[1]))
        zero = op.CastLike(0.0, input)
        bias = op.Expand(zero, bias_shape)

    result = _aten_convolution_onnx(
        input,
        weight,
        bias,
        transposed=False,
        strides=strides,
        pads=pads,
        dilations=dilations,
        groups=groups,
    )

    return result


@torch_op("aten::conv2d", trace_only=True)
def aten_conv2d(
    input: TFloat,
    weight: TFloat,
    bias: Optional[TFloat] = None,
    stride: Sequence[int] = (1, 1),
    padding: Sequence[int] = (0, 0),
    dilation: Sequence[int] = (1, 1),
    groups: int = 1,
) -> TFloat:
    """conv2d(Tensor input, Tensor weight, Tensor? bias=None, int[2] stride=1, int[2] padding=0, int[2] dilation=1, int groups=1) -> Tensor"""

    # Attributes need to be manipulated in Python to match ONNX's conv2d
    if not isinstance(padding, Sequence):
        padding = (padding, padding)
    pads = [*padding, *padding]

    if not isinstance(dilation, Sequence):
        dilation = (dilation, dilation)
    dilations = list(dilation)

    if not isinstance(stride, Sequence):
        stride = (stride, stride)
    strides = list(stride)

    if bias is None:
        weight_dim_0 = op.Shape(weight, start=0, end=1)
        bias_shape = op.Expand(weight_dim_0, op.Constant(value_ints=[1]))
        zero = op.CastLike(0.0, input)
        bias = op.Expand(zero, bias_shape)

    result = _aten_convolution_onnx(
        input,
        weight,
        bias,
        transposed=False,
        strides=strides,
        pads=pads,
        dilations=dilations,
        groups=groups,
    )

    return result


@torch_op("aten::conv3d", trace_only=True)
def aten_conv3d(
    input: TFloat,
    weight: TFloat,
    bias: Optional[TFloat] = None,
    stride: Sequence[int] = (1, 1, 1),
    padding: Sequence[int] = (0, 0, 0),
    dilation: Sequence[int] = (1, 1, 1),
    groups: int = 1,
) -> TFloat:
    """conv3d(Tensor input, Tensor weight, Tensor? bias=None, int[3] stride=1, int[3] padding=0, int[3] dilation=1, int groups=1) -> Tensor"""

    # Attributes need to be manipulated in Python to match ONNX's conv3d
    if not isinstance(padding, Sequence):
        padding = (padding, padding, padding)
    pads = [*padding, *padding]

    if not isinstance(dilation, Sequence):
        dilation = (dilation, dilation, dilation)
    dilations = list(dilation)

    if not isinstance(stride, Sequence):
        stride = (stride, stride, stride)
    strides = list(stride)

    if bias is None:
        weight_dim_0 = op.Shape(weight, start=0, end=1)
        bias_shape = op.Expand(weight_dim_0, op.Constant(value_ints=[1]))
        zero = op.CastLike(0.0, input)
        bias = op.Expand(zero, bias_shape)

    result = _aten_convolution_onnx(
        input,
        weight,
        bias,
        transposed=False,
        strides=strides,
        pads=pads,
        dilations=dilations,
        groups=groups,
    )

    return result


def aten_conv_tbc(
    self: TensorType, weight: TensorType, bias: TensorType, pad: int = 0
) -> TensorType:
    """conv_tbc(Tensor self, Tensor weight, Tensor bias, int pad=0) -> Tensor"""

    raise NotImplementedError()


def aten_conv_tbc_backward(
    self: TensorType, input: TensorType, weight: TensorType, bias: TensorType, pad: int
) -> tuple[TensorType, TensorType, TensorType]:
    """conv_tbc_backward(Tensor self, Tensor input, Tensor weight, Tensor bias, int pad) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_conv_transpose1d(
    input: TensorType,
    weight: TensorType,
    bias: Optional[TensorType] = None,
    stride: Sequence[int] = (1,),
    padding: Sequence[int] = (0,),
    output_padding: Sequence[int] = (0,),
    groups: int = 1,
    dilation: Sequence[int] = (1,),
) -> TensorType:
    """conv_transpose1d(Tensor input, Tensor weight, Tensor? bias=None, int[1] stride=1, int[1] padding=0, int[1] output_padding=0, int groups=1, int[1] dilation=1) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::convolution", trace_only=True)
def aten_convolution(
    input: TFloat,
    weight: TFloat,
    bias: Optional[TFloat],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    transposed: bool,
    output_padding: Sequence[int],
    groups: int,
) -> TFloat:
    """convolution(Tensor input, Tensor weight, Tensor? bias, int[] stride, SymInt[] padding, int[] dilation, bool transposed, SymInt[] output_padding, int groups) -> Tensor"""

    if not isinstance(padding, Sequence):
        padding = (padding, padding)
    pads = [*padding, *padding]

    if not isinstance(dilation, Sequence):
        dilation = (dilation, dilation)
    dilations = list(dilation)

    if not isinstance(stride, Sequence):
        stride = (stride, stride)
    strides = list(stride)

    if bias is None:
        weight_dim_0 = op.Shape(weight, start=0, end=1)
        bias_shape = op.Expand(weight_dim_0, op.Constant(value_ints=[1]))
        zero = op.CastLike(0.0, input)
        bias = op.Expand(zero, bias_shape)

    result = _aten_convolution_onnx(
        input,
        weight,
        bias,
        transposed,
        strides=strides,
        pads=pads,
        dilations=dilations,
        output_padding=output_padding,
        groups=groups,
    )

    return result


@torch_op("aten::convolution", private=True)
def _aten_convolution_onnx(
    input: TFloat,
    weight: TFloat,
    bias: TFloat,
    transposed: BOOL,
    strides: Sequence[int],
    pads: Sequence[int],
    dilations: Sequence[int],
    output_padding: Sequence[int] = (0,),
    groups: int = 1,
) -> TFloat:
    """ConvXd with attributes pre-computed to fit the ONNX spec."""

    # NOTE: transposed must be an input because when provided as an attribute,
    # it will be an integer, not a boolean, which will fail the if condition.
    # Alternatively we could cast transposed to BOOL.
    # E.g. `if op.Cast(transposed, BOOL.dtype): ...`

    weight_size = op.Size(op.Shape(weight))
    no_batch = op.Size(op.Shape(input)) != weight_size

    if no_batch:
        input = op.Unsqueeze(input, op.Constant(value_ints=[0]))

    if transposed:
        result = op.ConvTranspose(
            input,
            weight,
            bias,
            strides=strides,
            pads=pads,
            group=groups,
            dilations=dilations,
            output_padding=output_padding,
        )
    else:
        result = op.Conv(
            input,
            weight,
            bias,
            strides=strides,
            pads=pads,
            group=groups,
            dilations=dilations,
        )

    if no_batch:
        result = op.Squeeze(result, op.Constant(value_ints=[0]))

    return result


def aten_convolution_backward(
    grad_output: TensorType,
    input: TensorType,
    weight: TensorType,
    bias_sizes: Optional[INT64],
    stride: Sequence[int],
    padding: INT64,
    dilation: Sequence[int],
    transposed: bool,
    output_padding: INT64,
    groups: int,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """convolution_backward(Tensor grad_output, Tensor input, Tensor weight, SymInt[]? bias_sizes, int[] stride, SymInt[] padding, int[] dilation, bool transposed, SymInt[] output_padding, int groups, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_convolution_backward_overrideable(
    grad_output: TensorType,
    input: TensorType,
    weight: TensorType,
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    transposed: bool,
    output_padding: Sequence[int],
    groups: int,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """convolution_backward_overrideable(Tensor grad_output, Tensor input, Tensor weight, int[] stride, int[] padding, int[] dilation, bool transposed, int[] output_padding, int groups, bool[3] output_mask) -> (Tensor grad_input, Tensor grad_weight, Tensor grad_bias)"""

    raise NotImplementedError()


def aten_convolution_overrideable(
    input: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    transposed: bool,
    output_padding: Sequence[int],
    groups: int,
) -> TensorType:
    """convolution_overrideable(Tensor input, Tensor weight, Tensor? bias, int[] stride, int[] padding, int[] dilation, bool transposed, int[] output_padding, int groups) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::copy")
def aten_copy(
    self: TTensor, src: TTensor, non_blocking: bool = False  # pylint: disable=unused-argument
) -> TTensor:
    """copy(Tensor self, Tensor src, bool non_blocking=False) -> Tensor"""

    self = op.Identity(src)
    return self


def aten_copysign(self: TensorType, other: TensorType) -> TensorType:
    """copysign.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_corrcoef(self: TensorType) -> TensorType:
    """corrcoef(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::cos")
def aten_cos(self: TFloat) -> TFloat:
    """cos(Tensor self) -> Tensor"""

    return op.Cos(self)


@torch_op("aten::cosh")
def aten_cosh(self: TFloat) -> TFloat:
    """cosh(Tensor self) -> Tensor"""

    return op.Cosh(self)


def aten_cosine_embedding_loss(
    input1: TensorType,
    input2: TensorType,
    target: TensorType,
    margin: float = 0.0,
    reduction: int = 1,
) -> TensorType:
    """cosine_embedding_loss(Tensor input1, Tensor input2, Tensor target, float margin=0.0, int reduction=Mean) -> Tensor"""

    raise NotImplementedError()


def aten_cosine_similarity(
    x1: TensorType, x2: TensorType, dim: int = 1, eps: float = 1e-08
) -> TensorType:
    """cosine_similarity(Tensor x1, Tensor x2, int dim=1, float eps=1e-08) -> Tensor"""

    raise NotImplementedError()


def aten_count_nonzero(self: TensorType, dim: Optional[int] = None) -> TensorType:
    """count_nonzero(Tensor self, int? dim=None) -> Tensor"""

    raise NotImplementedError()


def aten_cov(
    self: TensorType,
    correction: int = 1,
    fweights: Optional[TensorType] = None,
    aweights: Optional[TensorType] = None,
) -> TensorType:
    """cov(Tensor self, *, int correction=1, Tensor? fweights=None, Tensor? aweights=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::cross")
def aten_cross(self: TTensor, other: TTensor, dim: int = -1) -> TTensor:
    """cross(Tensor self, Tensor other, int? dim=None) -> Tensor"""

    zero = op.Constant(value_ints=[0])
    one = op.Constant(value_ints=[1])
    two = op.Constant(value_ints=[2])
    three = op.Constant(value_ints=[3])
    axes = op.Expand(dim, op.Constant(value_ints=[1]))

    # Reference https://en.wikipedia.org/w/index.php?title=Cross_product&oldid=1143125073
    a1 = op.Slice(self, zero, one, axes)
    a2 = op.Slice(self, one, two, axes)
    a3 = op.Slice(self, two, three, axes)
    b1 = op.Slice(other, zero, one, axes)
    b2 = op.Slice(other, one, two, axes)
    b3 = op.Slice(other, two, three, axes)
    # Broadcasting is implicitly supported by Mul
    c1 = op.Sub(op.Mul(a2, b3), op.Mul(a3, b2))
    c2 = op.Sub(op.Mul(a3, b1), op.Mul(a1, b3))
    c3 = op.Sub(op.Mul(a1, b2), op.Mul(a2, b1))

    return op.Concat(c1, c2, c3, axis=dim)


def aten_crow_indices(self: TensorType) -> TensorType:
    """crow_indices(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_crow_indices_copy(self: TensorType) -> TensorType:
    """crow_indices_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_ctc_loss(
    log_probs: TensorType,
    targets: TensorType,
    input_lengths: TensorType,
    target_lengths: TensorType,
    blank: int = 0,
    reduction: int = 1,
    zero_infinity: bool = False,
) -> TensorType:
    """ctc_loss.Tensor(Tensor log_probs, Tensor targets, Tensor input_lengths, Tensor target_lengths, int blank=0, int reduction=Mean, bool zero_infinity=False) -> Tensor"""

    raise NotImplementedError()


def aten_cudnn_affine_grid_generator(
    theta: TensorType, N: int, C: int, H: int, W: int
) -> TensorType:
    """cudnn_affine_grid_generator(Tensor theta, int N, int C, int H, int W) -> Tensor grid"""

    raise NotImplementedError()


def aten_cudnn_affine_grid_generator_backward(
    grad: TensorType, N: int, C: int, H: int, W: int
) -> TensorType:
    """cudnn_affine_grid_generator_backward(Tensor grad, int N, int C, int H, int W) -> Tensor grad_theta"""

    raise NotImplementedError()


def aten_cudnn_batch_norm(
    input: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    training: bool,
    exponential_average_factor: float,
    epsilon: float,
) -> tuple[TensorType, TensorType, TensorType, TensorType]:
    """cudnn_batch_norm(Tensor input, Tensor weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool training, float exponential_average_factor, float epsilon) -> (Tensor, Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_cudnn_batch_norm_backward(
    input: TensorType,
    grad_output: TensorType,
    weight: TensorType,
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    save_mean: Optional[TensorType],
    save_var: Optional[TensorType],
    epsilon: float,
    reserveSpace: TensorType,
) -> tuple[TensorType, TensorType, TensorType]:
    """cudnn_batch_norm_backward(Tensor input, Tensor grad_output, Tensor weight, Tensor? running_mean, Tensor? running_var, Tensor? save_mean, Tensor? save_var, float epsilon, Tensor reserveSpace) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_cudnn_convolution(
    self: TensorType,
    weight: TensorType,
    padding: Sequence[int],
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
    allow_tf32: bool,
) -> TensorType:
    """cudnn_convolution(Tensor self, Tensor weight, int[] padding, int[] stride, int[] dilation, int groups, bool benchmark, bool deterministic, bool allow_tf32) -> Tensor"""

    raise NotImplementedError()


def aten_cudnn_convolution_add_relu(
    self: TensorType,
    weight: TensorType,
    z: TensorType,
    alpha: Optional[float],
    bias: Optional[TensorType],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    groups: int,
) -> TensorType:
    """cudnn_convolution_add_relu(Tensor self, Tensor weight, Tensor z, Scalar? alpha, Tensor? bias, int[] stride, int[] padding, int[] dilation, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_cudnn_convolution_relu(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    groups: int,
) -> TensorType:
    """cudnn_convolution_relu(Tensor self, Tensor weight, Tensor? bias, int[] stride, int[] padding, int[] dilation, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_cudnn_convolution_transpose(
    self: TensorType,
    weight: TensorType,
    padding: Sequence[int],
    output_padding: Sequence[int],
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
    allow_tf32: bool,
) -> TensorType:
    """cudnn_convolution_transpose(Tensor self, Tensor weight, int[] padding, int[] output_padding, int[] stride, int[] dilation, int groups, bool benchmark, bool deterministic, bool allow_tf32) -> Tensor"""

    raise NotImplementedError()


def aten_cudnn_grid_sampler(self: TensorType, grid: TensorType) -> TensorType:
    """cudnn_grid_sampler(Tensor self, Tensor grid) -> Tensor output"""

    raise NotImplementedError()


def aten_cudnn_grid_sampler_backward(
    self: TensorType, grid: TensorType, grad_output: TensorType
) -> tuple[TensorType, TensorType]:
    """cudnn_grid_sampler_backward(Tensor self, Tensor grid, Tensor grad_output) -> (Tensor grad_self, Tensor grad_grid)"""

    raise NotImplementedError()


def aten_cudnn_is_acceptable(self: TensorType) -> bool:
    """cudnn_is_acceptable(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_cummax(self: TensorType, dim: int) -> tuple[TensorType, TensorType]:
    """cummax(Tensor self, int dim) -> (Tensor values, Tensor indices)"""

    raise NotImplementedError()


def aten_cummaxmin_backward(
    grad: TensorType, input: TensorType, indices: TensorType, dim: int
) -> TensorType:
    """cummaxmin_backward(Tensor grad, Tensor input, Tensor indices, int dim) -> Tensor"""

    raise NotImplementedError()


def aten_cummin(self: TensorType, dim: int) -> tuple[TensorType, TensorType]:
    """cummin(Tensor self, int dim) -> (Tensor values, Tensor indices)"""

    raise NotImplementedError()


def aten_cumprod(self: TensorType, dim: int, dtype: Optional[int] = None) -> TensorType:
    """cumprod(Tensor self, int dim, *, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_cumprod_backward(
    grad: TensorType, input: TensorType, dim: int, output: TensorType
) -> TensorType:
    """cumprod_backward(Tensor grad, Tensor input, int dim, Tensor output) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::cumsum", trace_only=True)
def aten_cumsum(
    self: TRealUnlessInt16OrInt8, dim: Union[INT32, INT64], dtype: int = -1
) -> TRealUnlessInt16OrInt8:
    """cumsum(Tensor self, int dim, *, ScalarType? dtype=None) -> Tensor"""

    if dtype == -1:
        cast = self
    else:
        cast = op.Cast(self, to=dtype)
    return _aten_cumsum_onnx(cast, dim)


@torch_op("aten::cumsum", private=True)
def _aten_cumsum_onnx(
    self: TRealUnlessInt16OrInt8, dim: Union[INT32, INT64]
) -> TRealUnlessInt16OrInt8:
    if op.Size(op.Shape(self)) == 0:
        # A scalar
        result = op.Identity(self)
    else:
        result = op.CumSum(self, dim)
    return result


def aten_data(self: TensorType) -> TensorType:
    """data(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_deg2rad(self: TensorType) -> TensorType:
    """deg2rad(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_dense_dim(self: TensorType) -> int:
    """dense_dim(Tensor self) -> int"""

    raise NotImplementedError()


def aten_det(self: TensorType) -> TensorType:
    """det(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::detach")
def aten_detach(self: TensorType) -> TensorType:
    """detach(Tensor(a) self) -> Tensor(a)"""

    return op.Identity(self)


def aten_detach_copy(self: TensorType) -> TensorType:
    """detach_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_diag(self: TensorType, diagonal: int = 0) -> TensorType:
    """diag(Tensor self, int diagonal=0) -> Tensor"""

    raise NotImplementedError()


def aten_diag_embed(
    self: TensorType, offset: int = 0, dim1: int = -2, dim2: int = -1
) -> TensorType:
    """diag_embed(Tensor self, int offset=0, int dim1=-2, int dim2=-1) -> Tensor"""

    raise NotImplementedError()


def aten_diagflat(self: TensorType, offset: int = 0) -> TensorType:
    """diagflat(Tensor self, int offset=0) -> Tensor"""

    raise NotImplementedError()


def aten_diagonal(
    self: TensorType, offset: int = 0, dim1: int = 0, dim2: int = 1
) -> TensorType:
    """diagonal(Tensor(a) self, int offset=0, int dim1=0, int dim2=1) -> Tensor(a)"""

    raise NotImplementedError()


def aten_diagonal_backward(
    grad_output: TensorType, input_sizes: INT64, offset: int, dim1: int, dim2: int
) -> TensorType:
    """diagonal_backward(Tensor grad_output, SymInt[] input_sizes, int offset, int dim1, int dim2) -> Tensor"""

    raise NotImplementedError()


def aten_diagonal_copy(
    self: TensorType, offset: int = 0, dim1: int = 0, dim2: int = 1
) -> TensorType:
    """diagonal_copy(Tensor self, int offset=0, int dim1=0, int dim2=1) -> Tensor"""

    raise NotImplementedError()


def aten_diagonal_scatter(
    self: TensorType, src: TensorType, offset: int = 0, dim1: int = 0, dim2: int = 1
) -> TensorType:
    """diagonal_scatter(Tensor self, Tensor src, int offset=0, int dim1=0, int dim2=1) -> Tensor"""

    raise NotImplementedError()


def aten_diff(
    self: TensorType,
    n: int = 1,
    dim: int = -1,
    prepend: Optional[TensorType] = None,
    append: Optional[TensorType] = None,
) -> TensorType:
    """diff(Tensor self, int n=1, int dim=-1, Tensor? prepend=None, Tensor? append=None) -> Tensor"""

    raise NotImplementedError()


def aten_digamma(self: TensorType) -> TensorType:
    """digamma(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_dist(self: TensorType, other: TensorType, p: float = 2.0) -> TensorType:
    """dist(Tensor self, Tensor other, Scalar p=2) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::div")
def aten_div(self: TReal, other: TReal) -> TReal:
    """div.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Div(self, other)


def aten_divide(self: TensorType, other: TensorType) -> TensorType:
    """divide.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::dot")
def aten_dot(self: TFloat, tensor: TFloat) -> TFloat:
    """dot(Tensor self, Tensor tensor) -> Tensor"""

    return op.MatMul(self, tensor)


@torch_op("aten::dropout")
def aten_dropout(input: TFloat, p: FLOAT, train: BOOL) -> TFloat:
    """dropout(Tensor input, float p, bool train) -> Tensor"""

    input_is_scalar = op.Size(op.Shape(input)) == 0
    if input_is_scalar:
        input = op.Reshape(input, op.Constant(value_ints=[-1]))
        result, _ = op.Dropout(input, p, train)
        result = op.Squeeze(result)
    else:
        result, _ = op.Dropout(input, p, train)

    return result


def aten_dstack(tensors: Sequence[TensorType]) -> TensorType:
    """dstack(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


def aten_einsum(
    equation: str, tensors: Sequence[TensorType], path: Optional[int] = None
) -> TensorType:
    """einsum(str equation, Tensor[] tensors, *, int[]? path=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::embedding")
def aten_embedding(
    weight: TTensor,
    indices: TTensor,
    padding_idx: int = -1,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
):  # pylint: disable=unused-argument
    # embedding(Tensor weight, Tensor indices, int padding_idx=-1, bool scale_grad_by_freq=False, bool sparse=False) -> Tensor

    return op.Gather(weight, indices)


def aten_embedding_backward(
    grad: TensorType,
    indices: TensorType,
    num_weights: INT64,
    padding_idx: int,
    scale_grad_by_freq: bool,
    sparse: bool,
) -> TensorType:
    """embedding_backward(Tensor grad, Tensor indices, SymInt num_weights, int padding_idx, bool scale_grad_by_freq, bool sparse) -> Tensor"""

    raise NotImplementedError()


def aten_embedding_bag(
    weight: TensorType,
    indices: TensorType,
    offsets: TensorType,
    scale_grad_by_freq: bool = False,
    mode: int = 0,
    sparse: bool = False,
    per_sample_weights: Optional[TensorType] = None,
    include_last_offset: bool = False,
) -> tuple[TensorType, TensorType, TensorType, TensorType]:
    """embedding_bag(Tensor weight, Tensor indices, Tensor offsets, bool scale_grad_by_freq=False, int mode=0, bool sparse=False, Tensor? per_sample_weights=None, bool include_last_offset=False) -> (Tensor, Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_embedding_dense_backward(
    grad_output: TensorType,
    indices: TensorType,
    num_weights: INT64,
    padding_idx: int,
    scale_grad_by_freq: bool,
) -> TensorType:
    """embedding_dense_backward(Tensor grad_output, Tensor indices, SymInt num_weights, int padding_idx, bool scale_grad_by_freq) -> Tensor"""

    raise NotImplementedError()


def aten_embedding_sparse_backward(
    grad: TensorType,
    indices: TensorType,
    num_weights: int,
    padding_idx: int,
    scale_grad_by_freq: bool,
) -> TensorType:
    """embedding_sparse_backward(Tensor grad, Tensor indices, int num_weights, int padding_idx, bool scale_grad_by_freq) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::empty")
def aten_empty(size: IntType, dtype: int = FLOAT.dtype) -> TTensor:  # type: ignore[type-var]
    # empty(SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor

    # using Zeros to simulate np.empty()
    size = op.Cast(size, to=INT64.dtype)
    zero = op.Constant(value_float=0.0)
    zero = op.Cast(zero, to=dtype)

    return op.Expand(zero, size)


@torch_op("aten::empty_like", trace_only=True)
def aten_empty_like(self: TTensor, dtype: int = -1) -> TTensor:
    """empty_like(Tensor self, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        zero = op.CastLike(0, self)
    else:
        zero = op.Cast(0, to=dtype)

    return _aten_empty_like_onnx(self, zero)


@torch_op("aten::empty_like", private=True)
def _aten_empty_like_onnx(self: TTensor, zero) -> TTensor:
    shape = op.Shape(self)
    return op.Expand(zero, shape)


def aten_empty_quantized(
    size: Sequence[int], qtensor: TensorType, memory_format: Optional[str] = None
) -> TensorType:
    """empty_quantized(int[] size, Tensor qtensor, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::empty_strided")
def aten_empty_strided(
    size: INT64, stride: INT64  # pylint: disable=unused-argument
) -> TTensor:  # type: ignore[type-var]
    # empty_strided(SymInt[] size, SymInt[] stride, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor

    # using Zeros to simulate empty()
    size = op.Cast(size, to=INT64.dtype)
    zero = op.Constant(value_float=0.0)

    return op.Expand(zero, size)


@torch_op("aten::eq")
def aten_eq(self: TTensor, other: TTensor) -> BOOL:
    """eq.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Equal(self, other)


@torch_op("aten::equal")
def aten_equal(self: TTensor, other: TTensor) -> BOOL:
    """equal(Tensor self, Tensor other) -> bool"""

    sub_self_other = op.Sub(self, other)
    abs_sub = op.Abs(sub_self_other)
    sum_of_abs = op.ReduceSum(abs_sub, keepdims=0)
    return op.Equal(sum_of_abs, 0)


@torch_op("aten::erf")
def aten_erf(self: TReal) -> TReal:
    """erf(Tensor self) -> Tensor"""

    return op.Erf(self)


def aten_erfc(self: TensorType) -> TensorType:
    """erfc(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_erfinv(self: TensorType) -> TensorType:
    """erfinv(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::exp")
def aten_exp(self: TFloat) -> TFloat:
    """exp(Tensor self) -> Tensor"""

    return op.Exp(self)


@torch_op("aten::exp2")
def aten_exp2(self: TFloat) -> TFloat:
    """exp2(Tensor self) -> Tensor"""

    two = op.Constant(value_int=2)
    two = op.CastLike(two, self)
    return op.Pow(two, self)


@torch_op("aten::expand")
def aten_expand(self: TTensor, size: TInt) -> TTensor:
    """expand(Tensor(a) self, SymInt[] size, *, bool implicit=False) -> Tensor(a)"""
    size = op.Cast(size, to=INT64.dtype)
    # NOTE: PyTorch supports `not changing dim` by -1, but ONNX supports `not changing dim` by 1.
    # To support -1 dim, we need to convert -1 to 1.
    size = op.Abs(size)
    return op.Expand(self, size)


@torch_op("aten::expand_as")
def aten_expand_as(self: TTensor, other: TTensor) -> TTensor:
    """expand_as(Tensor(a) self, Tensor other) -> Tensor(a)"""

    shape = op.Shape(other)
    result = op.Expand(self, shape)
    return result


def aten_expand_copy(self: TensorType, size: INT64, implicit: bool = False) -> TensorType:
    """expand_copy(Tensor self, SymInt[] size, *, bool implicit=False) -> Tensor"""

    raise NotImplementedError()


def aten_expm1(self: TensorType) -> TensorType:
    """expm1(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_eye(n: int) -> TensorType:
    """eye(int n, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_fake_quantize_per_channel_affine(
    self: TensorType,
    scale: TensorType,
    zero_point: TensorType,
    axis: int,
    quant_min: int,
    quant_max: int,
) -> TensorType:
    """fake_quantize_per_channel_affine(Tensor self, Tensor scale, Tensor zero_point, int axis, int quant_min, int quant_max) -> Tensor"""

    raise NotImplementedError()


def aten_fake_quantize_per_channel_affine_cachemask(
    self: TensorType,
    scale: TensorType,
    zero_point: TensorType,
    axis: int,
    quant_min: int,
    quant_max: int,
) -> tuple[TensorType, TensorType]:
    """fake_quantize_per_channel_affine_cachemask(Tensor self, Tensor scale, Tensor zero_point, int axis, int quant_min, int quant_max) -> (Tensor output, Tensor mask)"""

    raise NotImplementedError()


def aten_fake_quantize_per_channel_affine_cachemask_backward(
    grad: TensorType, mask: TensorType
) -> TensorType:
    """fake_quantize_per_channel_affine_cachemask_backward(Tensor grad, Tensor mask) -> Tensor"""

    raise NotImplementedError()


def aten_fake_quantize_per_tensor_affine(
    self: TensorType, scale: float, zero_point: int, quant_min: int, quant_max: int
) -> TensorType:
    """fake_quantize_per_tensor_affine(Tensor self, float scale, int zero_point, int quant_min, int quant_max) -> Tensor"""

    raise NotImplementedError()


def aten_fake_quantize_per_tensor_affine_cachemask(
    self: TensorType, scale: float, zero_point: int, quant_min: int, quant_max: int
) -> tuple[TensorType, TensorType]:
    """fake_quantize_per_tensor_affine_cachemask(Tensor self, float scale, int zero_point, int quant_min, int quant_max) -> (Tensor output, Tensor mask)"""

    raise NotImplementedError()


def aten_fake_quantize_per_tensor_affine_cachemask_backward(
    grad: TensorType, mask: TensorType
) -> TensorType:
    """fake_quantize_per_tensor_affine_cachemask_backward(Tensor grad, Tensor mask) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_linear_fp16_weight(
    input: TensorType, packed_weight: TensorType, bias: TensorType
) -> TensorType:
    """fbgemm_linear_fp16_weight(Tensor input, Tensor packed_weight, Tensor bias) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_linear_fp16_weight_fp32_activation(
    input: TensorType, packed_weight: TensorType, bias: TensorType
) -> TensorType:
    """fbgemm_linear_fp16_weight_fp32_activation(Tensor input, Tensor packed_weight, Tensor bias) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_linear_int8_weight(
    input: TensorType,
    weight: TensorType,
    packed: TensorType,
    col_offsets: TensorType,
    weight_scale: float,
    weight_zero_point: float,
    bias: TensorType,
) -> TensorType:
    """fbgemm_linear_int8_weight(Tensor input, Tensor weight, Tensor packed, Tensor col_offsets, Scalar weight_scale, Scalar weight_zero_point, Tensor bias) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_linear_int8_weight_fp32_activation(
    input: TensorType,
    weight: TensorType,
    packed: TensorType,
    col_offsets: TensorType,
    weight_scale: float,
    weight_zero_point: float,
    bias: TensorType,
) -> TensorType:
    """fbgemm_linear_int8_weight_fp32_activation(Tensor input, Tensor weight, Tensor packed, Tensor col_offsets, Scalar weight_scale, Scalar weight_zero_point, Tensor bias) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_linear_quantize_weight(
    input: TensorType,
) -> tuple[TensorType, TensorType, float, int]:
    """fbgemm_linear_quantize_weight(Tensor input) -> (Tensor, Tensor, float, int)"""

    raise NotImplementedError()


def aten_fbgemm_pack_gemm_matrix_fp16(input: TensorType) -> TensorType:
    """fbgemm_pack_gemm_matrix_fp16(Tensor input) -> Tensor"""

    raise NotImplementedError()


def aten_fbgemm_pack_quantized_matrix(input: TensorType) -> TensorType:
    """fbgemm_pack_quantized_matrix(Tensor input) -> Tensor"""

    raise NotImplementedError()


def aten_feature_alpha_dropout(input: TensorType, p: float, train: bool) -> TensorType:
    """feature_alpha_dropout(Tensor input, float p, bool train) -> Tensor"""

    raise NotImplementedError()


def aten_feature_dropout(input: TensorType, p: float, train: bool) -> TensorType:
    """feature_dropout(Tensor input, float p, bool train) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::fill")
def aten_fill(self: TTensor, value: TTensor) -> TTensor:
    """fill.Tensor(Tensor self, Tensor value) -> Tensor"""

    # after fill, the self Tensor should keep origianl type
    shape = op.Shape(self)
    expanded = op.Expand(value, shape)
    result = op.CastLike(expanded, self)
    return result


def aten_fix(self: TensorType) -> TensorType:
    """fix(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::flip")
def aten_flip(self: TTensor, dims: INT64) -> TTensor:
    """flip(Tensor self, int[] dims) -> Tensor"""

    shape_dim = op.Shape(dims)
    neg_1 = op.Constant(value_int=-1)
    starts = op.Expand(neg_1, shape_dim)  # something like [-1, -1, -1]
    steps = op.Expand(neg_1, shape_dim)  # something like [-1, -1, -1]
    ends = op.Expand(_INT64_MIN, shape_dim)  # something like [-xxx, -xxx, -xxx]
    result = op.Slice(self, starts, ends, dims, steps)
    return result


def aten_fliplr(self: TensorType) -> TensorType:
    """fliplr(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_flipud(self: TensorType) -> TensorType:
    """flipud(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::floor")
def aten_floor(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """floor(Tensor self) -> Tensor"""

    return op.Floor(self)


def aten_floor_divide(self: TensorType, other: TensorType) -> TensorType:
    """floor_divide(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_fmax(self: TensorType, other: TensorType) -> TensorType:
    """fmax(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_fmin(self: TensorType, other: TensorType) -> TensorType:
    """fmin(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::fmod")
def aten_fmod(self: TReal, other: TReal) -> TReal:
    """fmod.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Mod(self, other, fmod=1)


def aten_frac(self: TensorType) -> TensorType:
    """frac(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_frexp(self: TensorType) -> tuple[TensorType, TensorType]:
    """frexp.Tensor(Tensor self) -> (Tensor mantissa, Tensor exponent)"""

    raise NotImplementedError()


def aten_frobenius_norm(self: TensorType) -> TensorType:
    """frobenius_norm(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_from_file(
    filename: str, shared: Optional[bool] = None, size: Optional[int] = 0
) -> TensorType:
    """from_file(str filename, bool? shared=None, int? size=0, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::full")
def aten_full(size: INT64, fill_value: FLOAT, dtype: int = FLOAT.dtype):
    """full(SymInt[] size, Scalar fill_value, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    size = op.Cast(size, to=INT64.dtype)
    fill_value = op.Cast(fill_value, to=dtype)
    return op.Expand(fill_value, size)


@torch_op("aten::full_like")
def aten_full_like(self, fill_value: TensorType, dtype: int = FLOAT.dtype):
    """full_like(Tensor self, Scalar fill_value, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    fill_value = op.Cast(fill_value, to=dtype)
    self_shape = op.Shape(self)

    return op.Expand(fill_value, self_shape)


def aten_fused_moving_avg_obs_fake_quant(
    self: TensorType,
    observer_on: TensorType,
    fake_quant_on: TensorType,
    running_min: TensorType,
    running_max: TensorType,
    scale: TensorType,
    zero_point: TensorType,
    averaging_const: float,
    quant_min: int,
    quant_max: int,
    ch_axis: int,
    per_row_fake_quant: bool = False,
    symmetric_quant: bool = False,
) -> TensorType:
    """fused_moving_avg_obs_fake_quant(Tensor self, Tensor observer_on, Tensor fake_quant_on, Tensor(a!) running_min, Tensor(b!) running_max, Tensor(c!) scale, Tensor(d!) zero_point, float averaging_const, int quant_min, int quant_max, int ch_axis, bool per_row_fake_quant=False, bool symmetric_quant=False) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::gather")
def aten_gather(
    self: TReal,
    index: TInt,
    dim: int,
    sparse_grad: bool = False,  # pylint: disable=unused-argument
) -> TReal:
    """gather(Tensor self, int dim, Tensor index, *, bool sparse_grad=False) -> Tensor"""

    if op.Size(op.Shape(index)) == 0:  # When (index) is empty, return (self)
        result = self
    else:
        if op.Size(op.Shape(self)) == 0:  # Unsqueeze for GatherElements op
            self = op.Reshape(self, op.Constant(value_ints=[-1]))
        if op.Size(index) == 0:  # Return empty array
            result = op.CastLike(index, self)
        else:
            index_int32 = op.Cast(index, to=INT32.dtype)
            result = op.GatherElements(self, index_int32, axis=dim)
    return result


def aten_gather_backward(
    grad: TensorType, self: TensorType, dim: int, index: TensorType, sparse_grad: bool
) -> TensorType:
    """gather_backward(Tensor grad, Tensor self, int dim, Tensor index, bool sparse_grad) -> Tensor"""

    raise NotImplementedError()


def aten_gcd(self: TensorType, other: TensorType) -> TensorType:
    """gcd(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::ge")
def aten_ge(self: TReal, other: TReal) -> BOOL:
    """ge.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.GreaterOrEqual(self, other)


def aten_geqrf(self: TensorType) -> tuple[TensorType, TensorType]:
    """geqrf(Tensor self) -> (Tensor a, Tensor tau)"""

    raise NotImplementedError()


def aten_ger(self: TensorType, vec2: TensorType) -> TensorType:
    """ger(Tensor self, Tensor vec2) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::greater")
def aten_greater(self: TReal, other: TReal) -> BOOL:
    """greater.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Greater(self, other)


@torch_op("aten::greater_equal")
def aten_greater_equal(self: TReal, other: TReal) -> BOOL:
    """greater_equal.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.GreaterOrEqual(self, other)


@torch_op("aten::grid_sampler", trace_only=True)
def aten_grid_sampler(
    input: TTensor,
    grid: TTensor,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
) -> TTensor:
    """grid_sampler(Tensor input, Tensor grid, int interpolation_mode, int padding_mode, bool align_corners) -> Tensor"""

    inter_mode_options = ("bilinear", "nearest", "bicubic")
    inter_mode_str = inter_mode_options[interpolation_mode]

    padding_mode_options = ("zeros", "border", "reflection")
    padding_mode_str = padding_mode_options[padding_mode]

    # Only one onnx Op so don't put into private function
    return op.GridSample(
        input,
        grid,
        align_corners=align_corners,
        mode=inter_mode_str,
        padding_mode=padding_mode_str,
    )


@torch_op("aten::grid_sampler_2d", trace_only=True)
def aten_grid_sampler_2d(
    input: TTensor,
    grid: TTensor,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
) -> TTensor:
    """grid_sampler_2d(Tensor input, Tensor grid, int interpolation_mode, int padding_mode, bool align_corners) -> Tensor"""

    inter_mode_options = ("bilinear", "nearest", "bicubic")
    inter_mode_str = inter_mode_options[interpolation_mode]

    padding_mode_options = ("zeros", "border", "reflection")
    padding_mode_str = padding_mode_options[padding_mode]

    # Only one onnx Op so don't put into private function
    return op.GridSample(
        input,
        grid,
        align_corners=align_corners,
        mode=inter_mode_str,
        padding_mode=padding_mode_str,
    )


def aten_grid_sampler_2d_backward(
    grad_output: TensorType,
    input: TensorType,
    grid: TensorType,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType]:
    """grid_sampler_2d_backward(Tensor grad_output, Tensor input, Tensor grid, int interpolation_mode, int padding_mode, bool align_corners, bool[2] output_mask) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_grid_sampler_3d(
    input: TensorType,
    grid: TensorType,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
) -> TensorType:
    """grid_sampler_3d(Tensor input, Tensor grid, int interpolation_mode, int padding_mode, bool align_corners) -> Tensor"""

    raise NotImplementedError()


def aten_grid_sampler_3d_backward(
    grad_output: TensorType,
    input: TensorType,
    grid: TensorType,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType]:
    """grid_sampler_3d_backward(Tensor grad_output, Tensor input, Tensor grid, int interpolation_mode, int padding_mode, bool align_corners, bool[2] output_mask) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_group_norm(
    input: TensorType,
    num_groups: int,
    weight: Optional[TensorType] = None,
    bias: Optional[TensorType] = None,
    eps: float = 1e-05,
    cudnn_enabled: bool = True,
) -> TensorType:
    """group_norm(Tensor input, int num_groups, Tensor? weight=None, Tensor? bias=None, float eps=1e-05, bool cudnn_enabled=True) -> Tensor"""

    raise NotImplementedError()


def aten_gru_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: Optional[TensorType] = None,
    b_hh: Optional[TensorType] = None,
) -> TensorType:
    """gru_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor? b_ih=None, Tensor? b_hh=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::gt")
def aten_gt(self: TReal, other: TReal) -> BOOL:
    """gt.Tensor(Tensor self, Tensor other) -> Tensor"""

    # TODO(justinchuby): Input spec: non bool tensor
    # Boolean inputs can be pre-casted by policy
    return op.Greater(self, other)


def aten_hamming_window(window_length: int) -> TensorType:
    """hamming_window(int window_length, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_hann_window(window_length: int) -> TensorType:
    """hann_window(int window_length, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_hardshrink(self: TensorType, lambd: float = 0.5) -> TensorType:
    """hardshrink(Tensor self, Scalar lambd=0.5) -> Tensor"""

    raise NotImplementedError()


def aten_hardshrink_backward(
    grad_out: TensorType, self: TensorType, lambd: float
) -> TensorType:
    """hardshrink_backward(Tensor grad_out, Tensor self, Scalar lambd) -> Tensor"""

    raise NotImplementedError()


def aten_heaviside(self: TensorType, values: TensorType) -> TensorType:
    """heaviside(Tensor self, Tensor values) -> Tensor"""

    raise NotImplementedError()


def aten_hinge_embedding_loss(
    self: TensorType, target: TensorType, margin: float = 1.0, reduction: int = 1
) -> TensorType:
    """hinge_embedding_loss(Tensor self, Tensor target, float margin=1.0, int reduction=Mean) -> Tensor"""

    raise NotImplementedError()


def aten_histc(
    self: TensorType, bins: int = 100, min: float = 0.0, max: float = 0.0
) -> TensorType:
    """histc(Tensor self, int bins=100, Scalar min=0, Scalar max=0) -> Tensor"""

    raise NotImplementedError()


def aten_histogramdd(
    self: TensorType,
    bins: Sequence[int],
    range: Optional[float] = None,
    weight: Optional[TensorType] = None,
    density: bool = False,
) -> tuple[TensorType, TensorType]:
    """histogramdd(Tensor self, int[] bins, float[]? range=None, Tensor? weight=None, bool density=False) -> (Tensor hist, Tensor[] bin_edges)"""

    raise NotImplementedError()


def aten_hspmm(mat1: TensorType, mat2: TensorType) -> TensorType:
    """hspmm(Tensor mat1, Tensor mat2) -> Tensor"""

    raise NotImplementedError()


def aten_hstack(tensors: Sequence[TensorType]) -> TensorType:
    """hstack(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


def aten_hypot(self: TensorType, other: TensorType) -> TensorType:
    """hypot(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_i0(self: TensorType) -> TensorType:
    """i0(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_igamma(self: TensorType, other: TensorType) -> TensorType:
    """igamma(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_igammac(self: TensorType, other: TensorType) -> TensorType:
    """igammac(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_imag(self: TensorType) -> TensorType:
    """imag(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_index(self: TensorType, indices: Optional[Sequence[TensorType]]) -> TensorType:
    """index.Tensor(Tensor self, Tensor?[] indices) -> Tensor"""

    raise NotImplementedError()


def aten_index_add(
    self: TensorType, dim: int, index: TensorType, source: TensorType, alpha: float = 1
) -> TensorType:
    """index_add(Tensor self, int dim, Tensor index, Tensor source, *, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


def aten_index_copy(
    self: TensorType, dim: int, index: TensorType, source: TensorType
) -> TensorType:
    """index_copy(Tensor self, int dim, Tensor index, Tensor source) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::index_put")
def aten_index_put(
    self: TReal,
    indices: Sequence[INT64],
    values: TReal,
    accumulate: bool = False,
) -> TReal:
    """index_put(Tensor self, Tensor?[] indices, Tensor values, bool accumulate=False) -> Tensor"""

    index = op.SequenceAt(indices, 0)  # assume indices only have 1 element
    # change array([1,3]) to array([[1,1,1,1,1],[3,3,3,3,3]])
    self_dim_1 = op.Gather(op.Shape(self), 1)
    index_dim_0 = op.Gather(op.Shape(index), 0)
    neg_1 = op.Constant(value_ints=[-1])
    shape = op.Concat(op.Reshape(self_dim_1, neg_1), op.Reshape(index_dim_0, neg_1), axis=0)
    new_ind = op.Expand(index, shape)
    new_ind_t = op.Transpose(new_ind)

    if op.Cast(accumulate, to=BOOL.dtype):
        # put values into zeros array first, then add to input
        zeros = op.Expand(op.Constant(value_float=0.0), op.Shape(self))
        result = op.ScatterElements(zeros, new_ind_t, values)
        result = op.Add(result, self)
    else:
        result = op.ScatterElements(self, new_ind_t, values)
    return result


@torch_op("aten::index_put_bool", overload=True)
def aten_index_put_bool(
    self: TReal,
    indices: Sequence[BOOL],
    values: TReal,
    accumulate: bool = False,
) -> TReal:
    """index_put(Tensor self, Tensor?[] indices, Tensor values, bool accumulate=False) -> Tensor"""

    index = op.SequenceAt(indices, 0)  # assume indices only have 1 element
    # FIXME: ORT ArgMax fails on INT64 input even though ONNX allows it
    index_int = op.Cast(index, to=INT32.dtype)
    # if all False, return self
    if op.ReduceSum(index_int) == 0:
        result = self
    else:
        # change array([F,F,T,F,F]) to array([2])
        index = op.ArgMax(index_int)  # assume index only have 1 True
        # change array([2]) to array([2,2,2,2,2])
        self_dim_1 = op.Gather(op.Shape(self), 1)
        index_dim_0 = op.Gather(op.Shape(index), 0)
        neg_1 = op.Constant(value_ints=[-1])
        shape = op.Concat(
            op.Reshape(self_dim_1, neg_1), op.Reshape(index_dim_0, neg_1), axis=0
        )
        new_ind = op.Expand(index, shape)
        new_ind_t = op.Transpose(new_ind)

        # values must have same rank with input(self)
        if op.Size(op.Shape(values)) < op.Size(op.Shape(self)):  # type: ignore[operator]
            values = op.Unsqueeze(values, op.Constant(value_ints=[0]))

        if op.Cast(accumulate, to=BOOL.dtype):
            zeros = op.Expand(op.Constant(value_float=0.0), op.Shape(self))
            result = op.ScatterElements(zeros, new_ind_t, values)
            result = op.Add(result, self)
        else:
            result = op.ScatterElements(self, new_ind_t, values)

    return result


def aten_index_reduce(
    self: TensorType,
    dim: int,
    index: TensorType,
    source: TensorType,
    reduce: str,
    include_self: bool = True,
) -> TensorType:
    """index_reduce(Tensor self, int dim, Tensor index, Tensor source, str reduce, *, bool include_self=True) -> Tensor"""

    raise NotImplementedError()


# FIXME(#277): Script when attributes can come before inputs
@torch_op("aten::index_select", trace_only=True)
def aten_index_select(self: TTensor, dim: int, index: IntType) -> TTensor:
    """index_select(Tensor self, int dim, Tensor index) -> Tensor"""

    return _aten_index_select_onnx(self, index, dim=dim)


@torch_op("aten::index_select", private=True)
def _aten_index_select_onnx(self: TTensor, index: IntType, dim: int) -> TTensor:
    """index_select(Tensor self, int dim, Tensor index) -> Tensor"""

    if op.Size(op.Shape(self)) == 0:
        result = self
    else:
        # Index can be a scalar. Reshape it to a rank 1 tensor.
        index = op.Reshape(index, op.Constant(value_ints=[-1]))
        index = op.Cast(index, to=INT64.dtype)

        result = op.Gather(self, index, axis=dim)

    return result


def aten_index_select_backward(
    grad: TensorType, self_sizes: INT64, dim: int, index: TensorType
) -> TensorType:
    """index_select_backward(Tensor grad, SymInt[] self_sizes, int dim, Tensor index) -> Tensor"""

    raise NotImplementedError()


def aten_indices(self: TensorType) -> TensorType:
    """indices(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_indices_copy(self: TensorType) -> TensorType:
    """indices_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_inner(self: TensorType, other: TensorType) -> TensorType:
    """inner(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_instance_norm(
    input: TensorType,
    weight: Optional[TensorType],
    bias: Optional[TensorType],
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    use_input_stats: bool,
    momentum: float,
    eps: float,
    cudnn_enabled: bool,
) -> TensorType:
    """instance_norm(Tensor input, Tensor? weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool use_input_stats, float momentum, float eps, bool cudnn_enabled) -> Tensor"""

    raise NotImplementedError()


def aten_int_repr(self: TensorType) -> TensorType:
    """int_repr(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_inverse(self: TensorType) -> TensorType:
    """inverse(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_is_coalesced(self: TensorType) -> bool:
    """is_coalesced(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_complex(self: TensorType) -> bool:
    """is_complex(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_conj(self: TensorType) -> bool:
    """is_conj(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_distributed(self: TensorType) -> bool:
    """is_distributed(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_floating_point(self: TensorType) -> bool:
    """is_floating_point(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_inference(self: TensorType) -> bool:
    """is_inference(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_leaf(self: TensorType) -> bool:
    """is_leaf(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_neg(self: TensorType) -> bool:
    """is_neg(Tensor self) -> bool"""

    raise NotImplementedError()


@torch_op("aten::is_nonzero")
def aten_is_nonzero(self: Union[RealType, BOOL]) -> BOOL:
    """is_nonzero(Tensor self) -> bool"""

    # if size != 1, return False
    # else [0],[True],[0.0] return True, others return False
    result = op.Not(op.Size(self) != 1)
    if result:
        result = op.Cast(self, to=BOOL.dtype)
    return result


def aten_is_pinned(self: TensorType, device: Optional[str] = None) -> bool:
    """is_pinned(Tensor self, Device? device=None) -> bool"""

    raise NotImplementedError()


@torch_op("aten::is_same_size")
def aten_is_same_size(self: TTensor, other: TTensor) -> BOOL:
    """is_same_size(Tensor self, Tensor other) -> bool"""

    # Cannot compare different shape of two tensors using op.Equal()
    # So we need to compare the rank first, if rank is same, then compare shape
    self_rank = op.Size(op.Shape(self))
    other_rank = op.Size(op.Shape(other))
    result = op.Equal(self_rank, other_rank)
    if result:  # Same rank, then compare shape
        self_shape = op.Shape(self)
        other_shape = op.Shape(other)
        result_bool = op.Equal(self_shape, other_shape)
        result_int = op.Cast(result_bool, to=INT8.dtype)
        result = op.Cast(op.ReduceMin(result_int, keepdims=0), to=BOOL.dtype)

    return result


def aten_is_set_to(self: TensorType, tensor: TensorType) -> bool:
    """is_set_to(Tensor self, Tensor tensor) -> bool"""

    raise NotImplementedError()


def aten_is_signed(self: TensorType) -> bool:
    """is_signed(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_is_vulkan_available() -> bool:
    """is_vulkan_available() -> bool"""

    raise NotImplementedError()


@torch_op("aten::isclose")
def aten_isclose(
    self: TReal,
    other: TReal,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,  # pylint: disable=unused-argument
) -> BOOL:
    """isclose(Tensor self, Tensor other, float rtol=1e-05, float atol=1e-08, bool equal_nan=False) -> Tensor"""

    # FIXME: check equal_nan when self and other are all NaN
    # |input - other| <= atol + rtol x |other|
    left_part = op.Abs(op.Sub(self, other))
    right_part = op.Add(atol, op.Mul(rtol, op.Abs(other)))
    result = op.LessOrEqual(left_part, right_part)
    return result


@torch_op("aten::isfinite")
def aten_isfinite(self: TFloatOrBFloat16) -> BOOL:
    """isfinite(Tensor self) -> Tensor"""

    not_inf = op.Not(op.IsInf(self))
    not_nan = op.Not(op.IsNaN(self))  # TODO: The test case doesnt cover this condition
    return op.And(not_inf, not_nan)


@torch_op("aten::isinf")
def aten_isinf(self: Union[FLOAT, DOUBLE]) -> BOOL:
    """isinf(Tensor self) -> Tensor"""

    return op.IsInf(self)


@torch_op("aten::isnan")
def aten_isnan(self: TFloatOrBFloat16) -> BOOL:
    """isnan(Tensor self) -> Tensor"""

    return op.IsNaN(self)


@torch_op("aten::isneginf")
def aten_isneginf(self: TReal) -> BOOL:
    """isneginf(Tensor self) -> Tensor"""

    return op.And(op.Less(self, 0), op.IsInf(self))


@torch_op("aten::isposinf")
def aten_isposinf(self: TReal) -> BOOL:
    """isposinf(Tensor self) -> Tensor"""

    return op.And(op.Greater(self, 0), op.IsInf(self))


def aten_isreal(self: TensorType) -> TensorType:
    """isreal(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_istft(
    self: TensorType,
    n_fft: int,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    window: Optional[TensorType] = None,
    center: bool = True,
    normalized: bool = False,
    onesided: Optional[bool] = None,
    length: Optional[int] = None,
    return_complex: bool = False,
) -> TensorType:
    """istft(Tensor self, int n_fft, int? hop_length=None, int? win_length=None, Tensor? window=None, bool center=True, bool normalized=False, bool? onesided=None, int? length=None, bool return_complex=False) -> Tensor"""

    raise NotImplementedError()


def aten_item(self: TensorType) -> float:
    """item(Tensor self) -> Scalar"""

    raise NotImplementedError()


def aten_kaiser_window(window_length: int) -> TensorType:
    """kaiser_window(int window_length, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_kl_div(
    self: TensorType, target: TensorType, reduction: int = 1, log_target: bool = False
) -> TensorType:
    """kl_div(Tensor self, Tensor target, int reduction=Mean, *, bool log_target=False) -> Tensor"""

    raise NotImplementedError()


def aten_kron(self: TensorType, other: TensorType) -> TensorType:
    """kron(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_kthvalue(
    self: TensorType, k: int, dim: int = -1, keepdim: bool = False
) -> tuple[TensorType, TensorType]:
    """kthvalue(Tensor self, int k, int dim=-1, bool keepdim=False) -> (Tensor values, Tensor indices)"""

    raise NotImplementedError()


@torch_op("aten::layer_norm", trace_only=True)
def aten_layer_norm(
    input: TReal,
    normalized_shape: INT64,
    weight: Optional[TReal] = None,
    bias: Optional[TReal] = None,
    eps: float = 1e-05,
) -> TReal:
    """layer_norm(Tensor input, int[] normalized_shape, Tensor? weight=None, Tensor? bias=None, float eps=1e-05, bool cudnn_enable=True) -> Tensor"""

    # trace_only to use Python to obtain start_axis
    start_axis = -len(normalized_shape)

    if weight is None:
        one = op.Constant(value_float=1.0)
        weight = op.Expand(one, op.Shape(input, start=start_axis))

    if bias is None:
        zero = op.Constant(value_float=0.0)
        bias = op.Expand(zero, op.Shape(input, start=start_axis))

    return _aten_layer_norm_onnx(input, weight, bias, axis=start_axis, eps=eps)


@torch_op("aten::layer_norm", private=True)
def _aten_layer_norm_onnx(
    input: TReal,
    weight: TReal,
    bias: Optional[TReal],
    axis: int,
    eps: float = 1e-05,
) -> TReal:
    """layer_norm(Tensor input, int[] normalized_shape, Tensor? weight=None, Tensor? bias=None, float eps=1e-05, bool cudnn_enable=True) -> Tensor"""

    # TODO(justinchuby): Use OptionalHasElement after onnx/onnx#4982
    result, _, _ = op.LayerNormalization(input, weight, bias, axis=axis, epsilon=eps)
    return result


def aten_lcm(self: TensorType, other: TensorType) -> TensorType:
    """lcm(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_ldexp(self: TensorType, other: TensorType) -> TensorType:
    """ldexp.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::le")
def aten_le(self: TReal, other: TReal) -> BOOL:
    """le.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.LessOrEqual(self, other)


def aten_lerp(self: TensorType, end: TensorType, weight: TensorType) -> TensorType:
    """lerp.Tensor(Tensor self, Tensor end, Tensor weight) -> Tensor"""

    raise NotImplementedError()


def aten_less(self: TensorType, other: TensorType) -> TensorType:
    """less.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_less_equal(self: TensorType, other: TensorType) -> TensorType:
    """less_equal.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_lgamma(self: TensorType) -> TensorType:
    """lgamma(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_lift(self: TensorType) -> TensorType:
    """lift(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_lift_fresh(self: TensorType) -> TensorType:
    """lift_fresh(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_lift_fresh_copy(self: TensorType) -> TensorType:
    """lift_fresh_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_linear_backward(
    self: TensorType, grad_output: TensorType, weight: TensorType, output_mask: Sequence[bool]
) -> tuple[TensorType, TensorType, TensorType]:
    """linear_backward(Tensor self, Tensor grad_output, Tensor weight, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_linspace(start: float, end: float, steps: int) -> TensorType:
    """linspace(Scalar start, Scalar end, int steps, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("log")
def aten_log(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """log(Tensor self) -> Tensor"""

    return op.Log(self)


@torch_op("aten::log10")
def aten_log10(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """log10(Tensor self) -> Tensor"""

    return op.Div(op.Log(self), op.Log(10.0))


@torch_op("aten::log1p")
def aten_log1p(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """log1p(Tensor self) -> Tensor"""

    return op.Log(op.Add(self, 1.0))


@torch_op("aten::log2")
def aten_log2(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """log2(Tensor self) -> Tensor"""

    return op.Div(op.Log(self), op.Log(2.0))


@torch_op("aten::logaddexp")
def aten_logaddexp(self: TFloatOrBFloat16, other: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """logaddexp(Tensor self, Tensor other) -> Tensor"""

    return op.Log(op.Add(op.Exp(self), op.Exp(other)))


@torch_op("aten::logaddexp2")
def aten_logaddexp2(self: TFloatOrBFloat16, other: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """logaddexp2(Tensor self, Tensor other) -> Tensor"""
    summation = op.Add(op.Pow(2.0, self), op.Pow(2.0, other))

    return op.Div(op.Log(summation), op.Log(2.0))


@torch_op("aten::logcumsumexp")
def aten_logcumsumexp(self: TFloatOrBFloat16, dim: INT64) -> TFloatOrBFloat16:
    """logcumsumexp(Tensor self, int dim) -> Tensor"""

    if op.Size(op.Shape(self)) == 0:
        # A scalar
        result = op.Identity(self)
    else:
        # FIXME(justinchuby): Ensure numerical stability
        result = op.Log(op.CumSum(op.Exp(self), dim))

    return result


@torch_op("aten::logdet")
def aten_logdet(self: TFloat) -> TFloat:
    """logdet(Tensor self) -> Tensor"""

    return op.Log(op.Det(self))


@torch_op("aten::logical_and")
def aten_logical_and(self: BOOL, other: BOOL) -> BOOL:
    """logical_and(Tensor self, Tensor other) -> Tensor"""

    return op.And(self, other)


@torch_op("aten::logical_not")
def aten_logical_not(self: BOOL) -> BOOL:
    """logical_not(Tensor self) -> Tensor"""

    return op.Not(self)


@torch_op("aten::logical_or")
def aten_logical_or(self: BOOL, other: BOOL) -> BOOL:
    """logical_or(Tensor self, Tensor other) -> Tensor"""

    return op.Or(self, other)


@torch_op("aten::logical_xor")
def aten_logical_xor(self: BOOL, other: BOOL) -> BOOL:
    """logical_xor(Tensor self, Tensor other) -> Tensor"""

    return op.Xor(self, other)


def aten_logit(self: TensorType, eps: Optional[float] = None) -> TensorType:
    """logit(Tensor self, float? eps=None) -> Tensor"""

    raise NotImplementedError()


def aten_logspace(start: float, end: float, steps: int, base: float = 10.0) -> TensorType:
    """logspace(Scalar start, Scalar end, int steps, float base=10.0, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::logsumexp")
def aten_logsumexp(self: TReal, dim: INT64, keepdim: int = False) -> TReal:
    """logsumexp(Tensor self, int[1] dim, bool keepdim=False) -> Tensor"""

    if op.Size(op.Shape(self)) == 0:
        # A scalar
        result = self
    else:
        result = op.ReduceLogSumExp(self, dim, keepdims=keepdim)
    return result


def aten_lshift(self: TensorType, other: TensorType) -> TensorType:
    """__lshift__.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_lstm_cell(
    input: TensorType,
    hx: Sequence[TensorType],
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: Optional[TensorType] = None,
    b_hh: Optional[TensorType] = None,
) -> tuple[TensorType, TensorType]:
    """lstm_cell(Tensor input, Tensor[] hx, Tensor w_ih, Tensor w_hh, Tensor? b_ih=None, Tensor? b_hh=None) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_lstm_mps_backward(
    grad_y: TensorType,
    grad_hy: Optional[TensorType],
    grad_cy: Optional[TensorType],
    z_state: TensorType,
    cell_state_fwd: TensorType,
    input: TensorType,
    hx: Sequence[TensorType],
    params: Sequence[TensorType],
    has_biases: bool,
    num_layers: int,
    dropout: float,
    train: bool,
    bidirectional: bool,
    batch_first: bool,
) -> tuple[TensorType, TensorType, TensorType]:
    """lstm_mps_backward(Tensor grad_y, Tensor? grad_hy, Tensor? grad_cy, Tensor z_state, Tensor cell_state_fwd, Tensor input, Tensor[] hx, Tensor[] params, bool has_biases, int num_layers, float dropout, bool train, bool bidirectional, bool batch_first) -> (Tensor, Tensor[], Tensor[])"""

    raise NotImplementedError()


@torch_op("aten::lt")
def aten_lt(self: TReal, other: TReal) -> BOOL:
    """lt.Tensor(Tensor self, Tensor other) -> Tensor"""

    # TODO(justinchuby): Input spec: non bool tensor
    # Boolean inputs can be pre-casted by policy
    return op.Less(self, other)


def aten_lu_solve(self: TensorType, LU_data: TensorType, LU_pivots: TensorType) -> TensorType:
    """lu_solve(Tensor self, Tensor LU_data, Tensor LU_pivots) -> Tensor"""

    raise NotImplementedError()


def aten_lu_unpack(
    LU_data: TensorType,
    LU_pivots: TensorType,
    unpack_data: bool = True,
    unpack_pivots: bool = True,
) -> tuple[TensorType, TensorType, TensorType]:
    """lu_unpack(Tensor LU_data, Tensor LU_pivots, bool unpack_data=True, bool unpack_pivots=True) -> (Tensor P, Tensor L, Tensor U)"""

    raise NotImplementedError()


def aten_mH(self: TensorType) -> TensorType:
    """mH(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_mT(self: TensorType) -> TensorType:
    """mT(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_margin_ranking_loss(
    input1: TensorType,
    input2: TensorType,
    target: TensorType,
    margin: float = 0.0,
    reduction: int = 1,
) -> TensorType:
    """margin_ranking_loss(Tensor input1, Tensor input2, Tensor target, float margin=0.0, int reduction=Mean) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::masked_fill")
def aten_masked_fill(self: TTensor, mask: BOOL, value: TTensor) -> TTensor:
    """masked_fill.Tensor(Tensor self, Tensor mask, Tensor value) -> Tensor"""
    # NOTE: Do not attempt to cast `mask` to BOOL because mask should not take any other types.
    # `mask` coming in as other types is often an error and should fail the model.
    value_cast = op.CastLike(value, self)
    return op.Where(mask, value_cast, self)


def aten_masked_scatter(self: TensorType, mask: TensorType, source: TensorType) -> TensorType:
    """masked_scatter(Tensor self, Tensor mask, Tensor source) -> Tensor"""

    raise NotImplementedError()


def aten_masked_select(self: TensorType, mask: TensorType) -> TensorType:
    """masked_select(Tensor self, Tensor mask) -> Tensor"""

    raise NotImplementedError()


def aten_masked_select_backward(
    grad: TensorType, input: TensorType, mask: TensorType
) -> TensorType:
    """masked_select_backward(Tensor grad, Tensor input, Tensor mask) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::matmul")
def aten_matmul(
    self: TRealUnlessInt16OrInt8, other: TRealUnlessInt16OrInt8
) -> TRealUnlessInt16OrInt8:
    """matmul(Tensor self, Tensor other) -> Tensor"""

    return op.MatMul(self, other)


def aten_matmul_backward(
    grad: TensorType, self: TensorType, other: TensorType, mask: Sequence[bool]
) -> tuple[TensorType, TensorType]:
    """matmul_backward(Tensor grad, Tensor self, Tensor other, bool[2] mask) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_matrix_H(self: TensorType) -> TensorType:
    """matrix_H(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_matrix_exp(self: TensorType) -> TensorType:
    """matrix_exp(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_matrix_exp_backward(self: TensorType, grad: TensorType) -> TensorType:
    """matrix_exp_backward(Tensor self, Tensor grad) -> Tensor"""

    raise NotImplementedError()


def aten_matrix_power(self: TensorType, n: int) -> TensorType:
    """matrix_power(Tensor self, int n) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::max", trace_only=True)
def aten_max(
    self: TReal, dim_or_other: Union[TReal, INT64] = None, keepdim: BOOL = None
) -> TReal:
    """max(Tensor self) -> Tensor"""

    self_rank = op.Size(op.Shape(self))
    if self_rank == 0:
        self = op.Reshape(self, op.Constant(value_int=[-1]))

    output = 1

    if op.OptionalHasElement(dim_or_other):
        if isinstance(dim_or_other, int):
            if not op.OptionalHasElement(keepdim):
                keepdim = False
            result, indices = _aten_max_with_dim(self, dim_or_other, keepdim)
            output = 2
        else:  # dim_or_other is tensor
            result = _aten_max_with_other(self, dim_or_other)
    else:
        result = _aten_max_with_no_dim(self)

    if self_rank == 0:
        result = op.Squeeze(result)

    if output == 2:
        if self_rank == 0:
            indices = op.Squeeze(indices)  # type: ignore[has-type]
        return result, indices
    return result


@torch_op("aten::max", private=True)
def _aten_max_with_no_dim(self: TReal) -> TReal:
    result = op.ReduceMax(self, keepdims=0)
    return result


@torch_op("aten::max", private=True)
def _aten_max_with_other(self: TReal, other: TReal) -> TReal:
    result = op.Max(self, other)
    return result


@torch_op("aten::max", private=True)
def _aten_max_with_dim(self: TReal, dim: int, keepdim: bool):
    dims = op.Reshape(dim, op.Constant(value_int=[-1]))
    result = op.ReduceMax(self, dims, keepdims=keepdim)
    indices = op.ArgMax(self, axis=dim, keepdims=keepdim)
    return result, indices


@torch_op("aten::maximum")
def aten_maximum(self: TReal, other: TReal) -> TReal:
    """maximum(Tensor self, Tensor other) -> Tensor"""

    return op.Max(self, other)


def aten_mean(self: TensorType, dtype: Optional[int] = None) -> TensorType:
    """mean(Tensor self, *, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_median(self: TensorType) -> TensorType:
    """median(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_meshgrid(tensors: Sequence[TensorType]) -> TensorType:
    """meshgrid(Tensor[] tensors) -> Tensor[]"""

    raise NotImplementedError()


@torch_op("aten::min")
def aten_min(self: TReal) -> TReal:
    """min(Tensor self) -> Tensor"""

    return op.ReduceMin(self, keepdims=0)


@torch_op("aten::min", overload=True)
def aten_min_dim(self: TReal, dim: int, keepdim: bool = False) -> Tuple[TReal, TInt]:
    if op.Size(op.Shape(self)) == 0:
        result = self
        indices = op.Constant(value_int=0)
    else:
        dims = op.Reshape(dim, op.Constant(value_ints=[-1]))
        result = op.ReduceMin(self, dims, keepdims=keepdim)
        indices = op.ArgMin(self, axis=dim, keepdims=keepdim)

    return result, indices


@torch_op("aten::min", overload=True)
def aten_min_other(self: TReal, other: TReal) -> TReal:
    return op.Min(self, other)


@torch_op("aten::minimum")
def aten_minimum(self: TReal, other: TReal) -> TReal:
    """minimum(Tensor self, Tensor other) -> Tensor"""

    return op.Min(self, other)


def aten_miopen_batch_norm(
    input: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    training: bool,
    exponential_average_factor: float,
    epsilon: float,
) -> tuple[TensorType, TensorType, TensorType]:
    """miopen_batch_norm(Tensor input, Tensor weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool training, float exponential_average_factor, float epsilon) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_miopen_batch_norm_backward(
    input: TensorType,
    grad_output: TensorType,
    weight: TensorType,
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    save_mean: Optional[TensorType],
    save_var: Optional[TensorType],
    epsilon: float,
) -> tuple[TensorType, TensorType, TensorType]:
    """miopen_batch_norm_backward(Tensor input, Tensor grad_output, Tensor weight, Tensor? running_mean, Tensor? running_var, Tensor? save_mean, Tensor? save_var, float epsilon) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_miopen_convolution(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    padding: INT64,
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
) -> TensorType:
    """miopen_convolution(Tensor self, Tensor weight, Tensor? bias, SymInt[] padding, int[] stride, int[] dilation, int groups, bool benchmark, bool deterministic) -> Tensor"""

    raise NotImplementedError()


def aten_miopen_convolution_add_relu(
    self: TensorType,
    weight: TensorType,
    z: TensorType,
    alpha: Optional[float],
    bias: Optional[TensorType],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    groups: int,
) -> TensorType:
    """miopen_convolution_add_relu(Tensor self, Tensor weight, Tensor z, Scalar? alpha, Tensor? bias, int[] stride, int[] padding, int[] dilation, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_miopen_convolution_relu(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    groups: int,
) -> TensorType:
    """miopen_convolution_relu(Tensor self, Tensor weight, Tensor? bias, int[] stride, int[] padding, int[] dilation, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_miopen_convolution_transpose(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    padding: INT64,
    output_padding: INT64,
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
) -> TensorType:
    """miopen_convolution_transpose(Tensor self, Tensor weight, Tensor? bias, SymInt[] padding, SymInt[] output_padding, int[] stride, int[] dilation, int groups, bool benchmark, bool deterministic) -> Tensor"""

    raise NotImplementedError()


def aten_miopen_depthwise_convolution(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    padding: INT64,
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
) -> TensorType:
    """miopen_depthwise_convolution(Tensor self, Tensor weight, Tensor? bias, SymInt[] padding, int[] stride, int[] dilation, int groups, bool benchmark, bool deterministic) -> Tensor"""

    raise NotImplementedError()


def aten_miopen_rnn(
    input: TensorType,
    weight: Sequence[TensorType],
    weight_stride0: int,
    hx: TensorType,
    cx: Optional[TensorType],
    mode: int,
    hidden_size: int,
    num_layers: int,
    batch_first: bool,
    dropout: float,
    train: bool,
    bidirectional: bool,
    batch_sizes: Sequence[int],
    dropout_state: Optional[TensorType],
) -> tuple[TensorType, TensorType, TensorType, TensorType, TensorType]:
    """miopen_rnn(Tensor input, Tensor[] weight, int weight_stride0, Tensor hx, Tensor? cx, int mode, int hidden_size, int num_layers, bool batch_first, float dropout, bool train, bool bidirectional, int[] batch_sizes, Tensor? dropout_state) -> (Tensor, Tensor, Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_miopen_rnn_backward(
    input: TensorType,
    weight: Sequence[TensorType],
    weight_stride0: int,
    weight_buf: TensorType,
    hx: TensorType,
    cx: Optional[TensorType],
    output: TensorType,
    grad_output: Optional[TensorType],
    grad_hy: Optional[TensorType],
    grad_cy: Optional[TensorType],
    mode: int,
    hidden_size: int,
    num_layers: int,
    batch_first: bool,
    dropout: float,
    train: bool,
    bidirectional: bool,
    batch_sizes: Sequence[int],
    dropout_state: Optional[TensorType],
    reserve: TensorType,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType, TensorType]:
    """miopen_rnn_backward(Tensor input, Tensor[] weight, int weight_stride0, Tensor weight_buf, Tensor hx, Tensor? cx, Tensor output, Tensor? grad_output, Tensor? grad_hy, Tensor? grad_cy, int mode, int hidden_size, int num_layers, bool batch_first, float dropout, bool train, bool bidirectional, int[] batch_sizes, Tensor? dropout_state, Tensor reserve, bool[4] output_mask) -> (Tensor, Tensor, Tensor, Tensor[])"""

    raise NotImplementedError()


def aten_mkldnn_adaptive_avg_pool2d(
    self: TensorType, output_size: Sequence[int]
) -> TensorType:
    """mkldnn_adaptive_avg_pool2d(Tensor self, int[2] output_size) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_adaptive_avg_pool2d_backward(
    grad_output: TensorType, self: TensorType
) -> TensorType:
    """mkldnn_adaptive_avg_pool2d_backward(Tensor grad_output, Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_convolution(
    self: TensorType,
    weight: TensorType,
    bias: Optional[TensorType],
    padding: INT64,
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
) -> TensorType:
    """mkldnn_convolution(Tensor self, Tensor weight, Tensor? bias, SymInt[] padding, int[] stride, int[] dilation, int groups) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_linear_backward(
    self: TensorType, grad_output: TensorType, weight: TensorType, output_mask: Sequence[bool]
) -> tuple[TensorType, TensorType, TensorType]:
    """mkldnn_linear_backward(Tensor self, Tensor grad_output, Tensor weight, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_mkldnn_linear_backward_input(
    input_size: Sequence[int], grad_output: TensorType, weight: TensorType
) -> TensorType:
    """mkldnn_linear_backward_input(int[] input_size, Tensor grad_output, Tensor weight) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_linear_backward_weights(
    grad_output: TensorType, input: TensorType, weight: TensorType, bias_defined: bool
) -> tuple[TensorType, TensorType]:
    """mkldnn_linear_backward_weights(Tensor grad_output, Tensor input, Tensor weight, bool bias_defined) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_mkldnn_max_pool2d(
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0),
    dilation: Sequence[int] = (1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """mkldnn_max_pool2d(Tensor self, int[2] kernel_size, int[2] stride=[], int[2] padding=0, int[2] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_max_pool2d_backward(
    grad_output: TensorType,
    output: TensorType,
    input: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0),
    dilation: Sequence[int] = (1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """mkldnn_max_pool2d_backward(Tensor grad_output, Tensor output, Tensor input, int[2] kernel_size, int[2] stride=[], int[2] padding=0, int[2] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_max_pool3d(
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0, 0),
    dilation: Sequence[int] = (1, 1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """mkldnn_max_pool3d(Tensor self, int[3] kernel_size, int[3] stride=[], int[3] padding=0, int[3] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_mkldnn_max_pool3d_backward(
    grad_output: TensorType,
    output: TensorType,
    input: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0, 0),
    dilation: Sequence[int] = (1, 1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """mkldnn_max_pool3d_backward(Tensor grad_output, Tensor output, Tensor input, int[3] kernel_size, int[3] stride=[], int[3] padding=0, int[3] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::mm")
def aten_mm(
    self: TRealUnlessInt16OrInt8, mat2: TRealUnlessInt16OrInt8
) -> TRealUnlessInt16OrInt8:
    """mm(Tensor self, Tensor mat2) -> Tensor"""

    # TODO(justinchuby): Specify type conversion for uint8/int8/int16
    return op.MatMul(self, mat2)


def aten_mode(
    self: TensorType, dim: int = -1, keepdim: bool = False
) -> tuple[TensorType, TensorType]:
    """mode(Tensor self, int dim=-1, bool keepdim=False) -> (Tensor values, Tensor indices)"""

    raise NotImplementedError()


def aten_mps_convolution_backward(
    self: TensorType,
    grad_output: TensorType,
    weight: TensorType,
    padding: Sequence[int],
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """mps_convolution_backward(Tensor self, Tensor grad_output, Tensor weight, int[] padding, int[] stride, int[] dilation, int groups, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_mps_convolution_transpose_backward(
    self: TensorType,
    grad_output: TensorType,
    weight: TensorType,
    padding: Sequence[int],
    output_padding: Sequence[int],
    stride: Sequence[int],
    dilation: Sequence[int],
    groups: int,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType]:
    """mps_convolution_transpose_backward(Tensor self, Tensor grad_output, Tensor weight, int[] padding, int[] output_padding, int[] stride, int[] dilation, int groups, bool[2] output_mask) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_mps_max_pool2d_backward(
    grad_output: TensorType,
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0),
    dilation: Sequence[int] = (1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """mps_max_pool2d_backward(Tensor grad_output, Tensor self, int[2] kernel_size, int[2] stride=[], int[2] padding=0, int[2] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_msort(self: TensorType) -> TensorType:
    """msort(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::mul")
def aten_mul(self: TReal, other: TReal) -> TReal:
    """mul.Tensor(Tensor self, Tensor other) -> Tensor"""
    # FIXME(titaiwang): get rid of this when we have type_promotion
    other = op.CastLike(other, self)
    return op.Mul(self, other)


@torch_op("aten::mul", overload=True)
def aten_mul_bool(self: BOOL, other: BOOL) -> BOOL:
    """ONNX Mul doesn't support Boolean, so use And as an equivalent operator."""

    # TODO(justinchuby): Handle cases where type reconcilation is not enough,
    # since different ONNX operators are used based on different data types.

    return op.And(self, other)


def aten_multinomial(
    self: TensorType,
    num_samples: int,
    replacement: bool = False,
    generator: Optional[str] = None,
) -> TensorType:
    """multinomial(Tensor self, int num_samples, bool replacement=False, *, Generator? generator=None) -> Tensor"""

    raise NotImplementedError()


def aten_multiply(self: TensorType, other: TensorType) -> TensorType:
    """multiply.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_mv(self: TensorType, vec: TensorType) -> TensorType:
    """mv(Tensor self, Tensor vec) -> Tensor"""

    raise NotImplementedError()


def aten_mvlgamma(self: TensorType, p: int) -> TensorType:
    """mvlgamma(Tensor self, int p) -> Tensor"""

    raise NotImplementedError()


def aten_nan_to_num(
    self: TensorType,
    nan: Optional[float] = None,
    posinf: Optional[float] = None,
    neginf: Optional[float] = None,
) -> TensorType:
    """nan_to_num(Tensor self, float? nan=None, float? posinf=None, float? neginf=None) -> Tensor"""

    raise NotImplementedError()


def aten_nanmean(
    self: TensorType,
    dim: Optional[int] = None,
    keepdim: bool = False,
    dtype: Optional[int] = None,
) -> TensorType:
    """nanmean(Tensor self, int[1]? dim=None, bool keepdim=False, *, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_nanmedian(self: TensorType) -> TensorType:
    """nanmedian(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_nanquantile(
    self: TensorType,
    q: TensorType,
    dim: Optional[int] = None,
    keepdim: bool = False,
    interpolation: str = "linear",
) -> TensorType:
    """nanquantile(Tensor self, Tensor q, int? dim=None, bool keepdim=False, *, str interpolation='linear') -> Tensor"""

    raise NotImplementedError()


def aten_nansum(
    self: TensorType,
    dim: Optional[int] = None,
    keepdim: bool = False,
    dtype: Optional[int] = None,
) -> TensorType:
    """nansum(Tensor self, int[1]? dim=None, bool keepdim=False, *, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::narrow")
def aten_narrow(self: TTensor, dim: INT64, start: INT64, length: INT64) -> TTensor:
    """narrow(Tensor(a) self, int dim, SymInt start, SymInt length) -> Tensor(a)"""

    dim_rank = op.Size(op.Shape(dim))
    if dim_rank == 0:
        dim = op.Reshape(dim, op.Constant(value_ints=[-1]))

    start_rank = op.Size(op.Shape(start))
    if start_rank == 0:
        start = op.Reshape(start, op.Constant(value_ints=[-1]))

    length_rank = op.Size(op.Shape(length))
    if length_rank == 0:
        length = op.Reshape(length, op.Constant(value_ints=[-1]))

    end = op.Add(start, length)
    result = op.Slice(self, start, end, dim)
    return result


def aten_narrow_copy(self: TensorType, dim: int, start: INT64, length: INT64) -> TensorType:
    """narrow_copy(Tensor self, int dim, SymInt start, SymInt length) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::native_batch_norm", trace_only=True)
def aten_native_batch_norm(
    input: TFloat,
    weight: Optional[TFloat] = None,
    bias: Optional[TFloat] = None,
    running_mean: Optional[TFloat] = None,
    running_var: Optional[TFloat] = None,
    training: bool = False,
    momentum: float = 0.9,
    eps: float = 1e-05,
) -> Tuple[TFloat, TFloat, TFloat]:
    """native_batch_norm(Tensor input, Tensor? weight, Tensor? bias, Tensor? running_mean, Tensor? running_var, bool training, float momentum, float eps) -> (Tensor, Tensor, Tensor)"""

    if weight is None:  # Set to 1.0 as default
        weight = op.Expand(op.Constant(value_floats=[1.0]), op.Shape(input, start=1, end=2))

    if bias is None:  # Set to 0.0 as default
        bias = op.Expand(op.Constant(value_floats=[0.0]), op.Shape(input, start=1, end=2))

    axes = list(range(len(input.shape)))
    axes.pop(1)
    axes = op.Constant(value_ints=axes)
    if running_mean is None:  # Using input mean
        running_mean = op.Squeeze(op.ReduceMean(input, axes))

    if running_var is None:  # Using input var
        mean = op.ReduceMean(input, axes)
        input_sub_mean = op.Sub(input, mean)
        sqr_input_sub_mean = op.Mul(input_sub_mean, input_sub_mean)
        running_var = op.Squeeze(op.ReduceMean(sqr_input_sub_mean, axes))

    # Have to split to 2 private functions, because training_function return 3 outputs
    # While inference_function return 1 output
    if training is True:
        norm, mean, var = _aten_native_batch_norm_training_onnx(
            input, weight, bias, running_mean, running_var, axes, training, momentum, eps
        )
    else:
        norm, mean, var = _aten_native_batch_norm_inference_onnx(
            input, weight, bias, running_mean, running_var, training, momentum, eps
        )
    return norm, mean, var


@torch_op("aten::native_batch_norm", private=True)
def _aten_native_batch_norm_training_onnx(
    input: TFloat,
    weight: TFloat,
    bias: TFloat,
    running_mean: TFloat,
    running_var: TFloat,
    axes: INT64,
    training: bool,
    momentum: float,
    eps: float,
) -> Tuple[TFloat, TFloat, TFloat]:
    # Assert(training is True)
    norm, running_mean, running_var = op.BatchNormalization(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        epsilon=eps,
        momentum=momentum,
        training_mode=training,
    )
    # Compute var and rstd
    mean = op.ReduceMean(input, axes)
    input_sub_mean = op.Sub(input, mean)
    sqr = op.Mul(input_sub_mean, input_sub_mean)
    var = op.ReduceMean(sqr, axes, keepdims=0)
    rstd = op.Div(1.0, op.Sqrt(var + eps))
    # Get mean again with size = [1, C]
    mean = op.ReduceMean(input, axes, keepdims=0)
    return norm, mean, rstd


@torch_op("aten::native_batch_norm", private=True)
def _aten_native_batch_norm_inference_onnx(
    input: TFloat,
    weight: TFloat,
    bias: TFloat,
    running_mean: TFloat,
    running_var: TFloat,
    training: bool,
    momentum: float,
    eps: float,
) -> Tuple[TFloat, TFloat, TFloat]:
    # Assert(training is False)
    norm = op.BatchNormalization(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        epsilon=eps,
        momentum=momentum,
        training_mode=training,
    )
    # Cannot return 2 dup output, so have to do twice with different variable name
    empty_mean = op.Cast(op.Shape(input, 0, 0), to=FLOAT.dtype)
    empty_var = op.Cast(op.Shape(input, 0, 0), to=FLOAT.dtype)
    return norm, empty_mean, empty_var


def aten_native_batch_norm_backward(
    grad_out: TensorType,
    input: TensorType,
    weight: Optional[TensorType],
    running_mean: Optional[TensorType],
    running_var: Optional[TensorType],
    save_mean: Optional[TensorType],
    save_invstd: Optional[TensorType],
    train: bool,
    eps: float,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """native_batch_norm_backward(Tensor grad_out, Tensor input, Tensor? weight, Tensor? running_mean, Tensor? running_var, Tensor? save_mean, Tensor? save_invstd, bool train, float eps, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_native_channel_shuffle(self: TensorType, groups: int) -> TensorType:
    """native_channel_shuffle(Tensor self, int groups) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::native_dropout")
def aten_native_dropout(
    input: TFloatOrBFloat16, p: float, train: bool = True
) -> Tuple[TFloatOrBFloat16, BOOL]:
    """native_dropout(Tensor input, float p, bool? train) -> (Tensor, Tensor)"""

    result, mask = op.Dropout(input, p, train)
    return result, mask


def aten_native_dropout_backward(
    grad_output: TensorType, mask: TensorType, scale: float
) -> TensorType:
    """native_dropout_backward(Tensor grad_output, Tensor mask, float scale) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::native_group_norm", trace_only=True)
def aten_native_group_norm(
    input: TFloat,
    weight: Optional[TFloat] = None,
    bias: Optional[TFloat] = None,
    N: Optional[INT64] = None,  # pylint: disable=unused-argument
    C: Optional[INT64] = None,  # pylint: disable=unused-argument
    HxW: Optional[INT64] = None,  # pylint: disable=unused-argument
    group: int = 1,
    eps: float = 1e-05,
) -> Tuple[TFloat, TFloat, TFloat]:
    """native_group_norm(Tensor input, Tensor? weight, Tensor? bias, SymInt N, SymInt C, SymInt HxW, int group, float eps) -> (Tensor, Tensor, Tensor)"""

    # Actually we don't need N,C,HxW value because the input tensor has that information
    if weight is None:  # Set to 1.0 as default, the shape is Channel size
        weight = op.Expand(op.Constant(value_floats=[1.0]), op.Shape(input, start=1, end=2))

    if bias is None:  # Set to 0.0 as default, the shape is Channel size
        bias = op.Expand(op.Constant(value_floats=[0.0]), op.Shape(input, start=1, end=2))

    # Accoding to Torch, return rstd instead of var
    norm, mean, rstd = _aten_native_group_norm_onnx(input, weight, bias, group, eps)
    return norm, mean, rstd


@torch_op("aten::native_group_norm", private=True)
def _aten_native_group_norm_onnx(
    input: TFloat,
    weight: TFloat,
    bias: TFloat,
    group: INT64,
    eps: float,
) -> Tuple[TFloat, TFloat, TFloat]:
    # Because onnx.GroupNorm() need size=group for weight and bias
    # But the torch's aten function's input need size=channel, the size mismatched
    # So we have to use onnx.InstanceNorm() to simulate
    neg_1 = op.Constant(value_ints=[-1])
    # Create weight_instance_norm and bias_instance_norm, copied from Torch ONNX converter
    group_tensor = op.Reshape(group, neg_1)
    # 0 in the shape list keeps dimension value unchanged, for InstanceNorm need [0,group,-1]
    shape_input = op.Concat(op.Constant(value_ints=[0]), group_tensor, neg_1, axis=0)
    input_reshaped = op.Reshape(input, shape_input)
    weight_inst_norm = op.Expand(op.Constant(value_floats=[1.0]), group_tensor)
    bias_inst_norm = op.Expand(op.Constant(value_floats=[0.0]), group_tensor)
    norm = op.InstanceNormalization(
        input_reshaped, weight_inst_norm, bias_inst_norm, epsilon=eps
    )
    # Reshape back to input's shape
    norm = op.Reshape(norm, op.Shape(input))
    # Using the input weight and bias to do affine
    # But need to unsqueeze to the target shape for broading cast easy
    input_rank = op.Size(op.Shape(input))
    axes_unsqueeze = op.Range(1, input_rank - 1, 1)
    weight_full_shape = op.Unsqueeze(weight, axes_unsqueeze)
    bias_full_shape = op.Unsqueeze(bias, axes_unsqueeze)
    norm_mul_weight = op.Mul(norm, weight_full_shape)
    norm_result = op.Add(norm_mul_weight, bias_full_shape)
    # Compute mean and rstd, but using Torch algorithm
    # The returned shape for mean and vstd should be [N, group, -1]
    N = op.Shape(input, start=0, end=1)
    shape_N_group_neg1 = op.Concat(N, group_tensor, neg_1, axis=0)
    input_N_group_neg1 = op.Reshape(input, shape_N_group_neg1)
    # The output size is [N, group], so dims = [2]
    axes = op.Constant(value_ints=[2])
    # Get mean which size is [N, group, 1], for broadcasting
    mean = op.ReduceMean(input_N_group_neg1, axes)
    input_sub_mean = op.Sub(input_N_group_neg1, mean)
    sqr_input_sub_mean = op.Mul(input_sub_mean, input_sub_mean)
    # In Pytorch, vstd = 1/(sqrt(var + eps))
    var = op.ReduceMean(sqr_input_sub_mean, axes, keepdims=0)
    rstd = op.Div(1.0, op.Sqrt(var + eps))
    # Get the correct shape [N, group] for mean again
    mean = op.ReduceMean(input_N_group_neg1, axes, keepdims=0)
    return norm_result, mean, rstd


def aten_native_group_norm_backward(
    grad_out: TensorType,
    input: TensorType,
    mean: TensorType,
    rstd: TensorType,
    weight: Optional[TensorType],
    N: INT64,
    C: INT64,
    HxW: INT64,
    group: int,
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """native_group_norm_backward(Tensor grad_out, Tensor input, Tensor mean, Tensor rstd, Tensor? weight, SymInt N, SymInt C, SymInt HxW, int group, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


@torch_op("aten::native_layer_norm", trace_only=True)
def aten_native_layer_norm(
    input: TReal,
    normalized_shape: INT64,
    weight: Optional[TReal],
    bias: Optional[TReal],
    eps: float,
) -> Tuple[TReal, TReal, TReal]:
    """native_layer_norm(Tensor input, SymInt[] normalized_shape, Tensor? weight, Tensor? bias, float eps) -> (Tensor, Tensor, Tensor)"""

    # https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html#torch.nn.LayerNorm
    # The mean and standard-deviation are calculated over the last D dimensions,
    # where D is the dimension of normalized_shape. For example, if normalized_shape is
    # (3, 5) (a 2-dimensional shape), the mean and standard-deviation are computed
    # over the last 2 dimensions of the input (i.e. input.mean((-2, -1))).

    # Use Python to manipulate
    start_axis = -len(normalized_shape)

    if weight is None:
        one = op.Constant(value_floats=[1.0])
        weight = op.Expand(one, op.Shape(input, start=start_axis))
        weight = op.CastLike(weight, input)

    result, mean, rdenominator = op.LayerNormalization(
        input, weight, bias, axis=start_axis, epsilon=eps
    )

    return result, mean, rdenominator


def aten_native_layer_norm_backward(
    grad_out: TensorType,
    input: TensorType,
    normalized_shape: INT64,
    mean: TensorType,
    rstd: TensorType,
    weight: Optional[TensorType],
    bias: Optional[TensorType],
    output_mask: Sequence[bool],
) -> tuple[TensorType, TensorType, TensorType]:
    """native_layer_norm_backward(Tensor grad_out, Tensor input, SymInt[] normalized_shape, Tensor mean, Tensor rstd, Tensor? weight, Tensor? bias, bool[3] output_mask) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_native_norm(self: TensorType, p: float = 2.0) -> TensorType:
    """native_norm(Tensor self, Scalar p=2) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::ne")
def aten_ne(self: TReal, other: TReal) -> BOOL:
    """ne.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Not(op.Equal(self, other))


@torch_op("aten::neg")
def aten_neg(self: TReal) -> TReal:
    """neg(Tensor self) -> Tensor"""

    return op.Neg(self)


def aten_negative(self: TensorType) -> TensorType:
    """negative(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::new_empty", trace_only=True)
def aten_new_empty(self: TTensor, size: INT64, dtype: int = -1) -> TTensor:
    """new_empty(Tensor self, SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    # using zero to simulate empty array
    zero = op.Constant(value_float=0.0)
    result = op.Expand(zero, size)
    if dtype == -1:
        result = op.CastLike(result, self)
    else:
        result = op.Cast(result, to=dtype)
    return result


@torch_op("aten::new_empty_strided", trace_only=True)
def aten_new_empty_strided(
    self: TTensor,
    size: INT64,
    stride: INT64,  # pylint: disable=unused-argument
    dtype: int = -1,
) -> TTensor:
    """new_empty_strided(Tensor self, SymInt[] size, SymInt[] stride, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    # using zero to simulate empty array
    zero = op.ConstantOfShape(size)
    if dtype == -1:
        result = op.CastLike(zero, self)
    else:
        result = op.Cast(zero, to=dtype)
    return result


@torch_op("aten::new_full")
def aten_new_full(
    self, size: IntType, fill_value: TensorType, dtype: int = FLOAT.dtype
):  # pylint: disable=unused-argument
    # new_full(Tensor self, SymInt[] size, Scalar fill_value, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor

    size = op.Cast(size, to=INT64.dtype)
    fill_value = op.Cast(fill_value, to=dtype)

    return op.Expand(fill_value, size)


@torch_op("aten::new_ones")
def aten_new_ones(self: TReal, size: INT64) -> TReal:  # pylint: disable=unused-argument
    """new_ones(Tensor self, SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    one = op.Constant(value_float=1.0)
    return op.Expand(one, size)


@torch_op("aten::new_ones", overload=True)
def aten_new_ones_dtype(
    self: TReal, size: INT64, dtype: int  # pylint: disable=unused-argument
) -> TReal:
    one = op.Constant(value_float=1.0)
    one = op.Cast(one, to=dtype)
    return op.Expand(one, size)


@torch_op("aten::new_zeros")
def aten_new_zeros(self: TReal, size: INT64) -> TReal:  # pylint: disable=unused-argument
    """new_zeros(Tensor self, SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    zero = op.Constant(value_float=0.0)
    return op.Expand(zero, size)


@torch_op("aten::new_zeros", overload=True)
def aten_new_zeros_dtype(
    self: TReal, size: INT64, dtype: int  # pylint: disable=unused-argument
) -> TReal:
    zero = op.Constant(value_float=0.0)
    zero = op.Cast(zero, to=dtype)
    return op.Expand(zero, size)


def aten_nextafter(self: TensorType, other: TensorType) -> TensorType:
    """nextafter(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::nonzero")
def aten_nonzero(self: TTensor) -> INT64:
    """nonzero(Tensor self) -> Tensor"""

    return op.NonZero(self)


def aten_nonzero_numpy(self: TensorType) -> TensorType:
    """nonzero_numpy(Tensor self) -> Tensor[]"""

    raise NotImplementedError()


def aten_norm_except_dim(v: TensorType, pow: int = 2, dim: int = 0) -> TensorType:
    """norm_except_dim(Tensor v, int pow=2, int dim=0) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::normal")
def aten_normal(
    self: TTensor,
    mean: float = 0.0,
    std: float = 1.0,
) -> TFloat:  # type: ignore[type-var]
    # normal_functional(Tensor self, float mean=0, float std=1, *, Generator? generator=None) -> Tensor

    self_rank = op.Size(op.Shape(self))
    if self_rank == 0:
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    result = op.RandomNormalLike(self, mean=mean, scale=std)
    return result


def aten_not_equal(self: TensorType, other: TensorType) -> TensorType:
    """not_equal.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_nuclear_norm(self: TensorType, keepdim: bool = False) -> TensorType:
    """nuclear_norm(Tensor self, bool keepdim=False) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::ones")
def aten_ones(size: IntType, dtype: int = FLOAT.dtype):
    """ones(SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    size = op.Cast(size, to=INT64.dtype)
    one = op.Constant(value_float=1.0)
    one = op.Cast(one, to=dtype)
    return op.Expand(one, size)


@torch_op("aten::ones_like", trace_only=True)
def aten_ones_like(self: TTensor, dtype: int = -1) -> TTensor:
    """ones_like.

    Note: dtype is an onnx enum. Users should convert torch dtype to onnx dtype
    before calling this function.
    """
    # ones_like(Tensor self, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        one = op.CastLike(1, self)
    else:
        one = op.Cast(1, to=dtype)
    return _aten_ones_like_onnx(self, one)


@torch_op("aten::ones_like", private=True)
def _aten_ones_like_onnx(self: TTensor, one) -> TTensor:
    shape = op.Shape(self)
    return op.Expand(one, shape)


def aten_or(self: TensorType, other: TensorType) -> TensorType:
    """__or__.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


def aten_orgqr(self: TensorType, input2: TensorType) -> TensorType:
    """orgqr(Tensor self, Tensor input2) -> Tensor"""

    raise NotImplementedError()


def aten_ormqr(
    self: TensorType,
    input2: TensorType,
    input3: TensorType,
    left: bool = True,
    transpose: bool = False,
) -> TensorType:
    """ormqr(Tensor self, Tensor input2, Tensor input3, bool left=True, bool transpose=False) -> Tensor"""

    raise NotImplementedError()


def aten_outer(self: TensorType, vec2: TensorType) -> TensorType:
    """outer(Tensor self, Tensor vec2) -> Tensor"""

    raise NotImplementedError()


def aten_output_nr(self: TensorType) -> int:
    """output_nr(Tensor self) -> int"""

    raise NotImplementedError()


def aten_pairwise_distance(
    x1: TensorType, x2: TensorType, p: float = 2.0, eps: float = 1e-06, keepdim: bool = False
) -> TensorType:
    """pairwise_distance(Tensor x1, Tensor x2, float p=2, float eps=1e-06, bool keepdim=False) -> Tensor"""

    raise NotImplementedError()


def aten_pdist(self: TensorType, p: float = 2.0) -> TensorType:
    """pdist(Tensor self, float p=2) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::permute")
def aten_permute(self: TTensor, dims: Sequence[int]) -> TTensor:
    """permute(Tensor(a) self, int[] dims) -> Tensor(a)"""

    return op.Transpose(self, perm=dims)


def aten_permute_copy(self: TensorType, dims: Sequence[int]) -> TensorType:
    """permute_copy(Tensor self, int[] dims) -> Tensor"""

    raise NotImplementedError()


def aten_pin_memory(self: TensorType, device: Optional[str] = None) -> TensorType:
    """pin_memory(Tensor(a) self, Device? device=None) -> Tensor(a)"""

    raise NotImplementedError()


def aten_pinverse(self: TensorType, rcond: float = 1e-15) -> TensorType:
    """pinverse(Tensor self, float rcond=1e-15) -> Tensor"""

    raise NotImplementedError()


def aten_pixel_shuffle(self: TensorType, upscale_factor: int) -> TensorType:
    """pixel_shuffle(Tensor self, int upscale_factor) -> Tensor"""

    raise NotImplementedError()


def aten_pixel_unshuffle(self: TensorType, downscale_factor: int) -> TensorType:
    """pixel_unshuffle(Tensor self, int downscale_factor) -> Tensor"""

    raise NotImplementedError()


def aten_poisson(self: TensorType, generator: Optional[str] = None) -> TensorType:
    """poisson(Tensor self, Generator? generator=None) -> Tensor"""

    raise NotImplementedError()


def aten_poisson_nll_loss(
    input: TensorType,
    target: TensorType,
    log_input: bool,
    full: bool,
    eps: float,
    reduction: int,
) -> TensorType:
    """poisson_nll_loss(Tensor input, Tensor target, bool log_input, bool full, float eps, int reduction) -> Tensor"""

    raise NotImplementedError()


def aten_polar(abs: TensorType, angle: TensorType) -> TensorType:
    """polar(Tensor abs, Tensor angle) -> Tensor"""

    raise NotImplementedError()


def aten_polygamma(n: int, self: TensorType) -> TensorType:
    """polygamma(int n, Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_positive(self: TensorType) -> TensorType:
    """positive(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::pow")
def aten_pow(self: TReal, exponent: TTensor) -> TReal:
    """pow(Tensor self, Tensor exponent) -> Tensor"""

    return op.Pow(self, exponent)


def aten_prelu(self: TensorType, weight: TensorType) -> TensorType:
    """prelu(Tensor self, Tensor weight) -> Tensor"""

    raise NotImplementedError()


def aten_prelu_backward(
    grad_output: TensorType, self: TensorType, weight: TensorType
) -> tuple[TensorType, TensorType]:
    """prelu_backward(Tensor grad_output, Tensor self, Tensor weight) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_prod(self: TensorType, dtype: Optional[int] = None) -> TensorType:
    """prod(Tensor self, *, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_promote_types(type1: int, type2: int) -> int:
    """promote_types(ScalarType type1, ScalarType type2) -> ScalarType"""

    raise NotImplementedError()


def aten_put(
    self: TensorType, index: TensorType, source: TensorType, accumulate: bool = False
) -> TensorType:
    """put(Tensor self, Tensor index, Tensor source, bool accumulate=False) -> Tensor"""

    raise NotImplementedError()


def aten_q_per_channel_axis(self: TensorType) -> int:
    """q_per_channel_axis(Tensor self) -> int"""

    raise NotImplementedError()


def aten_q_per_channel_scales(self: TensorType) -> TensorType:
    """q_per_channel_scales(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_q_per_channel_zero_points(self: TensorType) -> TensorType:
    """q_per_channel_zero_points(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_q_scale(self: TensorType) -> float:
    """q_scale(Tensor self) -> float"""

    raise NotImplementedError()


def aten_q_zero_point(self: TensorType) -> int:
    """q_zero_point(Tensor self) -> int"""

    raise NotImplementedError()


def aten_qr(self: TensorType, some: bool = True) -> tuple[TensorType, TensorType]:
    """qr(Tensor self, bool some=True) -> (Tensor Q, Tensor R)"""

    raise NotImplementedError()


def aten_qscheme(self: TensorType) -> str:
    """qscheme(Tensor self) -> QScheme"""

    raise NotImplementedError()


def aten_quantile(
    self: TensorType,
    q: TensorType,
    dim: Optional[int] = None,
    keepdim: bool = False,
    interpolation: str = "linear",
) -> TensorType:
    """quantile(Tensor self, Tensor q, int? dim=None, bool keepdim=False, *, str interpolation='linear') -> Tensor"""

    raise NotImplementedError()


def aten_quantize_per_channel(
    self: TensorType, scales: TensorType, zero_points: TensorType, axis: int, dtype: int
) -> TensorType:
    """quantize_per_channel(Tensor self, Tensor scales, Tensor zero_points, int axis, ScalarType dtype) -> Tensor"""

    raise NotImplementedError()


def aten_quantize_per_tensor(
    self: TensorType, scale: float, zero_point: int, dtype: int
) -> TensorType:
    """quantize_per_tensor(Tensor self, float scale, int zero_point, ScalarType dtype) -> Tensor"""

    raise NotImplementedError()


def aten_quantize_per_tensor_dynamic(
    self: TensorType, dtype: int, reduce_range: bool
) -> TensorType:
    """quantize_per_tensor_dynamic(Tensor self, ScalarType dtype, bool reduce_range) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_batch_norm(
    input: TensorType,
    weight: Optional[TensorType],
    bias: Optional[TensorType],
    mean: TensorType,
    var: TensorType,
    eps: float,
    output_scale: float,
    output_zero_point: int,
) -> TensorType:
    """quantized_batch_norm(Tensor input, Tensor? weight, Tensor? bias, Tensor mean, Tensor var, float eps, float output_scale, int output_zero_point) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_gru_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: TensorType,
    b_hh: TensorType,
    packed_ih: TensorType,
    packed_hh: TensorType,
    col_offsets_ih: TensorType,
    col_offsets_hh: TensorType,
    scale_ih: float,
    scale_hh: float,
    zero_point_ih: float,
    zero_point_hh: float,
) -> TensorType:
    """quantized_gru_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor b_ih, Tensor b_hh, Tensor packed_ih, Tensor packed_hh, Tensor col_offsets_ih, Tensor col_offsets_hh, Scalar scale_ih, Scalar scale_hh, Scalar zero_point_ih, Scalar zero_point_hh) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_lstm_cell(
    input: TensorType,
    hx: Sequence[TensorType],
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: TensorType,
    b_hh: TensorType,
    packed_ih: TensorType,
    packed_hh: TensorType,
    col_offsets_ih: TensorType,
    col_offsets_hh: TensorType,
    scale_ih: float,
    scale_hh: float,
    zero_point_ih: float,
    zero_point_hh: float,
) -> tuple[TensorType, TensorType]:
    """quantized_lstm_cell(Tensor input, Tensor[] hx, Tensor w_ih, Tensor w_hh, Tensor b_ih, Tensor b_hh, Tensor packed_ih, Tensor packed_hh, Tensor col_offsets_ih, Tensor col_offsets_hh, Scalar scale_ih, Scalar scale_hh, Scalar zero_point_ih, Scalar zero_point_hh) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_quantized_max_pool1d(
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0,),
    dilation: Sequence[int] = (1,),
    ceil_mode: bool = False,
) -> TensorType:
    """quantized_max_pool1d(Tensor self, int[1] kernel_size, int[1] stride=[], int[1] padding=0, int[1] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_max_pool2d(
    self: TensorType,
    kernel_size: Sequence[int],
    stride: Optional[Sequence[int]] = None,
    padding: Sequence[int] = (0, 0),
    dilation: Sequence[int] = (1, 1),
    ceil_mode: bool = False,
) -> TensorType:
    """quantized_max_pool2d(Tensor self, int[2] kernel_size, int[2] stride=[], int[2] padding=0, int[2] dilation=1, bool ceil_mode=False) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_rnn_relu_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: TensorType,
    b_hh: TensorType,
    packed_ih: TensorType,
    packed_hh: TensorType,
    col_offsets_ih: TensorType,
    col_offsets_hh: TensorType,
    scale_ih: float,
    scale_hh: float,
    zero_point_ih: float,
    zero_point_hh: float,
) -> TensorType:
    """quantized_rnn_relu_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor b_ih, Tensor b_hh, Tensor packed_ih, Tensor packed_hh, Tensor col_offsets_ih, Tensor col_offsets_hh, Scalar scale_ih, Scalar scale_hh, Scalar zero_point_ih, Scalar zero_point_hh) -> Tensor"""

    raise NotImplementedError()


def aten_quantized_rnn_tanh_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: TensorType,
    b_hh: TensorType,
    packed_ih: TensorType,
    packed_hh: TensorType,
    col_offsets_ih: TensorType,
    col_offsets_hh: TensorType,
    scale_ih: float,
    scale_hh: float,
    zero_point_ih: float,
    zero_point_hh: float,
) -> TensorType:
    """quantized_rnn_tanh_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor b_ih, Tensor b_hh, Tensor packed_ih, Tensor packed_hh, Tensor col_offsets_ih, Tensor col_offsets_hh, Scalar scale_ih, Scalar scale_hh, Scalar zero_point_ih, Scalar zero_point_hh) -> Tensor"""

    raise NotImplementedError()


def aten_rad2deg(self: TensorType) -> TensorType:
    """rad2deg(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::rand")
def aten_rand(size: Sequence[int], dtype: int = 1) -> TReal:
    """rand(SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    return op.RandomUniform(shape=size, dtype=dtype)


def aten_rand_like(self: TensorType, memory_format: Optional[str] = None) -> TensorType:
    """rand_like(Tensor self, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    raise NotImplementedError()


def aten_randint(high: int, size: INT64) -> TensorType:
    """randint(int high, SymInt[] size, *, ScalarType? dtype=long, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_randint_like(
    self: TensorType, high: int, memory_format: Optional[str] = None
) -> TensorType:
    """randint_like(Tensor self, int high, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::randn")
def aten_randn(
    size: Sequence[int],
    dtype: int = 1,
    requires_grad: bool = False,  # pylint: disable=unused-argument
) -> TReal:
    """randn(SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    return op.RandomNormal(dtype=dtype, shape=size)


def aten_randn_like(self: TensorType, memory_format: Optional[str] = None) -> TensorType:
    """randn_like(Tensor self, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    raise NotImplementedError()


def aten_randperm(n: int) -> TensorType:
    """randperm(int n, *, ScalarType? dtype=long, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_range(start: float, end: float) -> TensorType:
    """range(Scalar start, Scalar end, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_ravel(self: TensorType) -> TensorType:
    """ravel(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_real(self: TensorType) -> TensorType:
    """real(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::reciprocal")
def aten_reciprocal(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """reciprocal(Tensor self) -> Tensor"""

    return op.Reciprocal(self)


def aten_record_stream(self: TensorType, s: str) -> Any:
    """record_stream(Tensor(a!) self, Stream s) -> ()"""

    raise NotImplementedError()


def aten_refine_names(self: TensorType, names: Sequence[str]) -> TensorType:
    """refine_names(Tensor(a) self, Dimname[] names) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::remainder")
def aten_remainder(self: TFloatOrBFloat16, other: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """remainder.Tensor(Tensor self, Tensor other) -> Tensor"""

    # a - a.div(b, rounding_mode="floor") * b
    rounded_quotient = op.Floor(op.Div(self, other))

    return op.Sub(self, op.Mul(rounded_quotient, other))


@torch_op("aten::remainder", overload=True)
def aten_remainder_int(self: TInt, other: TInt) -> TInt:
    """remainder.Tensor(Tensor self, Tensor other) -> Tensor"""

    return op.Mod(self, other)


def aten_rename(self: TensorType, names: Optional[str]) -> TensorType:
    """rename(Tensor(a) self, Dimname[]? names) -> Tensor(a)"""

    raise NotImplementedError()


def aten_renorm(self: TensorType, p: float, dim: int, maxnorm: float) -> TensorType:
    """renorm(Tensor self, Scalar p, int dim, Scalar maxnorm) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::repeat")
def aten_repeat(self: TTensor, repeats: TInt) -> TTensor:
    """repeat(Tensor self, SymInt[] repeats) -> Tensor"""

    if op.Size(repeats) == 0:
        result = self
    else:
        # TODO(justinchuby): Make ones_like a function when onnxscript supports it
        repeats = op.Cast(repeats, to=INT64.dtype)
        # shape = ones_like(repeats) := {
        one = op.Constant(value_int=1)
        repeats_shape = op.Shape(repeats)
        shape = op.Expand(one, repeats_shape)
        # }
        self_expanded = op.Expand(self, shape)
        result = op.Tile(self_expanded, repeats)
    return result


def aten_repeat_interleave(
    repeats: TensorType, output_size: Optional[int] = None
) -> TensorType:
    """repeat_interleave.Tensor(Tensor repeats, *, int? output_size=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::reshape")
def aten_reshape(self: TTensor, shape: IntType) -> TTensor:
    """reshape(Tensor(a) self, SymInt[] shape) -> Tensor(a)"""

    # Reshape only support INT64 as 'shape'
    shape = op.Cast(shape, to=INT64.dtype)
    return op.Reshape(self, shape)


def aten_reshape_as(self: TensorType, other: TensorType) -> TensorType:
    """reshape_as(Tensor(a) self, Tensor other) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::resolve_conj")
def aten_resolve_conj(self: TTensor) -> TTensor:
    """resolve_conj(Tensor(a) self) -> Tensor(a)"""

    return op.Identity(self)


@torch_op("aten::resolve_neg")
def aten_resolve_neg(self: TTensor) -> TTensor:
    """resolve_neg(Tensor(a) self) -> Tensor(a)"""

    return op.Identity(self)


def aten_result_type(tensor: TensorType, other: TensorType) -> int:
    """result_type.Tensor(Tensor tensor, Tensor other) -> ScalarType"""

    raise NotImplementedError()


def aten_retain_grad(self: TensorType) -> Any:
    """retain_grad(Tensor(a!) self) -> ()"""

    raise NotImplementedError()


def aten_retains_grad(self: TensorType) -> bool:
    """retains_grad(Tensor self) -> bool"""

    raise NotImplementedError()


def aten_rnn_relu_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: Optional[TensorType] = None,
    b_hh: Optional[TensorType] = None,
) -> TensorType:
    """rnn_relu_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor? b_ih=None, Tensor? b_hh=None) -> Tensor"""

    raise NotImplementedError()


def aten_rnn_tanh_cell(
    input: TensorType,
    hx: TensorType,
    w_ih: TensorType,
    w_hh: TensorType,
    b_ih: Optional[TensorType] = None,
    b_hh: Optional[TensorType] = None,
) -> TensorType:
    """rnn_tanh_cell(Tensor input, Tensor hx, Tensor w_ih, Tensor w_hh, Tensor? b_ih=None, Tensor? b_hh=None) -> Tensor"""

    raise NotImplementedError()


def aten_roll(
    self: TensorType, shifts: Sequence[int], dims: Optional[Sequence[int]] = None
) -> TensorType:
    """roll(Tensor self, int[1] shifts, int[1] dims=[]) -> Tensor"""

    raise NotImplementedError()


def aten_rot90(self: TensorType, k: int = 1, dims: Sequence[int] = (0, 1)) -> TensorType:
    """rot90(Tensor self, int k=1, int[] dims=[0,1]) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::round")
def aten_round(self: TFloat) -> TFloat:
    """round(Tensor self) -> Tensor"""

    return op.Round(self)


def aten_row_indices(self: TensorType) -> TensorType:
    """row_indices(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_row_indices_copy(self: TensorType) -> TensorType:
    """row_indices_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_row_stack(tensors: Sequence[TensorType]) -> TensorType:
    """row_stack(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


def aten_rrelu(
    self: TensorType,
    lower: float = 0.125,
    upper: float = 0.3333333333333333,
    training: bool = False,
    generator: Optional[str] = None,
) -> TensorType:
    """rrelu(Tensor self, Scalar lower=0.125, Scalar upper=0.3333333333333333, bool training=False, Generator? generator=None) -> Tensor"""

    raise NotImplementedError()


def aten_rshift(self: TensorType, other: TensorType) -> TensorType:
    """__rshift__.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::rsqrt")
def aten_rsqrt(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """rsqrt(Tensor self) -> Tensor"""

    return op.Reciprocal(op.Sqrt(self))


@torch_op("aten::rsub")
def aten_rsub(self: TReal, other: TReal, alpha: float = 1.0) -> TReal:
    """rsub.Tensor(Tensor self, Tensor other, *, Scalar alpha=1) -> Tensor"""
    # FIXME(titaiwang): get rid of this when we have type_promotion
    other = op.CastLike(other, self)
    alpha = op.CastLike(alpha, self)
    return op.Sub(other, op.Mul(self, alpha))


@torch_op("aten::scalar_tensor")
def aten_scalar_tensor(s: float, dtype: int = FLOAT.dtype) -> TTensor:  # type: ignore[type-var]
    """scalar_tensor(Scalar s, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    return op.Cast(s, to=dtype)


@torch_op("aten::scatter_add")
def aten_scatter_add(
    self: TReal,
    index: TInt,
    src: TReal,
    dim: int,
) -> TReal:
    """scatter_add(Tensor self, int dim, Tensor index, Tensor src) -> Tensor"""

    # if rank(self) == 0 will lead ORT failed, skipped
    return op.ScatterElements(self, index, src, axis=dim, reduction="add")


@torch_op("aten::scatter_reduce", trace_only=True)
def aten_scatter_reduce(
    self: TReal,
    dim: int,  # we have to use int here because ScatterElements() will use this attribute
    index: TInt,
    src: TReal,
    reduce: str,
    include_self: bool = True,  # pylint: disable=unused-argument
):
    """scatter_reduce.two(Tensor self, int dim, Tensor index, Tensor src, str reduce, *, bool include_self=True) -> Tensor"""

    reduce_mode = {  # convert torch string name to onnx string name
        "mean": "none",  # 'mean' doesn't support in ONNX 1.14 definition
        "sum": "add",
        "prod": "mul",
        "amin": "min",
        "amax": "max",
    }
    onnx_reduce = reduce_mode[reduce]
    return _aten_scatter_reduce_onnx(self, index, src, dim, onnx_reduce)


@torch_op("aten::scatter_reduce", overload=True)
def _aten_scatter_reduce_onnx(
    self: TReal,
    index: TInt,
    src: TReal,
    dim: int,
    onnx_reduce: str,
):
    self_rank = op.Size(op.Shape(self))
    if self_rank == 0:  # assert (index_rank == 0 and rank_src == 0)
        neg_1 = op.Constant(value_ints=[-1])
        self = op.Reshape(self, neg_1)
        index = op.Reshape(index, neg_1)
        src = op.Reshape(src, neg_1)
    result = op.ScatterElements(self, index, src, axis=dim, reduction=onnx_reduce)
    if self_rank == 0:
        result = op.Squeeze(result)
    return result


def aten_searchsorted(
    sorted_sequence: TensorType,
    self: TensorType,
    out_int32: bool = False,
    right: bool = False,
    side: Optional[str] = None,
    sorter: Optional[TensorType] = None,
) -> TensorType:
    """searchsorted.Tensor(Tensor sorted_sequence, Tensor self, *, bool out_int32=False, bool right=False, str? side=None, Tensor? sorter=None) -> Tensor"""

    raise NotImplementedError()


def aten_segment_reduce(
    data: TensorType,
    reduce: str,
    lengths: Optional[TensorType] = None,
    indices: Optional[TensorType] = None,
    offsets: Optional[TensorType] = None,
    axis: int = 0,
    unsafe: bool = False,
    initial: Optional[float] = None,
) -> TensorType:
    """segment_reduce(Tensor data, str reduce, *, Tensor? lengths=None, Tensor? indices=None, Tensor? offsets=None, int axis=0, bool unsafe=False, Scalar? initial=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::select")
def aten_select(self: TTensor, dim: int, index: int) -> TTensor:
    """select(Tensor self, int dim, int index) -> Tensor"""

    return op.Gather(self, index, axis=dim)


def aten_select_backward(
    grad_output: TensorType, input_sizes: INT64, dim: int, index: int
) -> TensorType:
    """select_backward(Tensor grad_output, SymInt[] input_sizes, int dim, int index) -> Tensor"""

    raise NotImplementedError()


def aten_select_scatter(self: TensorType, src: TensorType, dim: int, index: int) -> TensorType:
    """select_scatter(Tensor self, Tensor src, int dim, int index) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::selu")
def aten_selu(self: TFloat) -> TFloat:
    """selu(Tensor self) -> Tensor"""

    return op.Selu(self)


def aten_set_data(self: TensorType, new_data: TensorType) -> Any:
    """set_data(Tensor(a!) self, Tensor new_data) -> ()"""

    raise NotImplementedError()


def aten_sgn(self: TensorType) -> TensorType:
    """sgn(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::sigmoid")
def aten_sigmoid(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """sigmoid(Tensor self) -> Tensor"""

    return op.Sigmoid(self)


@torch_op("aten::sign")
def aten_sign(self: TReal) -> TReal:
    """sign(Tensor self) -> Tensor"""

    return op.Sign(self)


def aten_signbit(self: TensorType) -> TensorType:
    """signbit(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::sin")
def aten_sin(self: TFloat) -> TFloat:
    """sin(Tensor self) -> Tensor"""

    return op.Sin(self)


@torch_op("aten::sinh")
def aten_sinh(self: TFloat) -> TFloat:
    """sinh(Tensor self) -> Tensor"""

    return op.Sinh(self)


@torch_op("aten::slice", trace_only=True)
def aten_slice(
    self: TTensor,
    dim: int = 0,
    start: Optional[INT64] = None,
    end: Optional[INT64] = None,
    step: Optional[INT64] = None,
) -> TTensor:
    """slice.Tensor(Tensor(a) self, int dim=0, SymInt? start=None, SymInt? end=None, SymInt step=1) -> Tensor(a)"""

    # TODO: using OptionalHasElement() to check start/end value
    if start is not None:
        start = op.Cast(start, to=INT64.dtype)
        start = op.Reshape(start, op.Constant(value_ints=[-1]))
    else:
        start = op.Constant(value_ints=[0])

    if end is not None:
        end = op.Cast(end, to=INT64.dtype)
        end = op.Reshape(end, op.Constant(value_ints=[-1]))
    else:
        end = op.Constant(value_ints=[_INT64_MAX])

    dim = op.Cast(dim, to=INT64.dtype)
    dim = op.Reshape(dim, op.Constant(value_ints=[-1]))

    if step is not None:
        step = op.Cast(step, to=INT64.dtype)
        step = op.Reshape(step, op.Constant(value_ints=[-1]))
    else:
        step = op.Constant(value_ints=[1])

    return op.Slice(self, start, end, dim, step)


def aten_slice_backward(
    grad_output: TensorType,
    input_sizes: INT64,
    dim: int,
    start: INT64,
    end: INT64,
    step: INT64,
) -> TensorType:
    """slice_backward(Tensor grad_output, SymInt[] input_sizes, int dim, SymInt start, SymInt end, SymInt step) -> Tensor"""

    raise NotImplementedError()


def aten_slice_copy(
    self: TensorType,
    dim: int = 0,
    start: Optional[INT64] = None,
    end: Optional[INT64] = None,
    step: INT64 = 1,
) -> TensorType:
    """slice_copy.Tensor(Tensor self, int dim=0, SymInt? start=None, SymInt? end=None, SymInt step=1) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::slice_scatter", trace_only=True)
def aten_slice_scatter(
    self: TTensor,
    src: TTensor,
    dim: int = 0,
    start: Optional[INT64] = None,
    end: Optional[INT64] = None,
    step: INT64 = 1,
) -> TTensor:
    """slice_scatter(Tensor self, Tensor src, int dim=0, SymInt? start=None, SymInt? end=None, SymInt step=1) -> Tensor"""

    # Although 'start' and 'end' can be None in signature, but actually 'start' must be specified
    # Assert(start is not None)
    # And, 'end' also must be specified, and end-start must be equal to the size of 'src'
    # Assert(end-start == shape(src) > 0)
    # Try torch sample to get more information:
    # https://pytorch.org/docs/master/generated/torch.slice_scatter.html?highlight=slice_scatter#torch.slice_scatter
    # e.g. if dim=2, shape=5, permute will be [0,1]+[4]+[2,3]=[0,1,4,2,3]
    last = len(src.shape)
    perm = list(range(0, last))
    perm.insert(dim, perm.pop(-1))
    return _aten_slice_scatter_onnx(self, src, start, end, step, dim, perm)


@torch_op("aten::slice_scatter", private=True)
def _aten_slice_scatter_onnx(
    self: TTensor,
    src: TTensor,
    start: INT64,
    end: INT64,
    step: INT64,
    dim: int,
    perm: Sequence[int],
) -> TTensor:
    neg_1 = op.Constant(value_ints=[-1])
    # Get shapes expcept specifide dim
    # e.g. if dim=2, shape=(2,3,5,7), shape_expand will be (2,3,7,1)
    src_shape = op.Shape(src)
    last_dim = op.Reshape(op.Size(src_shape), neg_1)
    dim_tensor = op.Reshape(op.Constant(value_int=dim), neg_1)
    shape_before_dim = op.Slice(src_shape, op.Constant(value_ints=[0]), dim_tensor)
    shape_after_dim = op.Slice(src_shape, op.Add(dim_tensor, 1), last_dim)
    shape_expand = op.Concat(
        shape_before_dim, shape_after_dim, op.Constant(value_ints=[1]), axis=0
    )
    # Generate index but not finalized, need to do transpose later
    # e.g. [[0,1,2],[0,1,2],[0,1,2]...,[0,1,2]], total count = 2x3x7
    index_base = op.Range(start, end, step)  # e.g. [0,1,2]
    index_expand = op.Expand(index_base, shape_expand)
    indices = op.Transpose(index_expand, perm=perm)

    return op.ScatterElements(self, indices, src, axis=dim)


def aten_slogdet(self: TensorType) -> tuple[TensorType, TensorType]:
    """slogdet(Tensor self) -> (Tensor sign, Tensor logabsdet)"""

    raise NotImplementedError()


def aten_smm(self: TensorType, mat2: TensorType) -> TensorType:
    """smm(Tensor self, Tensor mat2) -> Tensor"""

    raise NotImplementedError()


def aten_sort(
    self: TensorType, dim: int = -1, descending: bool = False
) -> tuple[TensorType, TensorType]:
    """sort(Tensor self, int dim=-1, bool descending=False) -> (Tensor values, Tensor indices)"""

    raise NotImplementedError()


def aten_sparse_dim(self: TensorType) -> int:
    """sparse_dim(Tensor self) -> int"""

    raise NotImplementedError()


def aten_sparse_mask(self: TensorType, mask: TensorType) -> TensorType:
    """sparse_mask(Tensor self, Tensor mask) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::split")
def aten_split(self: TTensor, split_size: INT64, dim: int = 0) -> TTensor:
    """split.Tensor(Tensor(a -> *) self, SymInt split_size, int dim=0) -> Tensor(a)[]"""

    return op.SplitToSequence(self, split_size, axis=dim)


def aten_split_copy(self: TensorType, split_size: INT64, dim: int = 0) -> TensorType:
    """split_copy.Tensor(Tensor self, SymInt split_size, int dim=0) -> Tensor[]"""

    raise NotImplementedError()


@torch_op("aten::split_with_sizes")
def aten_split_with_sizes(self: TTensor, split_sizes: INT64, dim: int = 0) -> TTensor:
    """split_with_sizes(Tensor(a -> *) self, SymInt[] split_sizes, int dim=0) -> Tensor(a)[]"""

    return op.SplitToSequence(self, split_sizes, axis=dim)


def aten_split_with_sizes_copy(
    self: TensorType, split_sizes: INT64, dim: int = 0
) -> TensorType:
    """split_with_sizes_copy(Tensor self, SymInt[] split_sizes, int dim=0) -> Tensor[]"""

    raise NotImplementedError()


@torch_op("aten::sqrt")
def aten_sqrt(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """sqrt(Tensor self) -> Tensor"""

    return op.Sqrt(self)


def aten_square(self: TensorType) -> TensorType:
    """square(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::squeeze")
def aten_squeeze(self: TTensor) -> TTensor:
    """squeeze(Tensor(a) self) -> Tensor(a)"""

    return op.Squeeze(self)


@torch_op("aten::squeeze", overload=True)
def aten_squeeze_dim(self: TTensor, dim: int) -> TTensor:
    result = self
    if op.Size(op.Shape(self)) > 0:  # type: ignore[operator]
        # check if specified dimension is 1, do squeeze
        shape = op.Shape(self)
        dim_size = op.Gather(shape, dim, axis=0)
        if dim_size == 1:
            dims = op.Reshape(dim, op.Constant(value_ints=[-1]))
            result = op.Squeeze(self, dims)

    return result


def aten_squeeze_copy(self: TensorType) -> TensorType:
    """squeeze_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_sspaddmm(
    self: TensorType, mat1: TensorType, mat2: TensorType, beta: float = 1.0, alpha: float = 1.0
) -> TensorType:
    """sspaddmm(Tensor self, Tensor mat1, Tensor mat2, *, Scalar beta=1, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::stack")
def aten_stack(tensors: Sequence[TTensorOrString], dim: int = 0) -> TTensorOrString:
    """stack(Tensor[] tensors, int dim=0) -> Tensor"""
    return op.ConcatFromSequence(tensors, axis=dim, new_axis=1)


def aten_std(self: TensorType, unbiased: bool = True) -> TensorType:
    """std(Tensor self, bool unbiased=True) -> Tensor"""

    raise NotImplementedError()


def aten_std_mean(self: TensorType, unbiased: bool = True) -> tuple[TensorType, TensorType]:
    """std_mean(Tensor self, bool unbiased=True) -> (Tensor, Tensor)"""

    raise NotImplementedError()


def aten_stft(
    self: TensorType,
    n_fft: int,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    window: Optional[TensorType] = None,
    normalized: bool = False,
    onesided: Optional[bool] = None,
    return_complex: Optional[bool] = None,
) -> TensorType:
    """stft(Tensor self, int n_fft, int? hop_length=None, int? win_length=None, Tensor? window=None, bool normalized=False, bool? onesided=None, bool? return_complex=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::sub")
def aten_sub(self: TReal, other: TReal, alpha: float = 1.0) -> TReal:
    """sub.Tensor(Tensor self, Tensor other, *, Scalar alpha=1) -> Tensor"""
    alpha = op.CastLike(alpha, other)
    other = op.Mul(other, alpha)

    return op.Sub(self, other)


def aten_subtract(self: TensorType, other: TensorType, alpha: float = 1.0) -> TensorType:
    """subtract.Tensor(Tensor self, Tensor other, *, Scalar alpha=1) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::sum", trace_only=True)
def aten_sum_dim_IntList(
    self: TReal, dim: Optional[INT64] = None, keepdim: bool = False, dtype: int = -1
) -> TReal:
    """sum(Tensor self, SymInt dim, bool keepdim, *, ScalarType? dtype=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    # TODO: Combine the overloads when OptionalHasElement() works
    if dim is None:
        result = _aten_sum_dim_none(self, keepdim=keepdim)
    else:
        result = _aten_sum_dim_onnx(self, dim, keepdim=keepdim)

    if dtype != -1:
        result = op.Cast(result, to=dtype)

    return result


@torch_op("aten::sum", private=True)
def _aten_sum_dim_onnx(self: TReal, dim: INT64, keepdim: bool = False) -> TReal:
    self_is_scalar = op.Size(op.Shape(self)) == 0
    if self_is_scalar:
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    if op.Size(op.Shape(dim)) == 0:
        dim = op.Reshape(dim, op.Constant(value_ints=[-1]))
        dim = op.Cast(dim, to=INT64.dtype)
    result = op.ReduceSum(self, dim, keepdims=keepdim)

    if self_is_scalar:
        result = op.Squeeze(result)
    return result


@torch_op("aten::sum", private=True)
def _aten_sum_dim_none(self: TReal, keepdim: bool = False) -> TReal:
    self_is_scalar = op.Size(op.Shape(self)) == 0
    if self_is_scalar:
        self = op.Reshape(self, op.Constant(value_ints=[-1]))

    result = op.ReduceSum(self, keepdims=keepdim)

    if self_is_scalar:
        result = op.Squeeze(result)
    return result


def aten_sum_to_size(self: TensorType, size: Sequence[int]) -> TensorType:
    """sum_to_size(Tensor self, int[] size) -> Tensor"""

    raise NotImplementedError()


def aten_svd(
    self: TensorType, some: bool = True, compute_uv: bool = True
) -> tuple[TensorType, TensorType, TensorType]:
    """svd(Tensor self, bool some=True, bool compute_uv=True) -> (Tensor U, Tensor S, Tensor V)"""

    raise NotImplementedError()


def aten_swapaxes(self: TensorType, axis0: int, axis1: int) -> TensorType:
    """swapaxes(Tensor(a) self, int axis0, int axis1) -> Tensor(a)"""

    raise NotImplementedError()


def aten_swapdims(self: TensorType, dim0: int, dim1: int) -> TensorType:
    """swapdims(Tensor(a) self, int dim0, int dim1) -> Tensor(a)"""

    raise NotImplementedError()


@torch_op("aten::sym_size")
def aten_sym_size(self: TReal, dim: int = 0) -> TReal:
    """sym_size(Tensor self, int dim) -> Tensor"""
    # NOTE: onnxscript doesn't support attribute process,
    # so op.Shape(self, start=dim, end=dim + 1) is not supported.

    # TODO(titaiwang): ORT==1.15 fixes SegFault
    # https://github.com/microsoft/onnxscript/pull/484#discussion_r1136105039
    # Change the op to:
    # shape = op.Shape(self)
    # idx= op.Reshape(dim, [1])
    # return op.Gather(shape, idx)

    shape = op.Shape(self)
    # Reshape helps dim from int to tensor, and
    # input arguments support attribute processing.
    start = op.Reshape(dim, [1])
    end = op.Reshape(dim + 1, [1])
    return op.Slice(shape, start, end)


def aten_symeig(
    self: TensorType, eigenvectors: bool = False, upper: bool = True
) -> tuple[TensorType, TensorType]:
    """symeig(Tensor self, bool eigenvectors=False, bool upper=True) -> (Tensor eigenvalues, Tensor eigenvectors)"""

    raise NotImplementedError()


@torch_op("aten::t")
def aten_t(self: TTensor) -> TTensor:
    """t(Tensor(a) self) -> Tensor(a)"""

    rank = op.Size(op.Shape(self))
    if rank == 2:
        result = op.Transpose(self, perm=[1, 0])
    else:
        # rank < 2
        result = self
    return result


def aten_t_copy(self: TensorType) -> TensorType:
    """t_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_take(self: TensorType, index: TensorType) -> TensorType:
    """take(Tensor self, Tensor index) -> Tensor"""

    raise NotImplementedError()


def aten_take_along_dim(
    self: TensorType, indices: TensorType, dim: Optional[int] = None
) -> TensorType:
    """take_along_dim(Tensor self, Tensor indices, int? dim=None) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::tan")
def aten_tan(self: TFloat) -> TFloat:
    """tan(Tensor self) -> Tensor"""

    return op.Tan(self)


@torch_op("aten::tanh")
def aten_tanh(self: TFloat) -> TFloat:
    """tanh(Tensor self) -> Tensor"""

    return op.Tanh(self)


def aten_tensordot(
    self: TensorType, other: TensorType, dims_self: Sequence[int], dims_other: Sequence[int]
) -> TensorType:
    """tensordot(Tensor self, Tensor other, int[] dims_self, int[] dims_other) -> Tensor"""

    raise NotImplementedError()


def aten_threshold(self: TensorType, threshold: float, value: float) -> TensorType:
    """threshold(Tensor self, Scalar threshold, Scalar value) -> Tensor"""

    raise NotImplementedError()


def aten_threshold_backward(
    grad_output: TensorType, self: TensorType, threshold: float
) -> TensorType:
    """threshold_backward(Tensor grad_output, Tensor self, Scalar threshold) -> Tensor"""

    raise NotImplementedError()


def aten_tile(self: TensorType, dims: Sequence[int]) -> TensorType:
    """tile(Tensor self, int[] dims) -> Tensor"""

    raise NotImplementedError()


def aten_to_dense(self: TensorType, dtype: Optional[int] = None) -> TensorType:
    """to_dense(Tensor self, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_to_dense_backward(grad: TensorType, input: TensorType) -> TensorType:
    """to_dense_backward(Tensor grad, Tensor input) -> Tensor"""

    raise NotImplementedError()


def aten_to_mkldnn(self: TensorType, dtype: Optional[int] = None) -> TensorType:
    """to_mkldnn(Tensor self, ScalarType? dtype=None) -> Tensor"""

    raise NotImplementedError()


def aten_to_mkldnn_backward(grad: TensorType, input: TensorType) -> TensorType:
    """to_mkldnn_backward(Tensor grad, Tensor input) -> Tensor"""

    raise NotImplementedError()


def aten_to_padded_tensor(
    self: TensorType, padding: float, output_size: Optional[INT64] = None
) -> TensorType:
    """to_padded_tensor(Tensor self, float padding, SymInt[]? output_size=None) -> Tensor"""

    raise NotImplementedError()


def aten_to_sparse(self: TensorType) -> TensorType:
    """to_sparse(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_to_sparse_bsc(self: TensorType, blocksize: Sequence[int]) -> TensorType:
    """to_sparse_bsc(Tensor self, int[2] blocksize) -> Tensor"""

    raise NotImplementedError()


def aten_to_sparse_bsr(self: TensorType, blocksize: Sequence[int]) -> TensorType:
    """to_sparse_bsr(Tensor self, int[2] blocksize) -> Tensor"""

    raise NotImplementedError()


def aten_to_sparse_csc(self: TensorType) -> TensorType:
    """to_sparse_csc(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_to_sparse_csr(self: TensorType) -> TensorType:
    """to_sparse_csr(Tensor self) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::topk")
def aten_topk(
    self: TReal, k: INT64, dim: int = -1, largest: bool = True, sorted: bool = True
) -> Tuple[TReal, INT64]:
    """topk(Tensor self, int k, int dim=-1, bool largest=True, bool sorted=True) -> (Tensor values, Tensor indices)"""

    self_is_scalar = op.Size(op.Shape(self)) == 0
    if self_is_scalar:
        self = op.Unsqueeze(self, op.Constant(value_ints=[0]))
    k = op.Reshape(op.Cast(k, to=INT64.dtype), op.Constant(value_ints=[1]))
    values, indices = op.TopK(self, k, axis=dim, largest=largest, sorted=sorted)
    if self_is_scalar:
        values = op.Squeeze(values, op.Constant(value_ints=[0]))
        indices = op.Squeeze(indices, op.Constant(value_ints=[0]))
    return values, indices


def aten_trace(self: TensorType) -> TensorType:
    """trace(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_trace_backward(grad: TensorType, sizes: INT64) -> TensorType:
    """trace_backward(Tensor grad, SymInt[] sizes) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::transpose", trace_only=True)
def aten_transpose(self, dim0: int, dim1: int):
    """transpose.int(Tensor(a) self, int dim0, int dim1) -> Tensor(a)"""

    # Use trace only to construct the prem attribute in Transpose
    self_rank = len(self.shape)  # type: ignore[attr-defined]

    if self_rank == 0:
        result = self
    else:
        # Python code, change when onnxscript supports this
        dims = list(range(self_rank))
        dims[dim0], dims[dim1] = dims[dim1], dims[dim0]
        # Python code ends

        result = op.Transpose(self, perm=dims)

    return result


def aten_triangular_solve(
    self: TensorType,
    A: TensorType,
    upper: bool = True,
    transpose: bool = False,
    unitriangular: bool = False,
) -> tuple[TensorType, TensorType]:
    """triangular_solve(Tensor self, Tensor A, bool upper=True, bool transpose=False, bool unitriangular=False) -> (Tensor solution, Tensor cloned_coefficient)"""

    raise NotImplementedError()


@torch_op("aten::tril")
def aten_tril(self: TTensor, diagonal: int = 0) -> TTensor:
    """tril(Tensor self, int diagonal=0) -> Tensor"""

    return op.Trilu(self, diagonal, upper=0)


def aten_tril_indices(row: int, col: int, offset: int = 0) -> TensorType:
    """tril_indices(int row, int col, int offset=0, *, ScalarType? dtype=long, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_triplet_margin_loss(
    anchor: TensorType,
    positive: TensorType,
    negative: TensorType,
    margin: float = 1.0,
    p: float = 2.0,
    eps: float = 1e-06,
    swap: bool = False,
    reduction: int = 1,
) -> TensorType:
    """triplet_margin_loss(Tensor anchor, Tensor positive, Tensor negative, float margin=1.0, float p=2, float eps=1e-06, bool swap=False, int reduction=Mean) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::triu")
def aten_triu(self: TensorType, diagonal: int = 0) -> TensorType:
    """triu(Tensor self, int diagonal=0) -> Tensor"""

    return op.Trilu(self, diagonal, upper=1)


def aten_triu_indices(row: int, col: int, offset: int = 0) -> TensorType:
    """triu_indices(int row, int col, int offset=0, *, ScalarType? dtype=long, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    raise NotImplementedError()


def aten_true_divide(self: TensorType, other: TensorType) -> TensorType:
    """true_divide.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::trunc")
def aten_trunc(self: TFloatOrBFloat16) -> TFloatOrBFloat16:
    """trunc(Tensor self) -> Tensor"""

    # Reference https://github.com/onnx/onnx/issues/4588#issuecomment-1463970126
    integer_parts = op.Floor(op.Abs(self))
    is_negative = op.Less(self, 0.0)
    return op.Where(is_negative, op.Neg(integer_parts), integer_parts)


def aten_type_as(self: TensorType, other: TensorType) -> TensorType:
    """type_as(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::unflatten")
def aten_unflatten(self: TReal, dim: INT64, sizes: INT64):
    """unflatten(Tensor(a) self, int dim, SymInt[] sizes) -> Tensor(a)"""

    self_size = op.Shape(self)

    # PyTorch accepts negative dim as reversed counting
    self_rank = op.Size(self_size)
    dim = self_rank + dim
    dim = dim % self_rank

    head_start_idx = op.Constant(value_ints=[0])
    head_end_idx = op.Reshape(dim, op.Constant(value_ints=[1]))
    head_part_rank = op.Slice(self_size, head_start_idx, head_end_idx)

    tail_start_idx = op.Reshape(dim + 1, op.Constant(value_ints=[1]))
    tail_end_idx = op.Constant(value_ints=[_INT64_MAX])
    tail_part_rank = op.Slice(self_size, tail_start_idx, tail_end_idx)

    final_shape = op.Concat(head_part_rank, sizes, tail_part_rank, axis=0)

    return op.Reshape(self, final_shape)


def aten_unfold(self: TensorType, dimension: int, size: int, step: int) -> TensorType:
    """unfold(Tensor(a) self, int dimension, int size, int step) -> Tensor(a)"""

    raise NotImplementedError()


def aten_unfold_backward(
    grad_in: TensorType, input_sizes: INT64, dim: int, size: int, step: int
) -> TensorType:
    """unfold_backward(Tensor grad_in, SymInt[] input_sizes, int dim, int size, int step) -> Tensor"""

    raise NotImplementedError()


def aten_unfold_copy(self: TensorType, dimension: int, size: int, step: int) -> TensorType:
    """unfold_copy(Tensor self, int dimension, int size, int step) -> Tensor"""

    raise NotImplementedError()


def aten_unique_consecutive(
    self: TensorType,
    return_inverse: bool = False,
    return_counts: bool = False,
    dim: Optional[int] = None,
) -> tuple[TensorType, TensorType, TensorType]:
    """unique_consecutive(Tensor self, bool return_inverse=False, bool return_counts=False, int? dim=None) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_unique_dim(
    self: TensorType,
    dim: int,
    sorted: bool = True,
    return_inverse: bool = False,
    return_counts: bool = False,
) -> tuple[TensorType, TensorType, TensorType]:
    """unique_dim(Tensor self, int dim, bool sorted=True, bool return_inverse=False, bool return_counts=False) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_unique_dim_consecutive(
    self: TensorType, dim: int, return_inverse: bool = False, return_counts: bool = False
) -> tuple[TensorType, TensorType, TensorType]:
    """unique_dim_consecutive(Tensor self, int dim, bool return_inverse=False, bool return_counts=False) -> (Tensor, Tensor, Tensor)"""

    raise NotImplementedError()


def aten_unsafe_chunk(self: TensorType, chunks: int, dim: int = 0) -> TensorType:
    """unsafe_chunk(Tensor self, int chunks, int dim=0) -> Tensor[]"""

    raise NotImplementedError()


def aten_unsafe_split(self: TensorType, split_size: INT64, dim: int = 0) -> TensorType:
    """unsafe_split.Tensor(Tensor self, SymInt split_size, int dim=0) -> Tensor[]"""

    raise NotImplementedError()


def aten_unsafe_split_with_sizes(
    self: TensorType, split_sizes: INT64, dim: int = 0
) -> TensorType:
    """unsafe_split_with_sizes(Tensor self, SymInt[] split_sizes, int dim=0) -> Tensor[]"""

    raise NotImplementedError()


@torch_op("aten::unsqueeze")
def aten_unsqueeze(self: TTensor, dim: int) -> TTensor:
    """unsqueeze(Tensor(a) self, int dim) -> Tensor(a)"""

    dim = op.Cast(dim, to=INT64.dtype)
    return op.Unsqueeze(self, dim)


def aten_unsqueeze_copy(self: TensorType, dim: int) -> TensorType:
    """unsqueeze_copy(Tensor self, int dim) -> Tensor"""

    raise NotImplementedError()


def aten_value_selecting_reduction_backward(
    grad: TensorType, dim: int, indices: TensorType, sizes: INT64, keepdim: bool
) -> TensorType:
    """value_selecting_reduction_backward(Tensor grad, int dim, Tensor indices, SymInt[] sizes, bool keepdim) -> Tensor"""

    raise NotImplementedError()


def aten_values(self: TensorType) -> TensorType:
    """values(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_values_copy(self: TensorType) -> TensorType:
    """values_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_vander(
    x: TensorType, N: Optional[int] = None, increasing: bool = False
) -> TensorType:
    """vander(Tensor x, int? N=None, bool increasing=False) -> Tensor"""

    raise NotImplementedError()


def aten_var(self: TensorType, unbiased: bool = True) -> TensorType:
    """var(Tensor self, bool unbiased=True) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::var_mean", trace_only=True)
def aten_var_mean(self: TReal, unbiased: bool = True) -> Tuple[TReal, TReal]:
    """var_mean(Tensor self, bool unbiased=True) -> (Tensor, Tensor)"""

    # Assume bool(True) and int(1) are same in ONNX, so pass "unbiased" directly as "correction"
    # If not this case, should be explicitly set correction value according to unbiased value
    return _aten_var_mean_onnx(self, correction=float(unbiased), keepdim=False)


@torch_op("aten::var_mean", overload=True, trace_only=True)
def aten_var_mean_dim(
    self: TReal, dim: Optional[int], unbiased: bool = True, keepdim: bool = False
) -> Tuple[TReal, TReal]:
    """var_mean.dim(Tensor self, int[1]? dim, bool unbiased=True, bool keepdim=False) -> (Tensor, Tensor)"""

    # Although dim is Optional in signature, but we assume it must has value for this overload
    # Assert(dim is not None)
    if isinstance(dim, Tuple):
        dim_tensor = op.Constant(value_ints=dim)
    else:
        dim_tensor = op.Constant(value_int=dim)
    return _aten_var_mean_dim_onnx(
        self, dim_tensor, correction=float(unbiased), keepdim=keepdim
    )


@torch_op("aten::var_mean", overload=True, trace_only=True)
def aten_var_mean_correction(
    self: TReal,
    dim: Optional[int] = None,
    correction: Optional[float] = None,
    keepdim: bool = False,
) -> Tuple[TReal, TReal]:
    """var_mean.correction(Tensor self, int[1]? dim=None, *, Scalar? correction=None, bool keepdim=False) -> (Tensor, Tensor)"""

    if correction is None:
        correction = 1.0

    if dim is None:
        var, mean = _aten_var_mean_onnx(self, correction, keepdim)
    else:
        if isinstance(dim, Tuple):
            dim_tensor = op.Constant(value_ints=dim)
        else:
            dim_tensor = op.Constant(value_int=dim)
        var, mean = _aten_var_mean_dim_onnx(self, dim_tensor, correction, keepdim)
    return var, mean


@torch_op("aten::var_mean", private=True)
def _aten_var_mean_onnx(
    self: TReal, correction: float = 1.0, keepdim: bool = False
) -> Tuple[TReal, TReal]:
    # Compute mean and var
    mean = op.ReduceMean(self, keepdims=keepdim)
    sub_mean = op.Sub(self, mean)
    sqr_mean = op.Mul(sub_mean, sub_mean)
    var = op.ReduceMean(sqr_mean, keepdims=keepdim)
    # Adjust var according to correction value
    if correction > 0.0:
        self_shape = op.Shape(self)
        numel_float = op.Cast(op.ReduceProd(self_shape, keepdims=0), to=FLOAT.dtype)
        mul = op.Mul(var, numel_float)
        sub = op.Sub(numel_float, correction)
        var = op.Div(mul, sub)

    return var, mean


@torch_op("aten::var_mean", private=True)
def _aten_var_mean_dim_onnx(
    self: TReal, dim: INT64, correction: float, keepdim: bool = False
) -> Tuple[TReal, TReal]:
    dim = op.Reshape(dim, op.Constant(value_ints=[-1]))
    # Computer mean and var
    mean = op.ReduceMean(self, dim, keepdims=keepdim)
    sub_mean = op.Sub(self, op.ReduceMean(self, dim, keepdims=1))
    sqr_mean = op.Mul(sub_mean, sub_mean)
    var = op.ReduceMean(sqr_mean, dim, keepdims=keepdim)
    # Adjust var according to correction value
    if correction > 0.0:
        self_shape = op.Shape(self)
        dim_size = op.Gather(self_shape, dim, axis=0)
        numel_float = op.Cast(op.ReduceProd(dim_size, keepdims=0), to=FLOAT.dtype)
        mul = op.Mul(var, numel_float)
        sub = op.Sub(numel_float, correction)
        var = op.Div(mul, sub)

    return var, mean


def aten_vdot(self: TensorType, other: TensorType) -> TensorType:
    """vdot(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::view")
def aten_view(self: TTensor, size: IntType) -> TTensor:
    """view(Tensor(a) self, SymInt[] size) -> Tensor(a)"""

    size = op.Cast(size, to=INT64.dtype)  # Reshape only support INT64 as second input
    return op.Reshape(self, size)


def aten_view_as(self: TensorType, other: TensorType) -> TensorType:
    """view_as(Tensor(a) self, Tensor other) -> Tensor(a)"""

    raise NotImplementedError()


def aten_view_as_complex(self: TensorType) -> TensorType:
    """view_as_complex(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_view_as_complex_copy(self: TensorType) -> TensorType:
    """view_as_complex_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_view_as_real(self: TensorType) -> TensorType:
    """view_as_real(Tensor(a) self) -> Tensor(a)"""

    raise NotImplementedError()


def aten_view_as_real_copy(self: TensorType) -> TensorType:
    """view_as_real_copy(Tensor self) -> Tensor"""

    raise NotImplementedError()


def aten_view_copy(self: TensorType, size: INT64) -> TensorType:
    """view_copy(Tensor self, SymInt[] size) -> Tensor"""

    raise NotImplementedError()


def aten_vstack(tensors: Sequence[TensorType]) -> TensorType:
    """vstack(Tensor[] tensors) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::where")
def aten_where(condition: BOOL, self: TTensor, other: TTensor) -> TTensor:
    """where.self(Tensor condition, Tensor self, Tensor other) -> Tensor"""

    return op.Where(condition, self, other)


def aten_xor(self: TensorType, other: TensorType) -> TensorType:
    """__xor__.Tensor(Tensor self, Tensor other) -> Tensor"""

    raise NotImplementedError()


@torch_op("aten::zeros")
def aten_zeros(size: IntType, dtype: int = FLOAT.dtype):
    """zeros(SymInt[] size, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None) -> Tensor"""

    size = op.Cast(size, to=INT64.dtype)
    zero = op.Constant(value_float=0.0)
    zero = op.Cast(zero, to=dtype)

    return op.Expand(zero, size)


@torch_op("aten::zeros_like", trace_only=True)
def aten_zeros_like(self: TTensor, dtype: int = -1) -> TTensor:
    """zeros_like(Tensor self, *, ScalarType? dtype=None, Layout? layout=None, Device? device=None, bool? pin_memory=None, MemoryFormat? memory_format=None) -> Tensor"""

    # NOTE: trace_only because both if branches need to be the same type, but we have
    # a cast in the if branch.

    if dtype == -1:
        zero = op.CastLike(0, self)
    else:
        zero = op.Cast(0, to=dtype)

    return _aten_zeros_like_onnx(self, zero)


@torch_op("aten::zeros_like", private=True)
def _aten_zeros_like_onnx(self: TTensor, zero) -> TTensor:
    shape = op.Shape(self)
    return op.Expand(zero, shape)