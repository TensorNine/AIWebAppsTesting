# AI-Powered Browser Agent: Automate Web UI Testing with Plain English

Tired of complex, brittle code for web UI testing?  
This project introduces an **AI-Powered Browser Agent** that lets you automate web application testing using simple, plain English instructions. Leveraging the `browser-use` library and Google’s Gemini AI, it transforms your natural language into precise browser actions, making testing accessible and efficient for everyone.

## ✨ Features
- **Plain English Test Scripts**: Define test steps in a CSV file using natural language.
- **Automated Web Actions**: The agent autonomously navigates, types, clicks, and verifies content.
- **Restricted Browsing**: Confined to user-defined allowed domains for enhanced security.
- **Customizable AI Model**: Easily switch the underlying Gemini model via `config.py`.
- **Visual Proof**: Every test run is recorded as a GIF for quick review and detailed WebM videos.
- **Detailed Conversation Logs**: Review the AI agent’s full thought process and actions for each test.
- **Ready-to-Go Practice Site**: Includes a simple Streamlit-based inventory management demo app for immediate testing.

## 🚀 Getting Started
Follow these steps to set up and run your first automated web test.

### Prerequisites
- **Python**: Version 3.11 or newer.
- **pip**: Python’s package installer.

### Quick Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/TensorNine/AIWebAppsTesting.git
   cd AIWebAppsTesting
   ```

2. **Set Up a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**  
   First, create a `requirements.txt` file in your project root containing:
   ```
   pydantic
   python-dotenv
   browser-use
   streamlit
   bcrypt
   asyncio
   ```
   Then, install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium --with-deps --no-shell
   ```

4. **Configure Environment Variables**  
   Create or update a `.env` file in your main project folder to store your API key and any login credentials needed for testing:
   ```
   GOOGLE_API_KEY="YOUR_GOOGLE_GENERATIVE_AI_API_KEY_HERE"
   TEST_USERNAME="site_login_username"      # Optional
   TEST_PASSWORD="site_login_password"      # Optional
   ANONYMIZED_TELEMETRY=false               # Set to true to send anonymous usage data to Browser-use
   ```
   **Important**: Replace the placeholder values. Never share your `.env` file!

5. **Configure AI Model and Allowed Domains**  
   Open `config.py` and adjust the `LLM_MODEL` and `ALLOWED_DOMAINS` variables.  
   `ALLOWED_DOMAINS` is crucial for security, restricting where the agent can navigate.
   ```python
   # config.py
   LLM_MODEL = "gemini-2.5-flash"
   # CRITICAL: Define domains the agent is allowed to visit for security
   ALLOWED_DOMAINS = ['http://localhost:8501', 'http://localhost:8501/*']
   ```

## 📝 How to Write Your Tests
Your test instructions are defined in `testcases.csv`. Each row represents a test scenario, for example:

| scenario_name        | scenario_desc                                  | task_description                                                                 |
|----------------------|-----------------------------------------------|----------------------------------------------------------------------------------|
| Successful Login     | Verify successful login with valid credentials. | Go to http://localhost:8501; Type $TEST_USERNAME into the username box and $TEST_PASSWORD into the password box; Click the "Login" button; Check if I land on dashboard. |
| Failed Login (Invalid) | Verify error message for invalid login credentials. | Go to http://localhost:8501; Type wrong@tensornine.com and wrongpassword into the login form; Click the "Login" button; Check if error message "Invalid username or password" is displayed. |

### Note on Sensitive Data
- Placeholders like `$TEST_USERNAME` and `$TEST_PASSWORD` in `task_description` are replaced by values from your `.env` file before being passed to the agent.
- For higher security—where the AI model never sees sensitive data—consider using `browser-use`'s `Agent(sensitive_data=...)` parameter with generic placeholders.

## 🏃‍♀️ Running the Tests
1. **Start the Target Website (Demo App)**  
   Open a terminal and launch the included dummy inventory site:
   ```bash
   python -m streamlit run tensornine/main.py
   ```
   (Usually opens at `http://localhost:8501`. Keep this terminal window open.)

2. **Run the Browser Agent**  
   Open a new terminal and execute:
   ```bash
   python run_tests.py
   ```
   You will see terminal messages, a browser window may pop up, and a `test_artifacts/` folder will be created in your project root.

## 📂 Test Artifacts
Inside the `test_artifacts/` folder, you'll find a unique subdirectory for each test run (timestamped for easy tracking), e.g.:  
`test_artifacts/run_20240711_123456`

Each run-specific directory contains:
- `test_results.csv`: Summary of all tests, including success status and comments.
- `conversations/`: JSON logs of the AI's detailed conversation and actions for each test.
- Individual test case folders (e.g., `Successful_Login/`): Each containing its recorded GIF for visual proof.

Enjoy fast, flexible, and code-free web app test automation!