# /bin/bash
sudo docker build --tag backup .
sudo docker pull itzg/minecraft-server
sudo docker run -d -p 25565:25565 -v ~/mc-server:/data -e EULA=TRUE -e ONLINE_MODE=false --name mc-server itzg/minecraft-server:latest
sudo docker run -d -v ~/mc-server:/input -v ~/mc-server-backups:/output --name mc-backup backup:latest mc-server 60