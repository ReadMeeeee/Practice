from json import load
from models import InstructionBlock


def load_data(instruction_path: str) -> str:
    with open(instruction_path, "r", encoding="utf-8") as f:
        return f.read()


def load_instruction_file(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = load(f)

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