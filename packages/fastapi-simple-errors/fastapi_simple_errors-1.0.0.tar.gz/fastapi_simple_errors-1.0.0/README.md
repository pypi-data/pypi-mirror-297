[![Tests](https://github.com/patrsc/fastapi-simple-errors/actions/workflows/tests.yml/badge.svg)](https://github.com/patrsc/fastapi-simple-errors/actions/workflows/tests.yml)
[![Linting](https://github.com/patrsc/fastapi-simple-errors/actions/workflows/linting.yml/badge.svg)](https://github.com/patrsc/fastapi-simple-errors/actions/workflows/linting.yml)

# fastapi-simple-errors

Simple error handling for fastapi using custom error classes.

## Introduction

This small Python package aims to simplify error handling for
[FastAPI](https://fastapi.tiangolo.com/):
* It allows defining custom exception classes in a simple way with little boilerplate code.
* Your application functions can raise these errors and they will be propageted to FastAPI and
  result in a proper 4xx or 5xx status code to be sent to the client.
* Proper OpenAPI documentation can be generated using a generic response schema for errors, which includes the error ID (Python class name) and a human-readable error message.

This package was inspired by the following discussions and projects:
* [Include possible HTTPExceptions in OpenAPI spec](https://github.com/tiangolo/fastapi/discussions/9124)
* [FastAPI-Pydantic-Mongo_Sample_CRUD_API
](https://github.com/David-Lor/FastAPI-Pydantic-Mongo_Sample_CRUD_API/tree/master)

## Usage

The package [fastapi-simple-errors](https://pypi.org/project/fastapi-simple-errors/) is available
on [PyPi](https://pypi.org/), so it can be installed with Python package managers such as
`pip` or [poetry](https://python-poetry.org/).

First, you need to import the base errors from the package:

```py
from fastapi_simple_errors import BadRequestError, NotFoundError, UnauthorizedError
```

Now, you can define your custom errors based on you application's needs:

```py
class UserNotFoundError(NotFoundError):
    """The user was not found in the database."""


class InvalidUserIdError(BadRequestError):
    """The provided user ID is not valid."""


class InvalidTokenError(UnauthorizedError):
    """The provided authentication token is not valid."""

```

These error's inherit from FastAPI's `HTTPException` and will use the corresponding HTTP status
codes, for example:
* 400 for `BadRequestError`
* 401 for `UnauthorizedError`
* 404 for `NotFoundError`

In your FastAPI application, you could write:

```py
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    if user_id not in users:
        raise UserNotFoundError()
    return {"user": users[user_id]}
```

Note that this error could also be raised in sub-functions and will be propagated accordingly.

This will result in the following response:

```
HTTP/1.1 404 Not Found
...

{
    "detail": {
        "error": "UserNotFoundError",
        "message": "The user was not found in the database."
    }
}
```

Note that the error class name is returned in the response as error identifier and the error
message is used from the docstring. However, you could overwrite the message and also set custom
headers:

```py
raise UserNotFoundError("A custom message", headers={"X-State": "..."})
```

The predefined errors (like `NotFoundError`) all inherit from `AppError`.
This can be used to define your own errors with custom status codes, e.g.:

```py
from from fastapi_simple_errors import AppError
from fastapi import status

class TeapotError(AppError):
    """This server is a teapot."""

    status_code = status.HTTP_418_IM_A_TEAPOT
```

To include the errors (and error response schema) in the OpenAPI documentation,
you can use the package's `error_responses` function, like this:

```py
from fastapi_simple_errors import BadRequestError, NotFoundError, error_responses

@app.get("/users/{user_id}", responses=error_responses(BadRequestError, NotFoundError))
async def read_user(user_id: str):
    if is_invalid(user_id):
        raise InvalidUserIdError()
    if user_id not in users:
        raise UserNotFoundError()
    return {"user": users[user_id]}
```

For more concise code, you could alternatively use the `error_responses_from_status_codes` function:

```py
from fastapi_simple_errors import BadRequestError, NotFoundError
from fastapi_simple_errors import error_responses_from_status_codes as err

@app.get("/users/{user_id}", responses=err(400, 404))
async def read_user(user_id: str):
    if is_invalid(user_id):
        raise InvalidUserIdError()
    if user_id not in users:
        raise UserNotFoundError()
    return {"user": users[user_id]}
```

The generated OpenAPI documentation will look like this (using [Redoc](https://redocly.com/redoc)):

![openapi](https://raw.githubusercontent.com/patrsc/fastapi-simple-errors/main/openapi.png)

## Licence

MIT
