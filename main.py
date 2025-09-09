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
    for course in profile_req.course_list:
        print(course)

    return {"message": "dummy", "data": profile_req}
#endregion

