from pathlib import Path

from pydantic import BaseModel

from car_plate.configs.env import Context


__all__ = [
    'CarPartsConfigs',
]

class CarPartsConfigs(BaseModel):
    """Class to store configs for car parts segmentation"""

    weights_path: str
    classes: int
    encoder_weights: str
    path_to_metafile: str
    size: int
    iter_frame: int

    @classmethod
    def from_context(cls, context: 'Context') -> 'CarPartsConfigs':
        return cls(**context.yml['car_parts'])


class DamageConfigs(BaseModel):
    """Class to store configs for car parts segmentation"""

    weights_path: str
    classes: int
    encoder_weights: str
    path_to_metafile: str
    size: int

    @classmethod
    def from_context(cls, context: 'Context') -> 'DamagePartsConfigs':
        return cls(**context.yml['damage_parts'])


class Configs:
    @classmethod
    def from_package(cls, entrypoint: str, **kwargs) -> 'Configs':
        package_dir = Path(entrypoint).parent
        return cls(
            package_dir=package_dir,
            yml_path=package_dir / 'configs/configs.yml',
            **kwargs
        )

    def __init__(self, package_dir: str | Path, **kwargs) -> None:
        self.context = Context.load(package_dir, **kwargs)

        self.car_parts = CarPartsConfigs.from_context(self.context)
        self.car_damages = DamageConfigs.from_context(self.context)
