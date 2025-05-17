# Homeassistant Smart Charging using Easee EV Charger

A bunch of automations that allows you to do smart charging. This is useful is you have an energy contract that has dynamic prices during the day. I live in The Netherlands where you can get such a contract, prices change every hour. Each day around 15.00 we will get the new prices for the next day. This is usually based of the Day Ahead prices.

## Requirements

* Homeassistant
* An Easee Charger and the addon (via HACS): https://github.com/nordicopen/easee_hass
* The EnergyZero intergration: https://www.home-assistant.io/integrations/energyzero
* The Addon AppDaemon: https://github.com/hassio-addons/addon-appdaemon/releases

* Optional: sensor with SoC for EV
* Optional: at least one device connected to Home Assistant to receive notifications

For information about HACS, see https://hacs.xyz/docs/use/

## Installation

**Before installing, always make a backup!!**

Install the Easee integration from HACS and the Energyzero integration from Home Assistant, then install the Addon AppDaemon. Restart Homeassistant

### AppDaemin

Put the two files for Appdaemon in your addon folder. It should be in /addon_configs/(random string)_appdaemon/apps/

**Note** If you're already using AppDaemon, please add the 3 lines below your existing config!

### Packages

Install the template sensor by moving the packages directory to your /config (so you will end up with /config/packages/...)

### Input helpers

Define input helpers. You'll find those in Settings -> Integrations -> Helpers

* Input Boolean: Cheap Charging
* Input Boolean: Smart Charging

Add a 'toggle' which will be an input_boolean.

### Automations

Add the automations to your system by adding them to automations.yaml.

**NOTE**: Replace your car battery sensor by one you have. If you don't have a car battery sensor, disable this part in the automation!

### TODO

* Make it possible to set a min_price so when we calculate we will stay at or under this price.



