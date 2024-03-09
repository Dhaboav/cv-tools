import os
import random

class ImgSet:
    def __init__(self, label_path:str):
        self.__label_path = label_path
        self.__output_path = 'runs/ImageSets'
        os.makedirs(self.__output_path, exist_ok=True)
        self.__run()

    # Directory Stuff
    def __save_to_file(self, data, file_name):
        __save = os.path.join(self.__output_path)
        with open(os.path.join(__save, file_name), 'w') as file:
            for item in data:
                file.write('%s\n' % item)
    # ==============================================================================

    # Core         
    def __run(self):
        file_names = [os.path.splitext(f)[0] for f in os.listdir(self.__label_path) if os.path.isfile(os.path.join(self.__label_path, f))]
        random.shuffle(file_names)

        num_samples = len(file_names)
        num_train = int(num_samples * 0.8)
        num_val = int(num_samples * 0.1)

        # Split the file names into train, val, and test sets
        train_set = file_names[:num_train]
        val_set = file_names[num_train:num_train + num_val]
        test_set = file_names[num_train + num_val:]

        # Save the sets into separate text files
        self.__save_to_file(train_set, 'train.txt')
        self.__save_to_file(val_set, 'val.txt')
        self.__save_to_file(test_set, 'test.txt')

        # Create trainval.txt by combining items from train.txt and val.txt
        trainval_set = train_set + val_set
        self.__save_to_file(trainval_set, 'trainval.txt')

        # Printout
        self.total = len(file_names)