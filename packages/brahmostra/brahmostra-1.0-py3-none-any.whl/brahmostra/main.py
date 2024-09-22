import os
import subprocess
import getpass
import sys
import shutil  # For duplicating files
import time
from groq import Groq
from datetime import datetime
import pyperclip  # For clipboard operations
import threading
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

# Globals for undo functionality
last_deleted_file = None
last_deleted_content = None
output_directory = os.getcwd()  # Default output directory is the current directory

# Function to obfuscate API key input
def obfuscate_input(prompt):
    api_key = getpass.getpass(prompt)  # Hides the input as you type
    obfuscated_key = "GSK" + "X" * (len(api_key) - 3)
    print(f"API Key: {obfuscated_key}")
    return api_key

# Initialize the Groq client
api_key = obfuscate_input("Please input your Groq API key: ")
client = Groq(api_key=api_key)

# Variables to remember user preferences
selected_model = None
selected_code_type = None

# Function to handle model and language selection only if not set
def get_model_and_code_type():
    global selected_model, selected_code_type

    if not selected_model:
        model_input = input("Enter model name (default: llama-3.1-70b-versatile): ").strip()
        selected_model = model_input or "llama-3.1-70b-versatile"
    
    if not selected_code_type:
        code_type_input = input("Enter code type (Python, JavaScript, Bash, etc. Default is Python): ").strip()
        selected_code_type = code_type_input or "Python"

# Function to reset model and code type when input is empty
def reset_model_and_code_type():
    global selected_model, selected_code_type
    selected_model = None
    selected_code_type = None

# Function to check for syntax errors before running the code (supports only Python for now)
def check_syntax(code, language='python'):
    if language.lower() == 'python':
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f"Syntax error detected: {e}")
            return False
    return True  # Assume other languages are syntactically valid

# Function to log errors or actions
def log_action(action):
    log_file = "log.txt"
    with open(log_file, 'a') as file:
        file.write(f"{datetime.now()} - {action}\n")

# Function to export logs to a custom file
def export_logs(export_file="exported_logs.txt"):
    try:
        with open("log.txt", 'r') as log_file:
            log_content = log_file.read()
        
        with open(export_file, 'w') as export_file:
            export_file.write(log_content)
        
        print(f"Logs exported to {export_file.name}")
        log_action(f"Exported logs to {export_file.name}")
    except FileNotFoundError:
        print("No logs found to export.")

# Function to generate and save code based on prompt
def generate_code(prompt, file_name="generated_code.py"):
    try:
        if not prompt.strip():  # If the user prompt is empty, reset everything
            reset_model_and_code_type()
            print("Prompt is empty. Resetting all selections.")
            return

        # Only prompt for model and code type if they aren't already set
        get_model_and_code_type()  # Ensure we have model and code type selected

        print(f"Generating {selected_code_type} code with model {selected_model}...")
        system_prompt = (f"Generate {selected_code_type} code for: {prompt}. Only output the code itself, "
                         f"no explanations, no comments. Ensure the code is syntactically correct and well-formed.")

        start_time = time.time()  # Track start time

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": system_prompt}],
            model=selected_model,
        )
        
        # Get the generated code, ensuring it's only code
        generated_code = response.choices[0].message.content
        generated_code = generated_code.replace(f'```{selected_code_type.lower()}', '').replace('```', '').strip()  # Clean up formatting markers
        
        # Check for syntax errors before saving and running
        if check_syntax(generated_code, language=selected_code_type):
            # Save the generated code to a file with utf-8 encoding
            output_path = os.path.join(output_directory, file_name)
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(generated_code)
            
            exec_time = time.time() - start_time  # Calculate execution time
            print(f"{selected_code_type} code has been saved to {output_path}.")
            print(f"Code generation took {exec_time:.2f} seconds.")
            log_action(f"Generated {selected_code_type} code for prompt: '{prompt}' and saved to {output_path}. Execution time: {exec_time:.2f} seconds")
            
            # Optionally run Python files if valid
            if selected_code_type.lower() == "python":
                confirm_run = input(f"Do you want to run the generated Python file {file_name}? (y/n): ").lower()
                if confirm_run == 'y':
                    print(f"Running {file_name}...")
                    subprocess.run(['python', output_path])
        else:
            print(f"Generated code has syntax errors and will not be run. Please try again with a new prompt.")

    except Exception as e:
        print(f"Error generating code: {str(e)}")
        log_action(f"Error: {str(e)}")
        reset_model_and_code_type()

