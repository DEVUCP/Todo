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

   ```bash
   git clone https://github.com/DEVUCP/Todo.git
   ```

2. Make sure you have Python 3.12 or higher installed.
   You can check your version with :

   ```bash
   python --version
   ```

3. Install the required dependencies:

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
   
4. Create a Discord bot and get the token from the [Discord Developer Portal](https://discord.com/developers/applications)
5. replace "ENTER_YOUR_TOKEN_HERE" with your bot token in the `.env_example` file and rename it to `.env`

## Running the Bot

### Docker
<sub><i>Docker container (Dockerfile)</i></sub>

>Note : You must know how to use Docker and set persistent storage for the user data.

1. Build the Docker image:
   ```bash
   docker build -t todo-bot .
   ```


2. Run the Docker container:
   ```bash
   docker run --env-file .env --mount type=bind,source=/path/on/host/machine,target=/Todo/userdata/ todo-bot
   ```
   **_or_** if you don't have the `.env` file setup with your token:

   ```bash
   docker run -e TOKEN=your_token_here --mount type=bind,source=/path/on/host/machine,target=/Todo/userdata/ todo-bot
   ```

>Note : Both of the above commands use bind mount, if you want volume mount use the following command:

```bash
   docker run --env-file .env --mount type=volume,source=todo-user-data,target=/Todo/userdata/ todo-bot
```


#### Docker-Compose
<sub><i>Docker container (docker-compose.yml)</i></sub>

>Note : Docker-compose.yml is using volume mount, if you want bind mount then you have to configure it yourself.

1. Build the Docker image:
   ```bash
   docker-compose build
   ```
   Run the Docker container:
   ```bash
   docker-compose up
   ```


### Locally

<sub><i>Local machine (laptop, desktop, personal computer)</i></sub>

Run this command when in the directory where the bot is located:

   ```bash
   python main.py
   ```

or just double click on the `main.py` file

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
