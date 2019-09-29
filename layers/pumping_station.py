from layers.layer_base import LayerBase


class PumpingStation(LayerBase):
    def __init__(self):
        super().__init__("pumping_station")
        self.parse_dates = ['input_date', 'pump_installation_date', 'meter_installation_date']
