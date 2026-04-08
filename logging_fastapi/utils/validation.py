from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = ["audio/wav", "audio/mpeg"]

async def validate_audio(file: UploadFile):

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds limit"
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format"
        )