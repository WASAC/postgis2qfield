from layers.layer_base import LayerBase


class Junction(LayerBase):
    def __init__(self):
        super().__init__("junction")
        self.parse_dates = ['input_date']
