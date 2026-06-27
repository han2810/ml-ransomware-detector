from ..ml.predict import predict_dataframe


class PredictService:
    def predict(self, feature_frame):
        return predict_dataframe(feature_frame.copy())

