from PIL import Image, ImageDraw, ImageOps, GifImagePlugin, ImageChops
from os.path import isfile, join
from gi.repository import GLib
from munch import DefaultMunch
from datetime import datetime
import numpy as np
import webbrowser
import subprocess
import platform
import zipfile
import base64
import shutil
import json
import os


class Sfwa():

    def __init__(self):
        global root
        root = os.getcwd()

    # ~ GET the user preferences for the GUI
    def get_user_preferences(self):
        file = r'src/data/user.json'
        # open the file in read mode
        with open(file, 'r') as read_file:
            data = json.load(read_file)  # load the data
            # create a response dict with the data
            response = {
                "lang": data['language'],
                "theme": data['theme'],
                "directory": data['directory'],
                "animatedIsShow": data['animatedIsShow'],
            }
        # verify if the directory is valid and if it is not valid, set the default pictures directory as the directory
        if response['directory'] == "" or not os.path.isfile(response['directory']):
            response['directory'] = self.get_default_dir()
        return response  # return the response

    # ~ POST the user preferences for the GUI
    def set_user_preferences(self, data):
        # modify the keys in data creating a new dict in the same variable
        data = {
            "language": data['lang'],
            "theme": data['theme'],
            "directory": data['directory'],
            "animatedIsShow": data['animatedIsShow'],
        }
        file = r'src/data/user.json'
        # open the file in write mode to overwrite the data
        with open(file, 'w') as write_file:
            json.dump(data, write_file, indent=4)  # inserting the new data

    # ~ GET the language json file
    def get_language_json(self, lang):
        # get the directory of the language in base lang param
        file = f'src/lang/{lang}.json'
        # open in read mode the file
        with open(file, 'r') as read_file:
            response = json.load(read_file)  # load the response
        return response  # return the response

    # ~ return the default directory of the pictures
    def get_default_dir(self):
        # get the user operative system
        os_system = platform.system()
        # return dir of pictures folder
        if os_system == 'Windows':
            return f'C:/users/{os.getlogin()}/pictures'
        elif os_system == 'Linux':
            return GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES)

    # ~ return string with the base64 of the image directory passed
    def create_encode_icon(self, icon):
        new_img = open(icon, 'rb')  # open the file
        # encode the image in base64
        new_img_encode = base64.b64encode(new_img.read())
        return new_img_encode  # return the base64 of the image

    # ~ open the directory folder passed
    def open_folder(self, folder):
        # get the user operative system
        os_system = platform.system()
        # open the folder in the user operative system
        if os_system == 'Windows':
            os.starfile(folder)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', folder])

    # ~ open the license file in base of the language passed
    def open_license(self, lang):
        # get the directory of the licence in base lang param
        license = f'src/resources/license/license_{lang}.pdf'
        # get the user operative system
        os_system = platform.system()
        # open the file in the user operative system
        if os_system == 'Windows':
            os.starfile(license)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', license])

    # ~ open the terms of use file in base of the language passed
    def open_terms(self, lang):
        # get the directory of the terms in base lang param
        terms = f'src/resources/terms/terms_{lang}.pdf'
        # get the user operative system
        os_system = platform.system()
        # open the file in the user operative system
        if os_system == 'Windows':
            os.starfile(terms)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', terms])

    # ~ open the personal github
    def open_github(self):
        url = 'https://github.com/FelipeGCx'
        webbrowser.open(url, new=2,
                        autoraise=True)

    # ~ return data serialized
    def serialize_data(self, data):
        # this serialize the data of dict to can access the data like javascript object usign the dot notation
        # example data = {'name': 'Felipe'} pass of data['name'] to data.name
        return DefaultMunch.fromDict(data)  # return the data serialized

    # ~ Create a pack with the data passed
    def create_pack(self, data):
        # serialize the data
        data = self.serialize_data(data)
        response = False  # response default is false
        # evaluate the data app select for the user and call the function to create compatible the pack with that app
        if data.package == 'stickerMaker':
            response = self.create_pack_sticker_maker(data)
        else:
            response == self.create_pack_wemoji(data)
        os.chdir(root)  # change to the root directory for the next operations
        return response  # return the response

    # ~ Create the pack for the wemoji app
    def create_pack_wemoji(self, data):
        # copy the compresed file to the directory of the user
        dir_origin = 'src/resources/compressed'
        zip_file_name = 'wemoji.wemojipack'
        self.copy_file(dir_origin, data.directory, zip_file_name)
        # change of directory to the directory of the user
        os.chdir(data.directory)
        # create a folder for the pack
        folder_name = self.create_name('WSP')
        os.mkdir(folder_name)
        # change of directory to the folder of the pack
        os.chdir(f'{data.directory}/{folder_name}')
        # create file .wspdata
        text_file = '.wspdata'
        icon_name = 'tray_icon.png'
        # create the sentence to animated or regular pack
        if data.animated:
            sentence = {
                "a": folder_name,
                "b": data.namepack,
                "c": data.author,
                "d": "tray_icon.png",
                "i": "4",
                "j": False,
                "k": True
            }
        else:
            sentence = {
                "a": folder_name,
                "b": data.namepack,
                "c": data.author,
                "d": icon_name,
                "i": "4",
                "j": False,
                "k": False
            }
        # create the file .wspdata and write the sentence
        self.open_text_file(text_file, 'w', sentence, is_json=True)
        # create icon
        img_icon = self.transform_image(data.icon, size=(96, 96), radius=16)
        img_icon.save(icon_name)
        img_icon.close()
        # process the lote of images
        self.process_images(data.directory, folder_name,
                            data.animated, data.conserve)
        os.chdir(data.directory)
        # add the folder with all files in the zip file
        self.add_folder_to_zip(zip_file_name, folder_name)
        # rename the zip file to the name of the pack
        self.rename_pack(zip_file_name, data.namepack, 'wemojipack')
        # remove the unessary folder
        folder_dir = f'{data.directory}/{folder_name}'
        shutil.rmtree(folder_dir)
        return True  # return the response

    # ~ Create the pack for the sticker maker app
    def create_pack_sticker_maker(self, data):
        # copy the compresed file to the directory of the user
        dir_origin = 'src/resources/compressed'
        zip_file_name = 'stickermaker.wastickers'
        self.copy_file(dir_origin, data.directory, zip_file_name)
       # change of directory to the directory of the user
        os.chdir(data.directory)
        # create a folder for the pack
        folder_name = self.create_name('WSP')
        os.mkdir(folder_name)
        # change of directory to the folder of the pack
        os.chdir(f'{data.directory}/{folder_name}')
        # create files for name pack and author
        namepack_file = f'title.txt'
        author_file = 'author.txt'
        self.open_text_file(namepack_file, 'a', data.namepack)
        self.open_text_file(author_file, 'a', data.author)
        # create icon
        icon_name = 'tray_icon.png'
        img_icon = self.transform_image(data.icon, size=(96, 96), radius=16)
        img_icon.save(icon_name)
        img_icon.close()
        # process the lote of images
        self.process_images(data.directory, folder_name,
                            data.animated, data.conserve)
        os.chdir(data.directory)
        zip_dir = f'{data.directory}/{zip_file_name}'
        folder_dir = f'{data.directory}/{folder_name}'
        # add only the files in the zip file not the folder
        self.add_imgs_to_zip(zip_dir, folder_dir)
        os.chdir(data.directory)
        # rename the zip file to the name of the pack
        self.rename_pack(zip_file_name, data.namepack, 'wastickers')
        # remove the unessary folder
        shutil.rmtree(folder_dir)
        return True  # return the response

    # ~ return string, with prefix pass and 17 numbers exaple sufix WS: WS20220712168203521

    def create_name(self, prefix):
        # create the number with the datatime
        date = datetime.now()
        year = str(date.year)
        month = self.set_number(date.month)
        day = self.set_number(date.day)
        additional = str(round(date.year / 12))
        hour = self.set_number(date.hour)
        minute = self.set_number(date.minute)
        second = self.set_number(date.second)
        name = f'{prefix}{year}{month}{day}{additional}{hour}{minute}{second}'
        return name

    # ~ add 0 in the number if it is less than 10
    def set_number(self, number):
        return str(f'{0}{number}') if number < 10 else str(number)

    # ~ copy the file to the directory
    def copy_file(self, dir_origin, dir_to_move, file_name):
        # copy the file from directory origin to directory to move
        shutil.copy(f'{dir_origin}/{file_name}',
                    f'{dir_to_move}/{file_name}')

    # ~ open the text file with the mode passed
    def open_text_file(self, file_name, mode, sentence=None, is_json=False):
        # ~ open the file with the argument mode
        with open(file_name, mode) as open_file:
            # ~ read the file and return it
            if mode == 'r':
                return open_file.read()
            # ~ write the file for insert sentence
            elif mode == 'w' or mode == 'a':
                if is_json:
                    json.dump(sentence, open_file)
                else:
                    open_file.write(sentence)
                open_file.close()

    # ~ replace the suffix to the new suffix passed
    def replace_endwith(self, file_name, suffix):
        # separate the name and the suffix
        name, ext = os.path.splitext(file_name)
        return f'{name}.{suffix}'  # return the file_name with the new suffix

    # ~ return list of all files in the directory passed

    def files_in_dir(self, directory):
        # create a list of all content of the directory
        source = os.listdir(directory)
        # create a list comprehension to get only the files using isfile to condition
        files = [name for name in source if isfile(join(directory, name))]
        return files  # return the list of files

    # ~ return boolean, if the file is an image
    def validate_img(self, file_name):
        if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.webp') or file_name.endswith('.jpeg'):
            return True
        else:
            return False
    # ~ return boolean, if the file is an animated image

    def validate_gif(self, file_name):
        # ~ validates if the file is an gif image
        if file_name.endswith('.gif'):
            return True
        else:
            return False

    # ~ return an Pillow image object transformed to params passed
    def transform_image(self, file_name, size=(512, 512), radius=8):
        # has_transparency = self.has_transparency(file_name)
        # convert the radius to the size of the image
        radius = int(size[0]/100 * radius)
        # open the image
        img = Image.open(file_name)
        # parse the color of the image
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        # get the size of the image
        width, heigth = img.size
        # create a exponential size for resize the image
        # if the size is little, resize image the image to exponential size
        value_resize = (width*10, heigth*10)
        # value_resize = (width_complete,heigth_complete)
        if width < size[0] or heigth < size[0]:
            img = img.resize(value_resize)
        # make the thumbnail of the image to conserve the proportions
        img.thumbnail(size)
        # create mask for give the shape of the image
        # mask = Image.new('RGBA', img.size, (0, 0, 0, 0))
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        # create round rectangle params = ((x, y) + (width, height), radius, fill=0-255 it's the opacity)
        draw.rounded_rectangle((0, 0) + img.size, radius=radius, fill=255)
        # apply the mask to the image
        img_masked = Image.new("RGBA", size, (0, 0, 0, 0))
        img_masked.paste(img, mask=mask)
        # create background image transparent
        img_output = Image.new('RGBA', size, (0, 0, 0, 0))
        # define the position of the image
        x = int((size[0] - img.size[0]) / 2)
        y = int((size[1] - img.size[1]) / 2)
        # paste the image to the background in the center
        img_output.paste(img_masked, (x, y))
        # close the images
        img.close()
        mask.close()
        img_masked.close()
        # return the image output #^ remember close the image after use
        return img_output

    # ~ transform the animated image
    def transform_gif(self, file_name, dir, save_name):
        # define the color system
        GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_AFTER_FIRST
        # open the image with the gif format
        img = Image.open(file_name)
        # get the duration of the gif
        duration = img.info['duration']
        # create list for save the name frames
        frames = []
        # iterate the frames of the gif
        for frame in range(0, img.n_frames):
            img.seek(frame)
            name = f'{dir}{frame}.webp'
            img.save(name)
            # compress the image with the quality passed
            img_compress_name = self.compress_img(name, quality=25)
            # remove the image frame after use
            os.remove(name)
            # transform the image to set the sticker style and append to the array
            frames.append(self.transform_image(img_compress_name))
            # remove the compressed image frame after use
            os.remove(img_compress_name)

        # create webp file with the frames in array
        frames[0].save(f'{dir}/{save_name}', save_all=True,
                       append_images=frames, transparency=0, loop=0, duration=duration, optimize=True)
        # close the image after use
        img.close()

    # ~ write or append the file to zip file
    def open_zip_file(self, file_name, mode, add_file):
        with zipfile.ZipFile(file_name, mode) as zip_file:
            # zip_file.write(add_file, compress_type=zipfile.ZIP_STORED)
            zip_file.write(add_file, compress_type=zipfile.ZIP_DEFLATED)
            zip_file.close()

    # ~ add all files in the folder directory and the folder to the zip file
    def add_folder_to_zip(self, zip_file, folder):
        for file in os.listdir(folder):
            self.add_to_pack(zip_file, f'{folder}/{file}')

    # ~ add all files in the folder directory to the zip file
    def add_imgs_to_zip(self, zip_file, folder):
        os.chdir(folder)
        for file in os.listdir(folder):
            self.add_to_pack(zip_file, file)

    # ~ add the file to the zip file in mode append
    def add_to_pack(self, zip_file, file):
        self.open_zip_file(zip_file, 'a', file)

    # ~ remane the zip file to the new name with the extension passed
    def rename_pack(self, zip_file, new_name, file_extension):
        new_name = f'{new_name}.{file_extension}'
        os.rename(zip_file, new_name)

    # ~ validate the weight of the file
    def validate_weight(self, file_name, weight=512000):
        file_weight = os.path.getsize(file_name)
        print('peso', file_weight)
        if file_weight > weight:
            return False
        else:
            return True

    #! deprecated
    def open_sticker_maker():
        # ~ opens the application "sticker marker" url playstore
        webbrowser.open(
            'https://play.google.com/store/apps/details?id=com.marsvard.stickermakerforwhatsapp&hl=es_CO&gl=US',
            new=2,
            autoraise=True)

    #! deprecated
    def open_tutorial():
        # ~ opens the tutorial
        webbrowser.open(
            'https://www.youtube.com/watch?v=3qGXItbLMaA',
            new=2,
            autoraise=True)

    # ~ process the images in the folder in base params passed
    def process_images(self, directory, destiny, animated=False, conserve_imgs=True):
        # change to the directory passed
        os.chdir(directory)
        # list the image files in the directory
        files = self.files_in_dir(directory)
        checker = 0  # checker for the number of files in the directory
        file_format = 'webp' # define the final format to the image
        # iterate the image files in the directory
        for file in files:
            checker += 1  # increment the checker
            # check if the the number file is menor than 30
            if checker > 30:
                break
            # create the name for the image
            file_name = f"{self.create_name('WS')}{checker}.{file_format}"
            # check if the pack is animated
            if animated:
                # validate the file is an animated image
                if self.validate_gif(file):
                    # transform and save the image to webp
                    self.transform_gif(file, destiny, file_name)
                    # check if the weight final image is less than 512000
                    is_valid = self.validate_weight(f'{destiny}/{file_name}')
                    # remove the image if the weight is greater than 512000 to not create compatibility issues
                    # if not is_valid:
                    #     os.remove(file_name)
            else:
                # validate the file is an image
                if self.validate_img(file):
                    # check if the image is a .webp
                    if file.endswith('.webp'):
                        # open the image and only rezise it
                        img = Image.open(file)
                        img = img.resize((512, 512))
                        img.save(f'{destiny}/{file_name}')
                        img.close()
                    if file.endswith('.png'):
                        img_png = Image.open(file)
                        has_transparency = self.has_transparency(img_png)
                        img_png.close()
                        if has_transparency:
                            # crop the transparent border of the image
                            self.crop_image(file)
                        # transform and save the image to webp
                        img = self.transform_image(file)
                        img.save(f'{destiny}/{file_name}')
                        img.close()
                    else:
                        # transform and save the image to webp
                        img = self.transform_image(file)
                        img.save(f'{destiny}/{file_name}')
                        img.close()
            # check if the conserve the images
            if not conserve_imgs:
                os.remove(file)  # remove the image

    # ~ compress the image with the quality passed
    def compress_img(self, file_name, quality=50):
        # open the image
        img = Image.open(file_name)
        # convert color to RGB
        img = img.convert("RGB")
        # separate the file name and the extension
        name, ext = os.path.splitext(file_name)
        new_file_name = f"{name}.jpg"
        # save the image with the quality passed
        img.save(new_file_name, quality=quality, optimize=True)
        img.close()
        return new_file_name  # return the new file name
    
    def has_transparency(self,img):
        if img.info.get("transparency", None) is not None:
            return True
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True
        return False

    def crop_image(self, file):
        img = Image.open(file)
        img = self.trim(img)
        img.save(file)
    
    def trim(self,im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox)