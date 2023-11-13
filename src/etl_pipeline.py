import json
import requests
from time import sleep
import pandas as pd
from tqdm import tqdm
import dask.dataframe as dd


class POENinjaAPI:
    def __init__(self, save_path: str = "price_data.csv", league: str = "Ancestor"):
        
        self.base_url = f"https://poe.ninja/api/data/currencyhistory?league={league}&type=Currency&"
        self.currency_url = "currencyId={}"
        self.currency_dict = {
            "Mirror_of_Kalandra": 22,
            "Fracturing_Orb": 230,
            "Exalted_Orb": 2,
            "Awakened_Sextant": 48,
            "Orb_of_Annulment": 73,
            "Divine_Orb": 3,
            "Orb_of_Dominance": 189
        }
        self.save_path = save_path

    def get_currency_price(self):
        df = []
        for currency, currency_id in tqdm(self.currency_dict.items(), total=len(self.currency_dict)):
            url = self.base_url + self.currency_url.format(currency_id)
            result = requests.get(url).json()["receiveCurrencyGraphData"]
            df.append(pd.Series(
                data=[row["value"] for row in result],
                index=[row["daysAgo"] for row in result],
                name=currency,
            ))
            sleep(1)
        return pd.concat(df, axis=1)

def extract():
    api = POENinjaAPI()
    price_df = api.get_currency_price()
    return price_df

def transform_load(price_df):
    price_df = dd.from_pandas(price_df, npartitions=1)
    price_df = price_df.dropna()
    price_df = price_df.drop_duplicates()
    price_df = price_df.assign(
        Fracturing_Orb_div_price=price_df["Fracturing_Orb"] / price_df["Divine_Orb"]
        )
    price_df = price_df.assign(
        Exalted_Orb_div_price=price_df["Exalted_Orb"] / price_df["Divine_Orb"]
        )
    price_df.to_csv("/opt/airflow/data/price_data.csv", single_file=True,  index=False)


if __name__ == "__main__":
    price_df = extract()
    transform_load(price_df)
