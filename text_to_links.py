import requests
from dotenv import load_dotenv
import os
import csv

load_dotenv()
AUTH_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
# Convert response to JSON
auth_response_data = auth_response.json()
# Save the access token
access_token = auth_response_data['access_token']
# Pass the access token into the header for subsequent requests
headers = {
    'Authorization': f'Bearer {access_token}'
}

BASE_URL = 'https://api.spotify.com/v1/'
filename_output = 'songs.csv'

def look_up_track(song_name): 
    r = requests.get(BASE_URL + f'search?q={song_name}&type=track', headers=headers)
    r_data = r.json()
    return r_data

def parse_track_info(input_info): 
    if input_info['tracks']['total'] > 0:
        track_info = input_info['tracks']['items'][0]
        track_name = track_info['name']
        track_artist = track_info['artists'][0]['name']
        track_album = track_info['album']['name']
        track_url = track_info['external_urls']['spotify']
        data = {'song_name': track_name, 'artist': track_artist, 'album': track_album, 'URL': track_url}
        return data

def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        for line in csvfile: 
            stripped_line = line.strip()
            data.append(stripped_line)
    return data

# Writing to the csv file
input_data = read_csv('input.csv')
with open(filename_output, 'w', newline='', encoding='utf-8') as csvfile:
    # Defining the headers
    fieldnames = ['song_name', 'artist', 'album', 'URL']

    # Creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for song in input_data: 
        track_data = look_up_track(song)
        track_parsed = parse_track_info(track_data)
        data = track_parsed
        writer.writerow(data)
print(f'Data has been exported as {filename_output}')

