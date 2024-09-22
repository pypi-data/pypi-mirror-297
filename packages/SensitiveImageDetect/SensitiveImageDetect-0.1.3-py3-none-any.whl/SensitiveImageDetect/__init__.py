import pickle
from PIL import Image
import torch   
from torch.functional import F  
class Detect:
    """
    The Detect class is used for image classification tasks, leveraging a pre-trained model 
    to make predictions for single or multiple images.

    Attributes:
        model (torch.nn.Module): The loaded classification model.
        preprocess (callable): The image preprocessing function.
        classes (list): List of class labels, containing ['carton', 'other', 'politic', 'sex'].

    Methods:
        - __init__(self, device='cpu')
        - detect_single_type(self, img: Image) -> str
        - detect_single_prob(self, img: Image) -> dict
        - detect_list_type(self, img_list: list) -> list
        - detect_list_prob(self, img_list: list) -> list
    """

    def __init__(self, device='cpu'):
        """
        Initialize an instance of the Detect class, loading the model and preprocessing function.

        Parameters:
            device (str): The type of device to use, default is 'cpu'. Using 'cuda' can speed up computations.
        """
        f = open('./model.pickle', 'rb')
        self.model = pickle.load(f)
        f.close()
        f = open('./transform.pickle', 'rb')
        self.preprocess = pickle.load(f)
        f.close()
        self.model.eval()  # Set the model to evaluation mode
        self.device=device
        self.model.to(self.device)
        self.classes = ['carton', 'other', 'politic', 'sex']

    def detect_single_type(self, img: Image) -> str:
        """
        Predict the class label for a single image.

        Parameters:
            img (Image): An input image (JPG/JPEG format).

        Returns:
            str: The predicted class label.
        """
        try:
            img = self.preprocess(img)
            probality = F.softmax(self.model(torch.stack([img]).to(self.device)))
            ind = torch.argmax(probality[0])
            result = self.classes[ind]
            return result
        except Exception as e:
            raise e

    def detect_single_prob(self, img: Image) -> dict:
        """
        Predict the class probabilities for a single image.

        Parameters:
            img (Image): An input image (JPG/JPEG format).

        Returns:
            dict: A dictionary containing class labels and their corresponding probabilities, 
                  rounded to four decimal places.
        """
        try:
            img = self.preprocess(img)
            probality = F.softmax(self.model(torch.stack([img]).to(self.device)))
            result = {self.classes[i]: round(float(probality[0][i]), 4) for i in range(4)}
            return result
        except Exception as e:
            raise e

    def detect_list_type(self, img_list: list) -> list:
        """
        Predict the class labels for a list of images.

        Parameters:
            img_list (list): A list of input images (JPG/JPEG format).

        Returns:
            list: A list of predicted class labels.
        """
        try:
            for ind in range(len(img_list)):
                img_list[ind] = self.preprocess(img_list[ind])
            probality = F.softmax(self.model(torch.stack(img_list).to(self.device)))
            max, ind = torch.max(probality, dim=1)
            result = []
            for i in range(ind.size(0)):
                result.append(self.classes[ind[i]])
            return result
        except Exception as e:
            raise e

    def detect_list_prob(self, img_list: list) -> list:
        """
        Predict the class probabilities for a list of images.

        Parameters:
            img_list (list): A list of input images (JPG/JPEG format).

        Returns:
            list: A list of dictionaries, where each dictionary contains class labels 
                  and their corresponding probabilities for each image.
        """
        try:
            for ind in range(len(img_list)):
                img_list[ind] = self.preprocess(img_list[ind])
            probality = F.softmax(self.model(torch.stack(img_list).to(self.device)))
            max, ind = torch.max(probality, dim=1)
            result = []
            for i in range(ind.size(0)):
                result.append({self.classes[u]: round(float(probality[i][u]), 4) for u in range(4)})
            return result
        except Exception as e:
            raise e