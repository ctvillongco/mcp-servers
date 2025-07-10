# MCP Weather Server

This MCP server provides tools to get the current weather and a 10-day forecast for a given city using WeatherAPI.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/mcp-weather-server.git
   cd mcp-weather-server
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.8+ and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   - Open the `.weatherapi_key` file.
   - Replace `YOUR_API_KEY_HERE` with your WeatherAPI key.

4. **Run the Server:**
   ```bash
   python -m src.mcp_server_weather
   ```

## Tools

### Get Current Weather
- **Description:** Get current weather for a city.
- **Input Schema:**
  ```json
  {
    "city": "string",
    "country": "string (optional)",
    "units": "string (optional, 'metric', 'imperial', 'both')"
  }
  ```
- **Output Schema:**
  ```json
  {
    "temperature": {"metric": "float", "imperial": "float"},
    "condition": "string",
    "humidity": "int",
    "wind_speed": {"metric": "float", "imperial": "float"}
  }
  ```

### Get 10-Day Forecast
- **Description:** Get a 10-day weather forecast for a city.
- **Input Schema:**
  ```json
  {
    "city": "string",
    "country": "string (optional)",
    "units": "string (optional, 'metric', 'imperial', 'both')"
  }
  ```
- **Output Schema:**
  ```json
  {
    "forecast": [
      {
        "date": "string",
        "condition": "string",
        "temperature": {"metric": {"max": "float", "min": "float"}, "imperial": {"max": "float", "min": "float"}}
      }
    ]
  }
  ```

## Example Usage

- **Get Current Weather:**
  ```bash
  curl -X POST http://localhost:8000/tools/get_current_weather -d '{"city": "San Francisco", "units": "metric"}'
  ```

- **Get 10-Day Forecast:**
  ```bash
  curl -X POST http://localhost:8000/tools/get_forecast -d '{"city": "San Francisco", "units": "both"}'
  ```

## License

This project is licensed under the MIT License.
