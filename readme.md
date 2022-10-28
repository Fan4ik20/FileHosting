# SimpleFileHosting
## Description
An api for file hosting in which you can create accounts,  
directories and upload files
## Requirements
- Docker  
Or
- Python 3.10

## Installation
- clone this repo via command  
`git clone https://github.com/Fan4ik20/FileHosting.git`
## After installation
- if you want to run an application using python
  - Install the requirements  
  `cd fastwitter && pip install -r requirements.txt`
## Running
- Via Python
  - Go to source dir  
  `cd file_hosting`
  - Run application  
  `uvicorn api.main:api --reload`
- Via Docker
  - Build images and run containers
  `docker compose build && docker compose up -d`
  - To stop the containers use  
  `docker compose stop`
  - To remove the containers use  
  `docker compose down`
