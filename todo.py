import discord
import datetime
import pytz

# List of completion status emojis
complist = [":stop_button:", ":white_check_mark:", ":red_square:"]

class Task:
    """Represents a task with description, completion status, and due date."""
    description: str
    done: bool
    due: datetime.datetime

    def __init__(self, desc: str = "", duedate: datetime.datetime = None):
        """
        Initialize a new Task.

        Args:
            desc (str): The description of the task.
            duedate (datetime.datetime): The due date of the task.
        """
        self.description = desc
        self.due = duedate
        self.done = False
    
    def IsDue(self) -> bool:
        """
        Check if the task is due.

        Returns:
            bool: True if the task is due or overdue, False otherwise.
        """
        try:
            return self.due <= datetime.datetime.now()
        except:
            return False

    def SetDone(self, set: bool):
        """
        Set the completion status of the task.

        Args:
            set (bool): The new completion status.
        """
        self.done = set
    
    def SetDescription(self, desc: str):
        """
        Set the description of the task.

        Args:
            desc (str): The new description.
        """
        self.description = desc
    
    def TimeRemaining(self) -> str:
        """
        Calculate the time remaining until the task is due.

        Returns:
            str: A string representation of the time remaining or "OVERDUE" if the task is past due.
        """
        if self.IsDue():
            return "OVERDUE"
        
        time_remaining = self.due - datetime.datetime.now()
        days, seconds = time_remaining.days, time_remaining.seconds
        hours, minutes = seconds // 3600, (seconds % 3600) // 60
        
        tr_str = ""
        if days:
            tr_str += f"{days}d "
        if hours:
            tr_str += f"{hours}h "
        if minutes:
            tr_str += f"{minutes}m "
        
        return tr_str.strip()

class UserAccount:
    """Represents a user account with a list of tasks."""
    tasks: list[Task]
    userID: discord.User.id

    def __init__(self, userid: discord.User.id, new_task: Task = None):
        """
        Initialize a new UserAccount.

        Args:
            userid (discord.User.id): The ID of the user.
            new_task (Task, optional): An initial task to add to the user's list.
        """
        self.userID = userid
        self.tasks = []
        if new_task:
            self.tasks.append(new_task)
    
    def IsValidTask(self, task_id: int) -> bool:
        """
        Check if a task ID is valid for this user's task list.

        Args:
            task_id (int): The ID of the task to check.

        Returns:
            bool: True if the task ID is valid, False otherwise.
        """
        return 0 <= task_id < len(self.tasks)
    
    def DelTask(self, task_id: int) -> None:
        """
        Delete a task from the user's list of tasks.

        Args:
            task_id (int): The ID of the task to delete.
        """
        if self.IsValidTask(task_id):
            del self.tasks[task_id]
    
    def AddTask(self, new_task: Task):
        """
        Add a task to the user's list of tasks.

        Args:
            new_task (Task): The task to add.
        """
        self.tasks.append(new_task)
    
    def GetTask(self, index: int) -> Task:
        """
        Get a task from the user's list of tasks.

        Args:
            index (int): The index of the task to retrieve.

        Returns:
            Task: The task at the specified index, or None if the index is invalid.
        """
        return self.tasks[index] if self.IsValidTask(index) else None
    
    def GetId(self) -> int:
        """
        Get the user's ID.

        Returns:
            int: The user's ID.
        """
        return self.userID
    
    def GetTasks(self) -> list[Task]:
        """
        Get the user's list of tasks.

        Returns:
            list[Task]: The user's list of tasks.
        """
        return self.tasks
