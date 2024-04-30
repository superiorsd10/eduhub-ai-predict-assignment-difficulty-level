from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, status
import pickle


class Marks(BaseModel):
    marks: List[List[int]]
    maxMarks: List[int]


app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))


@app.post("/predict", status_code=status.HTTP_200_OK)
def predict(features: Marks):
    try:
        features = features.marks
        maxMarks = features.maxMarks
        new_features = []
        for feature in features:
            for index in range(len(feature)):
                feature[index] = round((feature[index]/maxMarks[index])*10)
        for feature in features:
            while len(feature) < 5:
                feature.insert(0, 10)
            sum_of_marks = 0
            number_of_assignments = len(feature)
            while len(feature) >= 5:
                sum_of_marks += feature[0]
                feature.pop(0)
            average = round(sum_of_marks / (number_of_assignments - 4))
            feature.insert(0, average)

            new_features.append(feature)

        predicted_difficulty_level = model.predict(new_features)

        predicted_difficulty_level = [
            str(level) for level in predicted_difficulty_level
        ]
        return {
            "prediction": predicted_difficulty_level,
        }

    except Exception as error:
        return {
            "error": str(error)  # Convert error to string
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
