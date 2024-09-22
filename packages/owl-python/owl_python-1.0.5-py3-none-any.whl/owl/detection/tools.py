from owl.core.utils import create_folder
import os
import cv2
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import itertools
import shutil
import yaml
from uuid import uuid4


class DetectionDataChecker:
    """
    This class is used for checking dataset validity and markup scanning. It supports tools like
    checking annotations or plotting pretty charts to view samples per class in your labels.
    """
    def __init__(self, gallery, annotations, metadata):
        """
        Initializes DataChecker instance.
        Parameters:
        - gallery: path to directory with images
        - annotations: path to folder with annotations
        - metadata: metadata file, required for detection (data.yaml in ultralytics YOLO)
        - classlist: list with classnames in classification task
        """
        self.gallery_path = gallery
        self.annotations_path = annotations
        self.metadata = metadata
        self.images = os.listdir(self.gallery_path)
        self.labels = os.listdir(self.annotations_path)
        
        
    def _parse_detection_meta(self):
        """
        Parse self.metadata yaml file
        """
        with open(self.metadata, "r") as metafile:
            contents = yaml.safe_load(metafile)
        return contents
    
    
    def _parse_detection_annotation(self, filepath):
        """
        Parse annotation file in detection task. Returns list of floats (coordinates) 
        and ints (classes).
        """
        with open(filepath, "r") as f:
            contents = f.read().split()
            contents = list(map(float, contents))
            for i in range(len(contents)):
                if i % 5 == 0:
                    contents[i] = int(contents[i])
        return contents
    
    
    def check(self):
        """
        Checks dataset validity based on self.task. Finally generates report 
        that shows validity of data. 
        """
        _warnings = 0
        length_check = (len(self.images) == len(self.labels))
        report = f"Check Report:\nSample Length Check: {length_check}\n"
        if length_check == False:
            _warnings += 1

        metadata = self._parse_detection_meta()
        for fn in tqdm(self.labels, desc="Check"):
            fn = os.path.join(self.annotations_path, fn)
            label = self._parse_detection_annotation(fn)
            if len(label) == 0:
                report += f"File {fn}: empty file\n"
                _warnings += 1
                continue
            elif len(label) % 5 != 0:
                report += f"File {fn}: annotation items length shoud be divisible by 5\n"
                _warnings += 1
                continue
            else:
                for i in range(len(label)):
                    if i % 5 == 0:
                        cls = label[i]
                        if cls < 0 or cls > metadata["nc"]:
                            report += f"File {fn}: annotation class should be in range nc\n"
                            _warnings += 1
                            continue
                            
        if _warnings > 0:
            report += f"Warnings found: {_warnings}. Please check report logs!"
        else:
            report += f"Everything is OK!"
            
        print(report)
        
    
    def get_class_filenames_dict(self):
        """
        Returns dictionary with class number as key and filenames
        that belongs to class as values.
        """
        metadata = self._parse_detection_meta()
        class_names = metadata["names"]
        
        filenames_per_class = {}
        for i in range(len(class_names)):
            filenames_per_class[i] = []
                
        for _fn in tqdm(self.labels, desc="Scanning"):
            fn = os.path.join(self.annotations_path, _fn)
            label = self._parse_detection_annotation(fn)
            for i in range(len(label)):
                if i % 5 == 0:
                    cls = label[i]
                    # delete .jpg extension from filename
                    filenames_per_class[cls].append(_fn[:-4])
                    
        return filenames_per_class
    

    def class_counts(self, return_counts=False, plot=True, backend="matplotlib"):
        """
        Counts samples per each class and create interactive bar chart 
        with class names and samples per each class. Return
        Parameters:
        - return_counts: should return class_counts dataframe
        - plot: should plot counts
        - backend: plotly or matplotlib 
        """
        metadata = self._parse_detection_meta()
        class_names = metadata["names"]
        samples_per_class = [0 for i in range(len(class_names))]
                
        for fn in tqdm(self.labels, desc="Scanning"):
            fn = os.path.join(self.annotations_path, fn)
            label = self._parse_detection_annotation(fn)
            for i in range(len(label)):
                if i % 5 == 0:
                    cls = label[i]
                    samples_per_class[cls] += 1
            
        df = pd.DataFrame({"names": class_names, "counts": samples_per_class})
        
        if plot:
            if backend == "plotly":
                fig = px.bar(df, y='counts', x='names', text='counts')
                fig.update_traces(textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                fig.show()
            elif backend == "matplotlib":
                plt.bar(df.names.values, df.counts.values)
                plt.title('Amount of samples per each class')
                plt.xlabel('names')
                plt.ylabel('counts')
                plt.show()
                
        if return_counts:
            return df
        

class DetectionDataTrimmer:
    """
    Class for trimming data to avoid class imbalance. WARNING: if use for multilabel
    detection work could be incorrect.
    """
    def __init__(self, data_checker):
        """
        Initializes DataTrimmer.
        Parameters:
        - data_checker: DetectionDataChecker
        """
        self.dc = data_checker
        self.filenames_per_class = data_checker.get_class_filenames_dict()

    
    def trim(self, use_random):
        """
        Finds class (es) with minimum amount of samples and trim others.
        Parameters:
        - use_random: deletes random files
        """
        value_counts = [len(v) for v in self.filenames_per_class.values()]
        min_values = min(value_counts)
        if use_random:
            for k, v in self.filenames_per_class.items():
                self.filenames_per_class[k] = list(set(v))
        images_to_remove = []
        labels_to_remove = []
        for k, values in tqdm(self.filenames_per_class.items(), desc="Collecting info.."):
            diff = len(values) - min_values
            if diff == 0:
                continue
            else:
                filenames_to_remove = self.filenames_per_class[k][:diff]
                images_to_remove.extend(list(map(lambda x: f"{os.path.join(self.dc.gallery_path, x)}.jpg", filenames_to_remove)))
                labels_to_remove.extend(list(map(lambda x: f"{os.path.join(self.dc.annotations_path, x)}.txt", filenames_to_remove)))
        for ifn, lfn in tqdm(zip(images_to_remove, labels_to_remove), desc="Trimming.."):
            if os.path.exists(ifn):
                os.remove(ifn)
            if os.path.exists(lfn):
                os.remove(lfn)


class DetectionDataAugmentor:
    """
    Augments detection dataset.
    """
    def __init__(self, data_checker, transform):
        """
        Initializes DataAugmentor.
        Parameters:
        - data_checker: DetectionDataChecker
        - transform: albumentations transform
        INFO: label_fields in A.Compose BBoxParams label_fields arg should be called `class_labels`
        """
        self.dc = data_checker
        self.filenames_per_class = data_checker.get_class_filenames_dict()
        self.transform = transform
        
        
    def _augment_one(self, img_path, label_path):
        """
        Augments one image. Returns augmented image and YOLO format bboxes.
        """
        img = cv2.imread(img_path)
        label_contents = self.dc._parse_detection_annotation(label_path)
        bboxes = []
        class_labels = []
        for i in range(0, len(label_contents), 5):
            box = [label_contents[i+1], label_contents[i+2], label_contents[i+3], label_contents[i+4]]
            bboxes.append(box)
            class_labels.append(label_contents[i])
        transformed = self.transform(
            image = img,
            bboxes = bboxes,
            class_labels=class_labels
        )
        for i in range(len(transformed["bboxes"])):
            transformed["bboxes"][i] = [transformed["class_labels"][i]] + list(transformed["bboxes"][i])
        return transformed["image"], transformed["bboxes"]
        
                    
    def base_augment(self, amount):
        """
        Augments set. 
        Parameters:
        - amount: amount of transforms to apply.
        """
        for _ in tqdm(range(amount), desc="Augmenting.."):
            filename = np.random.choice(list(set(itertools.chain(*self.filenames_per_class.values()))))
            img_path = f"{os.path.join(self.dc.gallery_path, filename)}.jpg"
            label_path = f"{os.path.join(self.dc.annotations_path, filename)}.txt"
            img, box = self._augment_one(img_path, label_path)
            box_str = ""
            for i in box:
                box_str += " ".join(list(map(str, i)))
                box_str += "\n"
            new_filename = str(uuid4())
            new_img_path = f"{os.path.join(self.dc.gallery_path, new_filename)}.jpg"
            new_label_path = f"{os.path.join(self.dc.annotations_path, new_filename)}.txt"
            cv2.imwrite(new_img_path, img)
            with open(new_label_path, "w") as f:
                f.write(box_str)
    
    
    def erase_imbalance_augment(self):
        """
        Augments set and trying to erase imbalance. WARNING: may work incorrect
        with multilabel detection.
        """
        value_counts = [len(v) for v in self.filenames_per_class.values()]
        max_values = max(value_counts)

        for k, values in self.filenames_per_class.items():
            diff = max_values - len(values)
            if diff == 0:
                continue
            else:
                self.single_class_augment(k, diff)
    
    
    def single_class_augment(self, class_id, amount):
        """
        Augments single class. 
        Parameters:
        - amount: amount of transforms to apply.
        - class_id: index of class
        """
        for _ in tqdm(range(amount), desc=f"Augmenting class #{class_id}.."):
            filename = np.random.choice(list(set(self.filenames_per_class[class_id])))
            img_path = f"{os.path.join(self.dc.gallery_path, filename)}.jpg"
            label_path = f"{os.path.join(self.dc.annotations_path, filename)}.txt"
            img, box = self._augment_one(img_path, label_path)
            box_str = ""
            for i in box:
                box_str += " ".join(list(map(str, i)))
                box_str += "\n"
            new_filename = str(uuid4())
            new_img_path = f"{os.path.join(self.dc.gallery_path, new_filename)}.jpg"
            new_label_path = f"{os.path.join(self.dc.annotations_path, new_filename)}.txt"
            cv2.imwrite(new_img_path, img)
            with open(new_label_path, "w") as f:
                f.write(box_str)


class DetectionDataSplitter:
    """
    This class is used for splitting detection data into smaller sets. This is useful when
    computing high amount of data.
    """
    def __init__(self, data_checker):
        """
        Initializes DataSplitter.
        Parameters:
        - data_checker: DetectionDataChecker
        """
        self.filenames_per_class = data_checker.get_class_filenames_dict()
        self.dc = data_checker
        
        
    def split_on_folders(self, root, num_folders, use_random=True, test_size=0.2):
        """
        Split data from DetectionDataChecker into subsamples.
        Parameters:
        - root: root folder of all subsamples
        - num_folders: amount of subsets
        - use_random: shuffle data before creating sets
        - test: size of validation set
        """
        split_dict = {}
        
        if use_random:
            for k, v in self.filenames_per_class.items():
                self.filenames_per_class[k] = list(set(v))
        
        for i in tqdm(range(1, num_folders+1), desc="Prepare.."):
            train_images = []
            train_labels = []
            val_images = []
            val_labels = []
            
            for k, v in self.filenames_per_class.items():
                num_files = len(v) // num_folders
                filenames = v[(i-1)*num_files:i*num_files]
                filenames_train = filenames[:int(len(filenames)*(1-test_size))]
                filenames_val = filenames[int(len(filenames)*(1-test_size)):]
                
                train_images.extend(list(map(lambda x: f"{os.path.join(self.dc.gallery_path, x)}.jpg", filenames_train)))
                train_labels.extend(list(map(lambda x: f"{os.path.join(self.dc.annotations_path, x)}.txt", filenames_train)))
                
                val_images.extend(list(map(lambda x: f"{os.path.join(self.dc.gallery_path, x)}.jpg", filenames_val)))
                val_labels.extend(list(map(lambda x: f"{os.path.join(self.dc.annotations_path, x)}.txt", filenames_val)))
                
                
            split_dict[str(i)] = {
                "train": {
                    "images": train_images,
                    "labels": train_labels
                },
                "val": {
                    "images": val_images,
                    "labels": val_labels
                }
            }
            
        create_folder(root, remove=True)
            
        for k, v in tqdm(split_dict.items(), desc="Split.."):
            folder_path = os.path.join(root, k)
            create_folder(folder_path)
            for sample in ("train", "val"):
                sample_path = (os.path.join(folder_path, sample))
                create_folder(os.path.join(sample_path))
                sample_im_path = os.path.join(sample_path, "images")
                sample_labels_path = os.path.join(sample_path, "labels")
                create_folder(sample_im_path)
                create_folder(sample_labels_path)
                for file in v[sample]["images"]:
                    shutil.copy(file, sample_im_path)
                for file in v[sample]["labels"]:
                    shutil.copy(file, sample_labels_path)
              


class DetectionDataVisualizer:
    """
    Class for visualizing detection data.
    """
    def __init__(self, data_checker):
        """
        Initializes DataSplitter.
        Parameters:
        - data_checker: DetectionDataChecker
        """
        self.dc = data_checker

        
    def _draw_boxes(self, image_path, label_path):
        """
        Draws boxes on image.
        """
        image = cv2.imread(image_path)
        height, width, _ = image.shape
    
        with open(label_path, 'r') as f:
            yolo_data = f.readlines()
    
        boxes = []
        for line in yolo_data:
            class_id, x, y, w, h = line.strip().split()
            x, y, w, h = float(x), float(y), float(w), float(h)
            x1 = int((x - w/2) * width)
            y1 = int((y - h/2) * height)
            x2 = int((x + w/2) * width)
            y2 = int((y + h/2) * height)
            boxes.append((class_id, x, y, w, h))
    
        for box in boxes:
            class_id, x, y, w, h = box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{self.dc._parse_detection_meta()['names'][int(class_id)]}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image
    
    
    def random_plot(self, n_images):
        """
        Plots N random images with boxes in subplots.
        Parameters:
        - n_images: amout of images to plot
        """
        images = []
        labels = []
        for _ in range(n_images):
            idx = np.random.randint(len(self.dc.images))
            images.append(os.path.join(self.dc.gallery_path, self.dc.images[idx]))
            labels.append(os.path.join(self.dc.annotations_path, self.dc.labels[idx]))
            
        n_cols = int(np.ceil(np.sqrt(n_images)))
        n_rows = int(np.ceil(n_images / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols)
        axes = axes.flatten()
        
        for i, (ax, image, label) in enumerate(zip(axes, images, labels)):
            image = self._draw_boxes(image, label)
            ax.imshow(image)
            ax.axis('off')
        
        for ax in axes[n_images:]:
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        
    def plot_images(self, filenames):
        """
        Shows images with given filenames. List of filenames should contain more
        than one image.
        Parameters:
        - filenames: list with paths to images
        """
        n_images = len(filenames)
        images = []
        labels = []
        for fn in filenames:
            idx = self.dc.images.index(fn)
            images.append(os.path.join(self.dc.gallery_path, self.dc.images[idx]))
            labels.append(os.path.join(self.dc.annotations_path, self.dc.labels[idx]))
            
        n_cols = int(np.ceil(np.sqrt(n_images)))
        n_rows = int(np.ceil(n_images / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols)
        axes = axes.flatten()
        
        for i, (ax, image, label) in enumerate(zip(axes, images, labels)):
            image = self._draw_boxes(image, label)
            ax.imshow(image)
            ax.axis('off')
        
        for ax in axes[n_images:]:
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        
    def plot_image(self, filename):
        """
        Shows image with given filename. 
        Parameters:
        - filename: name of file with image
        """
        idx = self.dc.images.index(filename)
        image = os.path.join(self.dc.gallery_path, self.dc.images[idx])
        label = os.path.join(self.dc.annotations_path, self.dc.labels[idx])
        plt.imshow(self._draw_boxes(image, label))
        plt.show()
