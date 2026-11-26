from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TelemetryMessage(BaseModel):
    """
    Defines the standard telemetry message
    accepted by ColdTrace.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    device_id: str = Field(
        min_length=3,
        max_length=64
    )

    shipment_id: str = Field(
        min_length=3,
        max_length=64
    )

    message_id: UUID

    temperature: float = Field(
        ge=-80.0,
        le=100.0
    )

    humidity: float = Field(
        ge=0.0,
        le=100.0
    )

    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "Timestamp must include timezone information"
            )

        return value