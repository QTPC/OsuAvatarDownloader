import os
import threading
from urllib import request
from ossapi import Ossapi


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
        print("Folder created successfully")
    except FileExistsError:
        print("Folder already exists")


def save_img(img_url, file_name, file_path='./images'):
    try:
        if not os.path.exists(file_path):
            print('Folder', file_path, 'does not exist, creating a new one')
            os.makedirs(file_path)
        file_suffix = os.path.splitext(img_url)[1]
        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        request.urlretrieve(img_url, filename=filename)
    except IOError as e:
        print('File operation failed', e)
    except Exception as e:
        print('ERROR:', e)


def download_avatar(line):
    api = Ossapi(int(client_id), client_secret)
    try:
        url = api.user(str(line.strip()), mode="mania", key="username").avatar_url
        name = api.user(str(line.strip()), mode="mania", key="username").username
        print("Downloading:" + name)
        save_img(url, name)
    except Exception as e:
        print('Error while processing:', e)


def get_user_input():
    global client_id, client_secret
    print("create a new client at https://osu.ppy.sh/home/account/edit#oauth before using this.")
    option = input("Please choose the input method (1. Direct input 2. Read from txt file: ")
    if option == "1":
        client_id = input("Please enter the client_id:")
        client_secret = input("Please enter the client_secret:")
        usernames = input("Please enter the usernames, separated by commas: ").split(",")
    elif option == "2":
        client_id = input("Please enter the client_id:")
        client_secret = input("Please enter the client_secret:")
        file_path = input("Please enter the address of the txt file: ")
        try:
            with open(file_path, 'r') as file:
                usernames = file.readlines()
        except FileNotFoundError:
            print("Cannot find the specified txt file. Please make sure the file exists and enter the correct file "
                  "address.")
            exit()
    else:
        print("Invalid option.")
        exit()
    return client_id, client_secret, usernames


client_id, client_secret, usernames = get_user_input()

threads = []
for username in usernames:
    thread = threading.Thread(target=download_avatar, args=(username,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

