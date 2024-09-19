import pkg_resources

import cv2
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
import torchvision.models as models

from experiments.AFLW.pip_32_16_60_r101_l2_l1_10_1_nb10 import Config as AFLW_R101_Config
from experiments.AFLW.pip_32_16_60_r50_l2_l1_10_1_nb10 import Config as AFLW_R50_Config
from experiments.AFLW.pip_32_16_60_r18_l2_l1_10_1_nb10 import Config as AFLW_R18_Config
from experiments.COFW.pip_32_16_60_r101_l2_l1_10_1_nb10 import Config as COFW_R101_Config
from experiments.COFW.pip_32_16_60_r50_l2_l1_10_1_nb10 import Config as COFW_R50_Config
from experiments.COFW.pip_32_16_60_r18_l2_l1_10_1_nb10 import Config as COFW_R18_Config
from experiments.data_300W.pip_32_16_60_r101_l2_l1_10_1_nb10 import Config as data_300W_R101_Config
from experiments.data_300W.pip_32_16_60_r50_l2_l1_10_1_nb10 import Config as data_300W_R50_Config
from experiments.data_300W.pip_32_16_60_r18_l2_l1_10_1_nb10 import Config as data_300W_R18_Config
from experiments.data_300W_CELEBA.pip_32_16_60_r18_l2_l1_10_1_nb10_wcc import Config as data_300W_CELEBA_R18_Config
from experiments.data_300W_COFW_WFLW.pip_32_16_60_r18_l2_l1_10_1_nb10_wcc import Config as data_300W_COFW_WFLW_R18_Config
from experiments.LaPa.pip_32_16_60_r101_l2_l1_10_1_nb10 import Config as LaPa_R101_Config
from experiments.LaPa.pip_32_16_60_r50_l2_l1_10_1_nb10 import Config as LaPa_R50_Config
from experiments.LaPa.pip_32_16_60_r18_l2_l1_10_1_nb10 import Config as LaPa_R18_Config
from experiments.WFLW.pip_32_16_60_r101_l2_l1_10_1_nb10 import Config as WFLW_R101_Config
from experiments.WFLW.pip_32_16_60_r50_l2_l1_10_1_nb10 import Config as WFLW_R50_Config
from experiments.WFLW.pip_32_16_60_r18_l2_l1_10_1_nb10 import Config as WFLW_R18_Config

from lib.networks import Pip_resnet18, Pip_resnet50, Pip_resnet101, Pip_mbnetv2, Pip_mbnetv3
from lib.mobilenetv3 import mobilenetv3_large
from lib.functions import get_meanface

