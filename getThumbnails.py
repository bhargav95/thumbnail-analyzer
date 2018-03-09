import requests
import csv
import json

likelihood = {"UNKNOWN": 0,
              "VERY_UNLIKELY": 0,
              "UNLIKELY": 2,
              "POSSIBLE": 10,
              "LIKELY": 20,
              "VERY_LIKELY": 100
              }

payload = {"type": "video",
           "channelId": "UCCqEeDAUf4Mg0GgEN658tkA",
           "order": "date",
           "maxResults": 50,
           "part": "snippet",
           "key": "AIzaSyBxqrzSWhAdQxI6m_pk_7XTcSzxYctECDs",
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

            post_json_body['requests']['image']['source']['imageUrl']=thumbnail_url

            post_json_body = json.dumps(post_json_body)

            face_response = requests.post(
                'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBxqrzSWhAdQxI6m_pk_7XTcSzxYctECDs',
                data=post_json_body)

            try:
                annotations = face_response.json()['responses'][0]['faceAnnotations'][0]

                joy = likelihood[annotations['joyLikelihood']]

                print title, joy
            except Exception:
                pass

            writer.writerow([i['snippet']['title'], i['snippet']['thumbnails']['high']['url']])
