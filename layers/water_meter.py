from layers.layer_base import LayerBase


class WaterMeter(LayerBase):
    def __init__(self):
        super().__init__("water_meter")
        self.parse_dates = ['input_date', 'installation_date']
