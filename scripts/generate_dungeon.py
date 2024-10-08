import argparse

import yaml
from yaml import Loader

from hamingja_dungeon.utils.ascii_dungeon_generator.config.ascii_dungeon_config import (
    ASCIIDungeonConfig,
)

from hamingja_dungeon.utils.ascii_dungeon_generator.ascii_dungeon_generator import (
    ASCIIDungeonGenerator,
)


def get_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("output_file", help="The text file to save the map to.")
    # parser.add_argument("-w", type=int, help="Width of the map.", default=70)
    # parser.add_argument("-h", type=int, help="Height of the map.", default=70)
    parser.add_argument(
        "--config",
        type=str,
        help="Config file for the dungeon generation. Other specified arguments"
        "will not be overwritten.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    with open(args.config, "r") as file:
        data = yaml.load(file, Loader=Loader)
    gen_config = ASCIIDungeonConfig(**data)
    generator = ASCIIDungeonGenerator(gen_config)

    dungeon = generator.generate()
    dungeon.save_as(args.output_file)
    print(dungeon.content)