from car_plate.configs import Configs
from car_plate.model import UnetParts


configs = Configs.from_package(__file__)

ocr_recognition = UnetParts(configs.car_parts, configs.car_damages)
