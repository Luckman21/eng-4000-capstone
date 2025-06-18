import pytest
from unittest.mock import MagicMock
import paho.mqtt.client as mqtt
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from backend.controller.data_receiver import MQTTReceiver

# Pytest Fixture to setup MQTTReceiver instance
@pytest.fixture
def scale():
    """Fixture to create a mock MQTTReceiver instance."""
    mqtt_broker = "mqtt.eclipse.org"
    mqtt_port = 1883
    mqtt_temp_topic = "sensor/temperature"
    mqtt_humid_topic = "sensor/humidity"
    db_url = "sqlite:///:memory:"
    
    scale = MQTTReceiver(mqtt_broker, mqtt_port, mqtt_temp_topic, mqtt_humid_topic, db_url)
    
    # Mock the MQTT client connection
    scale.client = MagicMock(mqtt.Client)
    
    return scale

# Test when the temperature is within a valid range
@pytest.mark.parametrize("valid_temperature", [25.0, 20.0, 18.5])  # Valid temperatures in Celsius
def test_process_message_valid_temperature(scale, valid_temperature, capsys):
    """Test if the temperature is within the valid range."""
    payload = f"0|{valid_temperature}"
    scale.process_message(scale.mqtt_temp_topic, payload)
    
    # Verify output contains the correct message
    output = capsys.readouterr().out
    assert f"Received temperature: {valid_temperature}" in output

# Test when the humidity is within a valid range
@pytest.mark.parametrize("valid_humidity", [20.0, 10.0, 5.0])  # Valid humidity percentages
def test_process_message_valid_humidity(scale, valid_humidity, capsys):
    """Test if the humidity is within the valid range."""
    payload = f"0|{valid_humidity}"
    scale.process_message(scale.mqtt_humid_topic, payload)
    
    # Verify output contains the correct message
    output = capsys.readouterr().out
    assert f"Received humidity: {valid_humidity}" in output

# Test when the temperature is outside the valid range (too high)
@pytest.mark.parametrize("invalid_temperature", [100.0, 150.0])  # Invalid high temperatures
def test_process_message_invalid_temperature_high(scale, invalid_temperature, capsys):
    """Test if the temperature is outside the valid range (too high)."""
    payload = f"0|{invalid_temperature}"
    scale.process_message(scale.mqtt_temp_topic, payload)
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Received temperature: {invalid_temperature}" in output

# Test when the humidity is outside the valid range (too high)
@pytest.mark.parametrize("invalid_humidity", [120.0, 150.0])  # Invalid high humidity
def test_process_message_invalid_humidity_high(scale, invalid_humidity, capsys):
    """Test if the humidity is outside the valid range (too high)."""
    payload = f"0|{invalid_humidity}"
    scale.process_message(scale.mqtt_humid_topic, payload)
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Received humidity: {invalid_humidity}" in output

# Test when the temperature is a negative value
def test_process_message_negative_temperature(scale, capsys):
    """Test if the temperature is negative (outside the valid range)."""
    negative_temperature = -5.0
    payload = f"0|{negative_temperature}"
    scale.process_message(scale.mqtt_temp_topic, payload)
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Received temperature: {negative_temperature}" in output

# Test when the humidity is a negative value
def test_process_message_negative_humidity(scale, capsys):
    """Test if the humidity is negative (outside the valid range)."""
    negative_humidity = -10.0
    payload = f"0|{negative_humidity}"
    scale.process_message(scale.mqtt_humid_topic, payload)
    
    # Verify output indicates it's outside the valid range
    output = capsys.readouterr().out
    assert f"Received humidity: {negative_humidity}" in output

# Test when the payload is invalid (cannot be converted to float)
def test_process_message_invalid_float(scale, capsys):
    """Test if an invalid payload (non-numeric) causes an error."""
    invalid_payloads = ["no_ID|23.1", "0|no_data", "0,23.1"]  # Invalid formats
    
    for payload in invalid_payloads:
        scale.process_message(scale.mqtt_temp_topic, payload)
    
    # Verify error message is printed
    output = capsys.readouterr().out
    assert "Error processing message" in output

# Test when the payload is in an invalid format (using wrong delimiter)
def test_process_message_invalid_format(scale, capsys):
    """Test if the payload format is invalid (wrong delimiter or missing data)."""
    invalid_payloads = ["1,23.1", "1|wrong_format", "no_data"]
    
    for payload in invalid_payloads:
        scale.process_message(scale.mqtt_temp_topic, payload)
    
    # Verify error message is printed
    output = capsys.readouterr().out
    assert "Error processing message" in output