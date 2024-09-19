import base64
import json
from io import BytesIO
from PIL import Image
from datetime import datetime
import time
from random import randrange
import requests
from urllib.parse import unquote
import re
from Crypto.Cipher import AES
import os
import numpy
import cv2


def resize(img, h=None):
    if h is None:
        max_size = 640
        image_width, image_height = img.size
        if image_width > image_height:
            return resize_by_w_h(img, width=max_size, height=None)
        else:
            return resize_by_w_h(img, width=None, height=max_size)
    else:
        return resize_by_w_h(img, width=None, height=h)


def resize_by_w_h(img, width=None, height=None):
    if height is not None:
        print(img.size)
        w = img.width
        h = img.height
        rate = height / h
        to_w = int(w * rate)
        new_img = img.resize((to_w, int(height)))
        print(new_img.size)
        return new_img
    if width is not None:
        print(img.size)
        w = img.width
        h = img.height
        rate = width / w
        to_h = int(h * rate)
        new_img = img.resize((width, int(to_h)))
        print(new_img.size)
        return new_img

def base64ToImage(base64_string,type = 'RGB'):
    image_bytes = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_bytes)
    image = Image.open(image_buffer)
    if 'RGB' == type:
        return image.convert('RGB')
    else:
        return image

def nparray2base(img):
    print(type(img))
    encode_params = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
    _, buffer = cv2.imencode('.png', img, encode_params)
    b64_bytearr = base64.b64encode(buffer).decode("utf-8")
    return b64_bytearr


def pil_2_cv2(img):
    pil_image = img.convert('RGB')
    open_cv_image = numpy.array(pil_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image
def imageToBase64(image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return image_data
    #return base64.b64encode(image)

def binary2base(path):
    with open(path, "rb") as image_file:
        buffer = image_file.read()
        img_base64 = base64.b64encode(buffer).decode("utf-8")
        return img_base64
def readURLImage(url):
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Read the image from the response content
        #print(response.content)
        image = Image.open(BytesIO(response.content))
        # Now you can work with the image object
        # For example, you can display it:
        base64_data = base64.b64encode(response.content)
        #print(base64_data)
        #image.show()
        return image,base64_data
    else:
        #print("Failed to fetch the image")
        return None,None
##
# flag success/fail
# data when flag == success
# error when flag == fail
# #
def jsonMsg(status,data,error):
    result = {}
    result["status"] = status
    if "success" == status:
        result["data"] = data
    else:
        result["error"] = error
    return json.dumps(result)

def gen_rnd_filename(fmt):
    if fmt == "time1":
        return int(round(time() * 1000))
    elif fmt == "time2":
        return "%s%s" % (
            int(round(time() * 1000)),
            str(randrange(1000, 10000)),
        )
    elif fmt == "time3":
        return "%s%s" % (
            datetime.now().strftime("%Y%m%d%H%M%S"),
            str(randrange(1000, 10000)),
        )
    elif fmt == "time4":
        return "%s" % (
            datetime.now().strftime("%Y%m%d%H%M%S"),
        )
def recursive_decoder(obj):
    # Customize this function according to your needs
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = recursive_decoder(value)  # Recursively decode nested objects
        return obj
    elif isinstance(obj, list):
        return [recursive_decoder(item) for item in obj]  # Recursively decode nested objects in lists
    else:
        return obj

def dealJson(raw_str):
    if "" == raw_str or None == raw_str:
        return ""
    subtitle = []
    obj = json.loads(unquote(raw_str))
    body = obj["body"]
    for line in body:
        if "翻译" in line["content"]:
            continue
        content = line["content"].replace("\n"," ")
        subtitle.append(content)
    return " ".join(subtitle)

def padding_to(raw: bytes, padding: int, max_length: int = None):
    '''
    部分加解密是需要补齐位数到指定padding的
    '''
    c = len(raw)/padding
    block: int = int(c)
    if block != c:
        block += 1
    result = raw.ljust(padding*block, b'\0')
    if max_length:
        result = result[0:max_length]
    return result
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        credit to: ePi272314
        https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions
    """

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    ret = {
        'Password is less than 8 characters' : length_error,
        'Password does not contain a number' : digit_error,
        'Password does not contain a uppercase character' : uppercase_error,
        'Password does not contain a lowercase character' : lowercase_error,
        'Password does not contain a special character' : symbol_error,
    }

    return ret
"""
Need pycrypto but pycrypto is out of maintance
So we can install pycryptodome [almost drop-in replacement for the old PyCrypto library]
"""
def AesTool(action,param):
    key = str(os.environ.get("AESKEY"))
    iv = str(os.environ.get("AESIV"))
    if 'None' == key or 'None' == iv:
        return param
    PADDING = '\0'
    skey = padding_to(key.encode(), 32, 32)
    iv = padding_to(iv.encode(), 16, 16)
    encryptoobj = AES.new(skey, AES.MODE_CBC, iv)
    if "e" == action:
        e = encryptoobj.encrypt(padding_to(param.encode('utf-8'), 16))
        cryptedStr = base64.b64encode(e)
        return cryptedStr
    else:
        temp = base64.b64decode(param)
        origin = encryptoobj.decrypt(temp)
        originStr = origin.strip(PADDING.encode('utf-8')).decode()
        return originStr