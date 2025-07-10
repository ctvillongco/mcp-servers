import unittest
from unittest.mock import patch
from src.mcp_server_weather.server import WeatherServer, CurrentWeatherResult, ForecastResult

class TestWeatherServer(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.weather_server = WeatherServer(api_key=self.api_key)

    @patch('src.mcp_server_weather.server.requests.get')
    def test_get_current_weather(self, mock_get):
        mock_response = {
            "current": {
                "temp_c": 20.0,
                "temp_f": 68.0,
                "condition": {"text": "Sunny"},
                "humidity": 50,
                "wind_kph": 15.0,
                "wind_mph": 9.3
            }
        }
        mock_get.return_value.json.return_value = mock_response

        result = self.weather_server.get_current_weather("San Francisco", None, "both")
        expected = CurrentWeatherResult(
            temperature={"metric": 20.0, "imperial": 68.0},
            condition="Sunny",
            humidity=50,
            wind_speed={"metric": 15.0, "imperial": 9.3}
        )
        self.assertEqual(result, expected)

    @patch('src.mcp_server_weather.server.requests.get')
    def test_get_forecast(self, mock_get):
        mock_response = {
            "forecast": {
                "forecastday": [
                    {
                        "date": "2025-07-10",
                        "day": {
                            "maxtemp_c": 25.0,
                            "mintemp_c": 15.0,
                            "maxtemp_f": 77.0,
                            "mintemp_f": 59.0,
                            "condition": {"text": "Partly cloudy"}
                        }
                    }
                ]
            }
        }
        mock_get.return_value.json.return_value = mock_response

        result = self.weather_server.get_forecast("San Francisco", None, "both")
        expected = ForecastResult(
            forecast=[
                {
                    "date": "2025-07-10",
                    "condition": "Partly cloudy",
                    "temperature": {
                        "metric": {"max": 25.0, "min": 15.0},
                        "imperial": {"max": 77.0, "min": 59.0}
                    }
                }
            ]
        )
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
