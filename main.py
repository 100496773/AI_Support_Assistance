# main.py
# Paula Sanchez Sanz
# Simple Message Classifier for Customer Support
# This script reads messages from a CSV file, classifies them into categories
# based on keywords, and stores the results in a list.
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# --- 1. Define Categories & Keywords ---
# We define them as constants to avoid typos.

# Categories
CAT_SHIPMENT_STATUS = "Shipment Status"
CAT_DELIVERY_ISSUE = "Delivery Issue"
CAT_PAYMENT_INVOICE = "Payment/Invoice"
CAT_UNKNOWN = "Unknown" # Fallback for messages that don't match

# Optional Part: Sentiment
SENT_POSITIVE = "Positive"
SENT_NEGATIVE = "Negative"
SENT_NEUTRAL = "Neutral"

# Keyword lists for classification (in English)
KEYWORDS_PAYMENT = ["payment", "invoice", "pay", "processed", "bill"]
KEYWORDS_DELIVERY = ["damaged", "missing", "failed", "wrong address", "wet", "missed"]
KEYWORDS_SHIPMENT = ["shipment", "status", "order", "where is", "tracking", "track", "delivery yet"]


# --- 2. Classifier Functions ---

def classify_message(message):
    """
    Classifies a message into one of the predefined categories
    based on keywords.
    """
    message_low = message.lower()

    # We check for the most specific categories first (Payment & Delivery Issues)
    # before the more general 'Shipment Status'.

    if any(keyword in message_low for keyword in KEYWORDS_PAYMENT):
        return CAT_PAYMENT_INVOICE
    
    if any(keyword in message_low for keyword in KEYWORDS_DELIVERY):
        return CAT_DELIVERY_ISSUE

    if any(keyword in message_low for keyword in KEYWORDS_SHIPMENT):
        return CAT_SHIPMENT_STATUS
    
    # If no keywords match, return Unknown
    return CAT_UNKNOWN

def detect_sentiment(message, analyzer):
    """
    Detects the sentiment of a message using VADER.
    """
    # .polarity_scores() returns a dict (neg, neu, pos, compound)
    scores = analyzer.polarity_scores(message)
    
    # The 'compound score' is a normalized score from -1 (v. neg) to +1 (v. pos).
    # We use standard thresholds to classify.
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        return SENT_POSITIVE
    elif compound_score <= -0.05:
        return SENT_NEGATIVE
    else:
        return SENT_NEUTRAL

# --- 3. Main Processing Function ---

def main():
    """
    Main function to read CSV, process messages,
    and store results.
    """
    sentiment_analyzer = SentimentIntensityAnalyzer()

    # This list will "store" our results, as requested.
    processed_messages = []
    
    try:
        with open('messages.csv', mode='r', encoding='utf-8') as file:
            # Use DictReader to read the CSV as dictionaries
            reader = csv.DictReader(file)
            
            for row in reader:
                message_id = row['id']
                message_text = row['message']
                
                # Run the classification
                category = classify_message(message_text)
                
                # Run sentiment analysis
                sentiment = detect_sentiment(message_text, sentiment_analyzer) 

                # Store the results in our list
                processed_messages.append({
                    "id": message_id,
                    "message": message_text,
                    "category": category,
                    "sentiment": sentiment
                })

    except FileNotFoundError:
        print("ERROR: 'messages.csv' not found.")
        print("Please make sure the file is in the same directory as main.py")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if not processed_messages:
        print("No messages were processed.")
        return

    # Convert our list of dicts to a Pandas DataFrame for better display
    df = pd.DataFrame(processed_messages)
    
    # Adjust display options for better readability
    pd.set_option('display.max_rows', None) # Show all rows
    pd.set_option('display.max_colwidth', 50) # Shorten long messages
    pd.set_option('display.width', 100) # Adjust to terminal width

    print("========================================")
    print("  AI SUPPORT ASSISTANT - RESULTS        ")
    print("========================================")

    # Show the processed messages
    print("\n--- Processed Messages List ---")

    # Print the DataFrame using to_string() for clean formatting
    # and to remove the index (0, 1, 2...)
    print(df[['message', 'category', 'sentiment']])


    # --- Show summary by category ---
    print("\n\n--- Summary by Category ---")
    
    # .value_counts() does the counting for us
    category_summary = df['category'].value_counts()
    # .to_string() prints a clean version without "Name:..."
    print(category_summary.to_string())
    
    print("\n\n--- Summary by Sentiment ---")
    sentiment_summary = df['sentiment'].value_counts()
    # .to_string() prints a clean version without "Name:..."
    print(sentiment_summary.to_string())
    
    print("\n========================================")

# --- 4. Run the script ---
if __name__ == "__main__":
    main()