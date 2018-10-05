import requests
import csv
import time
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
           "pageToken": "CLYHEAA"
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

with open("results4.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(
        ["title", "image_url", "sadness", "neutral", "contempt", "disgust", "anger", "surprise", "fear", "happiness"])

    # First twenty pages max
    for _ in range(20):

        r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)

        if r.status_code == 200:
            res = r.json()

            print res

            if "nextPageToken" in res:
                payload['pageToken'] = res['nextPageToken']
            else:
                break

            for i in res['items']:

                flag = False

                while not flag:
                    title = i['snippet']['title']

                    if "album review" not in title.lower():
                        flag = True
                        continue

                    thumbnail_url = i['snippet']['thumbnails']['high']['url']

                    # print post_json_body['requests'][0]

                    post_json_body['requests'][0]['image']['source']['imageUri'] = thumbnail_url

                    # print post_json_body['requests'][0]

                    response = requests.post(face_api_url, params=params, headers=headers, json={"url": thumbnail_url})
                    faces = response.json()

                    try:
                        annotations = faces[0]['faceAttributes']['emotion']

                        annotations['title'] = i['snippet']['title']
                        annotations['image_url'] = i['snippet']['thumbnails']['high']['url']

                        print annotations

                        writer.writerow([
                            annotations['title'],
                            annotations['image_url'],
                            annotations['sadness'],
                            annotations['neutral'],
                            annotations['contempt'],
                            annotations['disgust'],
                            annotations['anger'],
                            annotations['surprise'],
                            annotations['fear'],
                            annotations['happiness'],
                        ])
                        flag = True
                    except (IndexError, UnicodeEncodeError) as e:
                        print i['snippet']['title'], str(e)
                        flag = True
                        pass
                    except KeyError:
                        print i['snippet']['title']
                        if faces.get('error').get('code') == "RateLimitExceeded":
                            print "RateLimitExceeded"
                            time.sleep(10)
                            continue
                        flag = True
