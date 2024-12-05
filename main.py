import todo
import discord
import datetime
import os
import pytz
import utils
import singletons
import dotenv
from saveload import SaveAccounts, LoadAccounts

class Client(discord.Client):
    async def Save(self):
        # Save accounts before closing
        SaveAccounts(singletons.account_list)
        print("Saved!")

    async def close(self):
        # Perform cleanup before closing
        await self.Save()
        
        # Call the parent class's close method
        await super().close()


# Set up Discord intents
intents = discord.Intents.all()
client = Client(intents=intents)


# Define command prefix and separator
MASTER_PREFIX = ">"
MASTER_SEPERATOR = "|"

# Help message dictionary
HELP_MSG = {
    '>help': 'Displays available commands\n ``>help <command>`` (to see more details about a command)',
    '>new': 'Creates a new task with description and duration\n ``>new <description> | <duration>`` (duration format: ``10M 1H 1D``)',
    '>edit': 'Edits an existing task by index\n ``>edit <index> | <new_description>``',
    '>complete': 'Marks a task as complete by index\n ``>complete <index>``',
    '>delete': 'Deletes a task by index\n ``>delete <index>``',
    '>show': 'Displays details of a specific task by index\n ``>show <index>``',
    '>showall': 'Displays all tasks'
}
ACCEPTED_TIMEFORMAT = "%I:%M"

loaded = False

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    global loaded
    
    if os.path.exists("userdata/user_accounts.json") and not loaded:
       # Load accounts from file if it exists
       singletons.account_list = LoadAccounts()
       loaded = True

       print("All tasks loaded successfully!")

    elif not os.path.exists("userdata/user_accounts.json"):
        loaded = True

@client.event
async def on_message(message : discord.Message):
    global loaded
    
    # Ignore bot's own messages
    if message.author == client.user:
        return
    
    if not message.content:
        return

    # Check if the message is a command and tasks are loaded
    if message.content[0] == MASTER_PREFIX and loaded:
       await InvokeTODO(message)
    elif message.content[0] == MASTER_PREFIX and not loaded:
        await utils.ExceptionReplyEmbed(message=message, error="Error: Tasks not loaded yet.", desc="Please wait a few seconds and try again.")

async def InvokeTODO(message : discord.Message):
    # Parse the command and execute the corresponding action
    command = message.content.strip(MASTER_PREFIX).split(" ")
    await ExecuteAction(command=command, message=message)

async def ExecuteAction(command : list[str], message : discord.Message):
    # Execute the appropriate action based on the command
    action = command[0].lower()
    command.pop(0)

    match action:
        case "help":
            await Help(command=command,message=message)
        case "new":
            newcommand = " ".join(command)
            await NewTask(command=newcommand,message=message)
        case "complete":
            try:
                await CompleteTask(task_id=int(command[0])-1,message=message)
            except IndexError:
                await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        case "delete":
            try:
                await DeleteTask(task_id=int(command[0])-1,message=message)
            except IndexError:
                await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        case "del":
            try:
                await DeleteTask(task_id=int(command[0])-1,message=message)
            except IndexError:
                await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        case "delall":
            await DeleteAllTasks(message=message)
        case "deleteall":
            await DeleteAllTasks(message=message)
        case "show":
            try:
                await ShowTask(task_id=int(command[0])-1,message=message)
            except IndexError:
                await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        case "showall":
            await ShowAllTasks(message=message)
        case "edit":
            await EditTask(command=command,message=message)
        case _:
            await utils.ExceptionReplyEmbed(error=f"Invalid action `'{action}'`",desc="use `>help` to see the list of valid actions.")

async def Help(command: list[str], message: discord.Message):
    """Displays available commands."""
    # Create an embed with all available commands
    if not len(command):
        embed = discord.Embed(title="Available Commands", color=0x6abe30)
    
        for cmd, description in HELP_MSG.items():
            embed.add_field(name=cmd, value=description, inline=False)
        await message.reply(embed=embed)
    
    # Show detailed help for a specific command
    elif len(command) == 1:
    
        if command[0] not in HELP_MSG and MASTER_PREFIX+command[0] not in HELP_MSG: # checks regular command and command with MASTER_PREFIX
            return
    
        if MASTER_PREFIX not in command[0]: # adds MASTER_PREFIX to command if not present so that it can be found in HELP_MSG
            command[0] = MASTER_PREFIX+command[0]
        
        embed = discord.Embed(title=f"Command: {command[0]}", color=0x6abe30)
        embed.add_field(name="Description", value=HELP_MSG[command[0]], inline=False)
        await message.reply(embed=embed)
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error", desc="Invalid Arguments, `>help` doesn't take any arguments.")


async def NewTask(command: str, message: discord.Message):
    """Creates a new task with description and duration."""

    # Find or create a user account
    acc_indx = utils.FindValidUser(message.author.id)

    if acc_indx < 0:  # instantiate and append new account
        new_acc = todo.UserAccount(userid=message.author.id)
        singletons.account_list.append(new_acc)
        acc_indx = len(singletons.account_list) - 1

    command_parts = command.split(MASTER_SEPERATOR)

    # Create new task
    acc = singletons.account_list[acc_indx]
    new_task = todo.Task(command_parts[0])
    new_task.due = None

    if len(command_parts) == 2:
        # Parse duration if provided
        duration = command_parts[1].strip().split()
        new_task.due = datetime.datetime.now()
        valid_duration = False
        
        for timecode in duration:
            num = ''.join(filter(str.isdigit, timecode))
            letter = timecode[-1].upper()
            
            if num and letter in ['M', 'H', 'D']:
                num = int(num)
                if (letter == 'M' and 0 < num <= 43200) or \
                   (letter == 'H' and num <= 720) or \
                   (letter == 'D' and num <= 30):
                    new_task.due += datetime.timedelta(**{
                        'M': {'minutes': num},
                        'H': {'hours': num},
                        'D': {'days': num}
                    }[letter])
                    valid_duration = True
        
        if not valid_duration:
            new_task.due = None

    # Create and send embed for new task
    embed = discord.Embed(
        title="New Task Created",
        description=f"Due Date: {new_task.due}" if new_task.due else "",
        color=0x6abe30
    )
    await message.reply(embed=embed)
    acc.tasks.append(new_task)
    await message.add_reaction('✅')
    
