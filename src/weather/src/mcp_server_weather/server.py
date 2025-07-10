from enum import Enum
import requests
from pydantic import BaseModel
from typing import List, Dict, Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp.shared.exceptions import McpError

# Enum for tool names
class WeatherTools(str, Enum):
    GET_CURRENT_WEATHER = "get_current_weather"
    GET_FORECAST = "get_forecast"

# Input schema for weather requests
class WeatherInput(BaseModel):
    city: str
    country: str = None
    units: str = "both"  # Options: "metric", "imperial", "both"

# Output schema for current weather
class CurrentWeatherResult(BaseModel):
    temperature: Dict[str, float]
    condition: str
    humidity: int
    wind_speed: Dict[str, float]

# Output schema for forecast
class ForecastResult(BaseModel):
    forecast: List[Dict[str, Any]]

# Weather server logic
import os

class WeatherServer:
    def __init__(self, api_key: str | None = None):
        if api_key is None:
            api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API key must be provided via constructor or API_KEY environment variable")
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"

    def get_current_weather(self, city: str, country: str, units: str) -> CurrentWeatherResult:
        """Get current weather for a city."""
        query = f"{city},{country}" if country else city
        url = f"{self.base_url}/current.json?key={self.api_key}&q={query}"
        print(f"Requesting URL: {url}")
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        if response.status_code != 200:
            raise McpError(f"WeatherAPI request failed with status {response.status_code}: {response.text}")
        data = response.json()

        if "error" in data:
            error_message = data["error"]
            if isinstance(error_message, dict) and "message" in error_message:
                raise McpError(error_message["message"])
            else:
                raise McpError(str(error_message))

        temperature = {
            "metric": data["current"]["temp_c"],
            "imperial": data["current"]["temp_f"]
        }
        wind_speed = {
            "metric": data["current"]["wind_kph"],
            "imperial": data["current"]["wind_mph"]
        }

        return CurrentWeatherResult(
            temperature=temperature if units == "both" else {units: temperature[units]},
            condition=data["current"]["condition"]["text"],
            humidity=data["current"]["humidity"],
            wind_speed=wind_speed if units == "both" else {units: wind_speed[units]}
        )

    def get_forecast(self, city: str, country: str, units: str) -> ForecastResult:
        """Get 10-day weather forecast for a city."""
        query = f"{city},{country}" if country else city
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={query}&days=10"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            raise McpError(data["error"]["message"])

        forecast = []
        for day in data["forecast"]["forecastday"]:
            day_forecast = {
                "date": day["date"],
                "condition": day["day"]["condition"]["text"],
                "temperature": {
                    "metric": {"max": day["day"]["maxtemp_c"], "min": day["day"]["mintemp_c"]},
                    "imperial": {"max": day["day"]["maxtemp_f"], "min": day["day"]["mintemp_f"]}
                }
            }
            forecast.append(day_forecast)

        return ForecastResult(
            forecast=forecast if units == "both" else [
                {
                    "date": f["date"],
                    "condition": f["condition"],
                    "temperature": f["temperature"][units]
                } for f in forecast
            ]
        )

async def serve() -> None:
    server = Server("mcp-weather")
    weather_server = WeatherServer(api_key="YOUR_API_KEY_HERE")  # Placeholder for API key

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available weather tools."""
        return [
            Tool(
                name=WeatherTools.GET_CURRENT_WEATHER.value,
                description="Get current weather for a city",
                inputSchema=WeatherInput.model_json_schema(),
            ),
            Tool(
                name=WeatherTools.GET_FORECAST.value,
                description="Get 10-day weather forecast for a city",
                inputSchema=WeatherInput.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        """Handle tool calls for weather queries."""
        print(f"call_tool invoked with name={name} arguments={arguments}")
        try:
            input_data = WeatherInput(**arguments)
            if name == WeatherTools.GET_CURRENT_WEATHER.value:
                result = weather_server.get_current_weather(
                    input_data.city, input_data.country, input_data.units
                )
            elif name == WeatherTools.GET_FORECAST.value:
                result = weather_server.get_forecast(
                    input_data.city, input_data.country, input_data.units
                )
            else:
                raise ValueError(f"Unknown tool: {name}")

            print(f"call_tool result: {result}")
            return [TextContent(type="text", text=result.json(indent=2))]

        except Exception as e:
            print(f"call_tool error: {e}")
            raise ValueError(f"Error processing weather query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
