import json
import os

import aiohttp
import requests
from dotenv import load_dotenv

load_dotenv(".env")


def get_yandex_token_with_auth() -> dict:
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    data = {"yandexPassportOauthToken": os.getenv("YIATH")}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_answer_from_gpt_model(
    system_text: str = None,
    user_text: str = None,
    retry=False,
    temp=0.1,
    max_tokens=5000,
) -> str | None:
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {os.getenv('YIAM')}",
        "x-folder-id": os.getenv("YIAM_FOLDER"),
    }

    # Prepare context and text
    instruct = system_text.strip()
    text = user_text.strip()

    # Prepare request parameters
    params = {
        "model": "general",
        "generationOptions": {
            "partialResults": False,
            "temperature": temp,
            "maxTokens": max_tokens,
        },
        "instructionText": instruct,
        "requestText": text,
    }

    url = "https://llm.api.cloud.yandex.net/llm/v1alpha/instruct"

    response = requests.post(url, headers=headers, json=params)

    get_yiam_token_response_json = get_yandex_token_with_auth()
    if "iamToken" in get_yiam_token_response_json:
        os.environ["YIAM"] = get_yiam_token_response_json.get("iamToken" or None)

    if response.status_code == 200:
        try:
            result = response.json()
            return result["result"]["alternatives"][0]["text"]
        except KeyError:
            # Handle the case where the 'alternatives' key is missing
            get_yiam_token_response_json = get_yandex_token_with_auth()
            if "iamToken" in get_yiam_token_response_json:
                os.environ["YIAM"] = get_yiam_token_response_json.get(
                    "iamToken" or None
                )
            if not retry:
                return get_answer_from_gpt_model(user_text=user_text, retry=True)
            else:
                return None
        except Exception:
            # Handle any other exceptions
            return None
    else:
        return None


async def a_get_yandex_token_with_auth() -> dict:
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    data = {"yandexPassportOauthToken": os.getenv("YIATH")}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data)) as response:
            response_data = await response.json()

    return response_data


async def a_get_answer_from_gpt_model(
    system_text: str = None,
    user_text: str = None,
    retry=False,
    temp=0.1,
    max_tokens=5000,
) -> str | None:
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {os.getenv('YIAM')}",
        "x-folder-id": os.getenv("YIAM_FOLDER"),
    }

    # Prepare context and text
    instruct = system_text.strip()
    text = user_text.strip()

    # Prepare request parameters
    params = {
        "model": "general",
        "generationOptions": {
            "partialResults": False,
            "temperature": temp,
            "maxTokens": max_tokens,
        },
        "instructionText": instruct,
        "requestText": text,
    }

    url = "https://llm.api.cloud.yandex.net/llm/v1alpha/instruct"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=params) as response:
            response = await response.json()

            try:
                return response["result"]["alternatives"][0]["text"]
            except KeyError:
                # Handle the case where the 'alternatives' key is missing
                get_yiam_token_response_json = await get_yandex_token_with_auth()
                if "iamToken" in get_yiam_token_response_json:
                    os.environ["YIAM"] = get_yiam_token_response_json.get(
                        "iamToken" or None
                    )
                if not retry:
                    return await get_answer_from_gpt_model(
                        user_text=user_text, retry=True
                    )
                else:
                    return None
            except Exception:
                # Handle any other exceptions
                return None
