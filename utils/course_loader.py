import json
import random
from typing import List, Dict
from collections import defaultdict

def load_courses_data() -> List[Dict]:
    """Load courses from data.json file"""
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception("data.json file not found")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in data.json")

def get_course_primary_type(course: Dict) -> str:
    """Determine the primary profile type of a course (the one with 1.0 coefficient)"""
    profile_types = ["insan_sarrafi", "kisisel_gelisen", "kultur_mantari", "teknoloji_gurusu", "vizyoner"]
    
    for profile_type in profile_types:
        if course.get(profile_type, 0.0) == 1.0:
            return profile_type
    
    # If no 1.0 found, return the one with highest value
    max_value = 0.0
    max_type = "insan_sarrafi"  # default
    
    for profile_type in profile_types:
        value = course.get(profile_type, 0.0)
        if value > max_value:
            max_value = value
            max_type = profile_type
    
    return max_type

def group_courses_by_type(courses: List[Dict]) -> Dict[str, List[Dict]]:
    """Group courses by their primary profile type"""
    grouped = defaultdict(list)
    
    for course in courses:
        primary_type = get_course_primary_type(course)
        grouped[primary_type].append(course)
    
    return dict(grouped)

def select_balanced_courses(grouped_courses: Dict[str, List[Dict]]) -> List[Dict]:
    """Select 16 courses in a balanced way: 3 from each of 4 types, 4 from one type"""
    profile_types = ["insan_sarrafi", "kisisel_gelisen", "kultur_mantari", "teknoloji_gurusu", "vizyoner"]
    selected_courses = []
    
    # Randomly choose which type gets 4 courses instead of 3
    special_type = random.choice(profile_types)
    
    for profile_type in profile_types:
        available_courses = grouped_courses.get(profile_type, [])
        
        if not available_courses:
            print(f"Warning: No courses found for profile type: {profile_type}")
            continue
        
        # Determine how many courses to select for this type
        courses_to_select = 4 if profile_type == special_type else 3
        
        # Make sure we don't try to select more courses than available
        courses_to_select = min(courses_to_select, len(available_courses))
        
        # Randomly select courses for this type
        selected = random.sample(available_courses, courses_to_select)
        selected_courses.extend(selected)
    
    return selected_courses

def transform_course_data(course: Dict, course_id: int) -> Dict:
    """Transform course data from JSON format to API format"""
    # Create profile_mass dictionary
    profile_mass = {
        "insan_sarrafi": int(course.get("insan_sarrafi", 0.0) * 100),
        "kisisel_gelisen": int(course.get("kisisel_gelisen", 0.0) * 100),
        "kultur_mantari": int(course.get("kultur_mantari", 0.0) * 100),
        "teknoloji_gurusu": int(course.get("teknoloji_gurusu", 0.0) * 100),
        "vizyoner": int(course.get("vizyoner", 0.0) * 100)
    }
    
    return {
        "id": course_id,
        "name": course.get("course_name", ""),
        "description": course.get("course_description", ""),
        "image": f"/images/{course.get('course_code', '')}.jpg",
        "profile_mass": profile_mass
    }