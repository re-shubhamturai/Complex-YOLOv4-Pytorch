#!/bin/sh

cd src

python3 test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home
# python3 test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home --show_image
