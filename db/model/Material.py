class Material:
    # Constructor

    def __init__(self, id, colour, name, material_type_id):
        self.id = id
        self.colour = colour
        self.name = name
        self.material_type_id = material_type_id

    # Set Methods

    def setID(self, newID):
        self.id = newID
        # Call DB

    def setColour(self, newColour):
        self.colour = newColour
        # Call DB

    def setName(self, newName):
        self.name = newName
        # Call DB

    def setMaterialTypeID(self, newMTID):
        self.material_type_id = newMTID
        # Call DB

# TODO: update DB info, getAll Method