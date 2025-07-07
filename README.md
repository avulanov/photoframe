# Photoframe

Tools for eink photoframe

## Intro
Currently, we use the following devices both based off eink tech
* Waveshare Photopainter: https://www.waveshare.com/photopainter.htm
    * Tech: ACeP (aka Gallery)
    * 7-color: black, white, red, green, blue, yellow, orange
    * Specs: https://files.waveshare.com/upload/d/db/7.3inch_e-Paper_%28F%29_Specification.pdf
* Philips Tableaux 13BDL4150IW https://www.ppds.com/en-us/display-solutions/digital-signage/philips-tableaux/13bdl4150iw-00
    * Tech: Spectra 6 (new gen)
    * Specs: https://www.datocms-assets.com/112519/1726686611-13bdl4150iw_00_2023-12-14_10h05m09s-pdf.pdf
    * It does not state how many colors it has, but based on inspection it has 8: black, white, red, green, blue, light blue, magenta, yellow
* Waveshare Photopainter-B: https://www.waveshare.com/photopainter-b.htm
    * Tech: Spectra 6 (new gen)
    * 6-color: black, white, red, green, blue, yellow

## Understanding color gamut
* 7 colors is too few to display a photo. Dithering technique is used to propagate the error to neighboring pixels. https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

## Ways to improve image quality
TLDR;
* Waveshare (both ACeP and Spectra 6): color saturation 2.0
* Waveshare (ACeP): use 6 colors w/o orange.
* Waveshare (Spectra 6): use 5 colors w/o yellow
* Philips (Spectra 6): original image
 
* Image enhance
    * Using tools from https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html
    * Color saturation seems to provide visually better images when displayed on the e-ink probably due to low contrast of the screen.
    * Brightness, contrast, sharpening introduces visual artifacts.
    * Denoising introduces blurring.
* Dithering
    * More algos: https://github.com/hbldh/hitherdither. Did not see much difference, maybe Atkinson lossy dithering gives marginal impact.
    * Gamma-aware: https://www.nayuki.io/page/gamma-aware-image-dithering. Human eye can distinguish shades of darker colors better. Tried in by adding conversion to linear color space to the code with multiple dithering algorithms. Did not see much difference probably due to low number of colors. `lnr = rgb / 255... lnr = np.where(lnr <= 0.04045, lnr / 12.92, ((lnr +  0.055) / 1.055)**2.4)`
* Less colors
    * ACeP: Using 6 colors (w/o orange) seems to visually look better. Orange seems to be used a lot by dithering algorithm since it falls "between" main colors. Also, new e-ink Spectra 6 screen uses only 6 colors too. Using 5 colors (w/o orange and yellow) is worse. Yellow is one of the main colors in CMY.
    * Spectra 6: Using 5 colors (w/o yellow) is better. Yellow causes skewness in dithering due to relation to a CMYK color space (vs RGB) 
* More colors
    * ACeP and Spectra 6. Use custom waveform to force eink produce more colors. Discussed in a dedicated section.
    * Philips seems to be able to use 8 base colors.

## More colors
* Use custom waveform to force eink produce more colors. Especially, we want to get the remaining from CMY - cyan (for the blue sky) and magenta. But also, equally spaced colors in between to avoid biasing we saw for orange.
* Great explanation about waveform and their usage in EPD can be found in https://hackaday.io/project/179058-understanding-acep-tecnology and https://github.com/Modos-Labs/Glider.
* EPD has a lookup table (LUT) with color as a key and a list of voltage impulses as a value (+/- and value). It takes Z frames to refresh the screen. The i-th impulse is applied at the i-th frame to a target pixel. Physically, eink particles of certain color move to front depending on the charge sign. Also, some particles move faster than the others due to their size. This gives the final visible color.
* There are 5 particle colors: BWCMY. The waveform LUT is designed to show 7 colors: BWRGBYO. Interestingly, it does not have Cyan or Magenta.
* LUT is stored in IC driver flash. IC driver is connected directly to the screen and via SPI interface to the driving board.
* IC driver has an API exposed to the driving board and can issue commands such as init the screen, show a picture, or sleep etc. EPD producer does not provide neither IC API specification nor IC model. Though EPD producer provide example code how to use the API. For example, panel setting (PSR) for [5.65 ACeP](https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/c/lib/e-Paper/EPD_5in65f.c) looks as follows:
```
    EPD_5IN65F_SendCommand(0x00);
    EPD_5IN65F_SendData(0xEF);
    EPD_5IN65F_SendData(0x08);
```
* IC drivers have capability to use LUT from the IC registers. So, in order to use custom LUT, one needs the following info:
    * (1) The command to enable loading LUT from IC registers.
    * (2) The list (addresses) of IC registers.
    * (3) Stock LUT, or an example of a waveform, to be able to experiment with its customization.
