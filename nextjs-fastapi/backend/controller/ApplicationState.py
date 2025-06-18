class ApplicationState:
    def __init__(self):
        # Dictionary to track previous material states
        self.previous_material_states = {}
        # Dictionary to track previous shelf states
        self.previous_shelf_states = {}

    def get_previous_material_state(self, material_id):
        return self.previous_material_states.get(material_id)

    def set_previous_material_state(self, material_id, mass):
        self.previous_material_states[material_id] = mass

    def get_previous_shelf_state(self, shelf_id):
        return self.previous_shelf_states.get(shelf_id)

    def set_previous_shelf_state(self, shelf_id, humidity, temperature):
        self.previous_shelf_states[shelf_id] = {'humidity': humidity, 'temperature': temperature}


app_state = ApplicationState()
