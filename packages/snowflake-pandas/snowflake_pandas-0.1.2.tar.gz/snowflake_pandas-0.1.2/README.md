# SNOWFLAKE PANDAS

## Installation

1. Install the package
    ```bash
    pip install snowflake-pandas
    ```

## Requirements

Currently, the pandas-oriented API methods in the Python connector API work with:
- Snowflake Connector 2.1.2 (or higher) for Python.
- PyArrow library version 3.0.x.
- Pandas 0.25.2 (or higher). Earlier versions might work, but have not been tested.

For more information, see the [Snowflake Connector for Python documentation](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-install).

## Caution

If you already have any version of the PyArrow library other than the recommended version listed above, please uninstall PyArrow before installing the Snowflake Connector for Python. Do not re-install a different version of PyArrow after installing the Snowflake Connector for Python.

For more information, see the [PyArrow library documentation](https://arrow.apache.org/docs/).


# Snowflake Connector for Python Pandas

This package provides a simple and efficient interface for connecting to Snowflake and interacting with it using Pandas. It supports common operations such as querying data, writing DataFrames to Snowflake, and managing table schemas.

## Benefits of Using This Package

1. **Seamless Integration with Pandas**:
    - Effortlessly write and read data using familiar Pandas DataFrames, simplifying data manipulation.

2. **Connection Pooling**:
    - Utilizes a connection pool to manage multiple connections efficiently, improving performance for concurrent operations.

3. **Custom Exception Handling**:
    - Implements a custom exception class for better error management, allowing for clearer debugging and error reporting.

4. **Automatic Table Creation**:
    - Supports automatic creation of tables when writing DataFrames, reducing the need for manual schema management.

5. **Flexible Schema Management**:
    - Easily add new columns to existing tables, making schema evolution straightforward.

6. **Comprehensive Query Support**:
    - Execute any SQL query and retrieve results as a DataFrame, providing flexibility for various data operations.

7. **Compatibility**:
    - Built to work with Snowflake Connector for Python (v2.1.2 or higher) and Pandas (v0.25.2 or higher), ensuring that you have access to the latest features and improvements.

