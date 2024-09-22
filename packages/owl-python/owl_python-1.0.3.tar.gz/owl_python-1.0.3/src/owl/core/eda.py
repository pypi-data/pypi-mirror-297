import os
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
import plotly.express as px
import pandas as pd
import seaborn as sns
import scipy.stats
import shutil
from ipywidgets import HTML, VBox
from plotly import graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
from owl.core.utils import load_img


class EdaDataset:
    """
    This class represents image dataset from directory (we call it gallery). Currently it supports methods 
    for plotting image data and tools like apply or undersampling.  
    """
    def __init__(self, gallery, im_size):
        """
        Initializes dataset from directory
        Parameters:
        - gallery: path to directory with images
        - im_size: tuple, size of images after loading
        """
        self.gallery = gallery
        self.filenames = os.listdir(self.gallery)
        self.data = np.array([load_img(f"{self.gallery}/{image_file}", im_size) for image_file in tqdm(self.filenames, desc="Loading")])
        self.cached_features_dataframe = None
        

    def apply(self, func, inplace=False):
        """
        Applies function to whole dataset (self.data)
        Parameters:
        - func: function to apply
        - inplace: should owl inplace current image with new ones. if
        false just returns processed data.
        """
        result = np.array(list(map(func, self.data)))
        if inplace == True:
            self.data = result
        else:
            return result
        

    def random_plot(self, n_images):
        """
        Plots N random images in subplots. Useful thing while exploring at your data.
        Parameters:
        - n_images: amout of images to plot
        """
        images = []
        for _ in range(n_images):
            idx = np.random.randint(len(self.data))
            images.append(self.data[idx])
            
        n_cols = int(np.ceil(np.sqrt(n_images)))
        n_rows = int(np.ceil(n_images / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols)
        axes = axes.flatten()
        
        for i, (ax, image) in enumerate(zip(axes, images)):
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
        for fn in filenames:
            idx = self.filenames.index(fn)
            images.append(self.data[idx])
            
        n_cols = int(np.ceil(np.sqrt(n_images)))
        n_rows = int(np.ceil(n_images / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols)
        axes = axes.flatten()
        
        for i, (ax, image) in enumerate(zip(axes, images)):
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
        idx = self.filenames.index(filename)
        image = self.data[idx]
        plt.imshow(image)
        plt.show()
        
    
        
    def _get_features(self, model, preprocess_function):
        """
        Extracts features from images (self.data) with Resnet50 and PCA. After 
        processing returns pd.DataFrame with components x & y and filenames.
        Because feature extraction is long operation we are caching data 
        in self.cached_features_dataframe.
        Parameters:
        - model: keras application (nn) to feature extraction
        - preprocess_function: function for input preprocessing before forward pass
        """
        if self.cached_features_dataframe is not None:
            return self.cached_features_dataframe
        else:
            images = self.apply(preprocess_function)
            features = model.predict(images)
            features = features.reshape(len(features), np.prod(features.shape[1:]))
            
            pca = PCA(n_components=2)
            pca_features = pca.fit_transform(features)
            
            x = [i[0] for i in pca_features]
            y = [i[1] for i in pca_features]
            
            df = pd.DataFrame()
            df["x"] = x
            df["y"] = y
            df["filenames"] = self.filenames
            df["filenames"] = df["filenames"].apply(lambda x: f"{self.gallery}/{x}")
            self.cached_features_dataframe = df
            self.cached_pca_features = pca_features
            
            return df
        
        
    def distplot(self, feature_params, kind="scatter"):
        """
        Creates 2d plot based on extracted features. You can use to show distribution
        of images on your dataset and analyze clusters.
        Parameters:
        - kind: how to plot. currently there're 3 type of plots supported:
            * scatter - plotly scatter and filename on hover
            * iscatter - interactive scatter that show image on hover inside jupyter noteboook.
            * joint - hex 2dim plot (sns.jointplot used)
        - feature_params: dictionary of {
            model: tf.keras.application,
            preprocess_function: tf.keras.application preprocess_input function
        }
        """
        df = self._get_features(feature_params["model"], feature_params["preprocess_function"])
        if kind == "scatter":
            fig = px.scatter(df, x="x", y="y", title="Images Distribution", hover_data="filenames")
            fig.show()
        elif kind == "joint":
            sns.jointplot(x="x", y="y", kind="hex", data=df) 
            plt.show() 
        elif kind == "iscatter":
            fig = px.scatter(df, x="x", y="y", title="Images Distribution", hover_data="filenames")
            template="<img src='{filenames}'>"
            html = HTML("")

            def update(trace, points, state):
                ind = points.point_inds[0]
                row = df.loc[ind].to_dict()
                html.value = template.format(**row)

            fig = go.FigureWidget(data=fig.data, layout=fig.layout)
            fig.data[0].on_click(update)

            return VBox([fig, html])
            
            
    def undersample(self, target_size, feature_params):
        """
        Undersamples dataset with kde-method. Returns filepaths of undersampled set and plots main sample
        and undersampled set on top to view distribution.
        Parameters:
        - target_size: target size of subsample, must be lower than size of dataset.
        - feature_params: dictionary of {
            model: tf.keras.application,
            preprocess_function: tf.keras.application preprocess_input function
        }
        """
        assert target_size < len(self.data)
        df = self._get_features(feature_params["model"], feature_params["preprocess_function"])
        data = np.array(list(zip(df["x"].values,df["y"].values)))
        kde = scipy.stats.gaussian_kde(data.T)
        p = 1 / kde.pdf(data.T)
        p /= np.sum(p)
        idx = np.random.choice(np.arange(len(data)), size=target_size, replace=False, p=p)
        sample = data[idx]
        
        plt.figure()
        plt.scatter(data[:, 0], data[:, 1], label='Data', s=10)
        plt.scatter(sample[:, 0], sample[:, 1], label='Sample', s=7)
        plt.legend()
        
        return df.filenames.values[idx]
    
    
    def search_outliers(self, threshold, copy_to=None):
        """
        Search outliers in image dataset. Counts cosine similarity btw images. Then 
        takes samples with lowest scores based on threshold. All possible outliers will 
        be copied to folder provided in copy_to parameter.
        Parameters:
        - threshold: value in (0, 1) interval to select best matches.
        - copy_to: directory, where you want to copy images. if folder not exists we'll
        create it.
        """
        matrix = cosine_similarity(self.apply(lambda x: x.flatten()))
        scores = {}
        
        for row, path in zip(matrix, self.filenames):
            scores[path] = sum(row)
        
        scores = dict(sorted(scores.items(), key=lambda x: x[1]))
        bound = int(len(scores) * threshold)
        files = list(scores.keys())[:bound]
        
        if copy_to is None:
            return files
        else:
            self.copy_subsample_to(files, copy_to)

    
    def copy_to(self, destination):
        """
        Copies all images from gallery to another gallery called destination.
        Parameters:
        - destination: directory, where you want to copy images. if folder not exists we'll
        create it.
        """
        if not os.path.exists(destination):
            os.makedirs(destination)
        for file in tqdm(self.filenames, desc="Copying"):
            shutil.copy(os.path.join(self.gallery, file), destination)
            
        
    def copy_subsample_to(self, files, destination):
        """
        Copies all images with given filenamesfrom gallery to another gallery called destination.
        Parameters:
        - files: which files to copy
        - destination: directory, where you want to copy images. if folder not exists we'll
        create it.
        """
        if not os.path.exists(destination):
            os.makedirs(destination)
        for file in tqdm(files, desc="Copying"):
            shutil.copy(os.path.join(self.gallery, file), destination)
            
            
    def as_iterable(self, annotations):
        """
        Returns zipped object for loop over image and path. If annotations folder provided
        they are also included.
        Parameters:
        - labels: path to folder with annotations
        """
        filepaths = [f"{self.gallery}/{fn}" for fn in self.filenames]
        if annotations is None:
            return zip(self.data, filepaths)
        else:
            labels = [f"{annotations}/{fn}" for fn in os.listdir(annotations)]
            return zip(self.data, filepaths, labels)
            