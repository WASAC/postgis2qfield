from layers.layer_base import LayerBase


class District(LayerBase):
    def __init__(self):
        super().__init__("district")


class Sector(LayerBase):
    def __init__(self):
        super().__init__("sector")


class Cell(LayerBase):
    def __init__(self):
        super().__init__("cell")


class Village(LayerBase):
    def __init__(self):
        super().__init__("village")
