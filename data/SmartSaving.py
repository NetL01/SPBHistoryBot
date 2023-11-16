def SmartSaving(user):
    with open('C://Users//razuv//PycharmProjects//SPBHistoryBot//data//Users.txt', 'r') as file:
        lines = file.readlines()
        if user + '\n' not in lines:
            with open('C://Users//razuv//PycharmProjects//SPBHistoryBot//data//Users.txt', 'a') as file:
                file.write(user + '\n')
                print('New user was saved.')
        else:
            print('User is not new')