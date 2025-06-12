import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime
import pytz

class CheapEnergyControl(hass.Hass):
    def initialize(self):
        # Run every hour
        self.run_every(self.check_energy_prices, "now", 60*60)
        # Also run when energy prices are updated
        self.listen_state(self.energy_prices_changed, "sensor.energy_prices_today")
        
        # Get and store timezone information at initialization
        try:
            # Try to get timezone from AppDaemon configuration
            self.timezone_str = self.get_plugin_config()["time_zone"]
        except (KeyError, TypeError):
            # Fallback to a default timezone if not available
            self.timezone_str = "Europe/Amsterdam"  # Replace with your default timezone
            self.log(f"Timezone not found in config, using default: {self.timezone_str}", level="WARNING")

    def energy_prices_changed(self, entity, attribute, old, new, kwargs):
        self.check_energy_prices(kwargs)

    def check_energy_prices(self, kwargs):
        self.log("Checking energy prices")

        # Get current time in local timezone using stored timezone
        now = datetime.now(pytz.timezone(self.timezone_str))
        current_hour = now.replace(minute=0, second=0, microsecond=0)

        # Get energy prices
        try:
            prices = self.get_state("sensor.energy_prices_today", attribute="prices")

            if not prices:
                self.log("No price data available")
                return

            # Sort by price
            sorted_prices = sorted(prices, key=lambda x: float(x["price"]))
            # Get 6 cheapest
            cheapest_6 = sorted_prices[:6]

            # Check if current hour is among the cheapest
            is_cheap_now = False
            for price_data in cheapest_6:
                # Parse timestamp
                timestamp_str = price_data["timestamp"]
                try:
                    # Parse UTC timestamp with timezone offset
                    price_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S%z")
                    # Convert to local time
                    price_time_local = price_time.astimezone(pytz.timezone(self.timezone_str))
                    # Get just the hour
                    price_hour = price_time_local.replace(minute=0, second=0, microsecond=0)

                    if price_hour == current_hour:
                        is_cheap_now = True
                        break
                except Exception as e:
                    self.log(f"Error parsing timestamp {timestamp_str}: {e}", level="ERROR")

            # Set the switch state
            if is_cheap_now:
                self.log("Current hour is among the 6 cheapest, turning ON cheap charging")
                self.turn_on("input_boolean.cheap_charging")
            else:
                self.log("Current hour is not among the 6 cheapest, turning OFF cheap charging")
                self.turn_off("input_boolean.cheap_charging")

        except Exception as e:
            self.log(f"Error processing energy prices: {e}", level="ERROR")
