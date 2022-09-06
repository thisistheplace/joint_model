"""
Usage:
------
    uvicorn usage:app --reload
"""

from fastapi import FastAPI

from app.interfaces import Joint

app = FastAPI()


@app.get("/model")
async def model(joint: Joint):
    return joint.schema_json()