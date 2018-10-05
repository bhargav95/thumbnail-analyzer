import csv

if __name__ == "__main__":
    with open("all_needledrop_ratings.csv", "r") as f1, open("results3.csv", "r") as f2:

        ratings = csv.reader(f1, delimiter=",")
        next(ratings, None)
        next(ratings, None)
        next(ratings, None)
        ratings_map = dict()

        for rating in ratings:
            artist, album, score, newline = rating
            artist = artist.strip()
            album = album.strip()
            score = score.strip()

            if artist not in ratings_map:
                ratings_map[artist] = dict()

            ratings_map[artist][album] = score

        emotions = csv.reader(f2, delimiter=",")
        next(emotions, None)

        count = 0

        with open("final.csv", "wb") as output:
            writer = csv.writer(output, delimiter=',')
            writer.writerow(
                ["title", "image_url", "sadness", "neutral", "contempt", "disgust", "anger", "surprise", "fear",
                 "happiness", "score"])
            for emotion in emotions:
                count += 1
                print emotion
                try:
                    artist, album = emotion[0].split(" - ")
                except ValueError:
                    print "ValueError"
                    artist, album = emotion[0].split("- ")

                album = album.replace("ALBUM REVIEWS", "").replace("ALBUM REVIEW", "").strip()
                album = " ".join(album.split())

                output_line = emotion
                try:
                    output_line.append(ratings_map[artist][album])
                    writer.writerow(output_line)
                except KeyError as e:
                    print count
                    print e
                    print ratings_map.get(artist, "")
                    raw_input()
