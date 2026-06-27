from ..ml.model_registry import (
    DEFAULT_MODEL_ID,
    MODELS,
    get_model_config,
    get_model_path,
    predict_dataframe,
)


class PredictService:
    @staticmethod
    def available_models():
        return [
            {"id": model["id"], "name": model["name"]}
            for model in MODELS
        ]

    @staticmethod
    def get_model(model_id):
        model_config = get_model_config(model_id)
        return {
            "id": model_config["id"],
            "name": model_config["name"],
            "path": get_model_path(model_id),
        }

    def predict(self, feature_frame, model_id=DEFAULT_MODEL_ID):
        self.get_model(model_id)
        return predict_dataframe(feature_frame, model_id)