# Function to list generated code files
def list_generated_files():
    files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
    if files:
        print("\n--- Generated Files ---")
        for idx, f in enumerate(files, 1):
            file_size = os.path.getsize(os.path.join(output_directory, f)) / 1024  # File size in KB
            print(f"{idx}. {f} - {file_size:.2f} KB")
        print("-----------------------\n")
    else:
        print("No generated files found.")

# Function to delete a generated file (with undo support)
def delete_file():
    global last_deleted_file, last_deleted_content
    list_generated_files()
    try:
        file_num = int(input("Enter the number of the file you want to delete (or 0 to cancel): "))
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if file_num > 0 and file_num <= len(files):
            last_deleted_file = files[file_num - 1]
            with open(os.path.join(output_directory, last_deleted_file), 'r', encoding='utf-8') as file:
                last_deleted_content = file.read()
            os.remove(os.path.join(output_directory, last_deleted_file))
            print(f"Deleted {last_deleted_file}")
            log_action(f"Deleted file: {last_deleted_file}")
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to undo the last file deletion
def undo_last_deletion():
    global last_deleted_file, last_deleted_content
    if last_deleted_file and last_deleted_content:
        with open(os.path.join(output_directory, last_deleted_file), 'w', encoding='utf-8') as file:
            file.write(last_deleted_content)
        print(f"Restored {last_deleted_file}")
        log_action(f"Restored file: {last_deleted_file}")
        last_deleted_file, last_deleted_content = None, None
    else:
        print("No file to restore.")

# Function to search for a keyword in generated files
def search_in_files(keyword):
    files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
    if not files:
        print("No generated files found.")
        return
    
    results = []
    for file in files:
        with open(os.path.join(output_directory, file), 'r', encoding='utf-8') as f:
            content = f.read()
            if keyword in content:
                results.append(file)
    
    if results:
        print(f"\nKeyword '{keyword}' found in:")
        for r in results:
            print(f" - {r}")
    else:
        print(f"Keyword '{keyword}' not found in any files.")

# Function to generate a brief summary of the generated code
def summarize_code(file_name):
    file_path = os.path.join(output_directory, file_name)
    if not os.path.exists(file_path):
        print(f"{file_name} does not exist.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        
        summary_prompt = f"Summarize the following {selected_code_type} code:\n{code}"
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": summary_prompt}],
            model=selected_model,
        )
        
        summary = response.choices[0].message.content
        print("\n--- Code Summary ---")
        print(summary)
        print("--------------------\n")
        log_action(f"Generated summary for {file_name}")
    except Exception as e:
        print(f"Error generating summary: {str(e)}")

# Function to duplicate a generated file
def duplicate_file():
    list_generated_files()
    try:
        file_num = int(input("Enter the number of the file you want to duplicate (or 0 to cancel): "))
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if file_num > 0 and file_num <= len(files):
            original_file = files[file_num - 1]
            duplicate_file = f"copy_of_{original_file}"
            shutil.copy(os.path.join(output_directory, original_file), os.path.join(output_directory, duplicate_file))
            print(f"Duplicated {original_file} as {duplicate_file}")
            log_action(f"Duplicated {original_file} as {duplicate_file}")
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to rename a generated file
def rename_file():
    list_generated_files()
    try:
        file_num = int(input("Enter the number of the file you want to rename (or 0 to cancel): "))
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if file_num > 0 and file_num <= len(files):
            original_file = files[file_num - 1]
            new_name = input("Enter the new name for the file (without extension): ") + os.path.splitext(original_file)[1]
            os.rename(os.path.join(output_directory, original_file), os.path.join(output_directory, new_name))
            print(f"Renamed {original_file} to {new_name}")
            log_action(f"Renamed {original_file} to {new_name}")
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to copy the content of a generated file to the clipboard
import pyperclip  # For clipboard operations

def copy_to_clipboard():
    list_generated_files()
    try:
        file_num = int(input("Enter the number of the file to copy to clipboard (or 0 to cancel): "))
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if file_num > 0 and file_num <= len(files):
            with open(os.path.join(output_directory, files[file_num - 1]), 'r', encoding='utf-8') as file:
                file_content = file.read()
                pyperclip.copy(file_content)
                print(f"Copied content of {files[file_num - 1]} to clipboard.")
                log_action(f"Copied {files[file_num - 1]} to clipboard")
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to archive old generated files into a ZIP file
import zipfile

