import json, io
import google.generativeai as genai
from fastapi import APIRouter, Path
from fastapi.exceptions import HTTPException
from firebase_admin import firestore
from fastapi import File, UploadFile, Depends
from PIL import Image
from app.dependency import get_db, get_bucket
from app.util import upload_image


router = APIRouter(prefix="/api")


@router.get("/meals")
def get_meals(db: firestore.Client = Depends(get_db)):
    meals_ref = db.collection("meals")
    return [{"id": meal.id, **meal.to_dict()} for meal in meals_ref.stream()]


@router.get("/meals/{meal_id}")
async def get_meal(meal_id: str = Path(...), db: firestore.Client = Depends(get_db)):
    meal_ref = db.collection("meals").document(meal_id)
    meal_snapshot = meal_ref.get()
    if not meal_snapshot.exists:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"id": meal_snapshot.id, **meal_snapshot.to_dict()}


@router.post("/meals")
async def add_meal(image: UploadFile = File(...), db: firestore.Client = Depends(get_db), bucket=Depends(get_bucket)):
    image = await image.read()
    image = Image.open(io.BytesIO(image))

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        [
            image,
            "Your mission is to identify which foods are present in the photo and estimate how many calories they contain!",
            "Try to identify the amount of each food present to improve the estimated total calorie amount.",
            "Capitalize the first letter of the name"
            "If no food is found, it leaves the food list empty and the total calories are zero."
            "The following json must be returned in the following format: {total_calories: integer, foods: [{name: string, calories: integer, amount: integer, unit: string, total_carbohydrates: string, proteins: string, total_fat: string, saturated_fat: string, sodium: string}]}"
            "The raw json must be returned in string format."
            'Use "pt-br" for data.',
        ]
    )

    image_url = upload_image(bucket, image)

    data = json.loads(response.candidates[0].content.parts[0].text)
    data["image_url"] = image_url

    doc_ref = db.collection("meals").document()
    doc_ref.set(data)

    return {"id": doc_ref.id, **data}
