import os 
from dotenv import load_dotenv

from datetime import date

import requests

import json

load_dotenv()

API_KEY= os.getenv("API_KEY")

CHANNEL_HANDLE="Veritasium"

maxResults=50

print("API KEY caricata:", API_KEY is not None)

def get_playlist_id(): 

    url=f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

    response=requests.get(url)


    #converto il body della HTTP response in formato JSON in una struttura dati python e la metto nella variabile data

    data=response.json()

    #navigo fino all'id nel json

    channel_playlistId=data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    print(channel_playlistId)

    return channel_playlistId


def get_video_ids(playlistId):

    video_ids=[]

    page_token= None

    while True:

     url =f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

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

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list,batch_size) :
        for i in range(0,len(video_id_list),batch_size):
          yield video_id_list[i:i + batch_size]
       

    try:
        for batch in batch_list(video_ids, 50):
             video_ids_str = ",".join(batch)


             url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails,snippet,statistics&id={video_ids_str}&key={API_KEY}"

             response=requests.get(url)  

             response.raise_for_status()

             data= response.json() 

             for item in data["items"]:
                 video_id = item["id"]
                 snippet = item["snippet"]
                 contentDetails = item["contentDetails"]
                 statistics = item["statistics"]

                 video_data = {
                    "video_id": video_id,
                    "publishedAt": snippet["publishedAt"],
                    "title": snippet["title"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount",None),
                    "likeCount": statistics.get("likeCount",None),
                    "commentCount": statistics.get("commentCount",None),
                 }
   
             extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
     raise e

def save_to_json(extracted_data):
   file_path=f"./data/YT_data_{date.today()}.json"

   with open(file_path,"w",encoding="utf-8") as json_outfile:
      json.dump(extracted_data,json_outfile,indent=4,ensure_ascii=False)


if __name__ == "__main__":
   playlistId= get_playlist_id()
   
   video_ids=get_video_ids(playlistId)

   video_data=(extract_video_data(video_ids))
   print(video_data)
    



