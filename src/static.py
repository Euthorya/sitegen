import os, shutil
import logging
logger = logging.getLogger(__name__)

PUBLIC_PATH = "./public/"
STATIC_PATH = "./static/"


def copy_static():
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
    os.mkdir(PUBLIC_PATH)
    #breakpoint()
    copy_dir(STATIC_PATH, PUBLIC_PATH)
    return True

def copy_dir(directory:str, destination:str):
    contents = os.listdir(directory)
    for content in contents:
        path = directory + content
       # breakpoint()
        if not os.path.isfile(path):
            path += "/"
            folder = destination + content + "/"
           # breakpoint()
            os.mkdir(folder)
            copy_dir(path, folder)
        else:
           # breakpoint()
            shutil.copy(path, destination)


