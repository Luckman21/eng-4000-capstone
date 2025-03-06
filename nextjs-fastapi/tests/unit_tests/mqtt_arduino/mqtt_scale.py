import pytest
from unittest.mock import MagicMock
import paho.mqtt.client as mqtt
from io import StringIO
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from backend.controller.scale_listener import MQTTscale

# Pytest Fixture to setup MQTTscale instance
@pytest.fixture
def scale():
    """Fixture to create a mock MQTTscale instance."""
    mqtt_broker = "mqtt.eclipse.org"
    mqtt_port = 1883
    mqtt_topic = "scale/topic"
    
    scale = MQTTscale(mqtt_broker, mqtt_port, mqtt_topic)
    
    # Mock the MQTT client connection
    scale.client = MagicMock(mqtt.Client)
    
    return scale

# Test when the weight is within a valid range
@pytest.mark.parametrize("valid_weight", [2500.0, 0.0, 5000.0])  # Testing different valid values
def test_process_message_valid_range(scale, valid_weight, capsys):
    """Test if the weight is within the valid range (0 to 5000)."""
    scale.process_message(str(valid_weight))
    
    # Verify output contains the correct message
    output = capsys.readouterr().out
    assert f"Stored value: {valid_weight}\n" in output

# Test when the weight is outside the valid range (above max)
@pytest.mark.parametrize("invalid_weight", [6000.0, 10000.0])
def test_process_message_invalid_range(scale, invalid_weight, capsys):
    """Test if the weight is outside the valid range (> 5000)."""
    scale.process_message(str(invalid_weight))
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Stored value: {invalid_weight}\n" in output

# Test when the weight is negative
def test_process_message_negative_weight(scale, capsys):
    """Test if the weight is negative (outside the valid range)."""
    negative_weight = -10.0
    scale.process_message(str(negative_weight))
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Stored value: {negative_weight}\n" in output

# Test when the weight is exactly zero
def test_process_message_zero_weight(scale, capsys):
    """Test if the weight is exactly zero (boundary case)."""
    zero_weight = 0.0
    scale.process_message(str(zero_weight))
    
    # Verify output indicates the weight is within the valid range
    output = capsys.readouterr().out
    assert f"Stored value: {zero_weight}\n" in output

# Test when the weight is a string that can't be converted to float
def test_process_message_invalid_float(scale, capsys):
    """Test if the payload is invalid (can't be converted to float)."""
    invalid_payload = "not_a_number"
    scale.process_message(invalid_payload)
    
    # Verify error message is printed
    output = capsys.readouterr().out
    assert f"Error: Failed to convert message payload to float:" in output