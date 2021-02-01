#!/bin/sh

cd src
# run echo $DISPLAY in your local machine after loging into the hulk and copy the resultant port number below
export DISPLAY=localhost:12.0

python3 test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home --show_image
