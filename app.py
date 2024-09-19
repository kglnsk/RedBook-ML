from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from models import CLIPImageClassifier
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

import io

app = FastAPI(
    title="CLIP Image Classifier API",
    description="An API for classifying images using a CLIP model.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize the classifier (this may take some time)
classifier = CLIPImageClassifier()

@app.post("/classify", summary="Classify an image", response_description="The classification results")
async def classify_image(file: UploadFile = File(...)):
    """
    Upload an image and get the classification result based on predefined categories.
    
    - **file**: Image file to be classified
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File is not an image.")
    
    try:
        # Read the image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.") from e
    
    # Get classification result
    result = classifier.classify_image(image)
    
    return JSONResponse(content=result)
