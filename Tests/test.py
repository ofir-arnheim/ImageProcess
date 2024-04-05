import requests

# URL of your Flask app endpoint
url = 'http://localhost:20000/upload'

# Path to the file you want to send
file_path = '../Data/fox.jpg'

# Open the file and read its contents
with open(file_path, 'rb') as file:
    file_data = file.read()

# Send a POST request with the file data
response = requests.post(url, files={'file': file_data})

# Print the response from the Flask app
print("Response from server:", response.text)