class LandmarkPredictor:
    def __init__(self, data_name, backbone_name, weight_file, use_gpu=True):
        self.data_name = data_name
        self.backbone_name = backbone_name
        self.weight_file = weight_file
        self.use_gpu = use_gpu

        # Load the correct config based on data_name and backbone_name
        self.cfg = self.get_config(data_name, backbone_name)

        # Load the model
        self.device = torch.device("cuda:0" if use_gpu and torch.cuda.is_available() else "cpu")
        self.net = self.load_model()
        self.net.to(self.device)
        
        # Load the mean face information
        self.meanface_path = self.get_meanface_path()
        self.meanface_indices, self.reverse_index1, self.reverse_index2, self.max_len = get_meanface(self.meanface_path, self.cfg.num_nb)

        # Load model weights
        self.load_weights()

        # Define preprocessing transforms
        self.preprocess = transforms.Compose([
            transforms.Resize((self.cfg.input_size, self.cfg.input_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def get_meanface_path(self):
        # Construct the relative path within the package
        meanface_path = f"data/{self.data_name}/meanface.txt"
        
        # Get the resource path using pkg_resources
        meanface_file = pkg_resources.resource_filename("pipnet", meanface_path)
        
        return meanface_file

    def get_config(self, data_name, backbone_name):
        if data_name == 'AFLW':
            if backbone_name == 'resnet18':
                return AFLW_R18_Config()
            elif backbone_name == 'resnet50':
                return AFLW_R50_Config()
            elif backbone_name == 'resnet101':
                return AFLW_R101_Config()
        elif data_name == 'COFW':
            if backbone_name == 'resnet18':
                return COFW_R18_Config()
            elif backbone_name == 'resnet50':
                return COFW_R50_Config()
            elif backbone_name == 'resnet101':
                return COFW_R101_Config()
        elif data_name == 'data_300W':
            if backbone_name == 'resnet18':
                return data_300W_R18_Config()
            elif backbone_name == 'resnet50':
                return data_300W_R50_Config()
            elif backbone_name == 'resnet101':
                return data_300W_R101_Config()
        elif data_name == 'data_300W_CELEBA':
            if backbone_name == 'resnet18':
                return data_300W_CELEBA_R18_Config()
        elif data_name == 'data_300W_COFW_WFLW':
            if backbone_name == 'resnet18':
                return data_300W_COFW_WFLW_R18_Config()
        elif data_name == 'LaPa':
            if backbone_name == 'resnet18':
                return LaPa_R18_Config()
            elif backbone_name == 'resnet50':
                return LaPa_R50_Config()
            elif backbone_name == 'resnet101':
                return LaPa_R101_Config()
        elif data_name == 'WFLW':
            if backbone_name == 'resnet18':
                return WFLW_R18_Config()
            elif backbone_name == 'resnet50':
                return WFLW_R50_Config()
            elif backbone_name == 'resnet101':
                return WFLW_R101_Config()
        else:
            raise ValueError("No such dataset or backbone!")

    def load_model(self):
        if self.cfg.backbone == 'resnet18':
            resnet18 = models.resnet18(weights=None)
            return Pip_resnet18(resnet18, self.cfg.num_nb, num_lms=self.cfg.num_lms, input_size=self.cfg.input_size, net_stride=self.cfg.net_stride)
        elif self.cfg.backbone == 'resnet50':
            resnet50 = models.resnet50(weights=None)
            return Pip_resnet50(resnet50, self.cfg.num_nb, num_lms=self.cfg.num_lms, input_size=self.cfg.input_size, net_stride=self.cfg.net_stride)
        elif self.cfg.backbone == 'resnet101':
            resnet101 = models.resnet101(weights=None)
            return Pip_resnet101(resnet101, self.cfg.num_nb, num_lms=self.cfg.num_lms, input_size=self.cfg.input_size, net_stride=self.cfg.net_stride)
        elif self.cfg.backbone == 'mobilenet_v2':
            mbnet = models.mobilenet_v2(weights=None)
            return Pip_mbnetv2(mbnet, self.cfg.num_nb, num_lms=self.cfg.num_lms, input_size=self.cfg.input_size, net_stride=self.cfg.net_stride)
        elif self.cfg.backbone == 'mobilenet_v3':
            mbnet = mobilenetv3_large()
            return Pip_mbnetv3(mbnet, self.cfg.num_nb, num_lms=self.cfg.num_lms, input_size=self.cfg.input_size, net_stride=self.cfg.net_stride)
        else:
            raise ValueError('No such backbone!')

    def load_weights(self):
        state_dict = torch.load(self.weight_file, map_location=self.device, weights_only=True)
        self.net.load_state_dict(state_dict)
        self.net.eval()

    def predict_landmarks(self, image_path):
        # Load the image based on the type of image_path
        if isinstance(image_path, str):
            # If the input is a file path, read the image from disk
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Unable to load image from path: {image_path}")
        elif isinstance(image_path, np.ndarray):
            # If the input is a NumPy array (already an image), use it directly
            image = image_path
        elif isinstance(image_path, Image.Image):
            # If the input is a PIL image, convert it to a NumPy array
            image = np.array(image_path)[:,:,::-1]
        else:
            raise TypeError(f"Unsupported image type: {type(image_path)}")

        det_height, det_width, _ = image.shape
        inputs = cv2.resize(image, (self.cfg.input_size, self.cfg.input_size))
        inputs = Image.fromarray(inputs[:,:,::-1].astype('uint8'), 'RGB')
        inputs = self.preprocess(inputs).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs_cls, outputs_x, outputs_y, outputs_nb_x, outputs_nb_y = self.net(inputs)

        tmp_batch, tmp_channel, _, tmp_width = outputs_cls.size()
        assert tmp_batch == 1

        lms_pred_x, lms_pred_y, lms_pred_nb_x, lms_pred_nb_y = self.extract_landmarks(outputs_cls, outputs_x, outputs_y, outputs_nb_x, outputs_nb_y, tmp_batch, tmp_channel, tmp_width)
        lms_pred_merge = self.merge_landmarks(lms_pred_x, lms_pred_y, lms_pred_nb_x, lms_pred_nb_y, det_width, det_height)

        return lms_pred_merge

    def extract_landmarks(self, outputs_cls, outputs_x, outputs_y, outputs_nb_x, outputs_nb_y, tmp_batch, tmp_channel, tmp_width):
        outputs_cls = outputs_cls.view(tmp_batch*tmp_channel, -1)
        max_ids = torch.argmax(outputs_cls, 1)
        # max_cls = torch.max(outputs_cls, 1)[0]
        max_ids = max_ids.view(-1, 1)
        max_ids_nb = max_ids.repeat(1, self.cfg.num_nb).view(-1, 1)

        outputs_x = outputs_x.view(tmp_batch*tmp_channel, -1)
        outputs_x_select = torch.gather(outputs_x, 1, max_ids)
        outputs_x_select = outputs_x_select.squeeze(1)
        outputs_y = outputs_y.view(tmp_batch*tmp_channel, -1)
        outputs_y_select = torch.gather(outputs_y, 1, max_ids)
        outputs_y_select = outputs_y_select.squeeze(1)

        outputs_nb_x = outputs_nb_x.view(tmp_batch*self.cfg.num_nb*tmp_channel, -1)
        outputs_nb_x_select = torch.gather(outputs_nb_x, 1, max_ids_nb)
        outputs_nb_x_select = outputs_nb_x_select.squeeze(1).view(-1, self.cfg.num_nb)
        outputs_nb_y = outputs_nb_y.view(tmp_batch*self.cfg.num_nb*tmp_channel, -1)
        outputs_nb_y_select = torch.gather(outputs_nb_y, 1, max_ids_nb)
        outputs_nb_y_select = outputs_nb_y_select.squeeze(1).view(-1, self.cfg.num_nb)

        tmp_x = (max_ids%tmp_width).view(-1,1).float()+outputs_x_select.view(-1,1)
        tmp_y = (max_ids//tmp_width).view(-1,1).float()+outputs_y_select.view(-1,1)
        tmp_x /= 1.0 * self.cfg.input_size / self.cfg.net_stride
        tmp_y /= 1.0 * self.cfg.input_size / self.cfg.net_stride

        tmp_nb_x = (max_ids%tmp_width).view(-1,1).float()+outputs_nb_x_select
        tmp_nb_y = (max_ids//tmp_width).view(-1,1).float()+outputs_nb_y_select
        tmp_nb_x = tmp_nb_x.view(-1, self.cfg.num_nb)
        tmp_nb_y = tmp_nb_y.view(-1, self.cfg.num_nb)
        tmp_nb_x /= 1.0 * self.cfg.input_size / self.cfg.net_stride
        tmp_nb_y /= 1.0 * self.cfg.input_size / self.cfg.net_stride
        return tmp_x, tmp_y, tmp_nb_x, tmp_nb_y

    def merge_landmarks(self, lms_pred_x, lms_pred_y, lms_pred_nb_x, lms_pred_nb_y, det_width, det_height):
        lms_pred = torch.cat((lms_pred_x, lms_pred_y), dim=1).flatten()
        tmp_nb_x = lms_pred_nb_x[self.reverse_index1, self.reverse_index2].view(self.cfg.num_lms, self.max_len)
        tmp_nb_y = lms_pred_nb_y[self.reverse_index1, self.reverse_index2].view(self.cfg.num_lms, self.max_len)
        tmp_x = torch.mean(torch.cat((lms_pred_x, tmp_nb_x), dim=1), dim=1).view(-1,1)
        tmp_y = torch.mean(torch.cat((lms_pred_y, tmp_nb_y), dim=1), dim=1).view(-1,1)
        lms_pred_merge = torch.cat((tmp_x, tmp_y), dim=1).flatten()
        lms_pred = lms_pred.cpu().numpy()
        lms_pred_merge = lms_pred_merge.cpu().numpy()

        lmks = []
        for i in range(self.cfg.num_lms):
            x_pred = lms_pred_merge[i*2] * det_width
            y_pred = lms_pred_merge[i*2+1] * det_height
            lmks.append([x_pred, y_pred])
        
        return lmks

    def __call__(self, image_path):
        return self.predict_landmarks(image_path)

    def draw_landmarks(self, image, lmks):
        for lmk in lmks:
            cv2.circle(image, (int(lmk[0]), int(lmk[1])), 1, (0, 0, 255), 2)
        return image

    def __repr__(self):
        return f"LandmarkPredictor(data_name={self.data_name}, backbone_name={self.backbone_name}, weight_file={self.weight_file}, use_gpu={self.use_gpu})"

if __name__ == '__main__':
    # Instantiate the class with configuration
    predictor = LandmarkPredictor(data_name="data_300W_CELEBA", backbone_name="resnet18", weight_file="../PIPNet/snapshots/data_300W_CELEBA/pip_32_16_60_r18_l2_l1_10_1_nb10_wcc/epoch59.pth")

    # Predict landmarks for a given image
    image = cv2.imread("/home/james/02.Codes/video-retalking/dat_assets/det_crop.png")
    landmarks = predictor(image)
    image = predictor.draw_landmarks(image, landmarks)
    cv2.imwrite("out.png", image)

