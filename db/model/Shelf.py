import sqlite3

class Shelf:
    # Constructor

    def __init__(self, id, humidity_pct, temperature_cel):
        self.id = id
        self.humidity_pct = humidity_pct
        self.temperature_cel = temperature_cel
    
    # Set Methods
    
    def setHumidityPCT(self, newHumidPCT):
        self.humidity_pct = newHumidPCT

        # Update humidity pct in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE shelf SET humidity_pct = '"+newHumidPCT+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new Humidity PCT for User class successful.")
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting Humidity PCT data from Shelf class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Shelf class closed.")
    
    def setTemperatureCel(self, newTempCel):
        self.temperature_cel = newTempCel

        # Update Temperature Cel in the databsae based on the ID
        try:
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "UPDATE shelf SET temperature_cel = '"+newTempCel+"' WHERE id = '"+self.id+"'"
            cursor.execute(data)
            conn.commit()
            print("Set new temperature cel for Shelf class successful.")
            cursor.close()

        except sqlite3.Error as e:
            print("Error while setting temperature cel data from Shelf class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Shelf class closed.")
    
    # For reference on this part https://youtu.be/fKXhuOvjQQ8?si=-KNLP-ykp-mbCfJ2
    def getAll():
        """
        Returns all the instances of User stored in the user table.
        """
        result = [] # An array to store all the results

        try:
            # Connect to the database (it will create the file if it doesn't exist)
            conn = sqlite3.connect('../capstone_db.db')
            cursor = conn.cursor()

            data = "SELECT * FROM shelf" # Select all from the shelf table
            cursor.execute(data)        # Set the cursor to execute this instruction
            rows = cursor.fetchall()    # Fetch all the rows from the shelf table

            for x in rows:  # For each row, append the element to the result array
                result.append(x)

            # Return the result array after closing the connection
            conn.close()
        
        except sqlite3.Error as e:
            print("Error while getting all data from Shelf class", e)
        
        finally:
            if (conn):
                conn.close()
                print("Connection from Shelf class closed.")

        return result