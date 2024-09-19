import json
import logging
import os
from typing import Optional

from pydantic import BaseModel

class SecretsJSON:
    def __init__(self, path: str, model: BaseModel) -> None:
        self.path: str = path
        self.model: Optional[BaseModel] = None
        
        if not os.path.exists(self.path):
            logging.error(f"Secrets file '{self.path}' does not exist.")
            return
        
        try:
            with open(self.path, 'r') as file:
                json_data = file.read()
        except IOError as e:
            logging.error(f"Error reading secrets file '{self.path}': {e}")
            return

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            return

        try:
            new_model = model(**data)
            self.model = new_model
        except Exception as ex:
            logging.error(f"Error creating model: {e}")
            