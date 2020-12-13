# Tweak filesystem: start qemu with init flag, switch to guest window to execute tweak and close window afterwards
qemu-system-arm -kernel ./${RPI_KERNEL} \
-cpu arm1176 -m 256 \
-M versatilepb -no-reboot -serial stdio \
-append "root=/dev/sda2 panic=1 rootfstype=ext4 rw init=/bin/bash" \
-drive "file=./${RPI_IMG_NAME}.img,index=0,media=disk,format=raw"

sed -i -e 's/^/#/' /etc/ld.so.conf
sed -i -e 's/^/#/' /etc/fstab

# Emulate Raspberry Pi
qemu-system-arm -kernel ./${RPI_KERNEL} \
-cpu arm1176 -m 256 \
-M versatilepb -no-reboot -serial stdio \
-append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
-drive "file=./${RPI_IMG_NAME}.img,index=0,media=disk,format=raw"
-redir tcp:5022::22
