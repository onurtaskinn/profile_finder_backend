
from pydantic import BaseModel, Field
from typing import List

#   {
#     id: 2,
#     name: "Zaman Yönetimi",
#     description: "Zamanı verimli kullanma yöntemleri",
#     image: "./images/zaman_yonetimi.jpg"
#   },


class Course(BaseModel):
    id: int = Field(..., description="Unique identifier for the course")
    name: str = Field(..., description="Name of the course")
    description: str = Field(..., description="Description of the course")
    image: str = Field(..., description="Path to the course image")
    profile_mass: dict = Field(..., description="Profile mass distribution for the course")
    tier: str = Field(..., description="Tier of the course, S, A, B, C")

class CourseListRequest(BaseModel):
    course_list: List[Course] = Field(..., description="List of available courses")


class FindProfileResponse(BaseModel):
    profile_name: str = Field(..., description="Name of the identified profile")
    profile_description: str = Field(..., description="Description of the identified profile")
    all_profiles: dict = Field(..., description="Mass distribution across all profiles")
    # recommended_courses: List[Course] = Field(..., description="List of recommended courses for the identified profile") ### MAYBE
    personalized_message: str = Field(..., description="Personalized message based on the identified profile")


class PersonalizedMessageResponse(BaseModel):
    personalized_message: str = Field(..., description="Personalized message based on the identified profile")