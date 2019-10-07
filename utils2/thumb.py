import os
from PIL import Image

def fit_size(path, size):
    img = Image.open(path)
    img.thumbnail((size, size), Image.NEAREST)
    img.save(path)

def fit_width(path, width):
    img = Image.open(path)
    img.thumbnail((width, 10000), Image.ANTIALIAS)
    img.save(path)

def square_thumb(path, size):
    img = Image.open(path)
    width, height = img.size
    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper
    img = img.crop((left, upper, right, lower))
    img = img.resize((size,size), Image.ANTIALIAS)
    filename = path.replace(os.path.dirname(path)+'/','')
    thumb_filename = filename.replace('.', '_'+str(size)+'.')
    thumb_path = path.replace(filename, thumb_filename)
    img.save(thumb_path)

def thumb(path, wsize, hsize):
    img = Image.open(path)
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = wsize, hsize
    dst_ratio = float(dst_width) / float(dst_height)
    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = float(src_width - crop_width) / 2
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = float(src_height - crop_height) / 3
    img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
    img = img.resize((dst_width, dst_height), Image.ANTIALIAS)
    filename = path.replace(os.path.dirname(path)+'/','')
    thumb_filename = filename.replace('.', '_'+str(wsize)+'.')
    thumb_path = path.replace(filename, thumb_filename)
    img.save(thumb_path)

