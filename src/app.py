from logic.sfwa import Sfwa
import webview
import pyautogui
import threading
import json
import sys
import os

sys.path.append("./src")
sys.path.append("./src/data")

sfwa = Sfwa()


def run(window):
    width, height = pyautogui.size()
    window.move(width - 300, height - 510)
    # window.hide()


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def getUserPreferences(self):
        response = sfwa.get_user_preferences()
        # window.show()
        return response

    def getLanguageJson(self, lang):
        response = sfwa.get_language_json(lang)
        return response

    def closeApp(self, user_preferences):
        sfwa.set_user_preferences(user_preferences)
        window.destroy()

    def minimizeApp(self):
        window.minimize()

    def selectFolder(self, dir):
        response = window.create_file_dialog(
            webview.FOLDER_DIALOG, directory=dir)
        return response[0]

    def selectIcon(self):
        file_types = ('Image Files (*.jpg;*.png;*.webp)',
                      'All Files (*.jpg;*.png;*.webp)')
        file = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        icon_dir = file[0]
        response = {
            'dir': icon_dir,
            # return string in base64
            'encode': sfwa.create_encode_icon(icon_dir).decode()
        }
        return response

    def openFolder(self, folder):
        sfwa.open_folder(folder)

    def openLicense(self,lang):
        sfwa.open_license(lang)

    def openTerms(self,lang):
        sfwa.open_terms(lang)

    def openGithub(self):
        sfwa.open_github()

    def createPack(self, data):
        response = sfwa.create_pack(data)
        return response


if __name__ == '__main__':
    api = Api()
    window = webview.create_window("StickerFast WA", "view/index.html",
                                   width=290, height=500, resizable=False, frameless=True,
                                   transparent=True, on_top=True, js_api=api, easy_drag=False)
    webview.start(run, window, http_server=True, debug=True)
