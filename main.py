import io
import PIL
import requests

from io import BytesIO
from typing import Optional
from PIL import Image
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile

from urllib.parse import urlparse
from fastapi.responses import StreamingResponse
from fastapi.param_functions import Query
 
app = FastAPI(
    title="sqy-narrow-to-wide-image",
    description="Use this API to increase the image wide angle without loosing image qualtiy, for better result use square image as input",
    version="2.0.1",
)

class ImageDetails(BaseModel):
    url_: str


@app.get("/")
async def root():
    return "Hello World!!!"

    
@app.post("/image_by_file")
async def insert_image_by_file(insert_image: UploadFile=File(...),):

    contents = await insert_image.read() #Building image
    original_image = Image.open(BytesIO(contents))
    format_ = original_image.format.lower()
    
    def get_content_type(format_):

        type_ = "image/jpg"
        
        if format_ == "gif":
            type_ = "image/gif"
        elif format_ == "webp":
            type_ = "image/webp"
        elif format_ == "png":
            type_ = "image/png"
        elif format_ == "jpeg":
            type_ = "image/jpeg"
        
        return type_


    wdt,baseheight = original_image.size
    hpercent = (baseheight / float(original_image.size[1]))
    wsize = int((float(original_image.size[1]) * float(hpercent)))
    original_image = original_image.resize((1020, 710), Image.Resampling.LANCZOS)

    buf = BytesIO()
    original_image.save(buf,format=format_.lower(), quality=100)
    buf.seek(0)
    
    return StreamingResponse(buf,media_type=get_content_type(format_))

@app.post("/image_by_URL")
async def insert_image_by_URL(insert_image:str):
    
    response = requests.get(insert_image)
    image_bytes = io.BytesIO(response.content)
    
    original_image = Image.open(image_bytes)
    format_ = original_image.format.lower()

    filename = insert_image.lower()

    #this function get the format type of input image
    def get_format(format_):  

        if format_ == "jpg":
            format_ = "jpg"
        elif format_== "jpeg":
            format_ = "jpeg"
        elif format_ == "webp":
            format_ = "WebP"
        elif format_ == "gif":
            format_ = "gif"
    
        return format_
 
   
    # #this function for gave the same type of format to output
    def get_content_type(format_):
        
        if format_ == "gif":
            type_ = "image/gif"
        elif format_ == "webp":
            type_ = "image/webp"
        elif format_ == "png":
            type_ = "image/png"
        elif format_ == "jpg":
            type_ = "image/jpg"
        elif format_ == "jpeg":
            type_ = "image/jpeg"
        #print(type_)
        return type_

    format_ = get_format(format_.lower())#here format_ store the type of image by filename

    wdt,baseheight = original_image.size
    hpercent = (baseheight / float(original_image.size[1]))
    wsize = int((float(original_image.size[1]) * float(hpercent)))
    original_image = original_image.resize((1020, 710), Image.Resampling.LANCZOS)

    buf = BytesIO()
    original_image.save(buf, format=format_.lower(), quality=100)
    buf.seek(0)

    return StreamingResponse(buf,media_type=get_content_type(format_))