# libraries
import pandas as pd
import csv

# Data

emotion_map = dict()
ratings_map = dict()

for i in range(11):
    ratings_map[i] = dict()

emotions = ["sadness", "neutral", "disgust", "anger", "surprise", "happiness", "fear", "contempt"]

with open("final.csv", "r") as input_file:
    reader = csv.DictReader(input_file, delimiter=',')

    for line in reader:
        for emotion in emotions:
            emotion_map[emotion] = emotion_map.get(emotion, 0.0) + float(line[emotion])
            try:
                ratings_map[int(line["score"])][emotion] = ratings_map[int(line["score"])].get(emotion, 0.0) + float(
                    line[emotion])
            except ValueError:
                pass

print emotion_map
print ratings_map

r = ratings_map.keys()
raw_data = dict()

for emotion in emotions:
    raw_data[emotion] = [v[emotion] for k, v in ratings_map.items()]

df = pd.DataFrame(raw_data)
