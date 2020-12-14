qemu-system-arm -kernel ./${RPI_KERNEL} \
    -cpu arm1176 -m 256 -M raspi \
    -dtb ${RPI_DTB_FILE} -no-reboot \
    -serial stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
    -drive "file=${RPI_IMG_NAME}.img,index=0,media=disk,format=raw" \
    -net user,hostfwd=tcp::5022-:22 -net nic
