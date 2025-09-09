
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
    tier: str = Field(..., description="Tier of the course, S, A, B, C")

class CourseListRequest(BaseModel):
    course_list: List[Course] = Field(..., description="List of available courses")