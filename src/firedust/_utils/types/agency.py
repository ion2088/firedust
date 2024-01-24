from pydantic import BaseModel
from typing import List


class ScheduledTask(BaseModel):
    task: str
    schedule: str


class WorkflowConfig(BaseModel):
    name: str
    description: str
    tasks: List[str]
    schedule: str
