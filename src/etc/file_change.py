import os


class FileChange:
    def __init__(self, name_format:str, folder_path:str):
        self.name_format = name_format
        self.folder_path = folder_path
        self.counter = 1

    def run(self): 
        for __filename in os.listdir(self.folder_path):
            __old_file_path = os.path.join(self.folder_path, __filename)
            if os.path.isfile(__old_file_path):
                _, __file_ext = os.path.splitext(__filename)
                __new_file_name = self.name_format.format(self.counter)
                __new_file_path = os.path.join(self.folder_path, __new_file_name + __file_ext)
                os.rename(__old_file_path, __new_file_path)
                self.counter += 1           