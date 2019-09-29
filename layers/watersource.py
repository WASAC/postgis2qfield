from layers.layer_base import LayerBase


class WaterSource(LayerBase):
    def __init__(self):
        super().__init__("watersource")
        self.parse_dates = ['input_date']
