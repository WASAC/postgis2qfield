from layers.layer_base import LayerBase


class Chamber(LayerBase):
    def __init__(self):
        super().__init__("chamber")
        self.parse_dates = ['input_date']
