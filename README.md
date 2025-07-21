AI-Powered Browser Agent: Automate Web UI Testing with Plain English
Tired of complex, brittle code for web UI testing? This project introduces an AI-Powered Browser Agent that lets you automate web application testing using simple, plain English instructions. 
Leveraging the browser-use library and Google's Gemini AI, it transforms your natural language into precise browser actions, making testing accessible and efficient.






✨ Features
Plain English Test Scripts: Define test steps in a CSV file using natural language.

Automated Web Actions: The agent navigates, types, clicks, and verifies content autonomously.

Restricted Browsing: Confined to user-defined "allowed domains" for enhanced security.

Customizable AI Model: Easily switch the underlying Gemini model via config.py.

Visual Proof: Every test run is recorded as a GIF for quick review and detailed WebM videos.

Detailed Conversation Logs: Review the AI agent's full thought process and actions for each test.

Ready-to-Go Practice Site: Includes a simple Streamlit-based inventory management demo app for immediate testing.

🚀 Getting Started
Follow these steps to set up and run your first automated web test.

Prerequisites
Python: Version 3.11 or newer.

pip: Python's package installer.

Quick Setup
Clone the Repository:

git clone https://github.com/TensorNine/AIWebAppsTesting.git
cd AIWebAppsTesting

Set Up a Virtual Environment (Recommended):

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Install Dependencies:
Create a requirements.txt file in your project root:

pydantic
python-dotenv
browser-use
streamlit
bcrypt
asyncio

Then, install them:

pip install -r requirements.txt
playwright install chromium --with-deps --no-shell

Configure Environment Variables:
Create or update a .env file in your main project folder. This file will store your Google API Key and any site login credentials needed for testing.

GOOGLE_API_KEY="YOUR_GOOGLE_GENERATIVE_AI_API_KEY_HERE"

TEST_USERNAME="site_login_username" # Optional: if your tasks require login

TEST_PASSWORD="site_login_password" # Optional: if your tasks require login

ANONYMIZED_TELEMETRY=false # Set to true to send anonymous usage data to Browser-use

Important: Replace the placeholder values. Never share your .env file!

Configure AI Model and Allowed Domains:
Open config.py and adjust the LLM_MODEL and ALLOWED_DOMAINS variables. ALLOWED_DOMAINS is crucial for security, restricting where the agent can navigate.

# config.py
# ...
LLM_MODEL = "gemini-2.5-flash"

# CRITICAL: Define domains the agent is allowed to visit for security
ALLOWED_DOMAINS = ['http://localhost:8501', 'http://localhost:8501/*']

📝 How to Write Your Tests
Your test instructions are defined in testcases.csv. Each row represents a test scenario.

scenario_name,scenario_desc,task_description
Successful Login,Verify the user can successfully log in with valid credentials.,Go to http://localhost:8501; Type $TEST_USERNAME into the username box and $TEST_PASSWORD into the password box; Click the "Login" button; Check if I land on the dashboard page.
Failed Login (Invalid Credentials),Verify the user receives an error message when logging in with invalid credentials.,Go to http://localhost:8501; Type wrong@tensornine.com and wrongpassword into the login form; Click the "Login" button; Check if an error message "Invalid username or password" is displayed.
# ... (add more test cases here) ...

Note on Sensitive Data: Placeholders like $TEST_USERNAME and $TEST_PASSWORD in task_description are replaced by values from your .env file before being passed to the agent. This means the AI model will see the actual credentials. For a higher level of security where the AI model never sees sensitive data, consider using browser-use's Agent(sensitive_data=...) parameter with generic placeholders.

🏃‍♀️ Running the Tests
Start Your Target Website (Demo App):
Open a terminal and launch the included dummy inventory site:

python -m streamlit run ternsornine/main.py

(This usually opens at http://localhost:8501. Keep this terminal window open.)

Run the Browser Agent:
Open a new terminal and execute the test script:

python run_tests.py

You will see terminal messages, a browser window might pop up, and a test_artifacts/ folder will be created in your project root.

Test Artifacts
Inside the test_artifacts/ folder, you'll find a unique subdirectory for each test run, timestamped for easy tracking (e.g., test_artifacts/run_20240711_123456). This run-specific directory will contain:

test_results.csv: A summary of all tests for that specific run, including success status and comments.

conversations/: A folder with JSON logs of the AI's detailed conversation and actions for each test.

Individual test case folders (e.g., Successful_Login/) each containing its recorded GIF.
