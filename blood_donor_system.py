import sqlite3

class BloodDonorSystem:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def ConnectDB(self):
        self.conn = sqlite3.connect('donors.db')
        self.cursor = self.conn.cursor()
    
    def CreateTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            blood_group TEXT,
            contact_info TEXT
        )''')
        self.conn.commit()
    
    def AddDonor(self, name, blood_group, contact_info):
        try:
            self.cursor.execute("INSERT INTO donors (name, blood_group, contact_info) VALUES (?, ?, ?)",
                                (name, blood_group, contact_info))
            self.conn.commit()
            return "Donor added successfully!"
        except Exception as e:
            return str(e)
    
    def UpdateDonor(self, id, name, blood_group, contact_info):
        try:
            self.cursor.execute("UPDATE donors SET name=?, blood_group=?, contact_info=? WHERE id=?", 
                                (name, blood_group, contact_info, id))
            self.conn.commit()
            return "Donor updated successfully!"
        except Exception as e:
            return str(e)
    
    def DeleteDonor(self, id):
        try:
            self.cursor.execute("DELETE FROM donors WHERE id=?", (id,))
            self.conn.commit()
            return "Donor deleted successfully!"
        except Exception as e:
            return str(e)
    
    def SearchDonor(self, search):
        blood_compatibility = {
            'A+': ['A+','AB+', 'O+'],
            'A-': ['A-', 'AB-','O-'],
            'B+': ['B+', 'AB+', 'O+'],
            'B-': ['B-', 'AB-','O-'],
            'AB+': ['A+', 'B+',  'AB+', 'O+',],
            'AB-': ['AB-', 'A-', 'B-', 'O-'],
            'O+': ['O+'],
            'O-': ['O-']
        }

        try:
            # Check if the search term is a known blood group
            if search in blood_compatibility:
                compatible_blood_groups = blood_compatibility[search]
                # Search for donors with compatible blood groups
                query = "SELECT * FROM donors WHERE blood_group IN ({seq})".format(
                    seq=','.join(['?']*len(compatible_blood_groups)))
                self.cursor.execute(query, compatible_blood_groups)
            else:
                # If search term is not a blood group, search in name and contact info fields
                self.cursor.execute("SELECT * FROM donors WHERE name LIKE ? OR contact_info LIKE ?",
                                    ('%' + search + '%', '%' + search + '%'))

            donors = self.cursor.fetchall()
            if donors:
                return donors
            else:
                return "There is no donor matching the search criteria."
        except Exception as e:
            return str(e)
