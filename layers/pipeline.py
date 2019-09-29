from layers.layer_base import LayerBase


class Pipeline(LayerBase):
    def __init__(self):
        super().__init__("pipeline")
        self.parse_dates = ['input_date']
