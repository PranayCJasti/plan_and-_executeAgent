from enum import Enum

class Status(Enum):
    """
    An enumeration representing the various states a task or project can be in.

    This class is used to track the progress of a task or project. The states 
    include 'NEW', 'AWAITING', 'INPROGRESS', 'ABANDONED', and 'DONE'. These 
    states help in identifying the current status of a task or project.

    Attributes:
        NONE (str): Represents the task is empty.
        NEW (str): Represents the initial state of a task or project.
        AWAITING (str): Represents the state when a task or project is waiting
          for some event or dependency.
        INPROGRESS (str): Represents the state when a task or project is 
          currently being worked on.
        ABANDONED (str): Represents the state when a task or project has been 
          left incomplete.
        DONE (str): Represents the state when a task or project has been 
          completed.
    """
    NONE: str = "NONE"
    NEW: str = "NEW"
    AWAITING: str = "AWAITING"
    INPROGRESS: str = "INPROGRESS"
    ABANDONED: str = "ABANDONED"
    DONE: str = "DONE"

    def __str__(self):
        """
        Returns the string representation of the Enum member.

        Returns:
            str: The value of the Enum member.
        """
        return self.value