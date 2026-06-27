from pathlib import Path

import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
LABEL_MAP = {
    0: "Benign",
    1: "Ransomware",
}


def load_model_package(model_path=MODEL_PATH):
    try:
        import joblib
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError("Thieu thu vien joblib. Vui long cai dat joblib de chay du doan.") from exc

    return joblib.load(model_path)


def predict_dataframe(sample_df, model_path=MODEL_PATH):
    model_package = load_model_package(model_path)
    model = model_package["model"]
    features = model_package.get("features")

    if features:
        for feature in features:
            if feature not in sample_df.columns:
                sample_df[feature] = 0
        sample_df = sample_df[features]

    prediction = model.predict(sample_df)[0]
    return LABEL_MAP.get(int(prediction), str(prediction))


def predict_excel(excel_path, model_path=MODEL_PATH):
    sample_df = pd.read_excel(excel_path)
    return predict_dataframe(sample_df, model_path)


if __name__ == "__main__":
    sample_file = "10002_file_ha_result.xlsx"
    result = predict_excel(sample_file)
    print("Ket qua du doan:", result)
