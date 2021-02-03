import numpy as np
import os

class ObjReadWriter:
    def __init__(self, depthFilePath, meshFilePath, outputMeshFilePath, depthOutputFilePath):
        self.depthFilePath = depthFilePath
        self.meshFilePath = meshFilePath
        self.outputMeshFilePath = outputMeshFilePath
        self.depthOutputFilePath = depthOutputFilePath
    
    def getDepthValues(self):
        f = open(self.depthFilePath,"r")
        Lines = f.readlines() 
        depthValues = []
        for line in Lines:
            lineSplited = line.split()
            depthValues.append(float(lineSplited[0]))
        return np.array(depthValues)
    
    def getMeshData(self):
        f = open(self.meshFilePath,"r")
        Lines = f.readlines() 
        ptcl = []
        pixCoordinates = []
        translation_table = []
        for line in Lines:
            lineSplited = line.split()
            if len(lineSplited) == 0:
                # print("blank line")
                continue
            if lineSplited[0] == "v":
                ptcl.append(np.array([float(lineSplited[1]), float(lineSplited[2]), float(lineSplited[3])]))
                # ptcl.append(float(lineSplited[3]))
            elif lineSplited[0] == "vt":
                pixCoordinates.append(np.array([float(lineSplited[1]), float(lineSplited[2])]))
            elif lineSplited[0] == "f":
                first_pair = lineSplited[1].split("/")
                second_pair = lineSplited[2].split("/")
                thired_pair = lineSplited[3].split("/")
                translation_table.append(np.array([float(first_pair[0]) - 1, float(first_pair[1]) - 1, float(second_pair[0]) - 1,
                                                   float(second_pair[1]) - 1, float(thired_pair[0]) - 1, float(thired_pair[1]) - 1]))
        return np.array(ptcl), np.array(pixCoordinates), np.array(translation_table)

    def writeMeshOutput(self, verticiesArray, pixelCoordinatesArray):
        if os.path.isfile(self.outputMeshFilePath):
            os.remove(self.outputMeshFilePath)
        with open(self.outputMeshFilePath, 'w') as f:
            f.write("mtllib material.mtl\n")
            f.write("usemtl material\n")
            for vertex in verticiesArray:
                f.write("v %s %s %s\n" % (vertex[0], vertex[1], vertex[2]))
            f.write("\n")
            for pixelCoordinate in pixelCoordinatesArray:
                f.write("vt %s %s\n" % (pixelCoordinate[0], pixelCoordinate[1]))

    def writeDepthOutput(self, depthArray):
        if os.path.isfile(self.depthOutputFilePath):
            os.remove(self.depthOutputFilePath)
        with open(self.depthOutputFilePath, 'w') as f:
            for depth in depthArray:
                f.write("%s\n" % depth)