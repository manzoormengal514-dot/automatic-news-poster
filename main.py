import os
import requests
from google import generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

genai.configure(api_key=GEMINI_API_KEY)

def fetch_latest_news():
    news_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWS_API_KEY"
    try:
        response = requests.get(news_url)
        data = response.json()
        if data.get("articles"):
            first_article = data["articles"][0]
            return first_article.get("title") + "\n\n" + first_article.get("description", "")
    except Exception as e:
        print("News fetch error:", e)
    
    return "AI and technology are changing the world rapidly today."

def generate_social_post(raw_news):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Read the news below and convert it into an engaging social media post for Facebook. 
    Write it in an attractive mix of Urdu (Roman) and English, and include relevant hashtags:
    
    News: {raw_news}
    """
    response = model.generate_content(prompt)
    return response.text

def post_to_facebook(message):
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    print("Fetching news...")
    news = fetch_latest_news()
    
    print("Generating post using Gemini...")
    final_post = generate_social_post(news)
    
    print("Posting to Facebook...")
    result = post_to_facebook(final_post)
    print("Response:", result)
