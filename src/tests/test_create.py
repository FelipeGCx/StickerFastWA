import sys
sys.path.append("./src")
from logic.sfwa import Sfwa
sfwa = Sfwa()

data = {
    "package":"stickerMaker",
    "animated": True,
    "namepack": "Test",
    "author": "You",
    "directory": "",
    "icon": "",
    "conserve": True,
}

sfwa.create_pack(data)
 