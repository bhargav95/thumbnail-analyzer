import requests
import csv

payload = {"type": "video",
           "channelId": "UCCqEeDAUf4Mg0GgEN658tkA",
           "order": "date",
           "maxResults": 50,
           "part": "snippet",
           "key": "AIzaSyBxqrzSWhAdQxI6m_pk_7XTcSzxYctECDs",
           "pageToken": ""
           }

with open("results.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)

    if r.status_code == 200:
        res = r.json()

        for i in res['items']:
            print i['snippet']['title'], i['snippet']['thumbnails']['high']['url']
            writer.writerow([i['snippet']['title'], i['snippet']['thumbnails']['high']['url']])
