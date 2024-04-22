# μWeatherStation :partly_sunny:

The student project operated within the Bachelor's program Communications systems for IoT at Brno University of Technology.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started


In the development of our IoT project, we have leveraged two technologies that ensure both efficiency and reliability in communication: Message Queuing Telemetry Transport (MQTT) and Narrowband IoT (NB-IoT). MQTT is a lightweight messaging protocol designed for use in situations where bandwidth and power are at a premium, making it an excellent choice for IoT applications. It operates on top of the TCP/IP protocol, allowing for efficient communication between devices in a publish/subscribe model.

On the other hand, Narrowband IoT (NB-IoT) is a standards-based low power wide area (LPWA) technology developed to enable a wide range of new IoT devices and services. NB-IoT significantly improves the power consumption of user devices, system capacity, and spectrum efficiency, especially in deep coverage.

The combination of MQTT and NB-IoT in our project ensures that our IoT solutions are not only energy efficient but also capable of operating in remote or hard-to-reach areas, making it an ideal choice for a wide variety of IoT applications, such as our deployment on old meteorological poles with a height of over 10 meters above ground.


### Block Diagram Solution


![MicroWeatherStation](https://github.com/vanekroman/MicroWeatherStation/blob/main/meteostanice.png)


### Calculations

Energy consumed per one message transmission
$E_{m s g}=\left(P_{t x} \cdot t_{t x}\right)+\left(P_{r x} \cdot t_{r x}\right)+\left(P_{\text {idle }} \cdot t_{\text {idle }}\right)[J]$

Energy consumed per day:
$E_{\text {day }}=E_{\text {msg }} \cdot N_{M T C P D}+\left(P_S+P_{\text {dev }}\right) \cdot 86400[\mathrm{~J}]$

### Dependencies

Software is written to run on RP2040 with UF2 bootloader flashed in. Aditional mudules are used as a
hardware:
* [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
* [Maker Pi Pico Base](https://www.cytron.io/p-maker-pi-pico-base)
* [Grove - LoRa-E5](https://wiki.seeedstudio.com/Grove_LoRa_E5_New_Version)
* [Grove - AHT20](https://wiki.seeedstudio.com/Grove-AHT20-I2C-Industrial-Grade-Temperature&Humidity-Sensor)

### Suggested toolchain

VSCODE + [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) extension.

## Help

Can´t run μPython on RP2040?\
  Check the μPython interpreter instalation [UF2 bootloader](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

## Authors

Contributors names and contact info

  [@vanekroman](https://github.com/vanekroman)
  Filip Tůma
  [Tomáš Calábek](https://github.com/siberiacaly)
  [Matěj Baranyk](https://github.com/baranykmatej)

<a href="https://github.com/vanekroman/MicroWeatherStation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=vanekroman/MicroWeatherStation" />
</a>

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* Readme starting template by [@DomPizzie](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* Contributors images made with [contrib.rocks](https://contrib.rocks).
