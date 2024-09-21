import json
import logging
import os
from typing import Any

from pydantic import BaseModel

class SecretsJSON:
    def __init__(self, path: str, model: BaseModel) -> None:
        self.path: str = path
        self.model: BaseModel = model
        self.json_data: Any = None
        
        try:
            with open(self.path, 'r') as file:
                self.json_data = model.model_validate_json(file.read())
        except IOError as ex:
            logging.error(f"Error reading/validating secrets file '{self.path}': {ex}")
            