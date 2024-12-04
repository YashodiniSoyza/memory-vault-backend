from enum import Enum


class MessageConstants(Enum):
    # Aggregator Configuration Messages
    AGGREGATOR_CONFIG_EXISTS = "Aggregator configuration already exists."
    AGGREGATOR_CONFIG_REGISTER_SUCCESS = "Aggregator configuration registered successfully"
    AGGREGATOR_CONFIG_NOT_FOUND = "Aggregator configuration not found."
    AGGREGATOR_CONFIG_UPDATE_SUCCESS = "Aggregator configuration updated successfully"
    AGGREGATOR_CONFIG_DELETE_SUCCESS = "Aggregator configuration deleted successfully"
    AGGREGATOR_CONFIG_UNEXPECTED_SAVE_ERROR = "Failed to save aggregator configuration due to an unexpected error."
    AGGREGATOR_CONFIG_UNEXPECTED_FETCH_ERROR = ("Failed to retrieve aggregator configurations due to an unexpected "
                                                "error.")
    AGGREGATOR_CONFIG_UNEXPECTED_UPDATE_ERROR = "Failed to update aggregator configuration due to an unexpected error."
    AGGREGATOR_CONFIG_UNEXPECTED_DELETE_ERROR = "Failed to delete aggregator configuration due to an unexpected error."
    VALIDATION_ERROR_SAVE = "Validation error during save: {}"
    VALIDATION_ERROR_UPDATE = "Validation error during update: {}"
    VALIDATION_ERROR_DELETE = "Validation error during deletion: {}"

    # Aggregator Messages
    AGGREGATOR_EXISTS = "Aggregator already exists with this identifier."
    AGGREGATOR_REGISTER_SUCCESS = "Aggregator registered successfully"
    AGGREGATOR_NOT_FOUND = "Aggregator not found with the specified ID."
    AGGREGATOR_UPDATE_SUCCESS = "Aggregator updated successfully"
    AGGREGATOR_DELETE_SUCCESS = "Aggregator deleted successfully"
    AGGREGATOR_UNEXPECTED_SAVE_ERROR = "Failed to save aggregator due to an unexpected error."
    AGGREGATOR_UNEXPECTED_FETCH_ERROR = "Failed to retrieve aggregators due to an unexpected error."
    AGGREGATOR_UNEXPECTED_UPDATE_ERROR = "Failed to update aggregator due to an unexpected error."
    AGGREGATOR_UNEXPECTED_DELETE_ERROR = "Failed to delete aggregator due to an unexpected error."

    # NimbleWay Configuration Messages
    NIMBLEWAY_CONFIG_SAVE_SUCCESS = "Configuration saved successfully"
    NIMBLEWAY_CONFIG_UPDATE_SUCCESS = "Configuration updated successfully"
    NIMBLEWAY_CONFIG_NOT_FOUND = "Configuration not found."
    NIMBLEWAY_UNEXPECTED_SAVE_ERROR = "Failed to save configuration due to an unexpected error."
    NIMBLEWAY_UNEXPECTED_FETCH_ERROR = "Failed to fetch configuration due to an unexpected error."
    NIMBLEWAY_UNEXPECTED_UPDATE_ERROR = "Failed to update configuration due to an unexpected error."
    NIMBLEWAY_UNEXPECTED_DELETE_ERROR = "Failed to delete configuration due to an unexpected error."

    # AES Decryption Messages
    AES_SECRET_KEY_NOT_FOUND = "AES secret key not found in environment variables."

    # API Request Messages
    API_GET_REQUEST_SUCCESS = "Successful GET request to %s with headers %s. Response status code: %s"
    API_GET_REQUEST_FAILURE = "Failed GET request to %s with headers %s. Response status code: %s. Error: %s"
    API_GET_REQUEST_NO_RESPONSE = "Failed GET request to %s with headers %s. No response received. Error: %s"
    API_POST_REQUEST_SUCCESS = "Successful POST request to %s with headers %s. Response status code: %s"
    API_POST_REQUEST_FAILURE = "Failed POST request to %s with headers %s. Response status code: %s. Error: %s"
    API_POST_REQUEST_NO_RESPONSE = "Failed POST request to %s with headers %s. No response received. Error: %s"
    NIMBLEWAY_FORBIDDEN_ERROR = "Nimbleway API call failed with Http 403 status %s with headers %s"
    NIMBLEWAY_GENERAL_FAILURE = "Nimbleway API call failed %s with headers %s"
    CONFIG_MISSING_FIELDS = "Configuration missing required fields for proxy URL formatting."
    INVALID_CONFIG = "Invalid configuration for proxy URL"

    # Token Management Messages
    ACCESS_TOKEN_INSERT_SUCCESS = "Access token inserted for partner_id: %s, aggregator_type: %s"
    ACCESS_TOKEN_UPDATE_SUCCESS = "Access token updated for partner_id: %s, aggregator_type: %s"
    ACCESS_TOKEN_DELETE_SUCCESS = "Access token deleted for partner_id: %s, aggregator_type: %s"
    ACCESS_TOKEN_NOT_FOUND = "Access token not found for partner_id: %s, aggregator_type: %s"
