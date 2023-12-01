import json
from joblib import dump
import os
import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error
import warnings

warnings.filterwarnings("ignore")

def write_metrics(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)

def read_metrics(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    test_size = 0.2
    random_state = 42
    data = pd.read_csv("/opt/airflow/data/price_data.csv")
    X, y = data.drop(columns="Mirror_of_Kalandra"), data["Mirror_of_Kalandra"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", ElasticNet(random_state=42))
        ]
    )
    params = {
        "model__alpha": np.arange(1, 10, 0.5),
        "model__l1_ratio": np.arange(0, 1.05, 0.05),
    }
    grid_search = GridSearchCV(
        pipe,
        param_grid=params,
        scoring="neg_mean_absolute_error",
    )
    grid_search.fit(X_train, y_train)
    best_pipe = grid_search.best_estimator_
    best_pipe.fit(X_train, y_train)
    y_pred = best_pipe.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    metric_file = "/opt/airflow/model/metrics.json"
    date = os.environ.get('TRAIN_DATE')
    model_version = f"pipeline_{date}"

    if os.path.isfile(metric_file):
        prev_mae = read_metrics(metric_file)["mae"]
        if mae > prev_mae:
            os.remove(glob.glob("/opt/airflow/model/pipeline*")[0])
            dump(best_pipe, f"/opt/airflow/model/{model_version}.joblib") 
            write_metrics({"mae": mae}, metric_file)
    else:
        dump(best_pipe, f"/opt/airflow/model/{model_version}.joblib") 
        write_metrics({"mae": mae}, metric_file)

    X.to_csv("/opt/airflow/data/inference_data.csv", index=False)

if __name__ == "__main__":
    main()