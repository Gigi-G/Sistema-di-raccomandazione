import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import math
from sklearn.metrics import mean_absolute_error
from modules.recommender_system.ContentBased import ContentBased

def predict(cb:ContentBased, data) -> any:
    predicted_ratings = []
    for i, ann in data.iterrows():
        try:
            if(math.isnan(ann['rating'])):
                rating = 0
            else:
                rating = cb.predict(int(ann['user_id'][4:]) - 1, ann['subject_id'])
        except:
            rating = np.nan
        predicted_ratings.append(rating)
    return np.array(predicted_ratings)


def gradient_descent(gradient, start, learn_rate, train_data, n_iter = 40, tolerance = 0.85):
    value = start
    result = [0, 0]
    for _ in tqdm(range(n_iter), total = n_iter):
        result = gradient(result[1], learn_rate, value, train_data)
        value = result[0]
        if result[1] <= tolerance:
            break
    return value

def find_threshold(back_mae, rate, threshold, train_data):
    #print(threshold)
    cb = ContentBased("./Dati/subjects.csv", data = train_data, threshold = threshold)
    predicted_ratings_1 = predict(cb, train_data)
    train_data = train_data.fillna(0)
    result = mean_absolute_error(train_data['rating'], predicted_ratings_1)
    if(result > back_mae):
        return [threshold + rate * threshold, result]
    return [threshold - rate * threshold, result]

def main() -> None:
    data = pd.read_csv("./Dati/Dati.csv")
    train_data, test_data = train_test_split(data, test_size = 0.25)

    #Find threshold
    print("Finding threshold for feature vectors...")
    threshold = gradient_descent(gradient = find_threshold, start = 0.5, learn_rate = 0.2, train_data = train_data)
    print("Threshold:", threshold)
    print()

    #Using train_data
    print("Using test_data...")
    cb = ContentBased("./Dati/subjects.csv", data = train_data, threshold = threshold)
    cb.print_utility_matrix()
    print("Base02 - SOCIAL MEDIA MANAGEMENT", cb.predict(1, 11))
    print()

    #Using test_data
    print("Using train_data...")
    predicted_ratings_1 = predict(cb, test_data)
    print(predicted_ratings_1)
    test_data = test_data.fillna(0)
    print("\nMean Absolute Error:")
    print(mean_absolute_error(test_data['rating'], predicted_ratings_1))

    #Using all data
    cb = ContentBased("./Dati/subjects.csv", data = data, threshold = threshold)
    cb.print_utility_matrix()
    print("Using all data...")
    predicted_ratings_1 = predict(cb, data)
    print(predicted_ratings_1)
    data = data.fillna(0)
    print("\nMean Absolute Error:")
    print(mean_absolute_error(data['rating'], predicted_ratings_1))

if __name__ == "__main__":
    main()
