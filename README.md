# photoframe
Tools for eink photoframe

Device: https://www.waveshare.com/photopainter.htm

How to add photos
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

References
* Original converter https://files.waveshare.com/upload/e/ea/ConverTo7c_bmp.zip

