import webbrowser
import subprocess
import platform
import zipfile
import base64
import shutil
import json
import os
from datetime import datetime
from munch import DefaultMunch
from os.path import isfile, join
from gi.repository import GLib
from PIL import Image, ImageDraw, ImageOps, GifImagePlugin


class Sfwa():

    def get_user_preferences(self):
        file = r'src/data/user.json'
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            response = {
                "lang": data['language'],
                "theme": data['theme'],
                "directory": data['directory'],
                "animatedIsShow": data['animatedIsShow'],
            }
        if response['directory'] == "" or os.path.isfile(response['directory']) == False:
            response['directory'] = self.get_default_dir()

        return response

    def set_user_preferences(self, data):
        data = {
            "language": data['lang'],
            "theme": data['theme'],
            "directory": data['directory'],
            "animatedIsShow": data['animatedIsShow'],
        }
        file = r'src/data/user.json'
        with open(file, 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def get_language_json(self, lang):
        file = f'src/lang/{lang}.json'
        with open(file, 'r') as read_file:
            response = json.load(read_file)
        return response

    def get_default_dir(self):
        # get the user operative system
        os_system = platform.system()
        # return dir of pictures folder
        if os_system == 'Windows':
            return f'C:/users/{os.getlogin()}/pictures'
        elif os_system == 'Linux':
            return GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES)

    def create_encode_icon(self, icon):
        new_img = open(icon, 'rb')
        new_img_encode = base64.b64encode(new_img.read())
        return new_img_encode

    def open_folder(self, folder):
        os_system = platform.system()
        if os_system == 'Windows':
            os.starfile(folder)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', folder])

    def open_license(self, lang):
        license = f'src/resources/license/license_{lang}.pdf'
        os_system = platform.system()
        if os_system == 'Windows':
            os.starfile(license)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', license])

    def open_terms(self, lang):
        terms = f'src/resources/terms/terms_{lang}.pdf'
        os_system = platform.system()
        if os_system == 'Windows':
            os.starfile(terms)
        elif os_system == 'Linux':
            subprocess.Popen(['xdg-open', terms])

    def open_github(self):
        url = 'https://github.com/FelipeGCx'
        webbrowser.open(url, new=2,
                        autoraise=True)

    def serialize_data(self, data):
        return DefaultMunch.fromDict(data)

    def create_pack(self, data):
        data = self.serialize_data(data)
        response = False
        if data.package == 'stickerMaker':
            response = self.create_pack_sticker_maker(data)
        else:
            response == self.create_pack_wemoji(data)
        return response

    def create_pack_wemoji(self, data):
        # move the compresed file to the directory of the user
        dir_origin = 'src/resources/compressed'
        zip_file_name = 'wemoji.wemojipack'
        self.move_file(dir_origin, data.directory, zip_file_name)
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
        self.open_text_file(text_file, 'w', sentence, is_json=True)
        # create icon
        img_icon = self.transform_image(data.icon,size=(96,96), radius=16)
        img_icon.save(icon_name)
        img_icon.close()
        # process the lote of images
        self.process_images(data.directory, folder_name,
                            data.animated, data.conserve)
        os.chdir(data.directory)
        self.add_folder_to_zip(zip_file_name, folder_name)
        self.rename_pack(zip_file_name, data.namepack, 'wemojipack')
        folder_dir = f'{data.directory}/{folder_name}'
        shutil.rmtree(folder_dir)
        return True

    def create_pack_sticker_maker(self, data):
        # move the compresed file to the directory of the user
        dir_origin = 'src/resources/compressed'
        zip_file_name = 'stickermaker.wastickers'
        self.move_file(dir_origin, data.directory, zip_file_name)
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
        self.open_text_file(namepack_file, 'a', data.namepack )
        self.open_text_file(author_file, 'a', data.author )
         # create icon
        icon_name = 'tray_icon.png'
        img_icon = self.transform_image(data.icon,size=(96,96), radius=16)
        img_icon.save(icon_name)
        img_icon.close()
        # process the lote of images
        self.process_images(data.directory, folder_name,
                            data.animated, data.conserve)
        os.chdir(data.directory)
        zip_dir = f'{data.directory}/{zip_file_name}'
        folder_dir = f'{data.directory}/{folder_name}'
        self.add_imgs_to_zip(zip_dir, folder_dir)
        os.chdir(data.directory)
        self.rename_pack(zip_file_name, data.namepack, 'wastickers')
        shutil.rmtree(folder_dir)
        return True

    def create_name(self, prefix):
        # ~ return string, with prefix pass and 17 numbers exaple sufix WS: WS20220712168203521
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

    def set_number(self, number):
        return str(f'{0}{number}') if number <= 9 else str(number)

    def move_file(self, dir_origin, dir_to_move, file_name):
        shutil.copy(f'{dir_origin}/{file_name}',
                    f'{dir_to_move}/{file_name}')

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

    def replace_endwith(self, file_name, suffix):
        if file_name.endswith('.jpg'):
            file_name = file_name.removesuffix('.jpg')
        elif file_name.endswith('.png'):
            file_name = file_name.removesuffix('.png')
        elif file_name.endswith('.jpeg'):
            file_name = file_name.removesuffix('.jpeg')
        elif file_name.endswith('.webp'):
            return file_name
        return f'{file_name}.{suffix}'

    def files_in_dir(self, directory):
       # ~ lists all file in the directory selected by the user
        source = os.listdir(directory)
        files = [name for name in source if isfile(join(directory, name))]
        return files

    def validate_img(self, file_name):
        # ~ validates if the file is an image
        if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.webp') or file_name.endswith('.jpeg'):
            return True
        else:
            return False

    def validate_gif(self, file_name):
        # ~ validates if the file is an gif image
        if file_name.endswith('.gif'):
            return True
        else:
            return False

    def transform_image(self, file_name, size=(512, 512), radius=8):
        radius = int(size[0]/100 * radius)
        img = Image.open(file_name)
        if img.mode != "RGB":
            img = img.convert("RGB")
        # get the size of the image
        width, heigth = img.size
        # create a exponential size for resize the image
        # if the size is little, resize image the image to exponential size
        width_complete = (size[0] - width) + width + 2
        heigth_complete = (size[1] - heigth) + heigth + 2
        value_resize = (width*10,heigth*10)
        # value_resize = (width_complete,heigth_complete)
        if  width < size[0] or heigth < size[0]:
            img = img.resize(value_resize)
        # make the thumbnail of the image for get the size of the image
        img.thumbnail(size)
        # create mask for give the shape of the image
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        # create round rectangle params = ((x, y) + (width, height), radius, fill=0-255 it's the opacity)
        draw.rounded_rectangle((0, 0) + img.size, radius=radius, fill=255)
        # apply the mask to the image
        img_masked = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img_masked.putalpha(mask)
        # create background image transparent
        img_output = Image.new('RGBA', size, (255, 255, 255, 0))
        # define the position of the image
        x = int((size[0] - img.size[0]) / 2)
        y = int((size[1] - img.size[1]) / 2)
        # paste the image to the background
        img_output.paste(img_masked, (x, y))
        # close the images
        img.close()
        mask.close()
        img_masked.close()
        # return the image output #^ remember close the image after use
        return img_output

    def transform_gif(self, file_name, dir, save_name):
        # define the color system
        GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_AFTER_FIRST
        # open the image with the gif format
        img = Image.open(file_name)
        # get the duration of the gif
        duration = img.info['duration']
        print('nombre',save_name)
        print('duracion',duration)
        print('frames', img.n_frames)
        # create array for save the frames
        frames = []
        # iterate the frames of the gif
        for frame in range(0, img.n_frames):
            img.seek(frame)
            name = f'{dir}{frame}.webp'
            img.save(name)
            img_compress_name = self.compress_img(name,quality=25)
            # remove the image frame after use
            os.remove(name)
            # transform the image to set the sticker style and append to the array
            frames.append(self.transform_image(img_compress_name))
            # remove the image frame after use
            os.remove(img_compress_name)
            
        # create webp file with the frames in array
        frames[0].save(f'{dir}/{save_name}', save_all=True,
                       append_images=frames, transparency=0, loop=0, duration=duration, optimize=True)
        # close the image after use
        img.close()
        
    def open_zip_file(self, file_name, mode, add_file):
            # ~ writes or appends file to zipfiles
        with zipfile.ZipFile (file_name, mode) as zip_file:
            # zip_file.write(add_file, compress_type=zipfile.ZIP_STORED)
            zip_file.write(add_file, compress_type=zipfile.ZIP_DEFLATED)
            zip_file.close()
        
    def add_folder_to_zip(self, zip_file, folder): 
        for file in os.listdir(folder):
            self.add_to_pack(zip_file, f'{folder}/{file}')
    
    def add_imgs_to_zip(self, zip_file, folder):
        os.chdir(folder)
        for file in os.listdir(folder):
            self.add_to_pack(zip_file, file)
            

    def add_to_pack(self, zip_file, file):
        self.open_zip_file(zip_file, 'a', file)
          

    def rename_pack(self, zip_file, new_name, file_extension):
        new_name = f'{new_name}.{file_extension}'
        os.rename(zip_file, new_name)
    
    def validate_weight(self,file_name,weight=512000):
        file_weight = os.path.getsize(file_name)
        print('peso',file_weight)
        # if file_weight > weight:
            # os.remove(file_name)

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

    def process_images(self, directory, destiny, animated=False, conserve_imgs=True):
        os.chdir(directory)
        files = self.files_in_dir(directory)
        checker = 0
        for file in files:
            checker += 1
            if checker > 30:
                break
            file_name = f"{self.create_name('WS')}{checker}.webp"
            if animated:
                if self.validate_gif(file):
                    self.transform_gif(file, destiny, file_name)
                    self.validate_weight(f'{destiny}/{file_name}')
            else:
                if self.validate_img(file):
                    if file.endswith('.webp'):
                        img = Image.open(file)
                        img = img.resize((512, 512))
                        img.save(f'{destiny}/{file_name}')
                        img.close()
                    else:
                        img = self.transform_image(file)
                        img.save(f'{destiny}/{file_name}')
                        img.close()
            if conserve_imgs == False:
                os.remove(file)

    def compress_img(self,file_name,quality=50):
        img = Image.open(file_name)
        img = img.convert("RGB")
        name, ext = os.path.splitext(file_name)
        new_file_name = f"{name}.jpg"
        img.save(new_file_name, quality=quality, optimize=True)
        img.close()
        return new_file_name
