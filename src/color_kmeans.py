from pathlib import Path
import cv2
from sklearn import cluster
import numpy as np
from kneed import DataGenerator, KneeLocator
import hashlib

class ColorKMeans():

    def __init__(self, *args, **kwargs):
        """Initialization

        Raises:
            Warning: if no path provided
        """
        
        # A path is given, the file is read
        if kwargs.get("path", None):
            self.path = Path(kwargs.get("path", None))
            self.image_read = self.read_image()
        # A content is given, the image is decoded
        if kwargs.get("contents", None):
            contents = kwargs.get("contents", None)
            npimg = np.fromstring(contents, np.uint8)
            self.image_read = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        self.md5 = hashlib.md5(self.image_read).hexdigest()
        self.handle_image()

    def make_thumbnail(self, size=(1024, 512)):
        pass


    def read_image(self,):
        return cv2.imread(str(self.path))


    def handle_image(self,):
        """Read the image from self.path and extract some infos (height, etc...)
        """

        # Resize image
        self.image_raw = cv2.resize(self.image_read, (256, 256), interpolation= cv2.INTER_LINEAR)

        # Conversion to RGB
        self.image = cv2.cvtColor(self.image_raw, cv2.COLOR_BGR2RGB)

        # Get some infos
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.n_colors = self.image.shape[2]
        self.pixels = int(self.width * self.height)


    def extract_colors(self, color_number=3):
        """Build a KMean model with a number of centroïds given by color_number color_number

        Args:
            color_number (int, optional): number of centroïds. Defaults to 3.

        Returns:
            _type_: _description_
        """

        # Make the image flat
        self.image_reshaped = self.image.reshape((-1, 3))# if self.is_gray else self.image

        # If the color_number ==0, we run a loop to find the elbow
        if color_number == 0:
            k_values = range(2,12)
        else:
            k_values = [color_number,]

        distortions = []
        labels = []
        palettes = []

        #Loop
        for k_value in k_values:
            
            # Create a KMeans cluster model
            model = cluster.MiniBatchKMeans(n_clusters=k_value)
            # Predict the labels of the pixels
            label = model.fit_predict(self.image_reshaped)
            # Extract the color palette (centroïds)
            palette = model.cluster_centers_.astype(int)
            
            distortions.append(model.inertia_)
            labels.append(label)
            palettes.append(palette)

        # Search the elbow if necessary
        if color_number == 0:
            kn = KneeLocator(x=list(k_values), 
                    y=list(distortions), 
                    curve='convex', 
                    direction='decreasing')
            
            index_selected = k_values.index(kn.knee)
        else:
            index_selected = 0
            
        # Select the palette and the labels
        palette_selected = palettes[index_selected]
        labels_selected = labels[index_selected]
                
        return labels_selected, palette_selected

if __name__ == "__main__":

    pass