#encoding: utf-8

import sys
import os.path
from PIL import Image, ImageEnhance, ImagePalette, ImageOps, ExifTags, ImageDraw, ImageFont
import argparse
import requests
from geopy.geocoders import Nominatim
from geopy.geocoders import Photon
import time


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process some images.')

# Add orientation parameter
parser.add_argument('image_file', type=str, help='Input image file')
parser.add_argument('--dir', choices=['landscape', 'portrait'], help='Image direction (landscape or portrait)')
parser.add_argument('--file_suffix', type=str, default='_frame', help='Output file suffix')
parser.add_argument('--save_original', type=int, default=0, help='Save original image (after crop)')
parser.add_argument('--device', choices=['waveshare', 'philips'], default='waveshare', help='Target device (waveshare or philips)')
parser.add_argument('--mode', choices=['scale', 'cut'], default='scale', help='Image conversion mode (scale or cut)')
parser.add_argument('--dither', type=int, choices=[Image.NONE, Image.FLOYDSTEINBERG], default=Image.FLOYDSTEINBERG, help='Image dithering algorithm (NONE(0) or FLOYDSTEINBERG(3))')
parser.add_argument('--color', type=float, default=2.0, help='image color saturation, 0.0 b&w, 1.0 original, 2.0 looks more vivid on ePaper')
parser.add_argument('--contrast', type=float, default=1.0, help='image contrast, 1.0 original')
parser.add_argument('--brightness', type=float, default=1.0, help='image brightness, 1.0 orignal')
parser.add_argument('--sharpness', type=float, default=1.0, help='image sharpness, 1.0 original')
parser.add_argument('--num_colors', type=int, default=6, help='num colors: 5 - BWRGB, 6 - BWRGBY (like Spectra 6, looks better than 7), 7 - BWRGBYO (ACeP)')
parser.add_argument('--add_time', type=int, default=1, help='add time to image')
parser.add_argument('--add_location', type=int, default=1, help='add location to image')

# Parse command line arguments
args = parser.parse_args()

# Get input parameter
input_filename = args.image_file
display_direction = args.dir
file_suffix = args.file_suffix
save_original = args.save_original
target_device = args.device
display_mode = args.mode
display_dither = Image.Dither(args.dither)
display_color = args.color
display_contrast = args.contrast
display_brightness = args.brightness
display_sharpness = args.sharpness
num_colors = args.num_colors
add_time = args.add_time
add_location = args.add_location

# Check whether the input file exists
if not os.path.isfile(input_filename):
    print(f'Error: file {input_filename} does not exist')
    sys.exit(1)

# Read input image
input_image = Image.open(input_filename)
exif = input_image._getexif()
# Rotate the image according to the EXIF information
input_image = ImageOps.exif_transpose(input_image)
enhancer_color = ImageEnhance.Color(input_image)
input_image = enhancer_color.enhance(display_color)
enhancer_contrast = ImageEnhance.Contrast(input_image)
input_image = enhancer_contrast.enhance(display_contrast)
enhancer_brightness = ImageEnhance.Brightness(input_image)
input_image = enhancer_brightness.enhance(display_brightness)
enhancer_sharpness = ImageEnhance.Sharpness(input_image)
input_image = enhancer_sharpness.enhance(display_sharpness)


def get_exif_property(exif_data, property_name):
    if not exif_data:
        return None

    for tag, value in exif_data.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        if decoded == property_name:
            return value
    return None

def get_location_name(gps_info):
    if not gps_info:
        return None
    geolocator = Nominatim(user_agent="pythongeocoder")
    def decimal_coords(coords, ref):
        decimal_degrees = float(coords[0]) + float(coords[1]) / 60 + float(coords[2]) / 3600
        if ref == "S" or ref =='W' :
            decimal_degrees = -1 * decimal_degrees
        return decimal_degrees
    lat = decimal_coords(gps_info[2], gps_info[1])
    lon = decimal_coords(gps_info[4], gps_info[3])
    location = None
    retries = 5
    timeout = 1
    while retries:
        retries -= 1
        try:
            location = geolocator.reverse((lat, lon), exactly_one=True)
            name = location.raw['name']
            if not name:
                if 'address' in location.raw and 'city' in location.raw['address']:
                    name = location.raw['address']['city']
            if not name:
                if 'address' in location.raw and 'village' in location.raw['address']:
                    name = location.raw['address']['village']
            if not name:
                if 'address' in location.raw and 'town' in location.raw['address']:
                    name = location.raw['address']['town']
            if not name:
                if 'address' in location.raw and 'state' in location.raw['address']:
                    name = location.raw['address']['state']
            if not name:
                if 'address' in location.raw and 'country' in location.raw['address']:
                    name = location.raw['address']['country']
            if not name:
                name = location
            return name
        except:
            print(f'Geolocator not responding. Retrying in {timeout} seconds...')
            time.sleep(timeout)
            timeout *= 2
    return location


