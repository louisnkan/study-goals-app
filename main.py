# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Create the FastAPI app
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# add this *right after* you define `app = FastAPI()`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory database
goals_db = []

# Define request body structure
class Goal(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Study Goals API!"}

# Get all goals
@app.get("/goals")
def get_goals():
    return {"goals": goals_db}

# Add a new goal
@app.post("/goals")
def add_goal(goal: Goal):
    goals_db.append(goal.dict())
    return {"message": "Goal added successfully!", "goal": goal}

# Mark a goal as completed
@app.put("/goals/{goal_index}")
def update_goal(goal_index: int):
    if 0 <= goal_index < len(goals_db):
        goals_db[goal_index]["completed"] = True
        return {"message": "Goal updated!", "goal": goals_db[goal_index]}
    return {"error": "Invalid goal index"}

# Delete a goal
@app.delete("/goals/{goal_index}")
def delete_goal(goal_index: int):
    if 0 <= goal_index < len(goals_db):
        removed = goals_db.pop(goal_index)
        return {"message": "Goal deleted!", "goal": removed}
    return {"error": "Invalid goal index"}
