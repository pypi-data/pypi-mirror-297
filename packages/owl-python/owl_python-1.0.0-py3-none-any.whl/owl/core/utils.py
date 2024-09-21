from PIL import Image
import numpy as np
from tqdm.auto import tqdm
import os
import shutil


def load_img(path, size):
    """
    Simple util for image loading.
    Parameters:
    - path: path to image
    - size: target image size
    """
    im = Image.open(path)
    im = im.resize(size)
    return np.array(im)
                

def convert_folder_to_jpg(folder_path, remove=True):
    """
    Util for converting folder files to jpg.
    Parameters:
    - remove: should delete image with previous extension
    """
    for filename in tqdm(os.listdir(folder_path), desc="Converting..."):
        if filename.lower().endswith(('.png', '.gif', '.bmp', '.tiff', '.jpeg')):
            img = Image.open(os.path.join(folder_path, filename))
            rgb_img = img.convert('RGB')
            rgb_img.save(os.path.join(folder_path, ".".join(filename.split('.')[:-1]) + '.jpg'), 'JPEG')
            if remove:
                os.remove(os.path.join(folder_path, filename))
                
                
def create_folder(path, remove=True):
    """
    Creates folder.
    Parameters:
    - remove: if True deletes folder if exists
    """
    if remove:
        if os.path.exists(path):
            shutil.rmtree(path)
    os.mkdir(path)
    