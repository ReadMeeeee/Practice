from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    text: str


@dataclass
class Chat:
    messages: list[Message]
    name: str = None
    numbers: list[str] = None


@dataclass
class CompanyChat:
    company: str
    whole_chat: str


@dataclass
class InstructionBlock:
    role: str
    instruction: str
    context: str
    format: str | None
    max_tokens: int


@dataclass
class LLMRequest:
    instruction_block: InstructionBlock
    task: str


    def to_prompt(self) -> list[dict[str, str]]:
        prompt = (
            f"{self.instruction_block.instruction}\n\n"
            f"Контекст:\n{self.instruction_block.context}\n\n"
            f"Формат вывода:\n{self.instruction_block.format}\n\n"
            f"Ограничение по токенам:\n{self.max_tokens}\n\n"
            f"Входные данные:\n{self.task}"
        )
        return [
            {"role": "system", "content": self.instruction_block.role},
            {"role": "user", "content": prompt}
        ]


    @property
    def max_tokens(self) -> int:
        return self.instruction_block.max_tokens



@dataclass
class ProblemWithSolution:
        description: str
        keywords: list[str]
        solution: str
        name: str = "untitled"
        numbers: list[str] = None
