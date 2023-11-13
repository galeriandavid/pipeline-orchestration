import os
import pickle
import pandas as pd


def main():
    data = pd.read_csv("/opt/airflow/data/inference_data.csv")

    with open("/opt/airflow/model/pipeline", "rb") as f:
        pipeline = pickle.load(f)

    pred_df = pd.DataFrame()
    pred_df["Mirror_of_Kalandra"] = pipeline.predict(data)

    pred_df.to_csv("/opt/airflow/data/predictions.csv", index=False)
    os.remove("/opt/airflow/data/inference_data.csv")


if __name__ == "__main__":
    main()