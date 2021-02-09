from torch.utils.data import Dataset
import numpy as np
import cv2

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

# Front side (of vehicle) Point Cloud boundary for BEV
BOUNDARY = {
    "minX": -25,
    "maxX": 25,
    "minY": -10,
    "maxY": 10,
    "minZ": -2,
    "maxZ": 2
}
# BEV_WIDTH = 1668
# BEV_HEIGHT = 2388

BEV_WIDTH = 608 
BEV_HEIGHT = 608
class IpadDataset(Dataset):
    def __init__(self, ptcl, pixCoordinates, imgPath, translation_table, depthValues):
        self.pixCoordinates = pixCoordinates
        self.ptcl = ptcl

        BOUNDARY["minX"] = min(self.ptcl[:, 0]) - 1.5
        BOUNDARY["maxX"] = max(self.ptcl[:, 0]) + 1.5
        BOUNDARY["minY"] = min(self.ptcl[:, 1]) - 1.5
        BOUNDARY["maxY"] = max(self.ptcl[:, 1]) + 1.5

        BOUNDARY["minZ"] = min(self.ptcl[:, 2]) - 1.5
        BOUNDARY["maxZ"] = max(self.ptcl[:, 2]) + 1.5

        # breakpoint()
        if abs(BOUNDARY["maxX"] - BOUNDARY["minX"]) < abs(BOUNDARY["maxY"] - BOUNDARY["minY"]):
            self.discretization = (BOUNDARY["maxY"] - BOUNDARY["minY"]) / BEV_HEIGHT
            self.orientation = "y"
        else:
            self.discretization = (BOUNDARY["maxX"] - BOUNDARY["minX"]) / BEV_HEIGHT
            self.orientation = "x"

        self.imgPath = imgPath
        self.translation_table = translation_table

        self.depth = depthValues
        self.ptcl_depth = self.append_depth_ptcl()
        self.sample_id_list = [1]
    #     Debug reasons
        # testBVFeature = self.makeBVFeature()

    def __getitem__(self, index):
        return self.load_img_with_targets(index)

    def append_depth_ptcl(self):
        depthValuesNorm = np.interp(self.depth, (self.depth.min(), self.depth.max()), (0.0, 1.0))
        return np.c_[self.ptcl, depthValuesNorm]

    def load_img_with_targets(self, index):
        sample_id = int(self.sample_id_list[index])
        img_file = self.imgPath
        rgb_map = self.makeBVFeature()
        return img_file, rgb_map

    def makeBVFeature(self):
        Height = BEV_HEIGHT + 1
        Width = BEV_WIDTH + 1

        # Discretize Feature Map
        PointCloud = np.copy(self.ptcl_depth)
        if self.orientation == "y":
            PointCloud[:, 0] = np.int_(np.floor(PointCloud[:, 0] / self.discretization) + Width/2)
            PointCloud[:, 1] = np.int_(np.floor(PointCloud[:, 1] / self.discretization))
        elif self.orientation == "x":
            PointCloud[:, 0] = np.int_(np.floor(PointCloud[:, 0] / self.discretization))
            PointCloud[:, 1] = np.int_(np.floor(PointCloud[:, 1] / self.discretization) + Width/2)

        # sort-3times
        indices = np.lexsort((-PointCloud[:, 2], PointCloud[:, 1], PointCloud[:, 0]))
        PointCloud = PointCloud[indices]
        
        # Height Map & Intensity Map & DensityMap
        heightMap = np.zeros((Height, Width))
        intensityMap = np.zeros((Height, Width))
        densityMap = np.zeros((Height, Width))

        _, indices = np.unique(PointCloud[:, 0:2], axis=0, return_index=True)
        PointCloud_frac = PointCloud[indices]

        max_height = float(np.abs(BOUNDARY['maxZ'] - BOUNDARY['minZ']))
        # breakpoint()
        heightMap[np.int_(PointCloud_frac[:, 0]), np.int_(PointCloud_frac[:, 1])] = np.abs(PointCloud_frac[:, 2]) / max_height

        _, indices, counts = np.unique(PointCloud[:, 0:2], axis=0, return_index=True, return_counts=True)
        PointCloud_top = PointCloud[indices]

        normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64))

        intensityMap[np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])] = PointCloud_top[:, 3]
        densityMap[np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])] = normalizedCounts
        
        # Inspect Maps
        # matplotlib.image.imsave("densityMap.png", densityMap)
        # matplotlib.image.imsave("heightMap.png", heightMap)
        # matplotlib.image.imsave("intensityMap.png", intensityMap)

        RGB_Map = np.zeros((3, Height - 1, Width - 1))
        RGB_Map[2, :, :] = densityMap[:BEV_HEIGHT, :BEV_WIDTH]  # r_map
        RGB_Map[1, :, :] = heightMap[:BEV_HEIGHT, :BEV_WIDTH]  # g_map
        RGB_Map[0, :, :] = intensityMap[:BEV_HEIGHT, :BEV_WIDTH]  # b_map

        return RGB_Map

    def __len__(self):
        return len(self.sample_id_list)
