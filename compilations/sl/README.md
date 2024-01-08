1) Download curses external shared library
    wget https://ftp.gnu.org/gnu/ncurses/ncurses-6.3.tar.gz

2) Extract tar file
    tar -xvf ncurses-6.3.tar.gz

3) go into the extracted folder and create build folder
    cd ncurses-6.3 && mkdir build && cd build

4) prepare the configuration
    ../configure

5) set necessary programs for compilation
     make -C include
     make -C progs tic

6) return to base installation folder
    cd ..

7) Configure ncurses for mips architecture
    ./configure --prefix=/home/user/git/test \      # share/lib/headers/bin will be stored here
                --host=mips-linux-gnu        \      # arch target
                --build=$(./config.guess)    \      # we are building on X arch
                --mandir=/usr/share/man      \      
                --with-manpage-format=normal \      # dont installing compressed manual pages
                --with-shared                \      # build and install C shared libraries
                --without-debug              \      # dont install debug libraries
                --without-ada                \      
                --disable-stripping          \      # dont strip binaries
                --enable-widec                      # support for wide-character libraries


8) make

9) make TIC_PATH=$(pwd)/build/progs/tic install (you will probably have to use 'sudo' with this command)

10) cross compile sl.c file
    mips-linux-gnu-gcc sl.c -o sl -I/home/user/git/test/include -L /home/user/git/test/lib -static -lncursesw

    if you want the file to be dynamically linked just remove the '-static' flag

11) verify binary sl metadata
    file ./sl
    readelf -h ./sl


### abort sl when char is pressed ###

sl_abort.c contains the sl.c code and adds functionality to abort the execution when 'q' char is pressed

    make all
