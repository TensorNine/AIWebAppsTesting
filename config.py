# config.py

# Define default paths for input and output files
INPUT_CSV_FILE = 'testcases.csv' # Path to the CSV file containing test case descriptions
OUTPUT_BASE_DIR = 'test_artifacts' # Base directory where all test results and GIFs will be saved
CONVERSATIONS_SUBDIR = 'conversations' # Subdirectories for recordings and conversation logs within each run's folder

# Define the LLM model to be used by the Browser Agent
# You can switch this to other available Google Generative AI models (e.g., "gemini-1.5-flash", "gemini-1.0-pro")
# Ensure the chosen model is suitable for the task and supported by langchain_google_genai.
LLM_MODEL = "gemini-2.5-flash"

# Define allowed domains for the BrowserSession for security.
# The agent will be restricted to only visiting URLs matching these patterns.
# This is crucial for preventing the agent from navigating to unintended sites,
# especially when handling sensitive data.
# Example: ['https://*.example.com', 'https://another-safe-site.com']
# For the dummy Streamlit app, we'll allow localhost.
ALLOWED_DOMAINS = ['http://localhost:8501', 'http://localhost:8501/*']


