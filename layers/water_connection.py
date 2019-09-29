from layers.layer_base import LayerBase


class WaterConnection(LayerBase):
    def __init__(self):
        super().__init__("water_connection")
        self.parse_dates = ['input_date', 'meter_installation_date', 'connection_date', 'disconnection_date']
