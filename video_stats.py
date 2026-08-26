import os 
from dotenv import load_dotenv

import requests

load_dotenv()

API_KEY= os.getenv("API_KEY")

CHANNEL_HANDLE="Veritasium"

print("API KEY caricata:", API_KEY is not None)

def get_playlistId(): 

    url=f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

    response=requests.get(url)


    #converto il body della HTTP response in formato JSON in una struttura dati python e la metto nella variabile data

    data=response.json()

    #navigo fino all'id nel json

    playlist_Id=data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    print("Playlist ID:", playlist_Id)

    return playlist_Id


def get_video_ids(playlist_id):

    video_ids=[]

    page_token= None

    while True:

     url =f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={API_KEY}"

     if page_token:
        url += f"&pageToken={page_token}"


     print("URL:", url)

     response= requests.get(url)

     data=response.json()

     print("Status:", response.status_code)
     print(data) 

     for item in data.get("items",[]):

        video_id=item["contentDetails"]["videoId"]

        video_ids.append(video_id)

     page_token = data.get("nextPageToken")

     if not page_token:
         break

    return video_ids     

if __name__ == "__main__":
   playlistId= get_playlistId()
   print(get_video_ids(playlistId))
    



