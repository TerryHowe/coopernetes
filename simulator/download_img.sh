# Download filesystem
curl -o ${RPI_IMG_NAME}.zip -L https://downloads.raspberrypi.org/raspios_lite_armhf/images/${RPI_IMG_DIR}/${RPI_IMG_NAME}.zip
unzip ${RPI_IMG_NAME}.zip
rm -f ${RPI_IMG_NAME}.zip
