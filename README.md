# color-match
A simple flask app that extracts color combinations from a picture with a KMean algorithm

![Screenshot of the dashboard](src/static/screenshot.png)

## Description

This app allows you to drop images in a a flask webapp and to find out its color composition. 

* The color composition is calculated with a `KMean` algorithm.
* The webapp is based on `flask`
* The grid system is managed by `Masonry`
* A `mongo` database is used to store the images and their parameters

## Installation with Docker

In this case, you only need `Docker`. The installation process will take place during the build of the container. To build it :

```docker-compose build```

## Run the projet

The container is launched with the following command :

```docker-compose up```

Open your web browser and go to `<your-local-ip>:5000` to see the flask app. Please adjust the parameters in the `docker-compose.yml`, `Dockerfile` and `settings.py` files.

## Credits

The images in the screenshot are provided by www.unsplash.com.