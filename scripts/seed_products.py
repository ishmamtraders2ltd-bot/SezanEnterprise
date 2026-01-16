import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / 'backend' / '.env')

async def seed_products():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Clear existing products
    await db.products.delete_many({})
    
    products = [
        {
            "id": "prod-001",
            "name": "R410A Refrigerant Gas",
            "category": "Refrigerants",
            "description": "High-purity R410A refrigerant gas suitable for residential and commercial air conditioning systems. Eco-friendly and energy-efficient.",
            "specifications": {
                "Type": "R410A",
                "Weight": "11.3 kg",
                "Purity": "99.9%",
                "Application": "AC Systems",
                "Packaging": "Cylinder"
            },
            "image_url": "https://images.unsplash.com/photo-1654220691341-be23a137bd0c?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Honeywell",
            "featured": True,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-002",
            "name": "Rotary Compressor 1.5 Ton",
            "category": "A/C Spare Parts",
            "description": "High-efficiency rotary compressor for 1.5 ton air conditioning units. Low noise operation and long service life.",
            "specifications": {
                "Capacity": "1.5 Ton",
                "Type": "Rotary",
                "Voltage": "220-240V",
                "Frequency": "50Hz",
                "Refrigerant": "R410A/R22"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "GMCC",
            "featured": True,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-003",
            "name": "Copper Tube 1/4 inch",
            "category": "Fridge Spare Parts",
            "description": "Premium quality copper tubing for refrigeration and air conditioning applications. Corrosion-resistant and durable.",
            "specifications": {
                "Size": "1/4 inch",
                "Material": "Pure Copper",
                "Length": "15 meters",
                "Wall Thickness": "0.8mm",
                "Usage": "Refrigeration Piping"
            },
            "image_url": "https://images.unsplash.com/photo-1648031740182-a2dee4978eb7?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Mueller",
            "featured": True,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-004",
            "name": "R134A Refrigerant Gas",
            "category": "Refrigerants",
            "description": "R134A refrigerant for automotive and commercial refrigeration. HFC-based, non-ozone depleting.",
            "specifications": {
                "Type": "R134A",
                "Weight": "13.6 kg",
                "Purity": "99.9%",
                "Application": "Automotive AC, Commercial Refrigeration",
                "Packaging": "Cylinder"
            },
            "image_url": "https://images.unsplash.com/photo-1654220691341-be23a137bd0c?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "DuPont",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-005",
            "name": "Condenser Coil 2 Ton",
            "category": "A/C Spare Parts",
            "description": "High-efficiency condenser coil for 2 ton AC units. Copper tubing with aluminum fins for optimal heat transfer.",
            "specifications": {
                "Capacity": "2 Ton",
                "Material": "Copper/Aluminum",
                "Tube Diameter": "7mm",
                "Fin Spacing": "1.5mm",
                "Dimensions": "800x600mm"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Sanhua",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-006",
            "name": "Evaporator Coil 1.5 Ton",
            "category": "A/C Spare Parts",
            "description": "Premium evaporator coil for split AC systems. Excellent cooling performance and corrosion resistance.",
            "specifications": {
                "Capacity": "1.5 Ton",
                "Material": "Copper",
                "Type": "Indoor Unit",
                "Tube Diameter": "7mm",
                "Coating": "Blue Fin"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Zhejiang",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-007",
            "name": "Refrigerator Thermostat Universal",
            "category": "Fridge Spare Parts",
            "description": "Universal refrigerator thermostat suitable for most brands. Accurate temperature control.",
            "specifications": {
                "Type": "Mechanical",
                "Temperature Range": "-35°C to +35°C",
                "Voltage": "220V",
                "Compatibility": "Universal",
                "Connection": "3-Pin"
            },
            "image_url": "https://images.unsplash.com/photo-1648031740182-a2dee4978eb7?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Danfoss",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-008",
            "name": "R22 Refrigerant Gas",
            "category": "Refrigerants",
            "description": "R22 refrigerant for older AC and refrigeration systems. HCFC-based, widely compatible.",
            "specifications": {
                "Type": "R22",
                "Weight": "13.6 kg",
                "Purity": "99.8%",
                "Application": "Legacy AC Systems",
                "Packaging": "Cylinder"
            },
            "image_url": "https://images.unsplash.com/photo-1654220691341-be23a137bd0c?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Chemours",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-009",
            "name": "Compressor 2 Ton Scroll Type",
            "category": "A/C Spare Parts",
            "description": "High-efficiency scroll compressor for commercial AC applications. Quiet operation and reliable performance.",
            "specifications": {
                "Capacity": "2 Ton",
                "Type": "Scroll",
                "Voltage": "380-420V",
                "Frequency": "50Hz",
                "Refrigerant": "R410A"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Copeland",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-010",
            "name": "Expansion Valve 1.5 Ton",
            "category": "A/C Spare Parts",
            "description": "Thermostatic expansion valve for precise refrigerant flow control. Brass construction for durability.",
            "specifications": {
                "Capacity": "1.5 Ton",
                "Type": "TXV",
                "Material": "Brass",
                "Connection": "1/4 inch",
                "Temperature Range": "-40°C to +10°C"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Emerson",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-011",
            "name": "Filter Drier Universal",
            "category": "A/C Spare Parts",
            "description": "Universal filter drier for removing moisture and contaminants from refrigeration systems.",
            "specifications": {
                "Type": "Solid Core",
                "Connection": "1/4 inch SAE",
                "Capacity": "5 Ton",
                "Material": "Copper",
                "Length": "150mm"
            },
            "image_url": "https://images.unsplash.com/photo-1734178832989-1a1617d7d983?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Alco",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": "prod-012",
            "name": "Defrost Timer Universal",
            "category": "Fridge Spare Parts",
            "description": "Universal defrost timer for refrigerators and freezers. 6-hour cycle with manual advance.",
            "specifications": {
                "Cycle Time": "6 Hours",
                "Voltage": "220V",
                "Type": "Mechanical",
                "Compatibility": "Universal",
                "Mounting": "Panel Mount"
            },
            "image_url": "https://images.unsplash.com/photo-1648031740182-a2dee4978eb7?crop=entropy&cs=srgb&fm=jpg&q=85",
            "brand": "Paragon",
            "featured": False,
            "created_at": "2025-01-01T00:00:00Z"
        }
    ]
    
    await db.products.insert_many(products)
    print(f"Successfully seeded {len(products)} products")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_products())
