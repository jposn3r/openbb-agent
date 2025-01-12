import time
import os
from dotenv import load_dotenv
from openbb import obb
from openbb_agents.agent import openbb_agent

# Load environment variables from .env file
load_dotenv()

# Get keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENBB_PAT = os.getenv("OPENBB_PAT")

# Set the OpenAI API key for the environment
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# NEWS INTEGRATION - TODO: API KEY ACCESS TO NEWS PROVIDERS
obb.news.company(symbol='AAPL', start_date='2024-02-01', end_date='2024-02-07', provider='fmp')

# Display the headlines of the news
obb.news.company(symbol='AAPL', display="headline", provider='yfinance')

# GET STOCK PRICE TEST
def query_with_retry(prompt, retries=3, delay=10):
    for attempt in range(retries):
        try:
            result = openbb_agent(prompt, openbb_pat=OPENBB_PAT)
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if "RateLimitError" in str(e):
                print(f"Rate limit reached. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e
    raise Exception("All retry attempts failed.")

try:
    result = query_with_retry("What is the current stock price of TSLA?")
    print(result)
except Exception as final_error:
    print(f"Failed to complete the query: {final_error}")
