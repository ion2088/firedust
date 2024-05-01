from typing import List

from pydantic import BaseModel


class ScheduledTask(BaseModel):
    task: str
    schedule: str


class WorkflowConfig(BaseModel):
    name: str
    description: str
    tasks: List[str]
    schedule: str
