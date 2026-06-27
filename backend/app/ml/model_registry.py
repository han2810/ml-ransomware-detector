from pathlib import Path

from .predictors.predict_model1 import predict_dataframe as predict_model1_dataframe
from .predictors.predict_model2 import predict_dataframe as predict_model2_dataframe


MODEL_DIR = Path(__file__).resolve().parent / "model"

# This is the only registry to edit when adding or removing a model.
# Each model can use its own prediction function.
MODELS = [
    {
        "id": "model1.pkl",
        "name": "Decision Tree",
        "filename": "model1.pkl",
        "predictor": predict_model1_dataframe,
    },
    {
        "id": "model2.pkl",
        "name": "Random Forest MLRAN",
        "filename": "model2.pkl",
        "predictor": predict_model2_dataframe,
    },
]

DEFAULT_MODEL_ID = MODELS[0]["id"]
MODEL_BY_ID = {model["id"]: model for model in MODELS}


def get_model_config(model_id=None):
    selected_model = model_id or DEFAULT_MODEL_ID
    try:
        return MODEL_BY_ID[selected_model]
    except KeyError as exc:
        raise ValueError(f"Model khong hop le: {selected_model}") from exc


def get_model_path(model_id=None):
    model_config = get_model_config(model_id)
    model_path = MODEL_DIR / model_config["filename"]
    if not model_path.is_file():
        raise FileNotFoundError(f"Khong tim thay file model: {model_path}")
    return model_path


def predict_dataframe(sample_df, model_id=None):
    model_config = get_model_config(model_id)
    model_path = get_model_path(model_config["id"])
    return model_config["predictor"](sample_df.copy(), model_path)
