import asyncio
import sys
from bson import ObjectId

sys.path.insert(0, "/app")

from app.database.client import get_db


# Indian States and UTs with their zones
STATES_DATA = [
    # North Zone
    {"name": "Jammu and Kashmir", "code": "JK", "capital": "Srinagar/Jammu", "zone": "North"},
    {"name": "Himachal Pradesh", "code": "HP", "capital": "Shimla", "zone": "North"},
    {"name": "Punjab", "code": "PB", "capital": "Chandigarh", "zone": "North"},
    {"name": "Uttarakhand", "code": "UK", "capital": "Dehradun", "zone": "North"},
    {"name": "Haryana", "code": "HR", "capital": "Chandigarh", "zone": "North"},
    {"name": "Delhi", "code": "DL", "capital": "Delhi", "zone": "North"},
    {"name": "Chandigarh", "code": "CH", "capital": "Chandigarh", "zone": "North"},
    
    # South Zone
    {"name": "Andhra Pradesh", "code": "AP", "capital": "Amaravati", "zone": "South"},
    {"name": "Telangana", "code": "TS", "capital": "Hyderabad", "zone": "South"},
    {"name": "Karnataka", "code": "KA", "capital": "Bengaluru", "zone": "South"},
    {"name": "Kerala", "code": "KL", "capital": "Thiruvananthapuram", "zone": "South"},
    {"name": "Tamil Nadu", "code": "TN", "capital": "Chennai", "zone": "South"},
    {"name": "Puducherry", "code": "PY", "capital": "Puducherry", "zone": "South"},
    
    # East Zone
    {"name": "Bihar", "code": "BR", "capital": "Patna", "zone": "East"},
    {"name": "Jharkhand", "code": "JH", "capital": "Ranchi", "zone": "East"},
    {"name": "Odisha", "code": "OD", "capital": "Bhubaneswar", "zone": "East"},
    {"name": "West Bengal", "code": "WB", "capital": "Kolkata", "zone": "East"},
    {"name": "Sikkim", "code": "SK", "capital": "Gangtok", "zone": "East"},
    
    # West Zone
    {"name": "Rajasthan", "code": "RJ", "capital": "Jaipur", "zone": "West"},
    {"name": "Gujarat", "code": "GJ", "capital": "Gandhinagar", "zone": "West"},
    {"name": "Maharashtra", "code": "MH", "capital": "Mumbai", "zone": "West"},
    {"name": "Goa", "code": "GA", "capital": "Panaji", "zone": "West"},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "code": "DN", "capital": "Daman", "zone": "West"},
    
    # Central Zone
    {"name": "Madhya Pradesh", "code": "MP", "capital": "Bhopal", "zone": "Central"},
    {"name": "Chhattisgarh", "code": "CG", "capital": "Raipur", "zone": "Central"},
    {"name": "Uttar Pradesh", "code": "UP", "capital": "Lucknow", "zone": "Central"},
    
    # Northeast Zone
    {"name": "Arunachal Pradesh", "code": "AR", "capital": "Itanagar", "zone": "Northeast"},
    {"name": "Assam", "code": "AS", "capital": "Dispur", "zone": "Northeast"},
    {"name": "Manipur", "code": "MN", "capital": "Imphal", "zone": "Northeast"},
    {"name": "Meghalaya", "code": "ML", "capital": "Shillong", "zone": "Northeast"},
    {"name": "Mizoram", "code": "MZ", "capital": "Aizawl", "zone": "Northeast"},
    {"name": "Nagaland", "code": "NL", "capital": "Kohima", "zone": "Northeast"},
    {"name": "Tripura", "code": "TR", "capital": "Agartala", "zone": "Northeast"},
]

