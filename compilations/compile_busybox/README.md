1) Download busybox source code
    wget https://busybox.net/downloads/busybox-1.36.1.tar.bz2

2) Extract tar file
    tar -xvf busybox-1.36.1.tar.bz2

3) configure busybox to be compiled as static
    a) make menuconfig -> Settings -> Build static library (not shared libs)

    b) cat .config | grep -i static (to verify configuration)

4) make ARCH=mips CROSS_COMPILE=mips-linux-gnu- -j $(nproc)

5) verify 'busybox' is compiled for MIPS architecture
    file busybox
    
