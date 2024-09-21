from enum import Enum


class ErrorMessages(Enum):
    USER_ALREADY_EXISTS = "A user with this mobile number already exists."
    NOT_FOUND = "{0} not found."
    INVALID_PASSWORD = "Invalid password."
    MFA_FAILED = "MFA authentication failed. Invalid {0} mfa code entered."

    OTP_LIMIT_REACHED = "Maximum OTP attempts reached in the last {0} minutes."
    OTP_EXPIRED = "OTP has expired."
    INVALID_OTP = "Invalid OTP."

    INVALID_TOKEN = "Could not validate credentials."
    TOKEN_EXPIRED = "Token has expired."

    AWS_SECRET_EXCEPTION = (
        "Unable to retrieve the secret at this time. Please try again later."
    )
    AWS_SES_EXCEPTION = "Unable to send the mail at this time. Please try again later."

    UNIFONIC_MISSING_DATA = "Unifonic API key or sender ID is missing."
    UNIFONIC_EXCEPTION = "Failed to send OTP: {0}"
    UNIFONIC_REQUEST_TIMEOUT = "Request to Unifonic timed out. Please try again later."

    FORBIDDEN = "Action not allowed: {0} are restricted from performing this operation."
    UNKNOWN = "Unknown error occurred. Please try again later."
    BLANK_PASSWORD = "Password has not been set. Please set the password first."


class SuccessMessages(Enum):
    OTP_SENT = "OTP generated and sent successfully."
    OTP_VERIFIED = "OTP verified successfully. User logged in successfully."
    PASSWORD_SET = "Password set successfully."
    PASSWORD_RESET_MAIL_SENT = "Password reset link sent successfully."
    PASSWORD_RESET_SUCCESS = "Password reset successfully."
    MFA_ENABLED = "Multi-factor authentication enabled successfully."
    LOGGED_IN = "Logged in successfully."


class LogEvents(Enum):
    INVALID_OTP = "INVALID_OTP"
    OTP_EXPIRED = "OTP_EXPIRED"
    OTP_GENERATED = "OTP_GENERATED"
    OTP_SENT = "OTP_SENT"
    OTP_VERIFIED = "OTP_VERIFIED"

    PASSWORD_RESET_MAIL_SENT = "PASSWORD_RESET_MAIL_SENT"
    PASSWORD_RESET_SUCCESS = "PASSWORD_RESET_SUCCESS"
    MFA_ENABLED = "MFA_ENABLED"
    MFA_VERIFICATION_FAILED = "MFA_VERIFICATION_FAILED"
    LOGGED_IN = "LOGGED_IN"
    INVALID_PASSWORD = "INVALID_PASSWORD"
