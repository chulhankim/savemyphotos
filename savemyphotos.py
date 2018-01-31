from os import listdir
import re

from PIL import Image
import piexif

img_name_list = [i for i in listdir('img') if i.endswith('.jpg')]

for img_name in img_name_list:
    img = Image.open('img/{}'.format(img_name))

    dt_list = re.split('[-,.\s]', img_name)[:-1]
    dt = '{}:{}:{} {}:{}:{}'.format(dt_list[0], dt_list[1], dt_list[2], dt_list[3], dt_list[4], dt_list[5])

    exif_dict = piexif.load(img.info['exif'])

    if piexif.ImageIFD.DateTime in exif_dict['0th']:
        continue

    print('Processing {}...'.format(img_name))

    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = dt
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = dt
    exif_dict['0th'][piexif.ImageIFD.DateTime] = dt

    exif_bytes = piexif.dump(exif_dict)
    img.save('result/{}'.format(img_name), exif=exif_bytes, quality=95)
