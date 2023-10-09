import asyncio
import os
import multiprocessing

import dotenv
from supabase import create_client, Client

import templates

from PanicEnv import PanicNewsEnv, GptAgent
import pandas as pd

dotenv.load_dotenv("../../.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

surl: str = SUPABASE_URL
skey: str = SUPABASE_KEY

supabase: Client = create_client(surl, skey)

Debug = True
Free = False


def load_prices(**kwargs):
    # TODO: load prices for
    return prices


def validate_sources_for(arg):
    for new in arg:
        print(new)
        coin = new.get("token")
        start_date = prices.get("start")
        end_date = prices.get(end_date)
        prices = load_prices(token=coin, start_date=start_date, end_date=end_date)

        env_args = {
            "stock_name": coin,
            "start_date": start_date,
            "end_date": end_date,
            "init_cash": 100,
            "init_hold": 0,
            "trade_volume": 100,
        }
        agent_args = {
            "model_name": templates.openai_gpt_model,
            "source": templates.source,  # "openai", "yandex", "local"
            "api_key": os.getenv("OPENAI_API_KEY")
            if templates.source == "openai"
            else "yandexgpt2",
            "buy_threshold": 0.3,  # the max positive sentiment is 1, so this should range from 0 to 1
            "sell_threshold": -0.3,  # the min negative sentiment is -1, so this should range from -1 to 0
        }

        env = PanicNewsEnv(env_args)
        agent = GptAgent(agent_args)

        obs = env.reset()
        terminal = False
        while not terminal:
            action = agent(obs)
            obs, reward, terminal, info = env.step(action)

        print(
            # return rate
            (env.asset_memory[-1] - env.asset_memory[0])
            / env.asset_memory[0]
        )

        account_value = env.asset_memory
        baseline_value = env.price_df.Close.tolist()
        date_list = env.date_list

        df_account_value = pd.DataFrame(
            [date_list, account_value], index=["time", "account_value"]
        ).T
        df_baseline = pd.DataFrame(
            [date_list, baseline_value], index=["time", "account_value"]
        ).T

        # df_account_value.head(2)
        # TODO: validated source and trade pairs can be approved here (for create orders)

    def get_return(df, value_col_name="account_value"):
        df["daily_return"] = df[value_col_name].pct_change(1)
        df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d")
        df.set_index("time", inplace=True, drop=True)
        df.index = df.index.tz_localize("UTC")
        return pd.Series(df["daily_return"], index=df.index)

    import pyfolio
    from pyfolio import timeseries

    daily_return = get_return(df_account_value)
    daily_return_base = get_return(df_baseline)

    perf_func = timeseries.perf_stats
    perf_stats_all = perf_func(
        returns=daily_return,
        factor_returns=daily_return_base,
        positions=None,
        transactions=None,
        turnover_denom="AGB",
    )
    print("==============DRL Strategy Stats===========")
    perf_stats_all

    return prediction


async def main():
    # get all unstacked news from supabase
    unstacked_news = (
        supabase.table("news").select("*").filter("status", "is", "null").execute().data
    )

    # get sentiment prediction with prediction pool
    print(unstacked_news)
    await sentiments_prediction_pool(unstacked_news)


async def sentiments_prediction_pool(news: list):
    # Create a multiprocessing Pool with the desired number of processes
    # num_processes = multiprocessing.cpu_count() if not Debug else 1  # Use the number of CPU cores
    # pool = multiprocessing.Pool(processes=num_processes)
    #
    # # Map the list of arguments to the worker function
    # sentiments = pool.map(supabase_worker, news, chunksize=4)
    #
    # # Close the pool to free resources
    # pool.close()
    # pool.join()
    validate_sources_for(news)

    # Print the results
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
