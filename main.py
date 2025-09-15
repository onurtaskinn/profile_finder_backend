import os
import time
import asyncio
from typing import Optional

from dotenv import load_dotenv
from utils.datamodels import CourseListRequest, FindProfileResponse

from fastapi import FastAPI, HTTPException,Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from utils.helper_functions import call_personalized_message_generator
from utils.profile_types import PROFILE_TYPES




load_dotenv()
is_production = os.getenv("ENVIRONMENT") == "production"


app = FastAPI(
    title="Profile Finder API",
    version="1.0.0"
)

app.mount("/images", StaticFiles(directory="images"), name="images")

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
                  'teknoloji_gurusu':0 , 
                  'kisisel_gelisen':0}
    
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



# Add these imports to your main.py
import uuid
from utils.course_loader import load_courses_data, group_courses_by_type, select_balanced_courses, transform_course_data
from utils.datamodels import TournamentCoursesResponse, TournamentCourse

# Add this new endpoint to your FastAPI app
@app.get("/get-tournament-courses")
async def get_tournament_courses():
    """
    Select 16 balanced courses for tournament:
    - 3 courses from each of 4 profile types
    - 4 courses from 1 randomly selected profile type
    Total: 16 courses
    """
    try:
        # Load all courses from data.json
        all_courses = load_courses_data()

        # Yin Yoga ile Masabaşı Esneme Molası: Bedeninizi ve Zihninizi Yenileyin #
        
        # Group courses by their primary profile type
        grouped_courses = group_courses_by_type(all_courses)
        
        # Log the distribution for debugging
        print("Course distribution by type:")
        for profile_type, courses in grouped_courses.items():
            print(f"  {profile_type}: {len(courses)} courses")
        
        # Select balanced courses
        selected_courses = select_balanced_courses(grouped_courses)
        
        if len(selected_courses) < 16:
            print(f"Warning: Only {len(selected_courses)} courses selected, expected 16")
        
        # Transform courses to API format
        tournament_courses = []
        for i, course in enumerate(selected_courses, 1):
            transformed_course = transform_course_data(course, i)
            tournament_courses.append(TournamentCourse(**transformed_course))
        
        # Generate unique tournament ID
        tournament_id = str(uuid.uuid4())
        
        response = TournamentCoursesResponse(
            tournament_id=tournament_id,
            courses=tournament_courses
        )
        
        print(f"Tournament {tournament_id} created with {len(tournament_courses)} courses")
        return response
        
    except Exception as e:
        print(f"Error creating tournament: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating tournament: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

