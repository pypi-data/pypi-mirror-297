from public.block import Block
from public.validation_configs.blocks import BlockTypes
from collections import Counter


def has_duplicate_block_names(blocks):
    block_names = [block.name for block in blocks]
    name_counts = Counter(block_names)
    duplicates = {name: count for name, count in name_counts.items() if count > 1}
    if duplicates:
        raise ValueError(f"Blocks with duplicate names found: {duplicates}")


def to_dict(self):
    return {
        "canvas_name": self.name,
        "blocks": [block.to_dict(self.workspace_id) for block in self.blocks],
        "canvas_id": self.id,
        "workspace_id": self.workspace_id,
        "requirements": self.requirements,
    }


def transform_blocks(self, blocks):
    print("Fetched blocks:")
    print(blocks)
    for block in blocks:
        transformed_block = Block(
            name=block["name"],
            id=block["id"],
            type=BlockTypes(block["type"]),
            content=block["content"],
        )
        self.blocks.append(transformed_block)


def assign_block_ids(self, new_blocks):
    for block in new_blocks:
        for existing_block in self.blocks:
            if block["name"] == existing_block.name:
                existing_block.id = block["id"]


def find_block_by_name(self, block_name):
    block_to_run = [block for block in self.blocks if block.name == block_name]
    if not block_to_run:
        raise ValueError(f"Block with name '{block_name}' not found")
    if len(block_to_run) > 1:
        raise ValueError(f"Multiple blocks with name '{block_name}' found")
    return block_to_run[0]
