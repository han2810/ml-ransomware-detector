import pickle


LABEL_MAP = {
    0: "Benign",
    1: "Ransomware",
}

def load_model_package(model_path):
    with model_path.open("rb") as file:
        return pickle.load(file)


def predict_dataframe(sample_df, model_path):
    model_package = load_model_package(model_path)
    model = model_package["model"]
    feature_columns = [str(column) for column in model_package["feature_columns"]]

    sample_df.columns = sample_df.columns.map(str)
    sample_df = sample_df.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(sample_df)[0]
    return LABEL_MAP.get(int(prediction), str(prediction))
