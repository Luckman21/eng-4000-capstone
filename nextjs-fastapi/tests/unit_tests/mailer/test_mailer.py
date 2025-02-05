import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from unittest.mock import MagicMock
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.service.mailer.PasswordChangeMailer import PasswordChangeMailer
from backend.service.mailer.LowStockMailer import LowStockMailer

verified_email = 'pantheonprototyping@gmail.com'

# Test the TempPasswordMailer class
@pytest.fixture
def mock_sendgrid():

    # Mock mailer
    mock_mailer_service = MagicMock()

    # Create a mock response object with a status_code
    mock_response = MagicMock()
    mock_response.status_code = 202  # Simulate a successful response with status code 202

    # Make send_email return this mock response
    mock_mailer_service.send_email.return_value = mock_response
    return mock_mailer_service


def test_send_temp_password_email_success(mock_sendgrid):

    # Initialize TempPasswordMailer with a mock sendgrid service
    temp_password_mailer = TempPasswordMailer(from_addr=verified_email)
    temp_password_mailer.client = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    temp_password = "temp123password"
    response = temp_password_mailer.send_notification(recipient, temp_password)

    # Assert that the send_email method was called once
    mock_sendgrid.send_email.assert_called_once_with(
        recipient,
        "Pantheon Inventory Management: Your Temporary Password",
        f"Well met,\n\nYour temporary password is: {temp_password}\n\nPlease use this password to log in and reset it as soon as possible.\n\nIf you have not requested a change, you can ignore this email.",
        verified_email
    )

    # Assert that the response is successful
    assert response.status_code == 202


def test_send_temp_password_email_failure(mock_sendgrid):

    # Simulate failure by making send_email raise an exception
    mock_sendgrid.send_email.side_effect = Exception("SendGrid API error")

    # Initialize TempPasswordMailer with a mock sendgrid service
    temp_password_mailer = TempPasswordMailer(from_addr=verified_email)
    temp_password_mailer.mailer_service = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    temp_password = "temp123password"

    # Call the method and assert that it prints the error
    with pytest.raises(Exception):  # Expect an exception to be raised
        temp_password_mailer.send_temp_password_email(recipient, temp_password)


def test_send_password_change_email_success(mock_sendgrid):

    # Initialize TempPasswordMailer with a mock sendgrid service
    password_change_mailer = PasswordChangeMailer(from_addr=verified_email)
    password_change_mailer.client = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    response = password_change_mailer.send_notification(recipient)

    # Assert that the send_email method was called once
    mock_sendgrid.send_email.assert_called_once_with(
        recipient,
        "Pantheon Inventory Management: Password Change Notice",
        f"Well met, Your password has successfully been changed. If this was not you, please contact a system Super Admin for support.",
        verified_email
    )

    # Assert that the response is successful
    assert response.status_code == 202


def test_send_password_change_email_failure(mock_sendgrid):

    # Simulate failure by making send_email raise an exception
    mock_sendgrid.send_email.side_effect = Exception("SendGrid API error")

    # Initialize TempPasswordMailer with a mock sendgrid service
    password_change_mailer = PasswordChangeMailer(from_addr=verified_email)
    password_change_mailer.client = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    temp_password = "temp123password"

    # Call the method and assert that it prints the error
    with pytest.raises(Exception):  # Expect an exception to be raised
        password_change_mailer.send_notification(recipient, temp_password)


def test_send_low_stock_email_success(mock_sendgrid):

    # Initialize TempPasswordMailer with a mock sendgrid service
    low_stock_mailer = LowStockMailer(from_addr=verified_email)
    low_stock_mailer.client = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    type = "type"
    colour = "colour"
    link = "link.com"

    response = low_stock_mailer.send_notification(recipient, type, colour, link)

    # Assert that the send_email method was called once
    mock_sendgrid.send_email.assert_called_once_with(
        recipient,
        "Pantheon Inventory Management: Low Stock Warning",
        f"Well met,\n\n You have 50g left of {colour} {type}.\n\n Use {link} to purchase more.",
        verified_email
    )

    # Assert that the response is successful
    assert response.status_code == 202


def test_send_low_stock_email_failure(mock_sendgrid):

    # Simulate failure by making send_email raise an exception
    mock_sendgrid.send_email.side_effect = Exception("SendGrid API error")

    # Initialize TempPasswordMailer with a mock sendgrid service
    low_stock_mailer = LowStockMailer(from_addr=verified_email)
    low_stock_mailer.client = mock_sendgrid  # Use the mocked service

    # Mock sending an email
    recipient = "recipient@example.com"
    type = "type"
    colour = "colour"
    link = "link.com"

    # Call the method and assert that it prints the error
    with pytest.raises(Exception):  # Expect an exception to be raised
        low_stock_mailer.send_notification(recipient, type, colour, link)