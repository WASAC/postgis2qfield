from layers.layer_base import LayerBase


class Reservoir(LayerBase):
    def __init__(self):
        super().__init__("reservoir")
        self.parse_dates = ['input_date', 'meter_installation_date']
