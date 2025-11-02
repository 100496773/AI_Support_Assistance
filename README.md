# AI Support Assistant - Engineering Intern Challenge

This project is a simple, keyword-based support ticket classifier built for the HappyRobot Engineering Intern technical challenge. It reads support messages from a `.csv` file, classifies them into predefined categories, analyzes their sentiment, and displays the results in a clean console dashboard.

##  Tech Stack & Libraries Used

* **Python 3.10**
* **Pandas:** For data manipulation and displaying the final results.
* **VaderSentiment:** For fast and accurate sentiment analysis of English text.

##  How to Run Locally

You can run this project on your local machine by following these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/100496773/AI_Support_Assistance.git
    cd AI_Support_Assistance
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS/Linux (WSL)
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```

You will see the full report printed directly to your console.

##  How to Run with Docker (Optional)

If you have Docker installed, you can build and run this project as a container.

1.  **Build the Docker image:**
    (Ensure you are in the project's root directory)
    ```bash
    docker build -t support-assistant .
    ```

2.  **Run the container:**
    (The `--rm` flag automatically cleans up and removes the container after it exits)
    ```bash
    docker run --rm support-assistant
    ```


##  How It Works: Classification Logic

The core classification logic is intentionally simple and robust, designed to be effective within the challenge's 4-6 hour scope.

1.  **Keyword-Based Matching:** The script uses predefined lists of keywords for each category (`Payment/Invoice`, `Delivery Issue`, `Shipment Status`).
2.  **Prioritization:** It checks for `Payment` and `Delivery Issue` keywords first, as these are more specific. A general `Shipment Status` keyword (like "delivery") might incorrectly override a more urgent "Delivery Issue" (like "damaged delivery").
3.  **Sentiment Analysis:** For sentiment, I chose to use the `vaderSentiment` library. It is lightweight, accurate for English, and provides a much more nuanced analysis (Positive, Negative, Neutral) than a simple keyword-based approach.

I chose this keyword-based logic because it is **fast to implement**, **easy to understand and maintain**, and **highly effective** for a well-defined problem with a small number of clear categories.