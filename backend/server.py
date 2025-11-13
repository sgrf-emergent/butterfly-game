from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import random
from bson import ObjectId

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class Butterfly(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    commonName: str
    latinName: str
    imageUrl: str
    difficulty: int = 1

    class Config:
        populate_by_name = True

class QuizQuestion(BaseModel):
    butterfly: Butterfly
    options: List[Butterfly]

class GameSession(BaseModel):
    score: int
    total: int
    timestamp: str

# Routes
@api_router.get("/")
async def root():
    return {"message": "Butterfly Identification API"}

@api_router.get("/butterflies", response_model=List[Butterfly])
async def get_butterflies():
    """Get all butterflies"""
    butterflies = await db.butterflies.find().to_list(100)
    return [Butterfly(**{**b, "_id": str(b["_id"])}) for b in butterflies]

@api_router.get("/quiz/question")
async def get_quiz_question():
    """Get a random quiz question with 5 options"""
    # Get all butterflies
    all_butterflies = await db.butterflies.find().to_list(100)
    
    if len(all_butterflies) < 5:
        raise HTTPException(status_code=400, detail="Not enough butterflies in database")
    
    # Select random correct answer
    correct_butterfly = random.choice(all_butterflies)
    
    # Select 4 other random butterflies as wrong options
    wrong_butterflies = [b for b in all_butterflies if b["_id"] != correct_butterfly["_id"]]
    selected_wrong = random.sample(wrong_butterflies, min(4, len(wrong_butterflies)))
    
    # Combine and shuffle
    all_options = [correct_butterfly] + selected_wrong
    random.shuffle(all_options)
    
    # Convert to Butterfly models
    correct = Butterfly(**{**correct_butterfly, "_id": str(correct_butterfly["_id"])})
    options = [Butterfly(**{**b, "_id": str(b["_id"])}) for b in all_options]
    
    return {
        "correctAnswer": correct,
        "options": options
    }

@api_router.post("/init-butterflies")
async def initialize_butterflies():
    """Initialize the database with butterfly data"""
    # Check if already initialized
    count = await db.butterflies.count_documents({})
    if count > 0:
        return {"message": f"Database already initialized with {count} butterflies"}
    
    # 30 realistic butterfly species
    butterflies = [
        {"commonName": "Monarch", "latinName": "Danaus plexippus", "imageUrl": "https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
        {"commonName": "Blue Morpho", "latinName": "Morpho menelaus", "imageUrl": "https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Painted Lady", "latinName": "Vanessa cardui", "imageUrl": "https://images.unsplash.com/photo-1533048324814-79b0a31982f1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
        {"commonName": "Red Admiral", "latinName": "Vanessa atalanta", "imageUrl": "https://images.unsplash.com/photo-1564514476902-542f8c30121e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHw0fHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Tiger Swallowtail", "latinName": "Papilio glaucus", "imageUrl": "https://images.unsplash.com/photo-1702338354821-0ea4fb0221e3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
        {"commonName": "Black Swallowtail", "latinName": "Papilio polyxenes", "imageUrl": "https://images.unsplash.com/photo-1657244670691-ec73025cf69e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Spicebush Swallowtail", "latinName": "Papilio troilus", "imageUrl": "https://images.unsplash.com/photo-1728946737947-3e1908c3750a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Pipevine Swallowtail", "latinName": "Battus philenor", "imageUrl": "https://images.unsplash.com/photo-1628181150173-f5f355d15f28?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Zebra Swallowtail", "latinName": "Eurytides marcellus", "imageUrl": "https://images.pexels.com/photos/2671074/pexels-photo-2671074.jpeg", "difficulty": 2},
        {"commonName": "Common Buckeye", "latinName": "Junonia coenia", "imageUrl": "https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Pearl Crescent", "latinName": "Phyciodes tharos", "imageUrl": "https://images.unsplash.com/photo-1484704193309-27eaa53936a7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Question Mark", "latinName": "Polygonia interrogationis", "imageUrl": "https://images.unsplash.com/photo-1509715513011-e394f0cb20c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Mourning Cloak", "latinName": "Nymphalis antiopa", "imageUrl": "https://images.unsplash.com/photo-1592861377549-3586948b6a74?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Viceroy", "latinName": "Limenitis archippus", "imageUrl": "https://images.pexels.com/photos/28749528/pexels-photo-28749528.jpeg", "difficulty": 2},
        {"commonName": "Gulf Fritillary", "latinName": "Agraulis vanillae", "imageUrl": "https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Great Spangled Fritillary", "latinName": "Speyeria cybele", "imageUrl": "https://images.unsplash.com/photo-1533048324814-79b0a31982f1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Cabbage White", "latinName": "Pieris rapae", "imageUrl": "https://images.unsplash.com/photo-1702338354821-0ea4fb0221e3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
        {"commonName": "Clouded Sulphur", "latinName": "Colias philodice", "imageUrl": "https://images.unsplash.com/photo-1728946737947-3e1908c3750a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Orange Sulphur", "latinName": "Colias eurytheme", "imageUrl": "https://images.unsplash.com/photo-1628181150173-f5f355d15f28?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Cloudless Sulphur", "latinName": "Phoebis sennae", "imageUrl": "https://images.unsplash.com/photo-1564514476902-542f8c30121e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHw0fHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Eastern Comma", "latinName": "Polygonia comma", "imageUrl": "https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "American Lady", "latinName": "Vanessa virginiensis", "imageUrl": "https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Common Checkered-Skipper", "latinName": "Pyrgus communis", "imageUrl": "https://images.unsplash.com/photo-1484704193309-27eaa53936a7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Silver-spotted Skipper", "latinName": "Epargyreus clarus", "imageUrl": "https://images.unsplash.com/photo-1509715513011-e394f0cb20c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Gray Hairstreak", "latinName": "Strymon melinus", "imageUrl": "https://images.unsplash.com/photo-1592861377549-3586948b6a74?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Spring Azure", "latinName": "Celastrina ladon", "imageUrl": "https://images.pexels.com/photos/2671074/pexels-photo-2671074.jpeg", "difficulty": 2},
        {"commonName": "Eastern Tailed-Blue", "latinName": "Cupido comyntas", "imageUrl": "https://images.pexels.com/photos/28749528/pexels-photo-28749528.jpeg", "difficulty": 3},
        {"commonName": "Little Yellow", "latinName": "Pyrisitia lisa", "imageUrl": "https://images.unsplash.com/photo-1657244670691-ec73025cf69e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
        {"commonName": "Hackberry Emperor", "latinName": "Asterocampa celtis", "imageUrl": "https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
        {"commonName": "Red-spotted Purple", "latinName": "Limenitis arthemis", "imageUrl": "https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 3}
    ]
    
    result = await db.butterflies.insert_many(butterflies)
    return {"message": f"Successfully initialized {len(result.inserted_ids)} butterflies"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
