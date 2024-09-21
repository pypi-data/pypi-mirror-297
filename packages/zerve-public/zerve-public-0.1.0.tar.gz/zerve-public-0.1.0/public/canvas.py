import json
import requests
import os
import yaml
from .block import Block
from .helpers.canvas_helpers import (
    assign_block_ids,
    find_block_by_name,
    has_duplicate_block_names,
    to_dict,
    transform_blocks,
)
from .validation_configs.blocks import COMPUTE_ENV_TYPE, BlockTypes

ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "https://canvas.api.zerve.ai/zerve_public")


class Canvas:
    def __init__(self, name="canvas", id=None, requirements=[]):
        self.name = name
        self.id = id
        self.requirements: list[str] = requirements
        self.blocks: list[Block] = []
        self.api_key, self.workspace_id = self.load_yaml_file()
        self.headers = {"X-API-Key": self.api_key}

    def load_yaml_file(self):
        """
        Load the API,WORKSPACE-ID from the YAML config file.
        """
        with open("config.yml", "r") as file:
            config = yaml.safe_load(file)
            if not config or not config.get("X-API-Key"):
                raise ValueError("API Key not found in config")
            return (config.get("X-API-Key"), config.get("WORKSPACE-ID"))

    def create_block(
        self,
        block_name,
        connected_ids=[],
        type: BlockTypes = BlockTypes.PYTHON,
        compute_environment_type: COMPUTE_ENV_TYPE = None,
    ):
        block = Block(
            name=block_name,
            connected_ids=connected_ids,
            type=type,
            compute_environment_type=compute_environment_type,
        )
        self.blocks.append(block)
        return block

    def get(self):
        print("Getting canvas")
        endpoint_url = f"{ENDPOINT_URL}/canvas/{self.id}"
        response = requests.get(endpoint_url, headers=self.headers).json()
        transform_blocks(self, response["blocks"])
        print(
            json.dumps(
                response["message"],
                indent=4,
            )
        )

    def run(self):
        print("Running canvas")
        has_duplicate_block_names(self.blocks)
        payload = to_dict(self)
        endpoint_url = f"{ENDPOINT_URL}/canvas"
        response = requests.post(
            endpoint_url, data=json.dumps(payload), headers=self.headers
        ).json()
        self.id = response["canvas_id"]
        assign_block_ids(self, response["blocks"])
        print(response["message"])

    def run_all(self, force_run=False):
        print("Running all blocks")
        payload = {"canvas_id": self.id, "force_run": force_run}
        endpoint_url = f"{ENDPOINT_URL}/run_all_blocks"
        response = requests.post(
            endpoint_url, data=json.dumps(payload), headers=self.headers
        ).json()
        print(response["message"])

    def run_block_by_name(self, block_name):
        print(f"Running block with name '{block_name}'")
        block = find_block_by_name(self, block_name)
        payload = {"canvas_id": self.id, "block_id": block.id}
        endpoint_url = f"{ENDPOINT_URL}/run_block"
        response = requests.post(
            endpoint_url, data=json.dumps(payload), headers=self.headers
        ).json()
        print(response["message"])

    def run_up_to_block_by_name(self, block_name, force_run=False):
        print(f"Running up to block with name '{block_name}'")
        block = find_block_by_name(self, block_name)
        payload = {"canvas_id": self.id, "block_id": block.id, "force_run": force_run}
        endpoint_url = f"{ENDPOINT_URL}/run_up_to_block"
        response = requests.post(
            endpoint_url, data=json.dumps(payload), headers=self.headers
        ).json()
        print(response["message"])

    def delete_block_by_name(self, block_name):
        print(f"Deleting block with name '{block_name}'")
        block = find_block_by_name(self, block_name)
        payload = {"canvas_id": self.id, "block_id": block.id}
        endpoint_url = f"{ENDPOINT_URL}/delete_block"
        response = requests.delete(
            endpoint_url, data=json.dumps(payload), headers=self.headers
        ).json()
        print(response["message"])
