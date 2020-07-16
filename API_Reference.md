# Fresh Fyyur API Reference

## Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default local location `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration
* Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format
```python
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The following error types are returned by the API when requests fail:
* 401: Unauthorized
* 404: Resource not found
* 422: Not Processible

## Endpoints
**GET /venues**