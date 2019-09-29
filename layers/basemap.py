from layers.layer_base import LayerBase


class River(LayerBase):
    def __init__(self):
        super().__init__("rivers_all_rw92")
        self.is_intersects = True


class Road(LayerBase):
    def __init__(self):
        super().__init__("roads_all")
        self.is_intersects = True


class Lake(LayerBase):
    def __init__(self):
        super().__init__("lakes_all")
        self.is_intersects = True


class Forest(LayerBase):
    def __init__(self):
        super().__init__("forest_cadastre")
        self.is_intersects = True


class NationalPark(LayerBase):
    def __init__(self):
        super().__init__("national_parks")
        self.is_intersects = True
