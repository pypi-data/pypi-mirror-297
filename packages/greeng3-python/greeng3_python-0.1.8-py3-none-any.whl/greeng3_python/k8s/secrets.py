import json
import logging
import os
from typing import Optional, Union

from pydantic import BaseModel, RootModel

class SecretsValidatedJSON:
    def __init__(self, path: str, model: BaseModel) -> None:
        self.path: str = path
        self.model: BaseModel = model
        self.secret_data: Optional[Union[BaseModel, RootModel]] = None
        
        try:
            with open(self.path, 'r') as file:
                self.secret_data = model.model_validate_json(file.read())
        except Exception as ex:
            logging.error(f"Error reading/validating secrets file '{self.path}': {ex}")
            