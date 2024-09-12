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
    * Using tools from https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html
    * Color saturation seems to provide visually better images when displayed on the e-ink probably due to low contrast of the screen.
    * Brightness, contrast, sharpening introduces visual artifacts.
    * Denoising introduces blurring.
* Dithering
    * More algos: https://github.com/hbldh/hitherdither. Did not see much difference, maybe Atkinson lossy dithering gives marginal impact.
    * Gamma-aware: https://www.nayuki.io/page/gamma-aware-image-dithering. Human eye can distinguish shades of darker colors better. Tried in by adding conversion to linear color space to the code with multiple dithering algorithms. Did not see much difference probably due to low number of colors. `lnr = rgb / 255... lnr = np.where(lnr <= 0.04045, lnr / 12.92, ((lnr +  0.055) / 1.055)**2.4)`
* Less colors
    * Using 6 colors (w/o orange) seems to visually look better. Orange seems to be used a lot by dithering algorithm since it falls "between" main colors. Also, new e-ink Spectra 6 screen uses only 6 colors too.
    * Using 5 colors (w/o orange and yellow) is worse. Yellow is one of the main colors in CMY.  
* More colors
    * Use custom waveform to force eink produce more colors. Discussed in a dedicated section

## More colors
* Use custom waveform to force eink produce more colors. Especially, we want to get the remaining from CMY - cyan (for the blue sky) and magenta. But also, equally spaced colors in between to avoid biasing we saw for orange.
* Great explanation about waveform and their usage in EPD can be found in https://hackaday.io/project/179058-understanding-acep-tecnology and https://github.com/Modos-Labs/Glider.
* EPD has a lookup table (LUT) with color as a key and a list of voltage impulses as a value (+/- and value). It takes Z frames to refresh the screen. The i-th impulse is applied at the i-th frame to a target pixel. Physically, eink particles of certain color move to front depending on the charge sign. Also, some particles move faster than the others due to their size. This gives the final visible color.
* There are 5 particle colors: BWCMY. The waveform LUT is designed to show 7 colors: BWRGBYO. Interestingly, it does not have Cyan or Magenta.
* LUT is stored in IC driver flash. IC driver is connected directly to the screen and via SPI interface to the driving board.
* IC driver has an API exposed to the driving board and can issue commands such as init the screen, show a picture, or sleep etc. The example code is provided by the EPD producer. It looks as follows: 'EPD_7IN3F_SendCommand(0x00); EPD_7IN3F_SendData(0x5F); EPD_7IN3F_SendData(0x69);'. EPD producer does not provide API specification. 
* IC drivers have capability to use LUT from the IC registers. So, in order to use custom LUT, one has to have the following info:
    * The command to enable loading LUT from IC registers.
    * The list (addresses) of IC registers.
    * Stock LUT, or an example of a waveform, to be able to experiment with its customization.
* For example, https://hackaday.io/project/179058-understanding-acep-tecnology explains that 5.65 ACeP display uses SPD1656 display driver, which has a pdf with specification, which explains which bit parameter to set to enable custom LUT (LUT_EN or LUT_SEL) during display init, the addresses of the registers for LUT, and the size of the content. They also were able to get the original LUT by some soldering and reading back the LUT flash. Code can be found in https://github.com/ts-manuel/Understanding-ACeP-Tecnology/tree/master. There is another example with the same screen in https://github.com/zephray/driving-lcds/tree/main/ac057tc1.
* The photoframe has 7.3 inch ACeP. The naive expectations are that all three steps required should be similar to 5.65 EPD. In fact, IC specs for different EPDs from https://www.good-display.com/companyfile/5/#c_portalResCompanyFile_list-15878877704403956-1 and  https://github.com/CursedHardware/epd-driver-ic looks fairly similar. 

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

