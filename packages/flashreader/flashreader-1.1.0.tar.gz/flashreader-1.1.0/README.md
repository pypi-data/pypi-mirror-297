# Python Flash Reader
Flash Reader allows to read and/or write any EEPROM or Flash memory via SPI or I2C.
This library is particularly useful in case of reverse engineering or prototyping for embedded systems (RPI, etc..).

```
from flashreader.memory import spiflash, m95, mx25, w25q, _24lc, _25lc, _25aa
from flashreader.platform import ft232h, raspberrypi

with ft232h.Platform() as platform: #Open FT232H adapter
    with spiflash.Memory(platform) as memory: #Open generic SPI flash
        print(f"Writing hello world @0x0000...")
        memory.write(0x0000, b'Hello World')

        buf = bytearray(memory.read(0x00000000, 11))
        print(f"Read @0x0000: {buf}")
```

## Supported platform
- [x] Raspberry pi 4
- [x] FT232H ([Adafruit](https://www.adafruit.com/product/2264))

## Support memory
- [x] Various spi serial flash
- [x] Macronix mx25R..., mx25L...
- [x] Microchip 25aa..., 25lc...
- [x] Winbond w25q...
- [x] Microchip 24lc...
- [x] ST m95...

## Quick start (Raspberry pi 4)
### Setup Raspbian

```
apt-get install python3 python3-pip python3-spidev python3-monotonic
sudo raspi-config
```
- Go to "Interfacing Options" > "SPI" > "Enable"
- Reboot the RPI

### Wiring
- **SPI:** PIN19(MOSI), PIN21(MISO), PIN23(SCK), PIN11(CS)
- **I2C:** PIN3(SDA), PIN5(SCL)

## Quick start (Windows)
### Setup Windows
- Plug FT232H
- Use Zadig (https://zadig.akeo.ie/), select the USB device in the list, select libusb-win32 and replace the driver (DO NOT USE WINUSB or any other driver).

### Wiring
- **SPI:** D0(SCK), D1(MOSI), D2(MISO), D3(CS)
- **I2C:** D0(SCL), D1(SDA)

## Run
Read spi flash (By using generic driver: spiflash)

`python -m flashreader --platform raspberrypi --memory spiflash --read ./dump.bin --offset 0`

Write spi flash (By using generic driver: spiflash)

`python -m flashreader --platform raspberrypi --memory spiflash --write ./dump.bin --offset 0`

