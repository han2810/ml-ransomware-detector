LABEL_MAP = {
    0: "Benign",
    1: "Ransomware",
}


def load_model_package(model_path):
    try:
        import joblib
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Thieu thu vien joblib. Vui long cai dat joblib de chay du doan."
        ) from exc

    return joblib.load(model_path)


def predict_dataframe(sample_df, model_path):
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
