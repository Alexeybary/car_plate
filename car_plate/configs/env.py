import typing
from pathlib import Path

from pydantic import BaseModel
from ruamel.yaml import YAML


class Context(BaseModel):
    yml: typing.Any
    package_dir: Path

    @classmethod
    def load(
        cls,
        package_dir: str | Path,
        yml_path: str | Path = None
    ) -> 'Context':
        """ Load configs from environment and YAML file """

        package_dir = Path(package_dir)
        if not package_dir.exists():
            raise FileNotFoundError(package_dir)

        yaml = YAML()
        yml_path = Path(yml_path or f'{package_dir}/configs/configs.yml')
        with yml_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        return cls(yml=yml_config, package_dir=package_dir)
