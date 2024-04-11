# μWeatherStation :partly_sunny:

The student project operated within the Bachelor's program Communications systems for IoT at Brno University of Technology.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

In the development of our IoT project, we have leveraged two technologies that ensure both efficiency and reliability in communication: Constrained Application Protocol (CoAP) and Narrowband IoT (NB-IoT). CoAP is a web transfer protocol optimized for use with constrained nodes and networks, offering a simple but powerful interface for interactions between IoT devices over the Internet. It is designed to easily translate to HTTP for simplified integration with the web while also providing a lightweight communication mechanism that conserves both power and bandwidth. On the other hand, Narrowband IoT (NB-IoT) is a standards-based low power wide area (LPWA) technology developed to enable a wide range of new IoT devices and services. NB-IoT significantly improves the power consumption of user devices, system capacity, and spectrum efficiency, especially in deep coverage. The combination of CoAP and NB-IoT in our project ensures that our IoT solutions are not only energy efficient but also capable of operating in remote or hard-to-reach areas, making it an ideal choice for a wide variety of IoT applications as in our case on old meteorological pole with the height above 10 metres above ground. 

### Block Diagram Solution

[[https://github.com/vanekroman/MicroWeatherStation/meteostanica.png|alt=meteostanica]]


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
