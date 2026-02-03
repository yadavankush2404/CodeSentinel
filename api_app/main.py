from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

class PRAnalysis(BaseModel):
    repo_url : str
    pr_num : int
    git_token: Optional[str] = None

@app.post("/start_task")
async def start_endpoint_task(task_req : PRAnalysis):
    data = {
        "repo_url" : task_req.repo_url,
        "pr_num" : task_req.pr_num,
        "git_token" : task_req.git_token
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8001/begin_task/",
            data = data
        )
        if response.status_code != 200:
            return{"message": "Failed to start task", "status": "Failed", "detail": response.text}
    print(data)
    res_data = response.json()

    return {"task_id": res_data.get("task_id"), "status" : res_data.get('status')}

@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://127.0.0.1:8001/task_status_view/{task_id}",
        )
        if response.status_code != 200:
            return {"message": "Failed to fetch", "detail": response.text}
        return response.json()
    
    return {"message": "Something went wrong!!"}