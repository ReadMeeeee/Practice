from os import path

from config import (
    chatgpt_api,
    deepseek_api,
    path_to_instruct_json,
    path_to_process,
    path_to_input_data
)
from processing import chat_process, process_all_docs
from file_io import upload_data
from models import ProblemWithSolution


def main():
    model = deepseek_api

    company_chats = process_all_docs(path_to_input_data, output_dir=path_to_process)

    if not company_chats:
        print("Нет данных для обработки.")
        return

    list_of_sol: list[ProblemWithSolution] = []
    for company in company_chats:
        task_filename = f"{company.company}.txt"
        path_to_task_txt = path.join(path_to_process, task_filename)

        try:
            sol = chat_process(
                model=model,
                path_to_instruct_json=path_to_instruct_json,
                path_to_task_txt=path_to_task_txt,
                multi_thread=True
            )
            list_of_sol.append(sol)

            '''
            separator = "-" * 50
            print(
                f"\nРезультат для компании: {company.company}\n"
                f"{separator}\n{sol.name}\n{separator}\n"
                f"{sol.description}\n{separator}\n"
                f"{' '.join(sol.keywords)}\n{separator}\n"
                f"{sol.solution}"
            )
            '''

        except FileNotFoundError:
            print(f"Файл не найден: {path_to_task_txt}")
        except Exception as e:
            print(f"Ошибка при обработке {company.company}: {e}")

    if list_of_sol:
        upload_data(json_path="solutions.json", list_of_sol=list_of_sol)
    else:
        print("Нет решений для записи.")


if __name__ == "__main__":
    main()
