import pickle
import os

class Users:
    def LoadUsers(self):
        target_dist = 'SavedUsers.pkl'
        if os.path.getsize(target_dist) > 0:
            with open('SavedUsers.pkl', 'rb') as f:
                loaded_dict = pickle.load(f)
                UsersDict = loaded_dict
                print('SavedUsers loaded')
            return UsersDict
        else:
            UserDict = {}
            print('UserList is empty')
            return UserDict

    def UploadUsers(message):
        if message.from_user.username == "netl01":
            with open("SavedUsers.pkl", 'wb') as f:
                pickle.dump("SavedUsers.pkl", f)





