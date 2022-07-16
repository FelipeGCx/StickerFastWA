from PIL import Image, ImageDraw, ImageOps, GifImagePlugin
import webp

file_name = '/home/felipegcz/Imágenes/TestNomal/1.jpeg'
file_name_webp = '/home/felipegcz/Imágenes/iconfinal.gif'
# file_name_webp = '/home/felipegcz/Imágenes/WS20220712168203521.webp'
destiny = '/home/felipegcz/Imágenes/TestNomal'
destiny_two = '/home/felipegcz/Imágenes'

img = Image.open(file_name)
img = img.convert("RGB")
img.save(f'{destiny}/testcom.jpeg', quality=40, optimize=True)
img.close()



# Load a PIL image array from the specified .webp animation file
anim = webp.load_images(file_name_webp)

# Grab a reference to the first frame, and save the entire PIL image array as GIF with 70ms frames (14.286 FPS)
anim[0].save(f'{destiny_two}/output.webp', save_all=True, append_images=anim[0:], duration=70, loop=0)
