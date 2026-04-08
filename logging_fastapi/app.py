import logging
from fastapi import FastAPI, UploadFile, File, HTTPException

logging.basicConfig(level=logging.INFO)

app = FastAPI()

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_TYPES = [
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "video/mp4"
]

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    logging.info(f"Upload request received: {file.filename}")

    try:
        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            logging.error("File too large")
            raise HTTPException(status_code=400, detail="File too large")

        if file.content_type not in ALLOWED_TYPES:
            logging.error("Invalid format")
            raise HTTPException(status_code=400, detail="Invalid file format")

        logging.info("File validated successfully")

        return {"message": "File validated successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")