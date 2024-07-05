"""
Tasks:
- method for creating a file and it's meta file
"""
from pathlib import Path
from os.path import isfile
from yaml import dump
from time import strftime, gmtime
from PIL import Image
from uuid import uuid4
#from picamera import PiCamera
from time import sleep
import csv

# TODO add error checking for functions
#########################################################
# data control layer
#########################################################

_SESSION_ID = None
_SUBDIR = "sensor_data"
_CAM_RESOLUTION = (1024, 768)

def initialize_session(directories, metadata_dirs):
    global _SESSION_ID
    # Session ID is only for csv data, which is attributed to a singular session
    _SESSION_ID = str(uuid4())
    # directories
    #TODO implement directory check
    create_directories(directories)
    #TODO implement creation of metadata
    create_metadata(metadata_dirs)

# I wrote this so that I would have an abstraction from accessing files
# though not realy good, it is not called that often
def create_access_path(dir, uuid,filetype):
    return rf"./{_SUBDIR}/{dir}/{uuid}.{filetype}"

def path_existence_check(potential_path):
    path = Path(potential_path)
    if not path.exists():
        try:
            path.mkdir(parents=True)
        except FileExistsError as e:
            raise e

def create_directories(dirs):
    for dir in dirs:
        try:
            path_existence_check(rf"./{_SUBDIR}/{dir}/")
        except FileExistsError:
            pass

def create_metadata(dirs):
    for dir in dirs:
        _create_metadata(rf"./{_SUBDIR}/{dir}",_SESSION_ID)

def write_data2csv(data,path):
    # path is a directory name
    _write_data2csv(iter(data),rf"./{_SUBDIR}/{path}",_SESSION_ID)
    return _SESSION_ID

def write_data2image(image,path):
    id = str(uuid4())
    _write_data2image(image,rf"./{_SUBDIR}/{path}",id)
    return id

# only used in combination with direct access classes
# not used, due to a np array also being passable
"""
def take_picam_image():
    global _CAM_RESOLUTION
    camera = PiCamera()
    camera.resolution = _CAM_RESOLUTION
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('foo.jpg')
"""


#########################################################
# data layer
#########################################################

def _create_metadata(path,uuid):
    with open(rf"{path}/{uuid}.yaml",'w') as file:
        dump({"uuid":uuid,"time":strftime("%d %b %Y %H:%M:%S", gmtime())},file)

def _write_data2csv(data_it, path,uuid):
    # check if path exists
    path_existence_check(path)
    # create csv 
    with open(rf"{path}/{uuid}.csv",'a',newline='') as file:
        csvfile = csv.writer(file,delimiter=',')
        csvfile.writerows(data_it)
    
    

def _write_data2image(image,path,uuid,):
    # check if path exists
    path_existence_check(path)
    # create meta file
    _create_metadata(path,uuid)
    # save image
    # old variant with saving from numpy array
    #im = Image().fromarray(image)
    image.save(rf"{path}/{uuid}.jpg")

def read_sop_text():

    path_existence_check("./config")
    if not isfile("./config/sop_config.txt"):
        with open("./config/sop_config.txt", "w") as file:
            file.write("There was no text for sop in config/sop_config.txt. So dummy text was created.")

    # this reads a txt automatically
    with open("./config/sop_config.txt",'r') as stream:
        return stream.read()