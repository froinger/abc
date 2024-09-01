from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time
import datetime
import threading

from papa.api.papa_service import scrape_jobs, crawler_status

app = FastAPI()


class Task(BaseModel):
    from_to: list
    start_time: str = None
    frequency: int = 24  # 频率，单位为小时


def schedule_task(task, background_tasks: BackgroundTasks):
    if task.start_time:
        delay = (datetime.datetime.strptime(task.start_time,
                                            "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).total_seconds()
        if delay > 0:
            time.sleep(delay)

    while True:
        scrape_jobs(task)
        time.sleep(task.frequency * 3600)


@app.post("/start_task/")
async def start_task(task: Task, background_tasks: BackgroundTasks):
    background_tasks.add_task(schedule_task, task, background_tasks)
    return {"message": "Task started."}

@app.get("/crawler_status/")
def get_crawler_status():
    return crawler_status


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=18000)
