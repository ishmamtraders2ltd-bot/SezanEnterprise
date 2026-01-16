from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


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
class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: str
    description: str
    specifications: dict
    image_url: str
    brand: Optional[str] = None
    featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(BaseModel):
    name: str
    category: str
    description: str
    specifications: dict
    image_url: str
    brand: Optional[str] = None
    featured: bool = False

class QuoteRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    product_name: str
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    quantity: int
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuoteRequestCreate(BaseModel):
    product_id: str
    product_name: str
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    quantity: int
    message: Optional[str] = None

class ContactMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str


# Routes
@api_router.get("/")
async def root():
    return {"message": "Sezan Enterprise API"}

# Product routes
@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, featured: Optional[bool] = None):
    query = {}
    if category:
        query["category"] = category
    if featured is not None:
        query["featured"] = featured
    
    products = await db.products.find(query, {"_id": 0}).to_list(1000)
    
    for product in products:
        if isinstance(product.get('created_at'), str):
            product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if isinstance(product.get('created_at'), str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return product

@api_router.post("/products", response_model=Product)
async def create_product(product_input: ProductCreate):
    product_dict = product_input.model_dump()
    product_obj = Product(**product_dict)
    
    doc = product_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.products.insert_one(doc)
    return product_obj

@api_router.get("/categories")
async def get_categories():
    categories = await db.products.distinct("category")
    return {"categories": categories}

# Quote request routes
@api_router.post("/quote-requests", response_model=QuoteRequest)
async def create_quote_request(quote_input: QuoteRequestCreate):
    quote_dict = quote_input.model_dump()
    quote_obj = QuoteRequest(**quote_dict)
    
    doc = quote_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.quote_requests.insert_one(doc)
    return quote_obj

@api_router.get("/quote-requests", response_model=List[QuoteRequest])
async def get_quote_requests():
    quotes = await db.quote_requests.find({}, {"_id": 0}).to_list(1000)
    
    for quote in quotes:
        if isinstance(quote.get('created_at'), str):
            quote['created_at'] = datetime.fromisoformat(quote['created_at'])
    
    return quotes

# Contact message routes
@api_router.post("/contact", response_model=ContactMessage)
async def create_contact_message(contact_input: ContactMessageCreate):
    contact_dict = contact_input.model_dump()
    contact_obj = ContactMessage(**contact_dict)
    
    doc = contact_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.contact_messages.insert_one(doc)
    return contact_obj

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
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