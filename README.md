# Alicemacs Object Storage API (AOS)

[![Build Status](https://travis-ci.org/owlinux1000/aos.svg?branch=master)](https://travis-ci.org/owlinux1000/aos)

This is an example of object storage service's api implemented by fastapi. 

## Features

AOS provided the following RESTful API
- Upload a file
- Download a file
- Download a meta data of uploaded file
- Delete an uploaded file

## Deploy

You can easy to use AOS via Docker!

```
git clone https://github.com/owlinux1000/aos
cd aos
docker build -t aos:latest .
docker run -p 8000:8000 aos:latest
```