# Sample districts for a few states (full list would have all districts)
DISTRICTS_DATA = [
    # Delhi
    {"name": "Central Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110001-110006"},
    {"name": "East Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110092-110096"},
    {"name": "New Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110001-110003"},
    {"name": "North Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110006-110054"},
    {"name": "South Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110014-110065"},
    {"name": "West Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110018-110087"},
    {"name": "North East Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110032-110053"},
    {"name": "North West Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110034-110089"},
    {"name": "South West Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110043-110075"},
    {"name": "South East Delhi", "state_code": "DL", "std_code": "11", "pin_code_range": "110044-110096"},
    {"name": "Shahdara", "state_code": "DL", "std_code": "11", "pin_code_range": "110032-110094"},
    
    # Maharashtra
    {"name": "Mumbai City", "state_code": "MH", "std_code": "22", "pin_code_range": "400001-400004"},
    {"name": "Mumbai Suburban", "state_code": "MH", "std_code": "22", "pin_code_range": "400053-400107"},
    {"name": "Pune", "state_code": "MH", "std_code": "20", "pin_code_range": "411001-411060"},
    {"name": "Nagpur", "state_code": "MH", "std_code": "712", "pin_code_range": "440001-440036"},
    {"name": "Thane", "state_code": "MH", "std_code": "22", "pin_code_range": "400601-400615"},
    {"name": "Nashik", "state_code": "MH", "std_code": "253", "pin_code_range": "422001-422013"},
    {"name": "Aurangabad", "state_code": "MH", "std_code": "240", "pin_code_range": "431001-431009"},
    {"name": "Kolhapur", "state_code": "MH", "std_code": "231", "pin_code_range": "416001-416013"},
    
    # Karnataka
    {"name": "Bengaluru Urban", "state_code": "KA", "std_code": "80", "pin_code_range": "560001-560109"},
    {"name": "Bengaluru Rural", "state_code": "KA", "std_code": "80", "pin_code_range": "560063-560099"},
    {"name": "Mysuru", "state_code": "KA", "std_code": "821", "pin_code_range": "570001-570028"},
    {"name": "Hubballi-Dharwad", "state_code": "KA", "std_code": "836", "pin_code_range": "580001-580032"},
    {"name": "Kalaburagi", "state_code": "KA", "std_code": "8472", "pin_code_range": "585101-585132"},
    {"name": "Mangaluru", "state_code": "KA", "std_code": "824", "pin_code_range": "575001-575030"},
    {"name": "Belagavi", "state_code": "KA", "std_code": "831", "pin_code_range": "590001-590016"},
    
    # Tamil Nadu
    {"name": "Chennai", "state_code": "TN", "std_code": "44", "pin_code_range": "600001-600130"},
    {"name": "Coimbatore", "state_code": "TN", "std_code": "422", "pin_code_range": "641001-641049"},
    {"name": "Madurai", "state_code": "TN", "std_code": "452", "pin_code_range": "625001-625028"},
    {"name": "Tiruchirappalli", "state_code": "TN", "std_code": "431", "pin_code_range": "620001-620024"},
    {"name": "Salem", "state_code": "TN", "std_code": "427", "pin_code_range": "636001-636016"},
    {"name": "Tirunelveli", "state_code": "TN", "std_code": "462", "pin_code_range": "627001-627011"},
    
    # Uttar Pradesh
    {"name": "Lucknow", "state_code": "UP", "std_code": "522", "pin_code_range": "226001-226029"},
    {"name": "Kanpur Nagar", "state_code": "UP", "std_code": "512", "pin_code_range": "208001-208027"},
    {"name": "Agra", "state_code": "UP", "std_code": "562", "pin_code_range": "282001-282013"},
    {"name": "Varanasi", "state_code": "UP", "std_code": "542", "pin_code_range": "221001-221010"},
    {"name": "Prayagraj", "state_code": "UP", "std_code": "532", "pin_code_range": "211001-211018"},
    {"name": "Ghaziabad", "state_code": "UP", "std_code": "120", "pin_code_range": "201001-201012"},
    {"name": "Noida", "state_code": "UP", "std_code": "120", "pin_code_range": "201301-201313"},
    
    # West Bengal
    {"name": "Kolkata", "state_code": "WB", "std_code": "33", "pin_code_range": "700001-700157"},
    {"name": "Howrah", "state_code": "WB", "std_code": "33", "pin_code_range": "711101-711204"},
    {"name": "North 24 Parganas", "state_code": "WB", "std_code": "33", "pin_code_range": "743100-743452"},
    {"name": "South 24 Parganas", "state_code": "WB", "std_code": "33", "pin_code_range": "743337-743502"},
    {"name": "Darjeeling", "state_code": "WB", "std_code": "354", "pin_code_range": "734101-734229"},
    
    # Gujarat
    {"name": "Ahmedabad", "state_code": "GJ", "std_code": "79", "pin_code_range": "380001-380063"},
    {"name": "Surat", "state_code": "GJ", "std_code": "261", "pin_code_range": "395001-395010"},
    {"name": "Vadodara", "state_code": "GJ", "std_code": "265", "pin_code_range": "390001-390025"},
    {"name": "Rajkot", "state_code": "GJ", "std_code": "281", "pin_code_range": "360001-360011"},
    {"name": "Bhavnagar", "state_code": "GJ", "std_code": "278", "pin_code_range": "364001-364005"},
    
    # Rajasthan
    {"name": "Jaipur", "state_code": "RJ", "std_code": "141", "pin_code_range": "302001-302034"},
    {"name": "Jodhpur", "state_code": "RJ", "std_code": "291", "pin_code_range": "342001-342015"},
    {"name": "Udaipur", "state_code": "RJ", "std_code": "294", "pin_code_range": "313001-313027"},
    {"name": "Kota", "state_code": "RJ", "std_code": "744", "pin_code_range": "324001-324010"},
    {"name": "Ajmer", "state_code": "RJ", "std_code": "145", "pin_code_range": "305001-305022"},
]

