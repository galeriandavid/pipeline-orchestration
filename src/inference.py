import os
from joblib import load
import glob
import pandas as pd


def main():
    data = pd.read_csv("/opt/airflow/data/inference_data.csv")

    model_path = glob.glob("/opt/airflow/model/pipeline*")[0]
    pipeline = load(model_path)

    pred_df = pd.DataFrame()
    pred_df["Mirror_of_Kalandra"] = pipeline.predict(data)

    pred_df.to_csv("/opt/airflow/data/predictions.csv", index=False)
    os.remove("/opt/airflow/data/inference_data.csv")


if __name__ == "__main__":
    main()