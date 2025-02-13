import os, shutil
import logging
logger = logging.getLogger(__name__)


def copy_static():
    if not os.path.exists("./public"):
        logger.warning("Directory does not exists, creating")
        os.mkdir("./public", "./static")
    else:
        pass
        
    copy_dir("./public")
    return True

def copy_dir(directory:str, destination:str):
    contents = os.listdir(directory)
    for content in contents:
        content = directory + content
        destination = destination + content
        if not os.path.isfile(content):
            os.mkdir(destination)
            copy_dir(content, destination)
        else:
            shutil.copy(content, destination)


