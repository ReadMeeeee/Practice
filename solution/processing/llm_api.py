from os import path
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

from solution.models import LLMRequest, ProblemWithSolution
from solution.file_io import load_data, load_instruction_file

class AIModelAPI:
    def __init__(self, api: str, url: str, model_name: str):
        self.api = api
        self.url = url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api, base_url=self.url)

    def get_response(self, request: LLMRequest,
                     max_tokens: int = 50, temperature: float = 0.1):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=request.to_prompt(),
            stream=False,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content


def chat_process(
        model: AIModelAPI,
        path_to_instruct_json: str,
        path_to_task_txt: str,
        multi_thread: bool = False
) -> ProblemWithSolution:
    def _call_request(request: LLMRequest) -> str:
        result = model.get_response(request, max_tokens=request.max_tokens)
        return result

    def _check_json_and_txt(path_json: str, path_to_txt: str, ) -> None:
        shaped_path_task = path.splitext(path.basename(path_to_txt))
        format_of_file_task = shaped_path_task[1]
        if format_of_file_task != ".txt":
            raise ValueError(f"Ожидаемый формат файла задачи - .txt, получен - {format_of_file_task}")

        shaped_path_instruct = path.splitext(path.basename(path_json))
        format_of_file_instruct = shaped_path_instruct[1]
        if format_of_file_instruct != ".json":
            raise ValueError(f"Ожидаемый формат файла инструкций - .json, получен - {format_of_file_task}")

    _check_json_and_txt(path_json=path_to_instruct_json, path_to_txt=path_to_task_txt)

    name = path.splitext(path.basename(path_to_task_txt))[0]

    general_task = load_data(path_to_task_txt)

    instructions = load_instruction_file(path_to_instruct_json)
    i_description = instructions["instruction_for_description"]
    i_keywords = instructions["instruction_for_keywords"]
    i_solution = instructions["instruction_for_solution"]

    r_description = LLMRequest(i_description, task=general_task)
    r_keywords = LLMRequest(i_keywords, task=general_task)
    r_solution = LLMRequest(i_solution, task=general_task)

    tasks = {
        "description": r_description,
        "keywords": r_keywords,
        "solution": r_solution
    }

    results: dict[str, str] = {}

    if multi_thread:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_label = {
                executor.submit(_call_request, request): label
                for label, request in tasks.items()
            }
            for future in as_completed(future_to_label):
                label = future_to_label[future]
                try:
                    results[label] = future.result(timeout=30)
                except Exception as e:
                    results[label] = f"Ошибка: {e}"

    else:
        for label, request in tasks.items():
            try:
                results[label] = _call_request(request)
            except Exception as e:
                results[label] = f"Ошибка: {e}"

    for key in tasks:
        results.setdefault(key, "")

    return ProblemWithSolution(
        name=name,
        description=results["description"],
        keywords=results["keywords"].split(','),
        solution=results["solution"]
    )