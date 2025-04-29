import json
import os
from dataclasses import dataclass, InitVar, field
from typing import Any


@dataclass
class FileManager:
    file_path: InitVar[str]
    file_name: InitVar[str]
    file_content: dict[str, Any] = field(init=False)

    def __post_init__(self, file_path: str, file_name: str) -> None:
        cur_dir = os.path.dirname(os.path.abspath(file_path))
        conf_path = os.path.join(cur_dir, file_name)
        with open(conf_path, 'r') as file:
            self.file_content = json.load(file)
