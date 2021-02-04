all: build

build:
	docker build --tag complex-yolov4:latest --target prod -f Dockerfile .

debug-build:
	docker build --tag complex-yolov4:latest --target debug -f Dockerfile .

run:
	docker stop $(docker ps --filter="name=mfund-complex-yolov4" --format '{{.Names}}') || true
	docker rm mfund-complex-yolov4 || true
	docker run --runtime=nvidia --name mfund-complex-yolov4 --net=host -e DISPLAY=${DISPLAY} --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" -v ${PWD}:/home -v /disk/mfund/kitti/training/:/home/dataset/kitti/training:ro -v /disk/mfund/kitti/testing/:/home/dataset/kitti/testing:ro complex-yolov4:latest

debug-run:
	docker stop $(docker ps --filter="name=mfund-complex-yolov4" --format '{{.Names}}') || true
	docker rm mfund-complex-yolov4 || true

	# docker run --runtime=nvidia --name mfund-complex-yolov4 --net=host -v ${PWD}:/home -p 5678:5678 -e DISPLAY=${DISPLAY} --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" -v /disk/mfund/kitti/training/:/home/dataset/kitti/training:ro -v /disk/mfund/kitti/testing/:/home/dataset/kitti/testing:ro complex-yolov4:latest
	docker run --runtime=nvidia --name mfund-complex-yolov4 --net=host -v ${PWD}:/home -p 5678:5678 -e DISPLAY=${DISPLAY} --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" -v /disk/mfund/auto:/home/dataset/kitti/testing:ro complex-yolov4:latest
	