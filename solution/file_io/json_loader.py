from json import load, dump
from os import path
from solution.models import InstructionBlock, ProblemWithSolution


def load_data(instruction_path: str) -> str:
    if not path.exists(instruction_path):
        raise FileNotFoundError(f"Файл не найден: {instruction_path}")

    with open(instruction_path, "r", encoding="utf-8") as f:
        return f.read()


def load_instruction_file(json_path: str):
    if not path.exists(json_path):
        raise FileNotFoundError(f"Файл не найден: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = load(f)

    required_keys = {"context", "role", "instructions"}
    if not required_keys.issubset(data):
        raise KeyError(f"JSON не содержит необходимые ключи: {required_keys - set(data)}")

    instructions_required = {"description", "keywords", "solution"}
    if not instructions_required.issubset(data["instructions"]):
        raise KeyError(f"Инструкции не содержат ключи: {instructions_required - set(data['instructions'])}")

    abbreviations = "\n".join(data["context"])
    role = data["role"]

    def make_instruction(key: str) -> InstructionBlock:
        item = data["instructions"][key]
        return InstructionBlock(
            role=role,
            instruction=item["instruction"],
            context=abbreviations,
            format=item["response_format"],
            max_tokens=item["max_tokens"]
        )

    return {
        "abbreviations": abbreviations,
        "instruction_for_description": make_instruction("description"),
        "instruction_for_keywords": make_instruction("keywords"),
        "instruction_for_solution": make_instruction("solution"),
    }


def upload_data(json_path: str, list_of_sol: list[ProblemWithSolution]):
    sol_json: list[dict] = []
    for sol in list_of_sol:
        str_to_write = {
            "company": sol.name,
            "description": sol.description,
            "keywords": sol.keywords,
            "solution": sol.solution
        }

        sol_json.append(str_to_write)

    with open(json_path, "w", encoding="utf-8") as f:
        dump(sol_json, f, ensure_ascii=False, indent=4)
