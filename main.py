import os
import time
import asyncio
from typing import Optional

from dotenv import load_dotenv
from datamodels import CourseListRequest

from fastapi import FastAPI,Request, Form
from fastapi.middleware.cors import CORSMiddleware




load_dotenv()
is_production = os.getenv("ENVIRONMENT") == "production"


app = FastAPI(
    root_path="/profile-finder-api",
    title="Profile Finder API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/find-profile")
async def find_profile(
    request: Request,
    profile_req: CourseListRequest
):
    final_mass = {'insan_sarrafi':0 , 
                  'kultur_mantari':0 , 
                  'vizyoner':0 , 
                  'cok_yonlu':0 , 
                  'hedef_odakli':0 , 
                  'teknoloji_gurusu':0 , 
                  'kisisel_gelisim':0}
    
    for course in profile_req.course_list:
        if course.tier == "S":
            print("S TIER COURSE DETECTED")
            for profile_id, mass in course.profile_mass.items():
                final_mass[profile_id] += mass
        elif course.tier == "A":
            print("A TIER COURSE DETECTED")
            for profile_id, mass in course.profile_mass.items():
                final_mass[profile_id] += mass * 0.75
        elif course.tier == "B":
            print("B TIER COURSE DETECTED")
            for profile_id, mass in course.profile_mass.items():
                final_mass[profile_id] += mass * 0.3
        elif course.tier == "C":
            print("C TIER COURSE DETECTED")
            for profile_id, mass in course.profile_mass.items():
                final_mass[profile_id] += mass * 0.1
    print("FINAL MASS:",final_mass)

    

    return {"message": "dummy", "data": profile_req}
#endregion

