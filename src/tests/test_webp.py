from dataclasses import dataclass
import sys
sys.path.append("./src")
from logic.sfwa import Sfwa
sfwa = Sfwa()

file_name = "/dir/WS20220712168203521.webp"
save_name = f"tranformWebp.webp"
directory = "/dir"
sfwa.transform_webp(file_name, directory,save_name)
