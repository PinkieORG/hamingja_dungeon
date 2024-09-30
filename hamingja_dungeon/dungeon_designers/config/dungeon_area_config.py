from typing import Any, Literal, Optional, Tuple

from pydantic import (BaseModel, confloat, conint, field_validator, model_validator)


def none_attribute(object: Any) -> Optional[str]:
    for field, value in object.__dict__.items():
        if value is None:
            return field
    return None


class DungeonAreaConfig(BaseModel):
    size: Tuple[conint(ge=1), conint(ge=1)]
    room_size_method: Literal["fixed", "range", "factor"]
    fixed_room_size: Optional[Tuple[conint(ge=3), conint(ge=3)]] = None
    range_room_size: Optional[
        Tuple[conint(ge=3), conint(ge=3), conint(ge=3), conint(ge=3)]
    ] = None
    factor_room_size: Optional[
        Tuple[
            confloat(ge=0.0, le=1.0),
            confloat(ge=0.0, le=1.0),
            confloat(ge=0.0, le=1.0),
            confloat(ge=0.0, le=1.0),
        ]
    ] = None

    @field_validator("range_room_size")
    @classmethod
    def max_greater_than_min_range(cls, v: Tuple[int, int, int, int]):
        min_height, max_height, min_width, max_width = v
        if min_height > max_height or min_width > max_width:
            raise ValueError("Minimum dimension cannot be larger than the maximum one.")
        return v

    @field_validator("factor_room_size")
    @classmethod
    def max_greater_than_min_factor(cls, v: Tuple[float, float, float, float]):
        (
            min_height_factor,
            max_height_factor,
            min_width_factor,
            max_width_factor,
        ) = v
        if min_height_factor > max_height_factor or min_width_factor > max_width_factor:
            raise ValueError("Minimum dimension cannot be larger than the maximum one.")
        return v

    @model_validator(mode="after")
    def check_room_size_method(self):
        mapping = {
            "fixed": self.fixed_room_size,
            "range": self.range_room_size,
            "factor": self.factor_room_size,
        }

        for method, object in mapping.items():
            if method == self.room_size_method:
                if not object:
                    raise ValueError(
                        f"{method} was selected but its associated parameters "
                        f"were not."
                    )
                """
                empty = none_attribute(object)
                if not empty:
                    raise ValueError(
                        f"{method} was selected but {empty} is " f"empty."
                    )
                    """
        return self
