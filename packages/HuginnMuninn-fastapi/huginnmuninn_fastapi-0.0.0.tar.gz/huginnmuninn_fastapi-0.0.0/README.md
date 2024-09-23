# HuginnMuninn FastAPI Exception Handling Package
## Overview
This package provides a flexible and structured way to handle exceptions in FastAPI applications. It introduces custom
exceptions that include detailed error codes and logging, making it easier to trace errors and respond with consistent
and informative HTTP responses.

The package includes:

* HuginnMuninnError: A base exception class for structured error handling.
* HuginnMuninnHTTPException: A subclass that allows custom HTTP exception handling in FastAPI.

## Features
* Structured Error Codes: The exception classes support structured error codes with the format
api_ref-interface_ref-generic_error_code-internal_error_code, which helps in categorizing and tracing errors.
* Logging: Each exception is logged when raised, making it easier to debug in production.
* FastAPI Integration: The HuginnMuninnHTTPException class can easily integrate with FastAPI's exception handler system
for custom HTTP responses.