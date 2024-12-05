import todo
import json
import datetime

def GetFilePath(filename : str) -> str:
    import os
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    # Construct the full path to the save file
    save_path = os.path.join(script_dir, filename)
    return save_path

save_file = GetFilePath("userdata/user_accounts.json")

def DelSave(task_indx: int, userid: int):
    user_dict = None
    with open(save_file,'r') as f:
        user_dict = json.load(f)
    f.close()
    for key in user_dict:
        if int(key) == userid:
            for task in user_dict[key]:
                pass

# convert UserAccount objects to dictionaries
def SaveAccounts(user_accounts: list):
    user_account_dicts = []
    for user_account in user_accounts:

        #print(user_account.tasks[user_accounts.index(user_account)].__dict__)
        task_dicts = []
        for task in user_account.tasks:
            task_dicts.append(task.__dict__)
        for task in task_dicts:
            task["due"] = str(task["due"])
        user_account_dict = {
            'userID': user_account.userID,
            'tasks': task_dicts
        }
        user_account_dicts.append(user_account_dict)

    # save to JSON
    with open(save_file, 'w') as f:
        json.dump(user_account_dicts, f, indent=4)

    for task in user_account.tasks:
        if task.due != "None":
            task.due = datetime.datetime.strptime(task.due,"%Y-%m-%d %H:%M:%S.%f")
        else:
            task.due = None



def LoadAccounts() -> list:
    with open(save_file, 'r') as f:
        user_account_dicts = json.load(f)

    user_accounts = []
    for user_account_dict in user_account_dicts:
        tasks = []
        for task_dict in user_account_dict['tasks']:
            task = todo.Task()
            for key, value in task_dict.items():
                if key == "due" and value != "None":
                    value = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S.%f")
                elif key == "due" and value  == "None":
                    value = None
                setattr(task, key, value)
            tasks.append(task)
        user_account = todo.UserAccount(user_account_dict['userID'], tasks[0] if tasks else None)
        user_account.tasks = tasks
        user_accounts.append(user_account)
    return user_accounts


