from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.api.security_schemas import TelemetryMessage


def valid_telemetry():
    """Return a valid sample telemetry message."""

    return {
        "device_id": "CT-DEVICE-001",
        "shipment_id": "SHIP-001",
        "message_id": str(uuid4()),
        "temperature": 4.2,
        "humidity": 55.0,
        "timestamp": "2026-11-26T03:50:00Z"
    }


def test_valid_telemetry_is_accepted():
    message = TelemetryMessage(**valid_telemetry())

    assert message.device_id == "CT-DEVICE-001"
    assert message.temperature == 4.2
    assert message.humidity == 55.0


def test_missing_device_id_is_rejected():
    data = valid_telemetry()
    del data["device_id"]

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_invalid_message_id_is_rejected():
    data = valid_telemetry()
    data["message_id"] = "not-a-valid-uuid"

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_temperature_outside_range_is_rejected():
    data = valid_telemetry()
    data["temperature"] = 150.0

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_humidity_outside_range_is_rejected():
    data = valid_telemetry()
    data["humidity"] = 120.0

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_naive_timestamp_is_rejected():
    data = valid_telemetry()
    data["timestamp"] = datetime(2026, 11, 26, 3, 50)

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_unknown_fields_are_rejected():
    data = valid_telemetry()
    data["unauthorized_field"] = "unexpected"

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_empty_device_id_is_rejected():
    data = valid_telemetry()
    data["device_id"] = ""

    with pytest.raises(ValidationError):
        TelemetryMessage(**data)


def test_whitespace_is_stripped_from_device_id():
    data = valid_telemetry()
    data["device_id"] = "  CT-DEVICE-001  "

    message = TelemetryMessage(**data)

    assert message.device_id == "CT-DEVICE-001"


def test_model_serializes_to_json():
    message = TelemetryMessage(**valid_telemetry())

    serialized = message.model_dump_json()

    assert "CT-DEVICE-001" in serialized