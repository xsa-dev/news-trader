from appwrite.client import Client
import os
from .agent import get_prices



def main(context):
    get_prices()
    
    if context.req.method == "GET":        
        return context.res.send("Hello, World! How are you?")

    return context.res.json(
        {
            "motto": "Build Fast. Scale Big. All in One Place.",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
    
main()
