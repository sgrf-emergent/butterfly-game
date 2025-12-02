from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import aiomysql
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import random
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MySQL connection pool
db_pool = None

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class Butterfly(BaseModel):
    id: Optional[int] = None
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

class GameScore(BaseModel):
    id: Optional[int] = None
    username: str
    score: int
    total: int
    difficulty: int
    percentage: int
    date: str

    class Config:
        populate_by_name = True

# Database connection helper
async def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await aiomysql.create_pool(
            host=os.environ.get('MYSQL_HOST', 'localhost'),
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', 'root'),
            db=os.environ.get('MYSQL_DATABASE', 'testdata'),
            charset='utf8mb4',
            autocommit=True,
            minsize=1,
            maxsize=10
        )
    return db_pool

# Routes
@api_router.get("/")
async def root():
    return {"message": "Butterfly Identification API"}

@api_router.get("/butterflies", response_model=List[Butterfly])
async def get_butterflies():
    """Get all butterflies"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT id, commonName, latinName, imageUrl, difficulty FROM butterflies")
            result = await cursor.fetchall()
            return [Butterfly(**row) for row in result]

@api_router.get("/quiz/question")
async def get_quiz_question(difficulty: int = 1):
    """Get a random quiz question with 5 options filtered by difficulty"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Get butterflies filtered by difficulty
            await cursor.execute(
                "SELECT id, commonName, latinName, imageUrl, difficulty FROM butterflies WHERE difficulty = %s",
                (difficulty,)
            )
            all_butterflies = await cursor.fetchall()
            
            if len(all_butterflies) < 5:
                raise HTTPException(status_code=400, detail=f"Not enough butterflies in database for difficulty {difficulty}")
            
            # Select random correct answer
            correct_butterfly = random.choice(all_butterflies)
            
            # Select 4 other random butterflies as wrong options
            wrong_butterflies = [b for b in all_butterflies if b['id'] != correct_butterfly['id']]
            selected_wrong = random.sample(wrong_butterflies, min(4, len(wrong_butterflies)))
            
            # Combine and shuffle
            all_options = [correct_butterfly] + selected_wrong
            random.shuffle(all_options)
            
            # Convert to Butterfly models
            correct = Butterfly(**correct_butterfly)
            options = [Butterfly(**b) for b in all_options]
            
            return {
                "correctAnswer": correct,
                "options": options
            }

