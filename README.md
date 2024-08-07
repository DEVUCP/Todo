# Discord Todo Bot

A Discord bot for managing tasks and to-do lists within your server.

## Features

- Create, edit, complete, and delete tasks
- Set due dates for tasks
- View individual tasks or all tasks at once
- User-specific task lists
- Persistent storage of tasks

## Commands

- `>help`: Displays available commands
- `>new`: Creates a new task with description and duration
- `>edit`: Edits an existing task by index
- `>complete`: Marks a task as complete by index
- `>delete`: Deletes a task by index
- `>show`: Displays details of a specific task by index
- `>showall`: Displays all tasks
- `>delall` or `>deleteall`: Deletes all tasks

## Setup

1. Clone the repository
2. Install the required dependencies:
   
   pip install discord pytz
   
3. Create a Discord bot and get the token from the [Discord Developer Portal](https://discord.com/developers/applications)
4. Set up an environment variable named `TodoToken` with your bot token
5. Run the bot:
   
   python main.py
   

## File Structure

- `main.py`: Main bot logic and command handling
- `saveload.py`: Functions for saving and loading user accounts and tasks
- `singletons.py`: Singleton instance of the account list
- `todo.py`: Classes for Task and UserAccount
- `utils.py`: Utility functions for various operations

## Usage

1. Invite the bot to your Discord server
2. Use the commands listed above to manage your tasks
3. Tasks are automatically saved and will persist between bot restarts

## Coding Conventions

The following coding conventions are used in this project:

1. **PEP 8**: The code follows PEP 8 style guide for Python code.

2. **Type Hints**: Type hints are used for function parameters and return values to improve code readability and maintainability.

3. **Docstrings**: Functions and classes are documented using docstrings, providing information about parameters, return values, and functionality.

4. **Naming Conventions**:
   - Classes use PascalCase (e.g., `UserAccount`, `Task`)
   - Functions and variables use snake_case (e.g., `get_task`, `user_id`)
   - Constants use UPPER_CASE (e.g., `MASTER_PREFIX`, `ACCEPTED_TIMEFORMAT`)

5. **Error Handling**: Exceptions are caught and handled appropriately, with user-friendly error messages sent as Discord embeds.

6. **Modular Structure**: The code is organized into separate files based on functionality (e.g., `main.py`, `todo.py`, `utils.py`).

7. **Asynchronous Programming**: The Discord bot uses asynchronous functions with `async` and `await` keywords for non-blocking operations.

8. **Constants**: Frequently used values are defined as constants at the top of the files.

9. **Comments**: Inline comments are used to explain complex logic or non-obvious code sections.

10. **String Formatting**: f-strings are used for string formatting when including variables in strings.

11. **Imports**: Imports are organized at the top of each file, grouped by standard library imports, third-party imports, and local imports.
