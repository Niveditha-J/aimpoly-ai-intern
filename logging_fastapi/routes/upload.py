from fastapi import APIRouter, UploadFile, File
from utils.validation import validate_audio

router = APIRouter()

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    validate_audio(file)

    return {"message": "Validation passed"}