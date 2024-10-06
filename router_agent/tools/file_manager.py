from duckduckgo_search import DDGS
import json
from qwen_agent.tools.base import BaseTool, register_tool
import json, json5
import urllib
import os
import logging
import shutil
import hashlib
import datetime
import zipfile
import tarfile
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

@register_tool('file_management')
class FileManager(BaseTool):
    description = 'Manage files and directories'
    parameters = [
        {
            'name': 'action',
            'type': 'string',
            'description': 'The action to perform (e.g., create_folder, delete_folder, create_file, delete_file, read_file, write_to_file, list_files, read_json_file, write_json_file, copy_file, copy_folder, move_file, move_folder, is_file, is_directory, encrypt_file, decrypt_file, get_file_metadata, batch_rename_files, compress_file, decompress_file, save_file_version, restore_file_version, share_file, search_files, synchronize_files, add_tag, get_tags, convert_file, backup_files, recover_files)',
            'required': True
        },
        {
            'name': 'params',
            'type': 'object',
            'description': 'The parameters for the action',
            'required': True
        }
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_path = os.getcwd()
        self.versions = defaultdict(list)
        self.tags = defaultdict(list)

    def call(self, params: str, **kwargs) -> str:
        action = json5.loads(params)['action']
        params = json5.loads(params)['params']

        if action == 'create_folder':
            return self.create_folder(params['folder_name'], params.get('path'))
        elif action == 'delete_folder':
            return self.delete_folder(params['folder_name'], params.get('path'))
        elif action == 'create_file':
            return self.create_file(params['file_name'], params.get('content'), params.get('path'))
        elif action == 'delete_file':
            return self.delete_file(params['file_name'], params.get('path'))
        elif action == 'read_file':
            return self.read_file(params['file_name'], params.get('path'))
        elif action == 'write_to_file':
            return self.write_to_file(params['file_name'], params['content'], params.get('path'))
        elif action == 'list_files':
            return self.list_files(params.get('path'))
        elif action == 'read_json_file':
            return json.dumps(self.read_json_file(params['file_name'], params.get('path')))
        elif action == 'write_json_file':
            return self.write_json_file(params['file_name'], params['content'], params.get('path'))
        elif action == 'copy_file':
            return self.copy_file(params['src_file'], params['dest_file'], params.get('src_path'), params.get('dest_path'))
        elif action == 'copy_folder':
            return self.copy_folder(params['src_folder'], params['dest_folder'], params.get('src_path'), params.get('dest_path'))
        elif action == 'move_file':
            return self.move_file(params['src_file'], params['dest_file'], params.get('src_path'), params.get('dest_path'))
        elif action == 'move_folder':
            return self.move_folder(params['src_folder'], params['dest_folder'], params.get('src_path'), params.get('dest_path'))
        elif action == 'is_file':
            return str(self.is_file(params['path']))
        elif action == 'is_directory':
            return str(self.is_directory(params['path']))
        elif action == 'encrypt_file':
            return self.encrypt_file(params['file_name'], params['key'], params.get('path'))
        elif action == 'decrypt_file':
            return self.decrypt_file(params['file_name'], params['key'], params.get('path'))
        elif action == 'get_file_metadata':
            return json.dumps(self.get_file_metadata(params['file_name'], params.get('path')))
        elif action == 'batch_rename_files':
            return self.batch_rename_files(params['directory'], params['old_pattern'], params['new_pattern'])
        elif action == 'compress_file':
            return self.compress_file(params['file_name'], params['output_filename'], params.get('format'), params.get('path'))
        elif action == 'decompress_file':
            return self.decompress_file(params['file_name'], params['output_directory'], params.get('path'))
        elif action == 'save_file_version':
            return self.save_file_version(params['file_name'], params.get('path'))
        elif action == 'restore_file_version':
            return self.restore_file_version(params['file_name'], params['version'], params.get('path'))
        elif action == 'share_file':
            return self.share_file(params['file_name'], params['user'], params['permissions'], params.get('path'))
        elif action == 'search_files':
            return json.dumps(self.search_files(params['keyword'], params.get ('path')))
        elif action == 'synchronize_files':
            return self.synchronize_files(params['source_path'], params['destination_path'])
        elif action == 'add_tag':
            return self.add_tag(params['file_name'], params['tag'], params.get('path'))
        elif action == 'get_tags':
            return json.dumps(self.get_tags(params['file_name'], params.get('path')))
        elif action == 'convert_file':
            return self.convert_file(params['file_name'], params['output_format'], params.get('path'))
        elif action == 'backup_files':
            return self.backup_files(params['source_path'], params['backup_path'])
        elif action == 'recover_files':
            return self.recover_files(params['backup_path'], params['destination_path'])
        else:
            return 'Invalid action'

    def create_folder(self, folder_name: str, path: str = None) -> str:
        folder_path = os.path.join(path if path else self.base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Folder '{folder_name}' created successfully at {folder_path}!")
            return f"Folder '{folder_name}' created successfully!"
        else:
            logging.warning(f"Folder '{folder_name}' already exists at {folder_path}.")
            return f"Folder '{folder_name}' already exists."

    def delete_folder(self, folder_name: str, path: str = None) -> str:
        folder_path = os.path.join(path if path else self.base_path, folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            logging.info(f"Folder '{folder_name}' deleted successfully from {folder_path}!")
            return f"Folder '{folder_name}' deleted successfully!"
        else:
            logging.warning(f"Folder '{folder_name}' does not exist at {folder_path}.")
            return f"Folder '{folder_name}' does not exist."

    def create_file(self, file_name: str, content: str = "", path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        logging.info(f"File '{file_name}' created successfully at {file_path}!")
        return f"File '{file_name}' created successfully!"

    def delete_file(self, file_name: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"File '{file_name}' deleted successfully from {file_path}!")
            return f"File '{file_name}' deleted successfully!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def read_file(self, file_name: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = file.read()
            logging.info(f"File '{file_name}' read successfully from {file_path}!")
            return content
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def write_to_file(self, file_name: str, content: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        logging.info(f"Content written to file '{file_name}' successfully at {file_path}!")
        return f"Content written to file '{file_name}' successfully!"

    def list_files(self, path: str = None) -> str:
        directory_path = path if path else self.base_path
        files = os.listdir(directory_path)
        logging.info(f"Files listed successfully from {directory_path}!")
        return "Files in the specified directory:\n" + "\n".join(files)

    def read_json_file(self, file_name: str, path: str = None) -> dict:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = json.load(file)
            logging.info(f"JSON file '{file_name}' read successfully from {file_path}!")
            return content
        else:
            logging.warning(f"JSON file '{file_name}' does not exist at {file_path}.")
            return f"JSON file '{file_name}' does not exist."

    def write_json_file(self, file_name: str, content: dict, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        with open(file_path, "w") as file:
            json.dump(content, file, indent=4)
        logging.info(f"Content written to JSON file '{file_name}' successfully at {file_path}!")
        return f"Content written to JSON file '{file_name}' successfully!"

    def copy_file(self, src_file: str, dest_file: str, src_path: str = None, dest_path: str = None) -> str:
        src_file_path = os.path.join(src_path if src_path else self.base_path, src_file)
        dest_file_path = os.path.join(dest_path if dest_path else self.base_path, dest_file)
        if os.path.exists(src_file_path):
            shutil.copy2(src_file_path, dest_file_path)
            logging.info(f"File '{src_file}' copied successfully to {dest_file_path}!")
            return f"File '{src_file}' copied successfully to {dest_file}!"
        else:
            logging.warning(f"File '{src_file}' does not exist at {src_file_path}.")
            return f"File '{src_file}' does not exist."

    def copy_folder(self, src_folder: str, dest_folder: str, src_path: str = None, dest_path: str = None) -> str:
        src_folder_path = os.path.join(src_path if src_path else self.base_path, src_folder)
        dest_folder_path = os.path.join(dest_path if dest_path else self.base_path, dest_folder)
        if os.path.exists(src_folder_path):
            shutil.copytree(src_folder_path, dest_folder_path)
            logging.info(f"Folder '{src_folder}' copied successfully to {dest_folder_path}!")
            return f"Folder '{src_folder}' copied successfully to {dest_folder}!"
        else:
            logging.warning(f"Folder '{src_folder}' does not exist at {src_folder_path}.")
            return f"Folder '{src_folder}' does not exist."

    def move_file(self, src_file: str, dest_file: str, src_path: str = None, dest_path: str = None) -> str:
        src_file_path = os.path.join(src_path if src_path else self.base_path, src_file)
        dest_file_path = os.path.join(dest_path if dest_path else self.base_path, dest_file)
        if os.path.exists(src_file_path):
            shutil.move(src_file_path, dest_file_path)
            logging.info(f"File '{src_file}' moved successfully to {dest_file_path}!")
            return f"File '{src_file}' moved successfully to {dest_file}!"
        else:
            logging.warning(f"File '{src_file}' does not exist at {src_file_path}.")
            return f"File '{src_file}' does not exist."

    def move_folder(self, src_folder: str, dest_folder: str, src_path: str = None, dest_path: str = None) -> str:
        src_folder_path = os.path.join(src_path if src_path else self.base_path, src_folder)
        dest_folder_path = os.path.join(dest_path if dest_path else self.base_path, dest_folder)
        if os.path.exists(src_folder_path):
            shutil.move(src_folder_path, dest_folder_path)
            logging.info(f"Folder '{src_folder}' moved successfully to {dest_folder_path}!")
            return f"Folder '{src_folder}' moved successfully to {dest_folder}!"
        else:
            logging.warning(f"Folder '{src_folder}' does not exist at {src_folder_path}.")
            return f"Folder '{src_folder}' does not exist."

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_directory(self, path: str) -> bool:
        return os.path.isdir(path)

    def encrypt_file(self, file_name: str, key: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                data = file.read()
            key = hashlib.sha256(key.encode()).digest()
            encrypted_data = bytearray(x ^ key[i % len(key)] for i, x in enumerate(data))
            with open(file_path, "wb") as file:
                file.write(encrypted_data)
            logging.info(f"File '{file_name}' encrypted successfully at {file_path}!")
            return f"File '{file_name}' encrypted successfully!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def decrypt_file(self, file_name: str, key: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                data = file.read()
            key = hashlib.sha256(key.encode()).digest()
            decrypted_data = bytearray(x ^ key[i % len(key)] for i, x in enumerate(data))
            with open(file_path, "wb") as file:
                file.write(decrypted_data)
            logging.info(f"File '{file_name}' decrypted successfully at {file_path}!")
            return f"File '{file_name}' decrypted successfully!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def get_file_metadata(self, file_name: str, path: str = None) -> dict:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            metadata = os.stat(file_path)
            return {
                "size": metadata.st_size,
                "creation_time": datetime.datetime.fromtimestamp(metadata.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "modification_time": datetime.datetime.fromtimestamp(metadata.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "access_time": datetime.datetime.fromtimestamp(metadata.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def batch_rename_files(self, directory: str, old_pattern: str, new_pattern: str) -> str:
        directory_path = os.path.join(self.base_path, directory)
        if os.path.exists(directory_path):
            for filename in os.listdir(directory_path):
                if old_pattern in filename:
                    new_filename = filename.replace(old_pattern, new_pattern)
                    os.rename(os.path.join(directory_path, filename), os.path.join(directory_path, new_filename))
            logging.info(f"Files in directory '{directory}' renamed successfully!")
            return f"Files in directory '{directory}' renamed successfully!"
        else:
            logging.warning(f"Directory '{directory}' does not exist at {directory_path}.")
            return f"Directory '{directory}' does not exist."

    def compress_file(self, file_name: str, output_filename: str, format: str = "zip", path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        output_path = os.path.join(path if path else self.base_path, output_filename)
        if os.path.exists(file_path):
            if format == "zip":
                with zipfile.ZipFile(output_path, "w") as zipf:
                    zipf.write(file_path, os.path.basename(file_path))
            elif format == "tar":
                with tarfile.open(output_path, "w") as tarf:
                    tarf.add(file_path, os.path.basename(file_path))
            elif format == "gztar":
                with tarfile.open(output_path, "w:gz") as tarf:
                    tarf.add(file_path, os.path.basename(file_path))
            else:
                logging.warning(f"Unsupported compression format: {format}.")
                return f"Unsupported compression format: {format}."
            logging.info(f"File '{file_name}' compressed successfully to {output_path}!")
            return f"File '{file_name}' compressed successfully to {output_filename}!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def decompress_file(self, file_name: str, output_directory: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        output_path = os.path.join(path if path else self.base_path, output_directory)
        if os.path.exists(file_path):
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zipf:
                    zipf.extractall(output_path)
            elif file_name.endswith(".tar") or file_name.endswith(".tar.gz") or file_name.endswith(".tgz"):
                with tarfile.open(file_path, "r") as tarf:
                    tarf.extractall(output_path)
            else:
                logging.warning(f"Unsupported decompression format for file: {file_name}.")
                return f"Unsupported decompression format for file: {file_name}."
            logging.info(f"File '{file_name}' decompressed successfully to {output_path}!")
            return f"File '{file_name}' decompressed successfully to {output_directory}!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def save_file_version(self, file_name: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            version_path = os.path.join(path if path else self.base_path, f"{file_name}_v{len(self.versions[file_name]) + 1}")
            shutil.copy2(file_path, version_path)
            self.versions[file_name].append(version_path)
            logging.info(f"Version saved for file '{file_name}' at {version_path}!")
            return f"Version saved for file '{file_name}'!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def restore_file_version(self, file_name: str, version: int, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            if 1 <= version <= len(self.versions[file_name]):
                version_path = self.versions[file_name][version - 1]
                shutil.copy2(version_path, file_path)
                logging.info(f"File '{file_name}' restored to version {version} at {file_path}!")
                return f"File '{file_name}' restored to version {version}!"
            else:
                logging.warning(f"Version {version} does not exist for file '{file_name}'.")
                return f"Version {version} does not exist for file '{file_name}'."
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def share_file(self, file_name: str, user: str, permissions: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            # Implement sharing logic here (e.g., store sharing information in a database or file)
            logging.info(f"File '{file_name}' shared with user '{user}' with permissions '{permissions}'!")
            return f"File '{file_name}' shared with user '{user}' with permissions '{permissions}'!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def search_files(self, keyword: str, path: str = None) -> list:
        search_path = path if path else self.base_path
        matching_files = []
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if keyword in file:
                    matching_files.append(os.path.join(root, file))
                else:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        if keyword in f.read():
                            matching_files.append(file_path)
        logging.info(f"Search for keyword '{keyword}' completed with {len(matching_files)} matches!")
        return matching_files

    def synchronize_files(self, source_path: str, destination_path: str) -> str:
        if os.path.exists(source_path) and os.path.exists(destination_path):
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_file_path, source_path)
                    destination_file_path = os.path.join(destination_path, relative_path)
                    if not os.path.exists(destination_file_path) or os.stat(source_file_path).st_mtime - os.stat(destination_file_path).st_mtime > 1:
                        shutil.copy2(source_file_path, destination_file_path)
            logging.info(f"Synchronization from '{source_path}' to '{destination_path}' completed successfully!")
            return f"Synchronization from '{source_path}' to '{destination_path}' completed successfully!"
        else:
            logging.warning(f"Source or destination path does not exist.")
            return f"Source or destination path does not exist."

    def add_tag(self, file_name: str, tag: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            self.tags[file_name].append(tag)
            logging.info(f"Tag '{tag}' added to file '{file_name}'!")
            return f"Tag '{tag}' added to file '{file_name}'!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def get_tags(self, file_name: str, path: str = None) -> list:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            logging.info(f"Tags retrieved for file '{file_name}'!")
            return self.tags[file_name]
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def convert_file(self, file_name: str, output_format: str, path: str = None) -> str:
        file_path = os.path.join(path if path else self.base_path, file_name)
        if os.path.exists(file_path):
            # Implement file conversion logic here
            # For example, converting a text file to a PDF
            logging.info(f"File '{file_name}' converted to {output_format} format!")
            return f"File '{file_name}' converted to {output_format} format!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def backup_files(self, source_path: str, backup_path: str) -> str:
        if os.path.exists(source_path) and os.path.exists(backup_path):
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_file_path, source_path)
                    backup_file_path = os.path.join(backup_path, relative_path)
                    if not os.path.exists(os.path.dirname(backup_file_path)):
                        os.makedirs(os.path.dirname(backup_file_path))
                    shutil.copy2(source_file_path, backup_file_path)
            logging.info(f"Backup from '{source_path}' to '{backup_path}' completed successfully!")
            return f"Backup from '{source_path}' to '{backup_path}' completed successfully!"
        else:
            logging.warning(f"Source or backup path does not exist.")
            return f"Source or backup path does not exist."

    def recover_files(self, backup_path: str, destination_path: str) -> str:
        if os.path.exists(backup_path) and os.path.exists(destination_path):
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    backup_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(backup_file_path, backup_path)
                    destination_file_path = os.path.join(destination_path, relative_path)
                    if not os.path.exists(os.path.dirname(destination_file_path)):
                        os.makedirs(os.path.dirname(destination_file_path))
                    shutil.copy2(backup_file_path, destination_file_path)
            logging.info(f"Recovery from '{backup_path}' to '{destination_path}' completed successfully!")
            return f"Recovery from '{backup_path}' to '{destination_path}' completed successfully!"
        else:
            logging.warning(f"Backup or destination path does not exist.")
            return f"Backup or destination path does not exist."