from os import makedirs
from models import CompanyChat


def ensure_folder_exists(folder_path: str = "to_process") -> None:
    makedirs(folder_path, exist_ok=True)


def write_text_to_file(
    data: CompanyChat,
    folder_path: str = "to_process"
) -> None:
    file_path = folder_path + '/' + data.company + ".txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data.whole_chat)