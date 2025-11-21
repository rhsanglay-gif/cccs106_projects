# main.py
"""Enhanced Weather Application with Dark Mode and Smart Features using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config
import random

# -------------------------
# Weather Trivia / Facts
# -------------------------
WEATHER_TRIVIA = [
    "The highest temperature ever recorded on Earth was 56.7°C in Death Valley, USA.",
    "Snowflakes can take up to an hour to fall to the ground.",
    "Lightning strikes the Earth about 100 times per second.",
    "The fastest wind recorded on Earth was 408 km/h during a cyclone.",
    "Rain contains vitamin B12 from soil bacteria."
]

def get_weather_trivia():
    return random.choice(WEATHER_TRIVIA)


# Calendar Event Suggestions
def suggest_calendar_event(weather_main):
    if "rain" in weather_main:
        return "☔ Reminder: Take an umbrella if you're going out today!"
    elif "clear" in weather_main:
        return "🌞 Great day for an outdoor activity or picnic!"
    elif "snow" in weather_main:
        return "❄️ Remember to dress warmly and check road conditions!"
    else:
        return "📅 Plan your day accordingly!"

# Weather-Based Music Recommendations
def recommend_music(weather_main):
    if "rain" in weather_main:
        return "🎵 Recommended Playlist: Rainy Day Jazz"
    elif "clear" in weather_main:
        return "🎵 Recommended Playlist: Sunny Pop Hits"
    elif "snow" in weather_main:
        return "🎵 Recommended Playlist: Cozy Winter Acoustic"
    elif "cloud" in weather_main:
        return "🎵 Recommended Playlist: Chill Lo-Fi Beats"
    else:
        return "🎵 Recommended Playlist: Mood Booster Hits"


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()

    def build_ui(self):
        """Build the user interface."""
        # App title
        self.title = ft.Text(
            "Weather App",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_800,
        )

        # Dark Mode toggle button
        self.dark_mode_toggle = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            on_click=self.toggle_dark_mode,
            tooltip="Toggle Dark Mode",
        )

        # City input
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            width=300,
        )

        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=15),
            ),
        )

        # Weather card (hidden initially)
        self.weather_container = ft.Container(
            visible=False,
            padding=25,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                color=ft.Colors.GREY_400,
                blur_radius=15,
                offset=ft.Offset(5, 5),
            ),
        )

        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_500,
            visible=False,
        )

        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)

        # Page layout
        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [self.title, self.dark_mode_toggle],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.city_input,
                    self.search_button,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            )
        )

    def toggle_dark_mode(self, e):
        """Toggle between light and dark mode."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.dark_mode_toggle.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.dark_mode_toggle.icon = ft.Icons.DARK_MODE
        self.page.update()

    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)

    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()

        if not city:
            self.show_error("Please enter a city name")
            return

        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()

        try:
            weather_data = await self.weather_service.get_weather(city)
            self.display_weather(weather_data)
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()

    def display_weather(self, data: dict):
        """Display weather information with enhanced UI and extra features."""
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)

        weather_main = data.get("weather", [{}])[0].get("main", "").lower()

        # Gradient background based on weather
        if "cloud" in weather_main:
            self.page.bgcolor = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.GREY_200, ft.Colors.GREY_400],
            )
        elif "rain" in weather_main:
            self.page.bgcolor = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.BLUE_200, ft.Colors.BLUE_400],
            )
        elif "snow" in weather_main:
            self.page.bgcolor = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.WHITE, ft.Colors.GREY_100],
            )
        elif "clear" in weather_main:
            self.page.bgcolor = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.YELLOW_100, ft.Colors.YELLOW_300],
            )
        else:
            self.page.bgcolor = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.LIGHT_BLUE_50, ft.Colors.LIGHT_BLUE_200],
            )
        self.page.update()

        # Weather card content
        weather_content = ft.Column(
            [
                ft.Text(f"{city_name}, {country}", size=28, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=120,
                            height=120,
                        ),
                        ft.Text(description, size=22, italic=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(f"{temp:.1f}°C", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                ft.Text(f"Feels like {feels_like:.1f}°C", size=18, color=ft.Colors.GREY_700),
                ft.Divider(),
                ft.Row(
                    [
                        self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%"),
                        self.create_info_card(ft.Icons.AIR, "Wind Speed", f"{wind_speed} m/s"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text(f"💡 Trivia: {get_weather_trivia()}", size=14, italic=True, color=ft.Colors.GREY_400),
                ft.Text(suggest_calendar_event(weather_main), size=14, color=ft.Colors.BLUE_700),
                ft.Text(recommend_music(weather_main), size=14, color=ft.Colors.GREEN_700),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        self.weather_container.content = weather_content
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()

    def create_info_card(self, icon, label, value):
        """Create info cards with enhanced design."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_400),
                    ft.Text(label, size=12, color=ft.Colors.GREY_400),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            width=160,
            shadow=ft.BoxShadow(color=ft.Colors.GREY_300, blur_radius=10, offset=ft.Offset(3, 3)),
        )

    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)