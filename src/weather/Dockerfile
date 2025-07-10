# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY src /app/src
COPY .weatherapi_key /app/.weatherapi_key

# Expose port if needed (adjust if your MCP server listens on a specific port)
# EXPOSE 8000

# Command to run the MCP weather server
CMD ["python", "-m", "src.mcp_server_weather"]
