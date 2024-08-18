[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)

<div align="center">

<h3 align="center">TOdo Bot</h3>
    <img src="assets/Bot-Icon.png" alt="Todo Bot Logo" width="200">
  <p align="center">
    project made in python 3.12
    <br>
    A discord bot for managing tasks and to-do lists within your server.
  </p>
</div>

<div align="center">
  <img src="assets/features-banner.gif" alt="Setup gif" width="">
</div>

## Features

- Create, edit, complete, and delete tasks.
- Set due dates for tasks.
- View individual tasks or all tasks at once.
- User-specific task lists.
- Persistent storage of tasks.

## _

<div align="center">
  <img src="assets/commands-banner.gif" alt="Commands Banner" width="">
</div>

## Commands

- `>help`: Displays available commands.
- `>new`: Creates a new task with description and duration.
- `>edit`: Edits an existing task by index.
- `>complete`: Marks a task as complete by index.
- `>delete`: Deletes a task by index.
- `>show`: Displays details of a specific task by index.
- `>showall`: Displays all tasks.
- `>delall` or `>deleteall`: Deletes all tasks.

## _

<div align="center">
  <img src="assets/setup-banner.gif" alt="Setup gif" width="">
</div>

## Setup

1. Clone the repository

   `git clone https://github.com/DEVUCP/Todo.git`

2. Make sure you have Python 3.12 or higher installed.
   You can check your version with :

   `python --version`

3. Install the required dependencies:

   `pip install discord pytz`
   
4. Create a Discord bot and get the token from the [Discord Developer Portal](https://discord.com/developers/applications)
5. Set up an environment variable named `TodoToken` with your bot token . . .

   [Windows 10](https://www.youtube.com/watch?v=z84UIZy_qgE)

   [Windows 11](https://www.youtube.com/watch?v=ow2jROvxyH4&t=2s)

   [Linux (Ubuntu)](https://www.youtube.com/watch?v=Y6_7xaxkPik)

   *if you can't seem to figure out how to do this, you can always just type your token in the code*
   example: `client.run("your_token_here")`
6. Run the bot:

   `python main.py`

## File Structure

- `main.py`: Main bot logic and command handling.
- `saveload.py`: Functions for saving and loading user accounts and tasks.
- `singletons.py`: Singleton instance of the account list.
- `todo.py`: Classes for Task and UserAccount.
- `utils.py`: Utility functions for various operations.

## Usage

1. Invite the bot to your Discord server.
2. Use the commands listed above to manage your tasks.
3. Tasks are automatically saved and will persist between bot restarts.

## Coding Conventions

The following coding conventions are used in this project:

1. **PEP 8**: The code follows PEP 8 style guide for Python code.
2. **Type Hints**: Type hints are used for function parameters and return values to improve code readability and maintainability.
3. **Docstrings**: Functions and classes are documented using docstrings, providing information about parameters, return values, and functionality.
4. **Naming Conventions**:

   - Functions and Classes use PascalCase (e.g., `UserAccount`, `Task`)
   - Variables use snake_case (e.g., `get_task`, `user_id`)
   - Constants use UPPER_CASE (e.g., `MASTER_PREFIX`, `ACCEPTED_TIMEFORMAT`)
5. **Error Handling**: Exceptions are caught and handled appropriately, with user-friendly error messages sent as Discord embeds.
6. **Modular Structure**: The code is organized into separate files based on functionality (e.g., `main.py`, `todo.py`, `utils.py`).
7. **Asynchronous Programming**: The Discord bot uses asynchronous functions with `async` and `await` keywords for non-blocking operations.
8. **Constants**: Frequently used values are defined as constants at the top of the files.
9. **Comments**: Inline comments are used to explain complex logic or non-obvious code sections.
10. **String Formatting**: f-strings are used for string formatting when including variables in strings.
11. **Imports**: Imports are organized at the top of each file, grouped by standard library imports, third-party imports, and local imports.
