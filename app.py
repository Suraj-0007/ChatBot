from flask import Flask, render_template, request, jsonify
from serpapi import GoogleSearch
import logging
from datetime import datetime
import pyjokes  # Import pyjokes for jokes functionality
import time  # Import time to introduce delay

app = Flask(__name__)

# Set your SerpAPI API Key
SERPAPI_API_KEY = "20daf3fcfcccbaec80f78915406582a17bf435b0a296cdda79268a7a1ba327ad"

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message").strip().lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Custom greeting for simple messages like "hi"
        if user_message in ["hi", "hello", "hey", "morning", "afternoon", "night"]:
            time.sleep(1)  # Delay response by 1 second
            return jsonify({"reply": greeting_response(user_message)})

        # Time Inquiry
        if "time" in user_message:
            time.sleep(1)  # Delay response by 1 second
            return jsonify({"reply": get_time()})

        # Joke Inquiry
        if "joke" in user_message or "funny" in user_message:
            time.sleep(1)  # Delay response by 1 second
            return jsonify({"reply": get_joke()})

        # Search the user's question on Google
        search_results = search_google(user_message)

        # Check if results exist
        if not search_results:
            time.sleep(1)  # Delay response by 1 second
            return jsonify({"reply": "I'm sorry, I couldn't find anything relevant. Can you try rephrasing your question?"})

        # Prepare the response from top results
        reply = format_search_results(search_results)

        time.sleep(1)  # Delay response by 1 second
        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Something went wrong. Please try again later."}), 500


def search_google(query):
    """
    Searches Google for the query using SerpAPI.
    """
    try:
        search = GoogleSearch({"q": query, "api_key": SERPAPI_API_KEY})
        results = search.get_dict()

        # Extract organic search results
        return results.get("organic_results", [])
    except Exception as e:
        logging.error(f"Google Search Error: {str(e)}")
        return None


def format_search_results(results):
    """
    Formats the search results into a user-friendly reply without links.
    """
    reply = "Based on what I found, here's what I can tell you:\n\n"
    for idx, result in enumerate(results[:1]):  # Get top 3 results
        title = result.get("title", "No title available")
        snippet = result.get("snippet", "No description available")

        # Append formatted title and snippet without the link
        reply += f"{idx + 1}. {title}\n{snippet}\n\n"

    return reply


# Helper Functions for General Prompts

def greeting_response(message):
    """Respond to greetings based on the time of day."""
    current_hour = datetime.now().hour

    if "morning" in message:
        return "Good Morning! 🌞 How can I assist you today?"
    elif "afternoon" in message:
        return "Good Afternoon! 🌻 How can I assist you?"
    elif "night" in message:
        return "Good Night! 🌙 Rest well!"
    elif "hi" in message or "hello" in message or "hey" in message:
        if current_hour < 12:
            return "Hello! 😊 How can I assist you this fine morning?"
        elif 12 <= current_hour < 18:
            return "Hello! 🌞 How can I assist you this afternoon?"
        else:
            return "Hello! 🌙 How can I assist you this evening?"

def get_time():
    """Return the current time."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}."

def get_joke():
    """Return a random joke using pyjokes."""
    joke = pyjokes.get_joke()
    return joke


if __name__ == "__main__":
    app.run(debug=True)