async def ShowTask(task_id: int, message : discord.Message):
    """Shows a single task."""
    userid = message.author.id
    useracc = None

    if task_id <= -1:
        await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        return
    
    if utils.GetAcc(userid):
        useracc = utils.GetAcc(userid)
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error: You have no tasks to show.", desc="Use `>new` to create a new task.")
        return

    try:
        usertask = useracc.tasks[task_id]
    except IndexError:
        await utils.ExceptionReplyEmbed(message=message, error= "Error: Invalid task ID.", desc="Use `>showall` to see all your tasks and their IDs")
        return
    
    # Create and send embed for the task
    embed = discord.Embed(color=0x6abe30)
    embed = utils.GetTaskEmbed(task=usertask,task_id=task_id,embed=embed)
    await message.reply(embed=embed)

async def ShowAllTasks(message: discord.Message):
    """Shows all tasks."""
    useracc = utils.GetAcc(message.author.id)
    
    if not useracc:
        await utils.ExceptionReplyEmbed(message=message, error="Error: You have no tasks to show", desc="Use `>new` to create a new task.")
        return
    
    if useracc.tasks:
        # Create and send embed for all tasks
        embed = discord.Embed(color=0x6abe30)
        embed = utils.GetTaskListEmbed(tasks=useracc.tasks,embed=embed)
        await message.reply(embed=embed)
    
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error: You have no tasks to show", desc="Use `>new` to create a new task.")

async def CompleteTask(task_id : str, message : discord.Message):
    """Completes a task."""
    useracc = utils.GetAcc(message.author.id)
    
    if useracc:
        try:
            # Mark task as complete and remove due date
            useracc.tasks[int(task_id)].done = True
            useracc.tasks[int(task_id)].due = None

            embed = discord.Embed(title="Task Completed", description=f"Task {task_id+1} has been marked as complete.", color=0x6abe30)
            await message.reply(embed=embed)
            await message.add_reaction('✅')
        
        except Exception as err:
            await utils.ExceptionReplyEmbed(message=message, error=f"Error: {err}", desc="Please check your task ID and try again.")
            return
   
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error: Task not found", desc="Use `>showall` to see all your tasks and their IDs")

async def EditTask(command : list[str], message : discord.Message):
    """Edits a task."""
    useracc = utils.GetAcc(message.author.id)
    command = " ".join(command)
    command = command.split(MASTER_SEPERATOR)

    try:
        new_desc = command[1]
    except IndexError:
        await utils.ExceptionReplyEmbed(message=message, error="Error: Invalid command format", desc="Use `>edit <task_id> | <new_description>` to edit a task")
        return
    
    task_indx = int(command[0]) -1 # Minus one to offset starting from 0 in any normal list. 
    
    if useracc:
        try:
            if useracc.tasks[task_indx].done:
                await utils.ExceptionReplyEmbed(message=message, error="Error: Task is already completed")
                return
            if useracc.tasks[task_indx].IsDue():
                await utils.ExceptionReplyEmbed(message=message, error="Error: Task is over-due")
                return
    
            # Update task description
            useracc.tasks[task_indx].description = new_desc
    
            embed = discord.Embed(title="Task Edited", description=f"Task {task_indx+1} has been updated.", color=0x6abe30)
            await message.reply(embed=embed)
            await message.add_reaction('✅')
    
        except Exception as err:
            await utils.ExceptionReplyEmbed(message=message, error=f"Run-Time Exception: {err}", desc="Please check your task ID and try again.")
            return
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error: Task not found", desc="Use `>showall` to see all your tasks and their IDs")

async def DeleteTask(task_id: str , message :discord.Message):
    """Deletes a task."""
    try:
        useracc = utils.GetAcc(message.author.id)
        useracc.DelTask(task_id=int(task_id))

        embed = discord.Embed(title="Task Deleted", description=f"Task {task_id+1} has been deleted.", color=0x6abe30)
        await message.reply(embed=embed)
        await message.add_reaction('✅')
    except:
        await utils.ExceptionReplyEmbed(message=message, error="Runtime Exception", desc="Please check your task ID and try again.")

async def DeleteAllTasks(message : discord.Message):
    """Deletes all tasks."""
    useracc = utils.GetAcc(message.author.id)
    if useracc:
        # Delete all tasks in reverse order
        for i in range(len(useracc.tasks)-1,-1,-1):
            useracc.DelTask(task_id=i)
        
        embed = discord.Embed(title="All Tasks Deleted", description="All your tasks have been deleted.", color=0x6abe30)
        await message.reply(embed=embed)
    else:
        await utils.ExceptionReplyEmbed(message=message, error="Error: You have no tasks to delete", desc="Use `>new` to create a new task.")


# If you don't have a token, create one at https://discord.com/developers/applications
# Enter your token in the .env_example file and rename it to .env
dotenv.load_dotenv()
client.run(os.getenv("token"))
