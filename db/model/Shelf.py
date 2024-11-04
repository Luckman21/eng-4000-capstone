class Shelf:
    # Constructor

    def __init__(self, id, humidity_pct, temperature_cel):
        self.id = id
        self.humidity_pct = humidity_pct
        self.temperature_cel = temperature_cel
    
    # Set Methods
    
    def setHumidityPCT(self, newHumidPCT):
        self.humidity_pct = newHumidPCT
        # Call DB
    
    def setTemperatureCel(self, newTempCel):
        self.temperature_cel = newTempCel
        # Call DB
    
# TODO: update DB info, getAll Method