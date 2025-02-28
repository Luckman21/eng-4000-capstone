import os

def delete_db():
    db_path = '../../capstone_db.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Database deleted successfully.")
    else:
        print("Database file does not exist.")

delete_db()
