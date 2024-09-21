from enum import IntEnum, Enum
from pydantic import BaseModel, root_validator


class BlockTypes(IntEnum):
    PYTHON = 1
    R = 2
    SQL = 3
    MARKDOWN = 4
    API_CONTROLLER = 7
    API_ROUTE = 8
    GEN_AI = 9
    BEDROCK = 10
    RMARKDOWN = 11
    ENDPOINT_INVOCATION = 13
    SNOWPARK = 14
    AGGREGATOR = 15


class MarathonSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"
    xlarge = "xlarge"
    xxlarge = "2xlarge"


class ComputeEnvironmentType(Enum):
    AWS_LAMBDA = 1
    AWS_FARGATE = 2


MARATHON_RESOURCE_SPECS = {
    MarathonSize.small: (1024, 8192),
    MarathonSize.medium: (2048, 16384),
    MarathonSize.large: (4096, 30720),
    MarathonSize.xlarge: (8192, 61440),
    MarathonSize.xxlarge: (16384, 122880),
}

BLOCKS_WITH_CONFIGURABLE_COMPUTE_ENV_TYPE = {
    BlockTypes.PYTHON,
    BlockTypes.SQL,
    BlockTypes.R,
    BlockTypes.GEN_AI,
    BlockTypes.SNOWPARK,
}


class COMPUTE_ENV_TYPE(BaseModel):
    ENV_TYPE: ComputeEnvironmentType | None
    MARATHON_SIZE: MarathonSize | None = None

    @root_validator(pre=True)
    def check_marathon_resource_specs(cls, values):
        env_type = values.get("ENV_TYPE")
        marathon_size = values.get("MARATHON_SIZE")

        if env_type == ComputeEnvironmentType.AWS_FARGATE and marathon_size is None:
            raise ValueError("MARATHON_SIZE is required when ENV_TYPE is AWS_FARGATE")
        if env_type == ComputeEnvironmentType.AWS_LAMBDA and marathon_size is not None:
            raise ValueError("MARATHON_SIZE is not allowed when ENV_TYPE is AWS_LAMBA")
        return values
