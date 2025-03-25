# Tech Context

## Technologies Used
- **Python**: Primary programming language for MCP server development.
- **MCP SDK**: Framework for building MCP servers and tools.
- **ML Alpha APIs**: RESTful APIs for accessing stock data, financial metrics, and SEC reports.

## Development Setup
- **Environment**: macOS
- **Python Version**: Specified in `.python-version` file.
- **Dependencies**: Managed using `pyproject.toml` and `uv.lock`.

## Technical Constraints
- **API Rate Limits**: Ensure compliance with ML Alpha API usage policies.
- **Data Security**: Protect sensitive financial data during transmission and storage.
- **Scalability**: Design tools to handle large-scale data requests efficiently.

## Dependencies
- **MCP SDK**: Provides core functionality for MCP server development.
- **Requests Library**: For HTTP communication with ML Alpha APIs.
- **Other Python Libraries**: As specified in `pyproject.toml`.
