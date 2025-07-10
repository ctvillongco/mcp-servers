# Project Brief: MCP Weather Server

This project implements an MCP server that provides current weather and 10-day forecast data for a given city using the WeatherAPI service. The server exposes two main tools: `get_current_weather` and `get_forecast`, each accepting city, optional country, and units parameters.

The server is designed to be containerized with Docker for easy deployment and integration with MCP clients. It securely manages the WeatherAPI key via environment variables or configuration files.

Key goals:
- Provide accurate, up-to-date weather information via MCP protocol.
- Support metric, imperial, or both units.
- Ensure robust error handling and input validation.
- Facilitate easy deployment with Docker.
- Include comprehensive testing and documentation.

This brief serves as the foundation for all other memory bank files and ongoing development.
