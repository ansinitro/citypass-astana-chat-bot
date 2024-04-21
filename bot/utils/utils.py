import os
import requests

def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully")
        return True
    else:
        print("Failed to download file")
        return False

def send_photo(url, photo_path):
    with open(photo_path, 'rb') as file:
        files = {'image': file}
        response = requests.post(url, files=files)
        
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        return response_json.get('message')
    else:
        print("Failed to send photo")
        return None

def download_send_and_delete(url, destination, server_url):
    if download_file(url, destination):
        city_name = send_photo(server_url, destination)
        if city_name:
            os.remove(destination)
            return city_name
        else:
            return None
    else:
        return None