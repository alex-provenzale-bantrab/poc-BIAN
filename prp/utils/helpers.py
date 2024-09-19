def format_error_response( status="BadRequest", message="", status_code=400):
    return {
        "status_code": status_code,
        "status": status,
        "message": message,
    }