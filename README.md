# Lighting Zone Integration

[![hacs][hacsbadge]][hacs] [![releasebadge]][release] [![Build Status][buildstatus-shield]][buildstatus-link] [![License][license-shield]](LICENSE.md)

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

A custom Home Assistant component for creating lighting zones within an area.

## Overview

The Lighting Zone integration allows you to group together light in a zone helper.
You can then use this helper to manipulate the brightness of these lights and gather info about them.

**Why not use a light group?** You might ask...

A light group in Home Assistant treats all the lights in the group as one and the same.
Meaning that all lights in the group will have the exact same color, temperature, and/or brightness.
The Lighting Zone helper does this differently. It allows you to dim all the lights in the zone, leaving their color/temperature alone.

The lighting zone supports two types of dimming through action services:

- **Absolute**: (`lighting_zone.dim_zone_absolute`) setting a certain brightness level to all lights in the zone.
    - *Example*: Calling this service with a dimming value of `50`, will set all the lights to a brightness value of `50`.
- **Relative**: (`lighting_zone.dim_zone_relative`) adjusting all the lights their brightness level relative to their current value.
    - *Example*: Calling this service with a value of `-10`, will decrease every lights brightness by 10. So a light with brightness `70` will go down to `60`. While another light in the zone will go from `50` to `40`.

**But this can be done by just calling the `light.turn_on` service on an area?..**

That's correct, assuming that you have scoped your areas to the lights you want to dim. **For example**: I have an area called *'Living Room'* that I want to scope to the physical Living Room area within my home. But within my living room I have a seating area and a dining area. I want to dim these two areas independently based on presence within them. Here we can create two Lighting Zones for these areas.

### More then just dimming

When you create a Lighting Zone it creates a binary sensor that represents it. This binary sensor will be `on` when any of the lights in the zone are on. And `off` when all lights are of.

The binary sensor entity will have a set of attributes like it's members, the lights that are on, the lights that are off, etc...
These attributes can be used in automation.

**For example:** I have a button on the wall that I want to use for toggling on/off the lights in a specific zone. I can use the state of the binary sensor to determine if the lights are on or off and act accordingly. Or I can use the `members_on` and `members_off` attributes to determine how many lights are on. And then act on that.

## Installation

To get started with the Lighting Zone integration, you'll need to download it through HACS with the button bellow:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rickmoonex&repository=hass-lighting-zone&category=Integration)

Simply download it, reboot, and you're ready to go.

### Manually adding integration through HACS

If the above button does not work for you, you can also add the repo manually:

1. Navigate to HACS -> Click on the three dots at the top right -> 'Custom repositories'
2. In the 'Repository' field, add `https://github.com/rickmoonex/hass-lighting-zone` -> Select the type 'Integration'
3. Now search for the 'Lighting Zone' integration and install it
4. Don't forget to reboot...

> [!NOTE]
> If you don't want to use HACS. You can manually add the integration by downloading the `.zip` file from the releases pages.

## Usage

To set up your first lighting zone:

1. Navigate to 'Settings' -> 'Devices & Services' -> 'Helpers'
2. Click 'Create Helper' and select 'Lighting Zone'
3. Give your zone a name and select the lights to be a member of the zone

Their you go, you've now created you first lighting zone.

Happy tinkering!

## Support

If you find this project helpful and want to support its development, consider buying me a coffee!
[![Buy Me a Coffee][buymecoffeebadge]][buymecoffee]

---

[buymecoffee]: https://www.buymeacoffee.com/rickmoonenk
[buymecoffeebadge]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
[license-shield]: https://img.shields.io/github/license/rickmoonex/hass-lighting-zone.svg?style=for-the-badge
[hacs]: https://github.com/rickmoonex/hass-lighting-zone
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[release]: https://github.com/rickmoonex/hass-lighting-zone/releases
[releasebadge]: https://img.shields.io/github/v/release/rickmoonex/hass-lighting-zone?style=for-the-badge
[buildstatus-shield]: https://img.shields.io/github/actions/workflow/status/rickmoonex/hass-lighting-zone/push.yml?branch=main&style=for-the-badge
[buildstatus-link]: https://github.com/rickmoonex/hass-lighting-zone/actions