from layers.layer_base import LayerBase


class Wtp(LayerBase):
    def __init__(self):
        super().__init__("wtp")
        self.parse_dates = ['input_date']
