# photoframe

Tools for eink photoframe

## Intro
* Device: https://www.waveshare.com/photopainter.htm
* 7-color: black, white, red, green, blue, yellow, orange
* Specs: https://files.waveshare.com/upload/d/db/7.3inch_e-Paper_%28F%29_Specification.pdf 

## Understanding color gamut
* 7 colors is too few to display a photo. Dithering technique is used to propagate the error to neighboring pixels. https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

## Ways to improve image quality
In short, we apply color saturation 2.0 and use 6 colors w/o orange.
* Image enhance
* Dithering
* More colors

## How to add photos
* Download jpg
* Run converter `convert.py`
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
Original firmware supports only 100 photos and sorted order. Updated firmware supports 1000 photos and random order + different timings
Source and binaries: https://github.com/tcellerier/Pico_ePaper_73/tree/main
* Press RUN, then press BOOT, then release RUN, then release BOOT, the computer will pop up a USB flash drive
* Copy firmware using `$ cp -X blink.uf2 /Volumes/RPI-RP2/`(see https://www.raspberrypi.com/news/the-ventura-problem/)

References
* Original converter https://files.waveshare.com/upload/e/ea/ConverTo7c_bmp.zip

