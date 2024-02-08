import asyncio
import os
import uuid

from app.depends import get_user
from app.models import User, UserInput
from fastapi import APIRouter, Depends, File, Request, UploadFile
from oaks_inference import image_processing
from PIL import Image
from tortoise.exceptions import DoesNotExist


async def call_ml(photo_path):
    return image_processing(photo_path)


ml = APIRouter()


@ml.post("/new")
async def new(user: User = Depends(get_user), file: UploadFile = File(...)):
    try:
        if not file.filename.split(".")[-1] in ["tif", "png"]:
            raise DoesNotExist
        random_filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        contents = file.file.read()
        path = os.path.join(os.getcwd(), "static", "from_user", random_filename)
        with open(path, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    to_save = "/static" + path.split("static")[-1]
    new_input = UserInput(input_photo=to_save)

    res = await call_ml(path)

    new_input.output_photo = res
    await new_input.save()

    await user.inputs.add(new_input)
    await user.save()

    return {"photo": res, "user": await user.json()}
