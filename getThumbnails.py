import requests
import csv
import json
import config

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

headers = {'Ocp-Apim-Subscription-Key': config.emotionAPI}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}

cId = {"chris": "UCCqEeDAUf4Mg0GgEN658tkA",
       "needledrop": "UCt7fwAhXDy3oNFTAzF2o8Pw"
       }

payload = {"type": "video",
           "channelId": cId["needledrop"],
           "order": "date",
           "maxResults": 50,
           "part": "snippet",
           "key": config.youtubeAPI,
           "pageToken": ""
           }

post_json_body = {
    "requests": [
        {
            "image": {
                "source": {
                    "imageUri": ""
                }
            },
            "features": [
                {
                    "type": "FACE_DETECTION",
                    "maxResults": 1
                }
            ]
        }
    ]
}

with open("results.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)

    if r.status_code == 200:
        res = r.json()

        for i in res['items']:
            title = i['snippet']['title']
            thumbnail_url = i['snippet']['thumbnails']['high']['url']

            # print post_json_body['requests'][0]

            post_json_body['requests'][0]['image']['source']['imageUri'] = thumbnail_url

            # print post_json_body['requests'][0]

            response = requests.post(face_api_url, params=params, headers=headers, json={"url": thumbnail_url})
            faces = response.json()

            try:
                annotations = faces[0]['faceAttributes']['emotion']

                print title, max(annotations, key=annotations.get), max(annotations.values())
                # raw_input()
                writer.writerow([i['snippet']['title'], i['snippet']['thumbnails']['high']['url']])
            except (IndexError,UnicodeEncodeError) as e:
                print i['snippet']['title'], str(e)
                pass
            except KeyError:
                print i['snippet']['title']
                print faces
                raw_input()

