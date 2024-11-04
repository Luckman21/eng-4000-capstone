class User_Type:
    # Constructor

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Set Methods

    def setName(self, newName):
        self.name = newName
        # Call DB

# TODO: update DB info, getAll Method