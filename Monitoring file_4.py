import time
import os
import difflib
import mysql.connector
from file_locking import is_file_open, create_backup, read_file
from backup_path import create_backup_paths_table_if_not_exists, store_backup_path_in_db, retrieve_backup_path_from_db
def create_table_if_not_exists(cursor):
    try:
        # Define your desired table schema here
        create_table_query = """
        CREATE TABLE IF NOT EXISTS differences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            operation VARCHAR(10),
            affected_lines LONGTEXT
        )
        """
        cursor.execute(create_table_query)

    except Exception as e:
        print(f"Error creating table: {e}")


def merge_replace_content(opcodes, copy_content):
    replace_content = []
    for opcode, start, end, _, _ in opcodes:
        if opcode == 'replace':
            replace_content.append(copy_content[start:end])
    return ''.join(replace_content)

def compare_and_store_changes(original_content, copy_content, cursor,conn):
    matcher = difflib.SequenceMatcher(None, original_content, copy_content)
    opcodes = matcher.get_opcodes()

    print(opcodes)

    try:
        for opcode, a_start, a_end, b_start, b_end in opcodes:
            original_diff = original_content[a_start:a_end]
            copy_diff = copy_content[b_start:b_end]

            if opcode == 'replace':
                operation = "Update"
                affected_lines = merge_replace_content(opcodes, copy_content)
            elif opcode == 'insert':
                operation = "Insert"
                affected_lines = copy_diff
            elif opcode == 'delete':
                operation = "Delete"
                affected_lines = original_diff
            else:
                continue  # Unchanged lines, skip

            check_exist_query = "SELECT * FROM differences WHERE operation=%s AND affected_lines=%s"
            cursor.execute(check_exist_query, (operation, affected_lines))
            result = cursor.fetchall()

            if not result :
                sql = "INSERT INTO differences (operation, affected_lines) VALUES (%s, %s)"
                print(f'INSERT INTO differences (operation, affected_lines) VALUES ({operation}, {affected_lines})')
                cursor.execute(sql, (operation, affected_lines))

        conn.commit()
        print("Differences stored in the database")

    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        conn.rollback()
    except Exception as e:
        print(f"General Error: {e}")
        conn.rollback()


def process_directory(directory_path, backup_directory,cursor,conn):
    for filename in os.listdir(directory_path):
        original_file_path = os.path.join(directory_path, filename)

        # Skip directories
        if os.path.isdir(original_file_path):
            continue

        # Process each file
        if is_file_open(original_file_path) is True:
            # Original file is open, create a backup
            backup_file_path = create_backup(original_file_path,backup_directory)
            store_backup_path_in_db(cursor, original_file_path, backup_file_path)
            conn.commit()
            print("Backup stored in database")
        else:
            print("File is closed. Can't proceed.")

        # Retrieve the backup file path for comparison

        # Proceed with comparison only if the original file is now closed

        if is_file_open(original_file_path) is False:

            stored_backup_path = retrieve_backup_path_from_db(cursor, original_file_path)

            if stored_backup_path:
                original_content = read_file(original_file_path)
                backup_content = read_file(stored_backup_path)

                create_table_if_not_exists(cursor)

                if original_content is not None and backup_content is not None:
                    compare_and_store_changes(backup_content, original_content, cursor,conn)


            else:
                print(f"No backup path found for the file: {original_file_path}")

        else:
            print("File is currently open. Can't proceed with comparison.")


if __name__ == "__main__":
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="Your_user",
            password="Your_password",
            database="Your_database"
        )
        cursor = conn.cursor()


        # Ensure the backup_paths table exists
        create_backup_paths_table_if_not_exists(cursor)
        conn.commit()
        directory_to_process = r'C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\New folder'
        backup_directory = r'C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\backup_directory'
        while True:
           process_directory(directory_to_process, backup_directory,cursor,conn)
           time.sleep(30)
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()