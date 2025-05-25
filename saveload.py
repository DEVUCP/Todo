import todo
import pickle
import datetime

def GetFilePath(filename : str) -> str:
    import os
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    # Construct the full path to the save file
    save_path = os.path.join(script_dir, filename)
    return save_path

save_file = GetFilePath("userdata/user_accounts.pickle")

def DelSave(task_indx: int, userid: int):
    user_dict = None
    with open(save_file,'rb') as f:
        user_dict = pickle.load(f)
    f.close()
    for key in user_dict:
        if int(key) == userid:
            for task in user_dict[key]:
                pass
def SaveAccounts(user_accounts: list):
    try:
        import os
        directory = os.path.dirname(save_file)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(save_file):
            with open(save_file, 'wb') as f:
                pickle.dump([], f)
        
        with open(save_file, 'wb') as f:
            pickle.dump(user_accounts, f)

    except Exception as e:
        print(e)
        print("Error saving accounts")

def LoadAccounts() -> list:
    with open(save_file, 'rb') as f:
        user_accounts = pickle.load(f)
        print(user_accounts)
    return user_accounts