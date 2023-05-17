# StickerFast WA

StickerFast WA is a desktop app to make sticker packs for Whatsapp, it's built in python using [pywebview](https://pywebview.flowrl.com)
- state: "Development"
- python version: Python 3.10.4
- built on the OS: Linux Ubuntu

# ⚠ Currently not working

*If you liked this project give me a star*

# ℹ️ Notes 
- Currently the wemoji packs are invalid (I'm work to fix it)
- Some animated stickers after processing exceed the 500kb allowed, while I find a solution I suggest to unzip the final package, optimize the stickers that exceed the size in [ezgif](https://ezgif.com/optiwebp) and reinsert them.

# 🚀 Getting started

### Install virtual enviroment if you don't have one
``` bash
pip install virtualenv
```

### Create your virtual enviroment
``` bash
virtualenv venv -p python3
```
  
### Init your virtual enviroment
``` bash
source venv/bin/activate
``` 
### Install the requirement.txt
``` bash
pip install -r requirements.txt 
```

### Run the app
``` bash
python3 src/app.py
```