def add_text_to_image(image, text, font=None, font_size=5, text_color=(0, 0, 0), bg_color=(255, 255, 255)):
    draw = ImageDraw.Draw(image)
    if font is None:
        font = ImageFont.load_default(font_size)
    else:
        font = ImageFont.truetype(font, font_size)
    #font = ImageFont.truetype("arial.ttf", 100)
    width, height = image.size
    position = (0, 0)
    # Calculate text size
    left, top, right, bottom = draw.textbbox(position, text, font=font)
    text_width = right - left
    new_position = ((width - text_width) // 2, height - font_size - 2)
    left, top, right, bottom = draw.textbbox(new_position, text, font=font)
    draw.rectangle((left - 2, top - 2, right + 2, bottom + 2), fill=bg_color)
        
    # Draw text
    draw.text(new_position, text, font=font, fill=text_color)
    
    return image

# Get the original image size
width, height = input_image.size

deviceToSize = {
    'waveshare': (800, 480),
    'philips': (1600, 1200)
}

# Specified target size
if display_direction:
    if display_direction == 'landscape':
        target_width, target_height = deviceToSize[target_device]
    else:
        target_height, target_width = deviceToSize[target_device]
else:
    if  width > height:
        target_width, target_height = deviceToSize[target_device]
    else:
        target_height, target_width = deviceToSize[target_device]
    
if display_mode == 'scale':
    # Computed scaling
    scale_ratio = max(target_width / width, target_height / height)

    # Calculate the size after scaling
    resized_width = int(width * scale_ratio)
    resized_height = int(height * scale_ratio)

    # Resize image
    output_image = input_image.resize((resized_width, resized_height))

    # Create the target image and center the resized image
    resized_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
    left = (target_width - resized_width) // 2
    top = (target_height - resized_height) // 2
    resized_image.paste(output_image, (left, top))
elif display_mode == 'cut':
    # Calculate the fill size to add or the area to crop
    if width / height >= target_width / target_height:
        # The image aspect ratio is larger than the target aspect ratio, and padding needs to be added on the left and right
        delta_width = int(height * target_width / target_height - width)
        padding = (delta_width // 2, 0, delta_width - delta_width // 2, 0)
        box = (0, 0, width, height)
    else:
        # The image aspect ratio is smaller than the target aspect ratio and needs to be filled up and down
        delta_height = int(width * target_height / target_width - height)
        padding = (0, delta_height // 2, 0, delta_height - delta_height // 2)
        box = (0, 0, width, height)

    resized_image = ImageOps.pad(input_image.crop(box), size=(target_width, target_height), color=(255, 255, 255), centering=(0.5, 0.5))

# add time and location to image
image_location_name = ''
image_time = ''
if add_location:
    gps_info = get_exif_property(exif, "GPSInfo")
    if gps_info:
        image_location_name = get_location_name(gps_info)
if add_time:
    image_time = get_exif_property(exif, "DateTimeOriginal")
    if image_time:
        parts = (image_time.split()[0]).split(':')
        image_time = f"{parts[2]}/{parts[1]}/{parts[0]}"
if image_location_name or image_time:
    label = f"{image_location_name} {image_time}"
    add_text_to_image(resized_image, label, font='/System/Library/Fonts/Supplemental/Arial.ttf', font_size=14, text_color=(0, 0, 0))

# Create a palette object
pal_image = Image.new("P", (1,1))
if num_colors == 7:
    pal_image.putpalette( (0,0,0,  255,255,255,  0,255,0,   0,0,255,  255,0,0,  255,255,0, 255,128,0) + (0,0,0)*249)
elif num_colors == 6:
    pal_image.putpalette( (0,0,0,  255,255,255,  0,255,0,   0,0,255,  255,0,0,  255,255,0,) + (0,0,0)*250)
elif num_colors == 5:
    pal_image.putpalette( (0,0,0,  255,255,255,  0,255,0,   0,0,255,  255,0,0) + (0,0,0)*251)
  
# The color quantization and dithering algorithms are performed, and the results are converted to RGB mode
quantized_image = resized_image.quantize(dither=display_dither, palette=pal_image).convert('RGB')


# Save output image
output_filename = os.path.splitext(input_filename)[0] + '_' + display_mode + file_suffix + '.bmp'
quantized_image.save(output_filename)
if save_original:
    output_filename = os.path.splitext(input_filename)[0] + '_' + display_mode + file_suffix + '_original.bmp'
    resized_image.save(output_filename)
print(f'Successfully converted {input_filename} to {output_filename}')

