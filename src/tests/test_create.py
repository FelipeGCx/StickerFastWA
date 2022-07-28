import sys
sys.path.append("./src")
from logic.sfwa import Sfwa
sfwa = Sfwa()

data = {
    "package":"wemoji",
    "animated": False,
    "namepack": "Test",
    "author": "You",
    "directory": "/home/felipegcz/Imágenes/TestNormal",
    "icon": "/home/felipegcz/Imágenes/icon.png",
    "conserve": True,
}

sfwa.create_pack(data)
 