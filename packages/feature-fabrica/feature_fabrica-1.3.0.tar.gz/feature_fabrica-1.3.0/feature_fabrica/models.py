# models.py
import hashlib
from collections.abc import Callable
from typing import Any, Optional

import numpy as np
from beartype import beartype
from pydantic import (BaseModel, ConfigDict, Field, PrivateAttr,
                      root_validator, validator)

from feature_fabrica.utils import compute_all_transformations


class FeatureSpec(BaseModel):
    description: str
    data_type: str
    group: str  | None = None
    dependencies: list[str] | None = Field(default_factory=list)
    transformation: dict | None = Field(default_factory=dict)

    @validator("data_type")
    def validate_data_type(cls, v):
        try:
            # Check if the data_type is a valid type
            if not (getattr(np, v, None)):
                raise ValueError(
                    f"Invalid data_type specified: {v}, it should be in numpy"
                )
        except Exception as e:
            raise ValueError(f"Invalid data_type: {v}, error: {str(e)}")
        return v


class PromiseValue(BaseModel):
    _value: np.ndarray | None = PrivateAttr(default=None)  # Internal attribute
    data_type: str | None = None
    transformation: Callable | dict[str, Callable] | None = None

    @property
    def value(self) -> np.ndarray | None:
        """Read-only property for value."""
        return self._value

    @beartype
    def __call__(self, data: np.ndarray | None = None):
        if self.transformation is not None:
            result = compute_all_transformations(self.transformation)
            self._set_value(result.value)
        else:
            if self._value is not None:
                raise ValueError("Value is already set.")
            self._set_value(data)

    def _set_value(self, value: np.ndarray | None):
        """Internal method to set value and transform to FeatureValue."""
        self._value = value
        if value is not None:
            data_type = self.data_type or value.dtype.name
            # Transform to a FeatureValue instance
            new_instance = FeatureValue(value=value, data_type='str_' if 'str' in data_type else data_type)
            self.__class__ = new_instance.__class__
            self.__dict__ = new_instance.__dict__

class FeatureValue(np.lib.mixins.NDArrayOperatorsMixin, BaseModel, validate_assignment=True):  # type: ignore[call-arg]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    value: np.ndarray = Field(default=None)
    data_type: str

    @root_validator(pre=True)
    def validate_value(cls, values):
        v = values.get("value")
        data_type = values.get("data_type")
        # Allow PromiseValue without validation
        if isinstance(v, PromiseValue):
            return values

        # Get the expected data type from numpy
        try:
            expected_dtype = getattr(np, data_type)
        except AttributeError:
            raise ValueError(f"Unsupported data type '{data_type}', use valid numpy dtype!")

        # Check if the value is a NumPy array
        if not isinstance(v, np.ndarray):
            raise ValueError(f"Value must be a NumPy array, got {type(v).__name__} instead.")

        # Validate that the array dtype matches or is compatible with the expected dtype
        # TODO: make casting type configurable
        if not (np.issubdtype(v.dtype.type, expected_dtype) or np.can_cast(v.dtype.type, expected_dtype, casting="unsafe")):
            raise ValueError(
                f"Array dtype '{v.dtype}' does not match or is not compatible with expected type '{data_type}'"
            )

        # Optionally, convert to the desired type if compatible
        if v.dtype.type is not expected_dtype:
            try:
                v = v.astype(expected_dtype)
            except TypeError:
                raise ValueError(f"Failed to convert array to expected dtype '{data_type}'.")
        values["value"] = v  # Update the value in the values dictionary
        return values

    def __array__(self, dtype=None, copy=None):
        # Automatically converts to np.ndarray when passed to a function that expects an array
        if dtype:
            return self.value.astype(dtype)
        return self.value.copy() if copy else self.value

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # Convert inputs to their underlying values if they are FeatureValue instances
        inputs = tuple(x.value if isinstance(x, FeatureValue) else x for x in inputs)

        # Perform the operation using the ufunc
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return result

    def __array_function__(self, func, types, args, kwargs):
        # Convert args to their underlying values if they are FeatureValue instances
        args = tuple(x.value if isinstance(x, FeatureValue) else x for x in args)
        # Perform the operation using the function
        result = func(*args, **kwargs)
        return result

    def __getitem__(self, idx):
        return self.value[idx]

    def __getattr__(self, name):
        return getattr(self.value, name)

    def __repr__(self):
        return f"FeatureValue(value={self.value})"

class TNode(BaseModel):
    transformation_name: str
    start_time: float
    end_time: float
    shape: tuple | None = None
    time_taken: float | None = None
    output_hash: str | None = None
    next: Optional["TNode"] = None  # Forward reference

    def to_dict(self) -> dict[str, Any]:
        # Convert the node and its next nodes to a dictionary
        node_dict = {
            "value": self.value,
            "transformation_name": self.transformation_name,
        }
        if self.next:
            node_dict["next"] = self.next.to_dict()
        else:
            node_dict["next"] = None
        return node_dict

    def compute_hash(self, data: np.ndarray) -> str:
        data_bytes = data.tobytes()
        return hashlib.sha256(data_bytes).hexdigest()

    def store_hash_and_shape(self, output_data: np.ndarray):
        self.shape = output_data.shape
        self.output_hash = self.compute_hash(output_data)

    def finilize_metrics(self) -> None:
        self.time_taken = self.end_time - self.start_time


class THead(BaseModel):
    next: TNode | None = None