# Beneficiary Categories
BENEFICIARY_CATEGORIES_DATA = [
    {"name": "Below Poverty Line (BPL)", "code": "BPL", "description": "Families below poverty line as per government criteria", "icon": "bpl"},
    {"name": "Senior Citizen", "code": "SC", "description": "Individuals aged 60 years and above", "icon": "senior"},
    {"name": "Child", "code": "CH", "description": "Children below 18 years of age", "icon": "child"},
    {"name": "Woman", "code": "WM", "description": "Female beneficiaries", "icon": "woman"},
    {"name": "Differently Abled", "code": "DA", "description": "Persons with disabilities (40% or more)", "icon": "disability"},
    {"name": "General", "code": "GN", "description": "General category without specific criteria", "icon": "general"},
]

# Dental Services
DENTAL_SERVICES_DATA = [
    {"name": "Extraction", "code": "EXT", "category": "Surgical"},
    {"name": "Filling", "code": "FL", "category": "Restorative"},
    {"name": "Scaling", "code": "SC", "category": "Preventive"},
    {"name": "Dentures", "code": "DN", "category": "Restorative"},
    {"name": "Orthodontics", "code": "ORT", "category": "Cosmetic"},
    {"name": "X-Ray", "code": "XR", "category": "Diagnostic"},
    {"name": "Root Canal Treatment", "code": "RCT", "category": "Restorative"},
    {"name": "Teeth Cleaning", "code": "TC", "category": "Preventive"},
    {"name": "Teeth Whitening", "code": "TW", "category": "Cosmetic"},
    {"name": "Crowns and Bridges", "code": "CB", "category": "Restorative"},
    {"name": "Dental Implants", "code": "DI", "category": "Surgical"},
    {"name": "Gum Surgery", "code": "GS", "category": "Surgical"},
    {"name": "Fluoride Treatment", "code": "FT", "category": "Preventive"},
    {"name": "Dental Sealants", "code": "DS", "category": "Preventive"},
    {"name": "Veneers", "code": "VN", "category": "Cosmetic"},
]


async def seed_states():
    db = get_db()
    
    # Check if states already exist
    existing_count = await db["states"].count_documents({})
    if existing_count > 0:
        print(f"States already seeded ({existing_count} records). Skipping.")
        return
    
    # Insert states
    for state in STATES_DATA:
        await db["states"].insert_one({
            **state,
            "active": True,
            "created_at": "2026-01-01T00:00:00Z"
        })
    
    print(f"Seeded {len(STATES_DATA)} states.")


async def seed_districts():
    db = get_db()
    
    # Get state code to ID mapping
    states = await db["states"].find({"active": True}).to_list(None)
    state_code_to_id = {state["code"]: str(state["_id"]) for state in states}
    
    # Check if districts already exist
    existing_count = await db["districts"].count_documents({})
    if existing_count > 0:
        print(f"Districts already seeded ({existing_count} records). Skipping.")
        return
    
    # Insert districts
    for district in DISTRICTS_DATA:
        state_id = state_code_to_id.get(district["state_code"])
        if state_id:
            await db["districts"].insert_one({
                "name": district["name"],
                "state_id": state_id,
                "std_code": district["std_code"],
                "pin_code_range": district["pin_code_range"],
                "active": True,
                "created_at": "2026-01-01T00:00:00Z"
            })
    
    print(f"Seeded {len(DISTRICTS_DATA)} districts.")


async def seed_beneficiary_categories():
    db = get_db()
    
    # Check if categories already exist
    existing_count = await db["beneficiary_categories"].count_documents({})
    if existing_count > 0:
        print(f"Beneficiary categories already seeded ({existing_count} records). Skipping.")
        return
    
    # Insert categories
    for category in BENEFICIARY_CATEGORIES_DATA:
        await db["beneficiary_categories"].insert_one({
            **category,
            "active": True,
            "created_at": "2026-01-01T00:00:00Z"
        })
    
    print(f"Seeded {len(BENEFICIARY_CATEGORIES_DATA)} beneficiary categories.")


async def seed_dental_services():
    db = get_db()
    
    # Check if services already exist
    existing_count = await db["dental_services"].count_documents({})
    if existing_count > 0:
        print(f"Dental services already seeded ({existing_count} records). Skipping.")
        return
    
    # Insert services
    for service in DENTAL_SERVICES_DATA:
        await db["dental_services"].insert_one({
            **service,
            "active": True,
            "created_at": "2026-01-01T00:00:00Z"
        })
    
    print(f"Seeded {len(DENTAL_SERVICES_DATA)} dental services.")


async def main():
    print("Starting master data seeding...")
    await seed_states()
    await seed_districts()
    await seed_beneficiary_categories()
    await seed_dental_services()
    print("Master data seeding completed.")


if __name__ == "__main__":
    asyncio.run(main())
