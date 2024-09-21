import inspect
from .validation_configs.blocks import (
    BLOCKS_WITH_CONFIGURABLE_COMPUTE_ENV_TYPE,
    COMPUTE_ENV_TYPE,
    MARATHON_RESOURCE_SPECS,
    BlockTypes,
    ComputeEnvironmentType,
)


class Block:
    def __init__(
        self,
        name="block",
        id=None,
        connected_ids=[],
        type: BlockTypes = BlockTypes.PYTHON,
        compute_environment_type: COMPUTE_ENV_TYPE = None,
        content=None,
    ):
        self.name = name
        self.id = id
        self.connected_ids = connected_ids
        self.type = type
        self.content = content
        self.compute_environment_type = compute_environment_type

    def to_dict(self, workspace_id):
        if self.compute_environment_type:
            if (
                self.type not in BLOCKS_WITH_CONFIGURABLE_COMPUTE_ENV_TYPE
                and self.compute_environment_type
            ):
                raise ValueError(
                    f"Block type {self.type.name} does not support compute environment configuration"
                )
            if (
                self.compute_environment_type.ENV_TYPE == ComputeEnvironmentType.AWS_FARGATE
                and not workspace_id
            ):
                raise ValueError(
                    "Workspace ID is required for AWS Fargate compute environment configuration"
                )

        return {
            "block_name": self.name,
            "connected_ids": self.connected_ids,
            "content": self.content,
            "type": self.type,
            "compute_environment_type": {
                "ENV_TYPE": self.compute_environment_type.ENV_TYPE.name,
                "MARATHON_RESOURCE_SPECS": MARATHON_RESOURCE_SPECS[
                    self.compute_environment_type.MARATHON_SIZE
                ]
                if self.compute_environment_type.MARATHON_SIZE
                else None,
            }
            if self.compute_environment_type
            else None,
        }

    def __enter__(self):
        self.frame = inspect.currentframe().f_back
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        function_source = inspect.getsource(self.frame.f_code)
        starting_line = self.frame.f_lineno
        function_lines = function_source.splitlines()

        # Find the line corresponding to the "with" statement
        with_line_index = None
        for idx, line in enumerate(function_lines):
            if starting_line == self.frame.f_code.co_firstlineno + idx:
                with_line_index = idx
                break

        # Find the indented block (inside the 'with' statement)
        if with_line_index is not None:
            # Extract lines within the with block based on indentation
            block_lines = []
            for line in function_lines[with_line_index + 1 :]:
                if line.startswith(" " * 4):  # Assuming 4 spaces for indentation
                    block_lines.append(line.strip())
                else:
                    break  # Stop when the indentation ends
            self.content = "\n".join(block_lines)
