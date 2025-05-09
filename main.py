from os import path

from config import (
    chatgpt_api,
    deepseek_api,
    path_to_instruct_json,
    path_to_process,
    path_to_input_data
)
from processing import chat_process, process_all_docs


def main():
    model = deepseek_api

    company_chats = process_all_docs(path_to_input_data, output_dir=path_to_process)

    for company in company_chats:
        task_filename = f"{company.company}.txt"
        path_to_task_txt = path.join(path_to_process, task_filename)

        if not path.exists(path_to_task_txt):
            print(f"Файл не найден: {path_to_task_txt}")
            continue

        try:
            sol = chat_process(
                model=model,
                path_to_instruct_json=path_to_instruct_json,
                path_to_task_txt=path_to_task_txt,
                multi_thread=True
            )

            separator = "-" * 50
            print(
                f"\nРезультат для компании: {company.company}\n"
                f"{separator}\n{sol.name}\n{separator}\n"
                f"{sol.description}\n{separator}\n"
                f"{' '.join(sol.keywords)}\n{separator}\n"
                f"{sol.solution}"
            )

        except Exception as e:
            print(f"Ошибка при обработке {company.company}: {e}")


if __name__ == "__main__":
    main()