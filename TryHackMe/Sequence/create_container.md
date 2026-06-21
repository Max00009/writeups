To create a new container with root access and root filesystems:
```bash
docker run -it --rm -v /:/host <whatever_image_available> /bin/bash
```
-it gives interactive shell
--rm deletes the container after leaving
-v /:/host mounts / directory of host machine with /host directory of our container
if /bin/bash not available try /bin/sh


To check what images are available:
```bash
docker images
```
