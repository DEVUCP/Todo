import todo
import discord
import datetime
import os
import pytz
import singletons

def NumIntoEmoji(num: int) -> str:
    """
    Convert a number into emoji representation.

    Args:
        num (int): The number to convert.

    Returns:
        str: The emoji representation of the number.
    """
    # Define a mapping of digits to their corresponding emoji representations
    emoji_map = {
        '0': ':zero:', '1': ':one:', '2': ':two:', '3': ':three:', '4': ':four:',
        '5': ':five:', '6': ':six:', '7': ':seven:', '8': ':eight:', '9': ':nine:'
    }
    # Convert each digit in the number to its emoji representation and join them
    return ''.join(emoji_map[digit] for digit in str(num))

def GetAcc(acc_id : discord.User.id) -> todo.UserAccount:
    """
    Get the user account for the given account ID.

    Args:
        acc_id (discord.User.id): The ID of the account to retrieve.

    Returns:
        todo.UserAccount: The user account if valid, None if not.
    """
    # Iterate through the account list to find a matching user ID
    for i in range(len(singletons.account_list)):
        if singletons.account_list[i].userID == acc_id:
            return singletons.account_list[i]
    else:
        # If no matching account is found, print a message and return None
        print("found nothing")
        return None

def FindValidUser(userid : discord.User.id) -> int:
    """
    Find the index of a valid user in the account list.

    Args:
        userid (discord.User.id): The ID of the user to find.

    Returns:
        int: The index of the user in the singletons.account_list if valid, -1 if not.
    """
    # Iterate through the account list to find a matching user ID
    for account in singletons.account_list:
        if account.userID == userid:
            return singletons.account_list.index(account)
    # If no matching account is found, return -1
    return -1

async def ExceptionReplyEmbed(message : discord.Message, error : str, desc : str = "") -> None:
    """
    Send an embed with an error message as the description.

    Args:
        message (discord.Message): The message to reply to.
        error (str): The error title.
        desc (str): The error description.
    """
    # Create an embed with the error information
    embed = discord.Embed(title=error, description=desc, color=discord.Color.red())
    # Reply to the message with the error embed
    await message.reply(embed=embed)

def GetTaskEmbed(task : todo.Task, task_id : int, embed : discord.Embed) -> discord.Embed:
    """
    Get an embed with the task's information.

    Args:
        task (todo.Task): The task to create an embed for.
        task_id (int): The ID of the task.
        embed (discord.Embed): The embed to add the task information to.

    Returns:
        discord.Embed: An embed with the task's information.
    """
    # Determine the appropriate emoji based on the task's status
    if task.due == None:
        emoji = ":infinity:"
    elif task.IsDue():
        emoji = "❌"
    else:
        emoji = ":clock2:"
    if task.done:
        emoji = "✅"

    # Add a field to the embed with the task information
    embed.add_field(name=f"{emoji} {task_id+1}. {task.description}" if not task.done else f"~~{emoji} {task_id+1}. {task.description}~~",value=f"Due <t:{int(task.due.timestamp())}:R>" if task.due != None else "", inline=False)
    return embed

def GetTaskListEmbed(tasks : list[todo.Task], embed : discord.Embed) -> discord.Embed:
    """
    Get an embed with information for a list of tasks.

    Args:
        tasks (list[todo.Task]): The list of tasks to create an embed for.
        embed (discord.Embed): The embed to add the task list information to.

    Returns:
        discord.Embed: An embed with the task list information.
    """
    # Set the embed title, color, and description
    embed.title = "Tasks"
    embed.color = discord.Color(0x6abe30)
    embed.description = "All your tasks in one place"
    
    # Add each task to the embed
    for task in tasks:
        embed = GetTaskEmbed(task, tasks.index(task), embed)

    return embed
