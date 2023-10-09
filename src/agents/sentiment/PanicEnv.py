import gymnasium as gym
import json
import pandas as pd
from easydict import EasyDict as edict
from tqdm.notebook import tqdm
from langchain import LLMChain
from langchain.llms.base import LLM

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from gpt_by_ya import get_answer_from_gpt_model


class PanicNewsEnv(gym.Env):
    def __init__(self, args):
        args = edict(args)
        self.stock_name = args.stock_name
        self.start_date = args.start_date
        self.end_date = args.end_date
        self.init_cash = args.init_cash if "init_cash" in args.keys() else 100
        self.init_hold = args.init_hold if "init_hold" in args.keys() else 0
        self.cal_on = args.cal_on if "cal_on" in args.keys() else "Close"
        self.trade_volume = args.trade_volume if "trade_volume" in args.keys() else 100

        self.read_file(args.stock_name)

    def read_file(self, stock_name):
        # sentences
        sentence_path = f"/workspaces/FinGPT/stocknet-dataset/tweet/preprocessed/{stock_name}/"
        self.tweets_df = pd.DataFrame()
        print("missing (empty means not missing):", end=" ")
        for date in pd.date_range(self.start_date, self.end_date):
            date = date.date().strftime("%Y-%m-%d")
            file_path = f"{sentence_path}/{date}"
            try:
                with open(file_path, "r") as f:
                    sentences = f.readlines()
                sentences_dict = [json.loads(i) for i in sentences]
                sentences = [" ".join(i["text"]) for i in sentences_dict]
                date = [date for i in sentences_dict]
                time_ = [pd.to_datetime(i["created_at"]).time() for i in sentences_dict]
                user_id_str = [i["user_id_str"] for i in sentences_dict]
                temp_df = pd.DataFrame([sentences, date, time_, user_id_str]).T
                # print(temp_df)
                self.tweets_df = pd.concat([self.tweets_df, temp_df])
            except:
                print(date, end=" ")
        self.tweets_df.columns = ["text", "date", "time", "user_id"]
        self.tweets_df = self.tweets_df.reset_index(drop=True)
        self.date_list = self.tweets_df.sort_values("date")["date"].unique().tolist()

        # Prices
        price_path = f"/workspaces/FinGPT/stocknet-dataset/price/raw/{stock_name}.csv"
        self.price_df = pd.read_csv(price_path)
        self.price_df = self.price_df[self.price_df.Date.isin(self.date_list)]
        self.price_df[self.cal_on] /= self.price_df.iloc[0][self.cal_on]
        self.date_list = self.price_df.sort_values("Date")["Date"].unique().tolist()

    def reset(self):
        self.day_index = 0
        self.today = self.date_list[self.day_index]
        self.today_sentences = self.tweets_df[self.tweets_df.date == self.today]
        self.today_price = self.price_df[self.price_df["Date"] == self.today]
        self.today_cash = self.init_cash
        self.today_hold = self.init_hold
        self.terminal = False
        self.asset_memory = [self.init_hold * self.today_price[self.cal_on].item() + self.today_cash]
        self.hold_memory = [self.init_hold]
        self.cash_memory = [self.init_cash]
        self.reward_momory = [0]
        self.action_memory = [0]

        return self.today_sentences.text.tolist()

    def update(self):
        if self.day_index >= len(self.date_list) - 1:
            self.terminal = True
        else:
            self.day_index += 1
            self.today = self.date_list[self.day_index]
            self.today_sentences = self.tweets_df[self.tweets_df.date == self.today]
            self.today_price = self.price_df[self.price_df["Date"] == self.today]

    def step(self, action):
        last_price = self.today_price[self.cal_on].item()
        last_hold = self.today_hold
        last_cash = self.today_cash
        last_asset = last_price * last_hold + last_cash
        self.update()
        if self.terminal:
            print("\n\nall_done")
        else:
            next_price = self.today_price[self.cal_on].item()
            if action > 0:
                buy_cost = self.trade_volume * next_price
                today_cash = self.today_cash - buy_cost
                if today_cash >= 0:
                    self.today_hold += self.trade_volume
                    self.today_cash = today_cash
                else:
                    avaliable_volumn = self.today_cash / next_price
                    self.today_hold += avaliable_volumn
                    self.today_cash = 0


            elif action < 0:
                today_hold = self.today_hold - self.trade_volume
                if today_hold >= 0:
                    sell_earn = self.trade_volume * next_price
                    self.today_cash += sell_earn
                    self.today_hold = today_hold
                else:
                    self.today_cash += next_price * self.today_hold
                    self.today_hold = 0

            else:
                pass

            next_asset = self.today_hold * next_price + self.today_cash
            self.reward = next_asset - last_asset
            self.asset_memory.append(next_asset)
            self.hold_memory.append(self.today_hold)
            self.reward_momory.append(self.reward)
            self.action_memory.append(action)
            self.cash_memory.append(self.today_cash)

        return self.today_sentences.text.tolist(), self.reward, self.terminal, {}


import openai
import numpy as np
import pickle
import time


class GptAgent:
    def __init__(self, args):
        args = edict(args)
        self.model_name = args.model_name
        self.source = args.source
        self.buy_threshold = args.get("buy_threshold", 0.3)
        self.sell_threshold = args.get("sell_threshold", -0.3)

        # Init
        if self.source == "openai":
            openai.api_key = args.api_key
        elif self.source == "local":
            with open(f"./data/{self.model_name}.pkl", "rb") as f:
                self.sentiment_dict = pickle.load(f)

    def __call__(self, obs):
        self.score_list = [self.get_sentiment(o) for o in obs]
        self.score_list_mean = np.mean(self.score_list)
        return 1 if self.score_list_mean > self.buy_threshold else -1 if self.score_list_mean < self.sell_threshold else 0

    def get_sentiment(self, sentence):
        # TODO: switch case to yandexgpt2
        if self.source == "openai":
            time.sleep(1)
            response = openai.Completion.create(
                model=self.model_name,
                prompt=f"Decide whether a sentence's sentiment is positive, neutral, or negative.\n\nSentence: \"{sentence}\"\nSentiment: ",
                temperature=0,
                max_tokens=60,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0
            )
            response = response["choices"][0]["text"]
        elif self.source == "local":
            response = self.sentiment_dict.get(sentence, "")

        if "negative" in response.lower():
            return -1
        elif "positive" in response.lower():
            return 1
        else:
            return 0
