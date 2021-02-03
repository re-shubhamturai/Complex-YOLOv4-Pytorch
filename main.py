import cv2
from ObjReadWriter import *
from testloader import *
from pathlib import Path

FILECONFIG = {
    "mesh": "mesh.obj",
    "texture": "texture.png",
    "depth": "depth.txt",
    "outputMesh": "outputMesh.obj",
    "outputDepth": "outputDepth.txt"
}

def convertBinToObj():
    for binfile in sorted(os.listdir("./velodyne")):
        filename, file_extension = os.path.splitext(binfile)
        if file_extension == ".obj":
            continue
        kittibin = open("./velodyne/" + binfile, "rb")
        kittyValues = np.array(np.fromfile(kittibin, dtype=np.float32, count=-1).reshape(-1, 4))
        filename = Path(binfile).stem
        with open("./velodyne/" + filename + ".obj", 'w') as f:
            for xyz in kittyValues:
                f.write("v %s %s %s\n" % (xyz[0], xyz[1], xyz[2]))

if __name__ == '__main__':
    print("Letzt Python")

    # Read every bin and convert to .obj
    convertBinToObj()

    #
    scanPath = os.path.join("./auto", "auto5")
    objRW = ObjReadWriter(os.path.join(scanPath, FILECONFIG["depth"]),
                          os.path.join(scanPath, FILECONFIG["mesh"]),
                          os.path.join(scanPath, FILECONFIG["outputMesh"]),
                          os.path.join(scanPath, FILECONFIG["outputDepth"]))
    imageColor = cv2.imread(os.path.join(scanPath, FILECONFIG["texture"]))

    # cv2.imshow("Original", imageColor)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    depthValues = objRW.getDepthValues()
    ptcl, pixCoordinates, translation_table = objRW.getMeshData()

    ipad_dataloader = create_ipad_dataloader(ptcl, pixCoordinates, imageColor, translation_table, depthValues)

    print("Script finished normaly!")




























































