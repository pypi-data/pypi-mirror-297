import re
from collections.abc import Iterable
from typing import Annotated, Union

import numpy as np
from beartype.vale import Is
from jaxtyping import Float, Integer

NumericArray = Union[Float[np.ndarray, "..."], Integer[np.ndarray, "..."]]
NumericValue = Union[np.floating, np.integer, float, int]

StrArray = Annotated[np.ndarray, Is[lambda array: array.dtype.kind == 'U']]
StrValue = Union[np.str_, str]

DateTimeArray = Annotated[np.ndarray, Is[lambda array: array.dtype.type is np.datetime64]]
TimeDeltaArray = Annotated[np.ndarray, Is[lambda array: array.dtype.type is np.timedelta64]]

StrOrNumArray = Union[StrArray, NumericArray]
AnyArray = Union[StrArray, NumericArray, DateTimeArray, TimeDeltaArray] # to be extended

DATE_REGEX = re.compile(
    r'^(\d{4}-\d{2}-\d{2})'          # Matches YYYY-MM-DD
    r'(?:[ T](\d{2})(?::(\d{2}))?(?::(\d{2}))?)?$'  # Optionally matches HH, HH:MM, or HH:MM:SS
)

def is_numpy_datetime_format(date_str: str) -> bool:
    # Check if the string matches the common datetime formats (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
    if not DATE_REGEX.match(date_str):
        return False
    return True

def has_ndarray_operators_mixin(obj):
    mixin_methods = ['__array_ufunc__', '__array__']
    return all(hasattr(obj, method) for method in mixin_methods)

def broadcast_and_normalize_numeric_array(iterable: Iterable) -> NumericArray:
    # Normalize all elements to np.array
    normalized_iterable = []
    for element in iterable:  # type: ignore[union-attr]
        if not isinstance(element, np.ndarray) and not has_ndarray_operators_mixin(element):
            element = np.array([element], dtype=np.float32)
        normalized_iterable.append(element)
    # Find the maximum shape among the elements
    max_shape = np.broadcast_shapes(*[elem.shape for elem in normalized_iterable])

    # Broadcast elements to the maximum shape
    broadcasted_iterable = [
        np.broadcast_to(elem, max_shape) for elem in normalized_iterable
    ]
    return broadcasted_iterable

def is_valid_numpy_dtype(data_type: str) -> bool:
    try:
        np.dtype(data_type)
        return True
    except TypeError:
        return False
