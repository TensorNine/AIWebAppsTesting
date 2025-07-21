#run_tests.py
import os
import csv
import asyncio
from pydantic import BaseModel, ValidationError
from browser_use.llm import ChatGoogle
from dotenv import load_dotenv
from browser_use import Agent, Controller, BrowserSession
from datetime import datetime

from config import INPUT_CSV_FILE, OUTPUT_BASE_DIR, LLM_MODEL, ALLOWED_DOMAINS, CONVERSATIONS_SUBDIR


load_dotenv(override=True)


class TestCase(BaseModel):
    scenario_name: str
    scenario_desc: str
    success: bool
    comments: str

class TestCases(BaseModel):
    testcases: list[TestCase]


controller = Controller(output_model=TestCases)


def load_env_variables():
    """Loads and returns test credentials (username and password) from environment variables."""
    test_username = os.getenv('TEST_USERNAME')
    test_password = os.getenv('TEST_PASSWORD')

    if not test_username or not test_password:
        print("Warning: TEST_USERNAME and/or TEST_PASSWORD environment variables are not set.")
        print("Please ensure they are set in your .env file if needed for task substitution.")
    return test_username, test_password


def read_test_cases(file_path: str) -> list[dict]:
    """Reads test cases from a specified CSV file."""
    all_tasks = []
    print(f"Loading tasks from {file_path}...")
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Only require scenario_name and task_description columns
            required_columns = {'scenario_name', 'task_description'}
            if not required_columns.issubset(reader.fieldnames):
                print(f"Error: CSV missing one or more required columns: {required_columns - set(reader.fieldnames)}.")
                return []
            for row in reader:
                all_tasks.append({
                    "name": row['scenario_name'],
                    "description": row['task_description'],
                })
        print(f"Loaded {len(all_tasks)} tasks.")
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please ensure the CSV file exists.")
        return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    return all_tasks


def setup_output_directories(base_dir: str, task_name: str) -> str:
    """Creates the base output directory and a task-specific subdirectory for artifacts."""
    os.makedirs(base_dir, exist_ok=True)
    task_name_sanitized = task_name.replace(' ', '_').replace(':', '').replace('/', '_').replace('\\', '_').replace('.', '')
    task_output_dir = os.path.join(base_dir, task_name_sanitized)
    os.makedirs(task_output_dir, exist_ok=True)
    return task_output_dir


async def run_single_test(
    task_info: dict,
    llm: ChatGoogle,
    controller: Controller,
    browser_session: BrowserSession,
    task_output_dir: str,
    run_recording_dir: str,
    run_conversation_dir: str,
    test_username: str, 
    test_password: str,
) -> TestCase:
    """Runs a single test case using the Browser Agent and processes its result."""
    task_name_sanitized = task_info.get('name', "Unnamed_Task").replace(' ', '_').replace(':', '').replace('/', '_').replace('\\', '_').replace('.', '')
    raw_task_description = task_info['description']
    
    
    processed_task_description = raw_task_description.replace('$TEST_USERNAME', test_username)
    processed_task_description = processed_task_description.replace('$TEST_PASSWORD', test_password)

    gif_path = os.path.join(task_output_dir, f"{task_name_sanitized}.gif")
    
    recording_path = os.path.join(run_recording_dir, f"{task_name_sanitized}_recording.webm")
    conversation_path = os.path.join(run_conversation_dir, f"{task_name_sanitized}_conversation.json")


    print(f"\n--- Running Task: {task_name_sanitized} ---")
    print(f"Description: {processed_task_description}") # Log the processed description
    print(f"Saving GIF to: {gif_path}")
    print(f"Saving Recording to: {recording_path}")
    print(f"Saving Conversation to: {conversation_path}")

    agent = Agent(
        task=processed_task_description, # Use the processed task description
        llm=llm,
        controller=controller,
        generate_gif=gif_path,
        browser_session=browser_session,
        use_vision=False, # Still recommended to avoid LLM seeing sensitive info if it appears on screen
        save_conversation_path=conversation_path,
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        parsed: TestCases = TestCases.model_validate_json(result)
        if parsed.testcases:
            testcase = parsed.testcases[0]
            print(f'Scenario: {testcase.scenario_name}')
            print(f'Description: {testcase.scenario_desc}')
            print(f'Success: {testcase.success}')
            print(f'Comments: {testcase.comments}')
            return testcase


def save_test_results(results: list[TestCase], output_file_path: str):
    """Saves a list of TestCase objects (test outcomes) to a CSV file."""
    if results:
        print(f"\nSaving all test results to {output_file_path}...")
        try:
            with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['scenario_name', 'scenario_desc', 'success', 'comments']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for testcase in results:
                    writer.writerow(testcase.model_dump())
            print(f"Saved {len(results)} test results.")
        except Exception as e:
            print(f"Error writing output CSV: {e}")
    else:
        print("\nNo results to save.")


async def main():
    """Main function to orchestrate the entire test execution process."""
    test_username, test_password = load_env_variables() # Credentials loaded here for substitution

    # Generate a unique run ID based on timestamp
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    current_run_output_dir = os.path.join(OUTPUT_BASE_DIR, run_id)
    os.makedirs(current_run_output_dir, exist_ok=True)

    # Create subdirectories for conversations within the run ID folder
    run_conversation_dir = os.path.join(current_run_output_dir, CONVERSATIONS_SUBDIR)
    os.makedirs(run_conversation_dir, exist_ok=True)


    print(f"Output artifacts for this run will be saved in: {os.path.abspath(current_run_output_dir)}")

    all_tasks = read_test_cases(INPUT_CSV_FILE)
    if not all_tasks:
        print("No tasks found or loaded. Exiting.")
        return

    llm = ChatGoogle(model=LLM_MODEL)
    
    browser_session = BrowserSession(allowed_domains=ALLOWED_DOMAINS)

    all_parsed_test_cases = []

    for i, task_info in enumerate(all_tasks):
        task_output_dir = setup_output_directories(current_run_output_dir, task_info.get('name', f"Unnamed_Task_{i+1}"))
        
        test_result = await run_single_test(
            task_info,
            llm,
            controller,
            browser_session,
            task_output_dir,
            run_recording_dir,
            run_conversation_dir,
            test_username, 
            test_password, 
        )
        if test_result:
            all_parsed_test_cases.append(test_result)

    final_output_csv_path = os.path.join(current_run_output_dir, 'test_results.csv')
    save_test_results(all_parsed_test_cases, final_output_csv_path)


if __name__ == "__main__":
    asyncio.run(main())
