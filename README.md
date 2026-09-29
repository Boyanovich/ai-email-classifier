# AI Email Classifier

This script automates the monitoring, fetching, and AI-based classification of unread emails from a Gmail inbox.

## Features

* Continually fetches unseen emails using the IMAP protocol over SSL.
* Automatically retrieves the best performing free LLM model dynamically via an external API.
* Uses the OpenRouter API to classify email content based on customizable instructions.
* Extracts plain text bodies from both simple and complex multipart emails seamlessly.
* Maintains flexibility by loading AI classification rules externally from a local `prompt.txt` file.

## Setup & Run

1. Install required dependencies: `pip install -r requirements.txt`
2. Create a `prompt.txt` file in the same directory and define your AI classification instructions.
3. Create a `.env` file in the root directory and add your credentials (`EMAIL_USER`, `EMAIL_PASS`, `OPENROUTER_KEY`).
4. Execute the script: `python main.py`