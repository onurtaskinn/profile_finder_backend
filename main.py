import os
import time
import asyncio
from typing import Optional

from dotenv import load_dotenv
from utils.datamodels import CourseListRequest, FindProfileResponse

from fastapi import FastAPI,Request, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.helper_functions import call_personalized_message_generator
from utils.profile_types import PROFILE_TYPES




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

    AI_Response, input_tokens, output_tokens = call_personalized_message_generator(final_mass)


    print("AI RESPONSE:",AI_Response.personalized_message)

    
    max = 0
    for key in final_mass:
        if final_mass[key] > max:
            max = final_mass[key]
            profile = key


    profile_name = PROFILE_TYPES[profile]["name"]
    print("IDENTIFIED PROFILE:",profile_name)
    profile_description = PROFILE_TYPES[profile]["description"]
    print("PROFILE DESCRIPTION:",profile_description)

    final_response = FindProfileResponse(
        profile_name=profile_name,
        profile_description=profile_description,
        all_profiles=final_mass,
        personalized_message=AI_Response.personalized_message
    )

    return final_response
#endregion

