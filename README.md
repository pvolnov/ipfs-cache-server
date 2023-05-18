# Cache server IPFS images
This server provides caching functionality for IPFS images using FastAPI and Docker.

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
Copy code
```
volumes:
  - /var/www/here-storage/cache:/workdir/cache
```
Set up Nginx to publish images from the cache folder.

## Run the server:

`docker-compose up`

##  Verify that the service is running:

The service will be accessible at http://0.0.0.0:7001.

You can make requests to the server by replacing the image link with `https://<link to your server>/<url>.` 

For example: http://0.0.0.0:7001/nftstorage.link/ipfs/bafybeieboqph4qqf2n7lasq4ehn6snke2nhdqzde4i4hlywwd3dd7mcjma/U1307.png.

## Contributing

Contributions are welcome! If you find any issues or want to contribute new features, feel