@api_router.post("/reset-database")
async def reset_database():
    """Reset the database by deleting all butterflies"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM butterflies")
            return {"message": f"Deleted all butterflies"}

@api_router.post("/init-butterflies")
async def initialize_butterflies():
    """Initialize the database with butterfly data"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # Check if already initialized
            await cursor.execute("SELECT COUNT(*) as count FROM butterflies")
            result = await cursor.fetchone()
            count = result[0]
            
            if count > 0:
                return {"message": f"Database already initialized with {count} butterflies"}
            
            # 30 realistic butterfly species
            butterflies = [
                {"commonName": "Monarch", "latinName": "Danaus plexippus", "imageUrl": "https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
                {"commonName": "Blue Morpho", "latinName": "Morpho menelaus", "imageUrl": "https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 2},
                {"commonName": "Painted Lady", "latinName": "Vanessa cardui", "imageUrl": "https://images.unsplash.com/photo-1533048324814-79b0a31982f1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
                {"commonName": "Red Admiral", "latinName": "Vanessa atalanta", "imageUrl": "https://images.unsplash.com/photo-1564514476902-542f8c30121e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHw0fHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
                {"commonName": "Tiger Swallowtail", "latinName": "Papilio glaucus", "imageUrl": "https://images.unsplash.com/photo-1702338354821-0ea4fb0221e3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
                {"commonName": "Black Swallowtail", "latinName": "Papilio polyxenes", "imageUrl": "https://images.unsplash.com/photo-1657244670691-ec73025cf69e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 1},
                {"commonName": "Spicebush Swallowtail", "latinName": "Papilio troilus", "imageUrl": "https://images.unsplash.com/photo-1728946737947-3e1908c3750a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
                {"commonName": "Pipevine Swallowtail", "latinName": "Battus philenor", "imageUrl": "https://images.unsplash.com/photo-1628181150173-f5f355d15f28?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85", "difficulty": 3},
                {"commonName": "Zebra Swallowtail", "latinName": "Eurytides marcellus", "imageUrl": "https://images.pexels.com/photos/2671074/pexels-photo-2671074.jpeg", "difficulty": 2},
                {"commonName": "Common Buckeye", "latinName": "Junonia coenia", "imageUrl": "https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85", "difficulty": 1},
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
            
            # Insert butterflies
            for butterfly in butterflies:
                await cursor.execute(
                    "INSERT INTO butterflies (commonName, latinName, imageUrl, difficulty) VALUES (%s, %s, %s, %s)",
                    (butterfly['commonName'], butterfly['latinName'], butterfly['imageUrl'], butterfly['difficulty'])
                )
            
            return {"message": f"Successfully initialized {len(butterflies)} butterflies"}

# ==================== ADMIN ENDPOINTS ====================

@api_router.get("/admin/butterflies", response_model=List[Butterfly])
async def get_admin_butterflies():
    """Get all butterflies for admin management"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT id, commonName, latinName, imageUrl, difficulty FROM butterflies")
            result = await cursor.fetchall()
            return [Butterfly(**row) for row in result]

@api_router.post("/admin/butterfly", response_model=Butterfly)
async def create_butterfly(butterfly: Butterfly):
    """Create a new butterfly"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "INSERT INTO butterflies (commonName, latinName, imageUrl, difficulty) VALUES (%s, %s, %s, %s)",
                (butterfly.commonName, butterfly.latinName, butterfly.imageUrl, butterfly.difficulty)
            )
            butterfly_id = cursor.lastrowid
            
            await cursor.execute(
                "SELECT id, commonName, latinName, imageUrl, difficulty FROM butterflies WHERE id = %s",
                (butterfly_id,)
            )
            result = await cursor.fetchone()
            return Butterfly(**result)

@api_router.put("/admin/butterfly/{butterfly_id}", response_model=Butterfly)
async def update_butterfly(butterfly_id: int, butterfly: Butterfly):
    """Update an existing butterfly"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "UPDATE butterflies SET commonName = %s, latinName = %s, imageUrl = %s, difficulty = %s WHERE id = %s",
                (butterfly.commonName, butterfly.latinName, butterfly.imageUrl, butterfly.difficulty, butterfly_id)
            )
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Butterfly not found")
            
            await cursor.execute(
                "SELECT id, commonName, latinName, imageUrl, difficulty FROM butterflies WHERE id = %s",
                (butterfly_id,)
            )
            result = await cursor.fetchone()
            return Butterfly(**result)

@api_router.delete("/admin/butterfly/{butterfly_id}")
async def delete_butterfly(butterfly_id: int):
    """Delete a butterfly"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM butterflies WHERE id = %s", (butterfly_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Butterfly not found")
            
            return {"message": "Butterfly deleted successfully"}

# Score endpoints
@api_router.post("/scores")
async def save_score(score_data: GameScore):
    """Save a game score"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            date_now = datetime.utcnow()
            
            await cursor.execute(
                "INSERT INTO scores (username, score, total, difficulty, percentage, date) VALUES (%s, %s, %s, %s, %s, %s)",
                (score_data.username, score_data.score, score_data.total, score_data.difficulty, score_data.percentage, date_now)
            )
            score_id = cursor.lastrowid
            
            await cursor.execute(
                "SELECT id, username, score, total, difficulty, percentage, DATE_FORMAT(date, '%%Y-%%m-%%dT%%H:%%i:%%s.000Z') as date FROM scores WHERE id = %s",
                (score_id,)
            )
            result = await cursor.fetchone()
            return GameScore(**result)

@api_router.get("/scores/{username}")
async def get_user_scores(username: str):
    """Get personal best scores and recent games for a user"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Get all scores for the user
            await cursor.execute(
                "SELECT id, username, score, total, difficulty, percentage, DATE_FORMAT(date, '%%Y-%%m-%%dT%%H:%%i:%%s.000Z') as date FROM scores WHERE username = %s ORDER BY date DESC",
                (username,)
            )
            all_scores = await cursor.fetchall()
            
            if not all_scores:
                return {
                    "personalBests": {
                        "easy": None,
                        "medium": None,
                        "hard": None
                    },
                    "recentGames": [],
                    "totalGames": 0
                }
            
            # Calculate personal bests by difficulty
            easy_scores = [s for s in all_scores if s["difficulty"] == 1]
            medium_scores = [s for s in all_scores if s["difficulty"] == 2]
            hard_scores = [s for s in all_scores if s["difficulty"] == 3]
            
            personal_bests = {
                "easy": max(easy_scores, key=lambda x: x["percentage"])["percentage"] if easy_scores else None,
                "medium": max(medium_scores, key=lambda x: x["percentage"])["percentage"] if medium_scores else None,
                "hard": max(hard_scores, key=lambda x: x["percentage"])["percentage"] if hard_scores else None
            }
            
            # Get recent 10 games
            recent_games_formatted = [GameScore(**game) for game in all_scores[:10]]
            
            return {
                "personalBests": personal_bests,
                "recentGames": recent_games_formatted,
                "totalGames": len(all_scores)
            }

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

@app.on_event("startup")
async def startup_db_pool():
    await get_db_pool()
    logger.info("MySQL connection pool created")

@app.on_event("shutdown")
async def shutdown_db_pool():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        logger.info("MySQL connection pool closed")
