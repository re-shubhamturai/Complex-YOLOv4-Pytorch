# set base image (host OS)
FROM nvidia/cuda:11.1-cudnn8-devel-ubuntu18.04 as base
LABEL maintainer="Shubham Turai <shubham.turai@robotic-eyes.com>"

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev python3-pip 
RUN /usr/bin/python3 -m pip install --upgrade pip

# RUN pip3 install -U -r requirements.txt
RUN pip3 install torch==1.5.0
RUN pip3 install torchvision==0.6.0
RUN pip3 install easydict==1.9
RUN pip3 install opencv-python==4.2.0.34
RUN apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip3 install numpy==1.18.3
RUN pip3 install torchsummary==1.5.1
RUN pip3 install tensorboard==2.2.1
RUN pip3 install scikit-learn==0.22.2
RUN pip3 install mayavi
RUN pip3 install shapely
RUN pip3 install tqdm


FROM base as debug
RUN pip3 install debugpy
# WORKDIR /home/src
# CMD python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home
# CMD python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home --show_image

WORKDIR /home
CMD ["./start.sh"]