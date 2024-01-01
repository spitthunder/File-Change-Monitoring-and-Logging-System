import mysql.connector
def create_backup_paths_table_if_not_exists(cursor):
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS backup_paths (
            id INT AUTO_INCREMENT PRIMARY KEY,
            original_file VARCHAR(255) NOT NULL,
            backup_file VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)

    except Exception as e:
        print(f"Error creating backup_paths table: {e}")

def store_backup_path_in_db(cursor, original_file_path, backup_file_path):
    try:
        sql_insert = "INSERT INTO backup_paths (original_file, backup_file) VALUES (%s, %s)"
        cursor.execute(sql_insert, (original_file_path, backup_file_path))
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1062:  # Duplicate entry
            sql_update = "UPDATE backup_paths SET backup_file = %s WHERE original_file = %s"
            cursor.execute(sql_update, (backup_file_path, original_file_path))

        else:
            print(f"Error storing backup path in database: {e}")
    except Exception as e:
        print(f"Error storing backup path in database: {e}")

def retrieve_backup_path_from_db(cursor, original_file_path):
    try:
        sql = "SELECT backup_file FROM backup_paths WHERE original_file = %s"
        cursor.execute(sql, (original_file_path,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving backup path from database: {e}")
        return None