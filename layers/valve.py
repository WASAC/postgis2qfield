from layers.layer_base import LayerBase


class Valve(LayerBase):
    def __init__(self):
        super().__init__("valve")
        self.parse_dates = ['input_date']
