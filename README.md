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

## Sample widget

![HA_Dynamic_chrg](https://github.com/user-attachments/assets/89e2377f-a555-4bf0-9a7f-62300869adef)

You can create a widget and let it show only when the cable is locked in the charger station. Sample yaml code

```yaml
- type: entities
        entities:
          - entity: input_boolean.cheap_charging
            name: Goedkoop tarief
            secondary_info: last-changed
          - entity: sensor.tesla_battery_level
            secondary_info: last-updated
            name: Batterijniveau Auto
          - entity: binary_sensor.supercharger_cable_locked
            name: Kabel in laadpaal
            secondary_info: last-updated
          - entity: input_number.minimaal_ev_batterij
            secondary_info: none
            name: Minimale acculading
          - entity: input_boolean.smartcharging
            name: Smartcharging
          - entity: sensor.supercharger_dynamic_charger_limit
            name: Amperage laadstation
          - entity: sensor.energyzero_today_energy_lowest_price_time
            name: Tijd tot laagste prijs
            secondary_info: none
          - entity: sensor.energyzero_today_energy_highest_price_time
            name: Tijd tot hoogste prijs
        title: Dynamisch Laadoverzicht
        show_header_toggle: true
        visibility:
          - condition: state
            entity: binary_sensor.supercharger_cable_locked
            state: 'off'
````

### Notes

I am still testing this and will update the scripts if needed. As always YMMV.