def archive_files():
    files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
    if not files:
        print("No files to archive.")
        return
    
    archive_name = input("Enter the name for the archive (without .zip): ") + ".zip"
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for file in files:
            zipf.write(os.path.join(output_directory, file), arcname=file)
    
    print(f"Archived {len(files)} files into {archive_name}.")
    log_action(f"Archived {len(files)} files into {archive_name}")

# Function to schedule a file deletion after a certain period
import threading

def schedule_deletion():
    list_generated_files()
    try:
        file_num = int(input("Enter the number of the file to delete (or 0 to cancel): "))
        delay = int(input("Enter the delay in seconds before deletion: "))
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if file_num > 0 and file_num <= len(files):
            file_to_delete = files[file_num - 1]
            print(f"Scheduled {file_to_delete} for deletion in {delay} seconds.")
            log_action(f"Scheduled {file_to_delete} for deletion in {delay} seconds")
            
            # Schedule deletion
            def delete_later():
                time.sleep(delay)
                if os.path.exists(os.path.join(output_directory, file_to_delete)):
                    os.remove(os.path.join(output_directory, file_to_delete))
                    print(f"{file_to_delete} has been deleted.")
                    log_action(f"Deleted {file_to_delete} after {delay} seconds")
            
            threading.Thread(target=delete_later).start()
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

# Function to delete multiple files
def batch_delete_files():
    list_generated_files()
    try:
        file_indices = input("Enter the numbers of the files to delete (comma-separated, or 0 to cancel): ")
        file_indices = [int(num.strip()) for num in file_indices.split(',')]
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        
        if 0 in file_indices:
            print("No files deleted.")
            return
        
        for file_num in file_indices:
            if 0 < file_num <= len(files):
                file_to_delete = files[file_num - 1]
                os.remove(os.path.join(output_directory, file_to_delete))
                print(f"Deleted {file_to_delete}")
                log_action(f"Deleted file: {file_to_delete}")
            else:
                print(f"Invalid file number: {file_num}")
    except ValueError:
        print("Please enter valid numbers.")

# Function to back up files to a remote server using SCP
import paramiko

def backup_to_remote():
    remote_host = input("Enter the remote server address: ")
    username = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")
    
    try:
        files = [f for f in os.listdir(output_directory) if f.endswith('.py') or f.endswith('.txt')]
        if not files:
            print("No files to backup.")
            return

        # Connect to remote server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_host, username=username, password=password)
        
        # Upload files
        sftp = ssh.open_sftp()
        remote_dir = input("Enter the remote directory path: ")
        for file in files:
            sftp.put(os.path.join(output_directory, file), os.path.join(remote_dir, file))
            print(f"Backed up {file} to {remote_host}:{remote_dir}")
            log_action(f"Backed up {file} to {remote_host}:{remote_dir}")
        
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Error during backup: {str(e)}")
        log_action(f"Error during backup: {str(e)}")

# Main loop to select functions
def main():
    while True:
        print("\nSelect an option:")
        print("1. Generate Code")
        print("2. List Generated Files")
        print("3. Delete a File")
        print("4. Undo Last Deletion")
        print("5. Search in Files")
        print("6. Summarize Code")
        print("7. Duplicate File")
        print("8. Rename File")
        print("9. Export Logs")
        print("10. Copy to Clipboard")
        print("11. Archive Files")
        print("12. Schedule File Deletion")
        print("13. Batch Delete Files")
        print("14. Backup Files to Remote Server")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                prompt = input("Enter a code prompt: ")
                file_name = input("Enter file name to save (default: generated_code.py): ") or "generated_code.py"
                generate_code(prompt, file_name)
            elif choice == 2:
                list_generated_files()
            elif choice == 3:
                delete_file()
            elif choice == 4:
                undo_last_deletion()
            elif choice == 5:
                keyword = input("Enter a keyword to search for: ")
                search_in_files(keyword)
            elif choice == 6:
                file_name = input("Enter the file name to summarize: ")
                summarize_code(file_name)
            elif choice == 7:
                duplicate_file()
            elif choice == 8:
                rename_file()
            elif choice == 9:
                export_file = input("Enter the name of the export log file (default: exported_logs.txt): ") or "exported_logs.txt"
                export_logs(export_file)
            elif choice == 10:
                copy_to_clipboard()
            elif choice == 11:
                archive_files()
            elif choice == 12:
                schedule_deletion()
            elif choice == 13:
                batch_delete_files()
            elif choice == 14:
                backup_to_remote()
            elif choice == 0:
                print("Exiting program...")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Run the program
if __name__ == "__main__":
    main()
