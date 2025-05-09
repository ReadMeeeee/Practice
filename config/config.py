from os import path, getenv
from dotenv import load_dotenv
from processing import AIModelAPI


CURRENT_FILE = path.abspath(__file__)
CURRENT_DIR = path.dirname(CURRENT_FILE)
ROOT_DIR = path.dirname(CURRENT_DIR)

path_to_process = path.join(ROOT_DIR, 'to_process')
path_to_input_data = path.join(ROOT_DIR, 'input_data')
path_to_instruct_json = path.join(ROOT_DIR, 'config', 'prompt_data.json')

load_dotenv()

chatgpt_api = AIModelAPI(getenv("API_GPT"), "https://api.openai.com/v1", "gpt-4-turbo")
deepseek_api = AIModelAPI(getenv("API_DS"), "https://api.deepseek.com", "deepseek-chat")
