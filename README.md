# ansible-role-homeassistant-frigate

An [Ansible](https://www.ansible.com/) role that provisions
[Home Assistant](https://www.home-assistant.io/),
[Frigate](https://github.com/blakeblackshear/frigate), and
[Mosquitto](https://mosquitto.org/)
[Docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/) containers.

[![homeassistant](https://github.com/andornaut/homeassistant-ibm1970-theme/blob/main/screenshots/light-colors-small.png)](https://github.com/andornaut/homeassistant-ibm1970-theme/blob/main/screenshots/light-colors-small.png)
[![frigate](./screenshots/frigate-small.png)](./screenshots/frigate.png)

## Configuration

* [Default Ansible variables](./defaults/main.yml)

### Home Assistant

* [Example automation.yaml](./examples/homeassistant/automations.yaml)
* [Example configuration.yaml](./examples/homeassistant/configuration.yaml)

Test configuration
```
docker exec homeassistant hass --config /config --script check_config
docker exec homeassistant hass --config /config --script check_config --secrets
```

### Frigate

* [Example config.yml](./examples/frigate/config.yml)
* [GitHub issue #311](https://github.com/blakeblackshear/frigate/issues/311)

#### Optimizing performance

* [Optimization documentation](https://blakeblackshear.github.io/frigate/configuration/optimizing/)
* [GitHub issue #1607](https://github.com/blakeblackshear/frigate/issues/1607)

##### Gathering information
```
$ vainfo --display drm --device /dev/dri/renderD128
$ ffmpeg -decoders | grep qsv
$ ffmpeg -hwaccels
```

##### AMD GPU
```
# Frigate config.yml
ffmpeg:
  hwaccel_args:
    - -hwaccel
    - vaapi
    - -hwaccel_device
    - /dev/dri/renderD128

# Ansible variables
homeassistant_frigate_env:
    LIBVA_DRIVER_NAME: radeonsi

# Test with:
docker exec frigate bash -c \
    'ffmpeg -hwaccel vaapi -vaapi_device /dev/dri/renderD128 -i $(find /media/frigate -iname '*.mp4' -print -quit 2>/dev/null) /tmp/output.mp4'
```

##### Intel CPU

```
# Frigate config.yml
ffmpeg:
  hwaccel_args:
    - -hwaccel
    - qsv
    - -qsv_device
    - /dev/dri/renderD128

# Ansible variables
homeassistant_frigate_env:
    LIBVA_DRIVER_NAME: i965

# Test with:
docker exec frigate bash -c \
    'ffmpeg -hwaccel qsv -qsv_device /dev/dri/renderD128 -i $(find /media/frigate -iname '*.mp4' -print -quit 2>/dev/null) /tmp/output.mp4'

# Monitor GPU usage
sudo apt install intel-gpu-tools radeontop

sudo intel_gpu_top
sudo radeontop
```

##### Common
```
# Frigate config.yml
ffmpeg:
  input_args:
    - -avoid_negative_ts
    - make_zero
    - -fflags
    - nobuffer
    - -flags
    - low_delay
    - -strict
    - experimental
    - -fflags
    - +genpts+discardcorrupt
    - -use_wallclock_as_timestamps
    - "1"
```

### Nginx

[ansible-role-letsencrypt-nginx](https://github.com/andornaut/ansible-role-letsencrypt-nginx) variables:

```
# Given:
#homeassistant_port: 8080
#homeassistant_frigate_port: 8081

letsencryptnginx_websites:
  - domain: ha.example.com
    proxy_port: 8080
    websocket_path: /api/websocket
  - domain: frigate.example.com
    proxy_port: 8081
    websocket_enabled: true
```

## HACS installation

* [Documentation](https://hacs.xyz/docs/setup/download):

```
docker exec -ti homeassistant \
    bash -c 'wget -O - https://get.hacs.xyz | bash -'
```

## Troubleshooting

### Neato reauthorization

* [Neato configuration](https://www.home-assistant.io/integrations/neato/#configuration)
* [Home Assistant forums](https://community.home-assistant.io/t/neato-integration-needs-to-be-reconfigured-after-updating-ha-from-2020-12-1-to-2021-1-1/266345/22)

The Neato integration can sometimes report this error:

> Failed to set up: Token not valid, trigger renewal

When this occurs, click the "Reconfigure" button in Home Assistant `/config/integrations`,
which will start a new authorization flow with Neato.
The reauthorization flow may trigger this error:

> The redirect uri included is not valid.

If that occurs, then ensure that the "Redirect URI" of the "application" configured in
[the Neato developers portal](https://developers.neatorobotics.com/applications)
points to `https://my.home-assistant.io/redirect/oauth`,
and ensure that [https://my.home-assistant.io/](https://my.home-assistant.io/)
is configured to point to your Home Assistant `external_url`,
which you can do by [navigating to it](https://my.home-assistant.io/) and submitting the form.

n.b. If you've deleted and re-created a new "application" in the Neato developer portal,
then be sure to update the client_id and client_secret in `secrets.yaml`.

### Upgrade, downgrade or pin a component's dependencies

Eg. Pin [pyenvisalink](https://github.com/Cinntax/pyenvisalink)
to version 4.0 to workaround
[this issue](https://github.com/home-assistant/core/issues/65762#issuecomment-1030872475).

```
docker exec -ti homeassistant \
    bash -c "find /usr/src/homeassistant/ \
    -name 'requirements*.txt' -or -name manifest.json \
    | xargs grep -l pyenvisalink \
    | xargs sed -i 's/pyenvisalink==[a-zA-Z0-9.]\+/pyenvisalink==4.0/g'"
```

## Links

* [BurningStone91's smart home setup](https://github.com/Burningstone91/smart-home-setup/)
* [Eclipse Mosquitto](https://mosquitto.org/) - MQTT message broker
* [FFmpeg QuickSync](https://trac.ffmpeg.org/wiki/Hardware/QuickSync)
* [FFmpeg VAAPI](https://trac.ffmpeg.org/wiki/Hardware/VAAPI)
* [Frigate](https://github.com/blakeblackshear/frigate) - NVR with realtime local object detection for IP cameras
* [Frigate lovelace card](https://github.com/dermotduffy/frigate-hass-card)
* [Frigate machine learning accelerator by Coral](https://coral.ai/products/)
* [Frigate mobile app notifications blueprint](https://community.home-assistant.io/t/frigate-mobile-app-notifications/311091)
* [Home Assistant automation trigger variables](https://www.home-assistant.io/docs/automation/templating/)
* [Home Assistant script syntax](https://www.home-assistant.io/docs/scripts/)
* [IBM1970 theme](https://github.com/andornaut/homeassistant-ibm1970-theme)
* [Material icons](https://materialdesignicons.com/) - Customize Home Assistant icons. Prefix with "mdi:".
* [Slider Entity Row card](https://github.com/thomasloven/lovelace-slider-entity-row)

### Integrations

* [Amcrest](https://www.home-assistant.io/integrations/amcrest/)
* [Denon AVR](https://www.home-assistant.io/integrations/denonavr/)
* [Ecobee](https://www.home-assistant.io/integrations/ecobee/)
* [Elgato Light](https://www.home-assistant.io/integrations/elgato/)
* [Envisalink](https://www.home-assistant.io/integrations/envisalink/)
* [Foscam](https://www.home-assistant.io/integrations/foscam/)
* [Frigate](https://github.com/blakeblackshear/frigate-hass-integration)
* [Google Cast](https://www.home-assistant.io/integrations/cast/)
* [HomeKit](https://www.home-assistant.io/integrations/homekit/)
* [Meross / Refoss](https://github.com/albertogeniola/meross-homeassistant)
* [Neato](https://www.home-assistant.io/integrations/neato/)
* [Roomba](https://www.home-assistant.io/integrations/roomba/)
  * [SDK](https://github.com/koalazak/dorita980)
* [Ruckus Unleashed](https://www.home-assistant.io/integrations/denonavr/)
