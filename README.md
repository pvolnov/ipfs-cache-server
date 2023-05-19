# Cache server IPFS images
This server provides caching functionality for IPFS images using FastAPI and Docker.

**Tutorial:** https://dev.to/pvolnov/setup-ipfs-images-cache-server-in-5-min-4n8f

## Prerequisites
Before deploying the service, ensure that you have the following prerequisites installed:

- Docker
- Docker Compose
- `sudo apt install -y pngquant`

## Getting Started
Setup configuration config.yml:

Open the config.yml file and update the following configuration parameters:
- `folder_size:` The maximum cache size in MB.
- `cache_folder:` The path to the cache folder (default is ./cache).
- `image_server_prefix:` web link to ngnix server to share images from cache folder
- `max_size:` The maximum number of images in the cache folder.
Set cache folder path in `docker-compose.yml:`

Open the docker-compose.yml file and update the volume mapping to your desired cache folder path:
yaml

```
volumes:
  - /var/www/here-storage/cache:/workdir/cache
```
Set up Nginx to publish images from the cache folder.

## Run the server:

`docker-compose up`

##  Verify that the service is running:

The service will be accessible at http://0.0.0.0:7001.


##  How to use

1. Make all requests via cache server, create url `https://<image server>/url?sz=XXX`

**Example**
- `server-url:` https://image.herewallet.app
- `ipfs url:` https://nftstorage.link/ipfs/bafybeieboqph4qqf2n7lasq4ehn6snke2nhdqzde4i4hlywwd3dd7mcjma/U1307.png
- `ipfs id:` nftstorage.link/ipfs/bafybeieboqph4qqf2n7lasq4ehn6snke2nhdqzde4i4hlywwd3dd7mcjma/U1307.png
- `size:` 512*512

Result: https://image.herewallet.app/nftstorage.link/ipfs/bafybeieboqph4qqf2n7lasq4ehn6snke2nhdqzde4i4hlywwd3dd7mcjma/U1307.png?sz=512

## Contributing

Contributions are welcome! If you find any issues or want to contribute new features, feel