* For example, https://hackaday.io/project/179058-understanding-acep-tecnology explains that 5.65 ACeP display uses SPD1656 display driver, which has a pdf with specification, which explains which bit parameter to set to enable custom LUT (LUT_EN or LUT_SEL) during panel setting, the addresses of the registers for LUT, and the size of the content. They also were able to get the original LUT by some soldering and reading back the LUT flash. Code can be found in https://github.com/ts-manuel/Understanding-ACeP-Tecnology/tree/master. There is another example with the same screen in https://github.com/zephray/driving-lcds/tree/main/ac057tc1.
    * The command to enable loading LUT from IC registers: done via PSR (panel setting) command (0x00): set 8th bit (0x88 instead of 0x08).
    * IC registers for colors are 0x21-0x28 (8th color is 'special' for screen clear).
    * Stock LUT
* The photoframe has 7.3 inch ACeP. The naive expectations are that all three steps required should be similar to 5.65 EPD. In fact, IC specs for different EPDs from https://www.good-display.com/companyfile/5/#c_portalResCompanyFile_list-15878877704403956-1 and  https://github.com/CursedHardware/epd-driver-ic looks fairly similar.
* Step (1). Panel setting (PSR) for Photoframe screen [7.3 ACeP](https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/c/lib/e-Paper/EPD_7in3f.c) looks as follows:
```
    EPD_7IN3F_SendCommand(0x00);
    EPD_7IN3F_SendData(0x5F);
    EPD_7IN3F_SendData(0x69);
```
* We try to change 0x69 to 0xE9 (set 8th bit), expecting that it will enable IC to use LUT from registers. Then we hope that IC has the same registers for LUT (0x21-0x29) as in 5.65 screen and waveform looks similar (since its the same ACeP tech). However, we've found that 0x21 register contains tables for VCom and all colors written sequentially. We tried numerous formats from different drivers data sheets. However, we could not find the right one, and only able to produce some random colors by overwriting the VCom data with some bytes.

# Waveshare Photopainter A & B
## How to add photos
* Download jpg
* Run converter `convert.py`
    * Color saturation `--color 2.0` enabled by default. Default is 6 colors for ACeP screen. Use `--num_colors 5` for Spectra 6 Photopainter B.
    * Single `python3 convert.py image.jpg`
    * Batch `for file in /photos/*; python3 convert.py "$file"`
    * Produces bmp files
* Copy to flash card
    * It should be FAT32
    * Remove all files
    * Create “pic” dir
    * Copy bmp files (better via shell) `cp /photos/*.bmp /Volumes/FLASHDEVICE/pic/ 
    * Make sure no hidden files (MAC OS can add _.* bmp files that confuses photoframe software) `ls -a`
* Insert flash card, press “next” button

## How to update firmware
### Photopainter A
Original firmware supports only 100 photos and sorted order. Updated firmware supports 1000 photos and random order + different timings
Source and binaries: https://github.com/tcellerier/Pico_ePaper_73/tree/main
* Press RUN, then press BOOT, then release RUN, then release BOOT, the computer will pop up a USB flash drive
* Copy firmware using `$ cp -X blink.uf2 /Volumes/RPI-RP2/`(see https://www.raspberrypi.com/news/the-ventura-problem/)

### Photopainter B
Photopainter B supports more than 100 photos and sorted order by default changing every 12 hours. Its possible to use random order and different timing using trivial changes in firmware https://www.waveshare.com/wiki/PhotoPainter_(B). Several firmware options are pre-built https://github.com/waveshareteam/PhotoPainter_B/tree/master/extra_uf2

References
* Original converter https://files.waveshare.com/upload/e/ea/ConverTo7c_bmp.zip

# Philips Tableaux
## How to add photos
* Recommended ways don't work
    * According to the manual, photos can be placed in /Pictures folder on the USB drive. The device is supposed to copy them locally and use. However, it does not work and devide keep showing "insert usb with Pictures".
    * According to the manual, device can show up as drive when connecting using microUSB. However, it does not work on MacOS.
* Alternatively, we use service microUSB port to connect to embedded Android file system and copy files to /storage/emulated/0/Pictures/ folder
* Install Android tooling
    * brew install scrcpy
    * brew install android-platform-tools
* Connect via microUSB and check devices
    * adb devices
    * adb -s AUEA2412000031 shell (for shell to explore device FS)
* Run converter `convert.py`
    * Useful parameters:
        * "--device philips" for 1600x1200 resolution
        * "--save_original" to save original bmp to let philips dithering (it knows the device pallette, likely 8 colors)
        * "--color 1" no color saturation
    * Single `python3 convert.py --device philips --save_original 1 --color 1 image.jpg`
    * Batch `for file in /photos/*; python3 convert.py --device philips --save_original 1 --color 1 "$file"`
    * Produces bmp files both with and w/o dithering ("_original")
* Copy files
    * adb -s AUEA2412000031 push *original.bmp /storage/emulated/0/Pictures/
* Copy config for custom time between pictures refresh (default is 30 seconds)
    * adb -s AUEA2412000031 push config.xml /storage/emulated/0/Pictures/
```
  <?xml version="1.0"?>
      <epd_config>
      <sleep on="1"></sleep>
      <interval second="86400"></interval>
      <remember on="1"></remember>
      <rotate degree="0"></rotate>
      </epd_config> 
```
