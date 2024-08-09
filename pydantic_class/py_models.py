"""
This module, `models.py`, contains various data models used throughout the project.

Each class in this module represents a different data model, with each model 
capturing a specific set of information required for the project. These models
are used to structure the data in a consistent and organized manner, enhancing 
the readability and maintainability of the code.
"""
from typing_extensions import ClassVar

from pydantic import Field, BaseModel
from models.constants import Status

class Task(BaseModel):
    """
    A data model representing a task and its current state within a project
    or workflow.
    """

    description: str = Field(
        description="A brief description outlining the objective of the task",
        default="",
        required=True
    )

    task_status: Status = Field(
        description="The current status indicating the progress of the task",
        default= Status.NONE,
        required=True
    )

    query_answered: bool = Field(
        description="A boolean flag indicating whether the task has been answered",
        default=False
    )

    additional_info: str = Field(
        description="Additional info requested.",
        default=""
    )

    question: str = Field(
        description="Question to supervisor if additional information is needed"
        " to proceed with task execution.",
        default=""
    )
