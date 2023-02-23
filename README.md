## Django REST online-pharmacy project

This is our Django REST online retail pharmacy team project. Also, the project is a graduation work for Python courses.

README.md file will be updated soon.

## Installation

The installation process is described based on the features used in the project at the time of the current commit.
The README file will be adapted when changes are added. In case of discrepancies, please describe them in the
**Issues**.

To install this application, you first need to clone this repository using the following command:

`git clone https://github.com/pbalkonskiy/OnlinePharmacy_API.git`

To further deploy the service you must have Docker and Docker compose installed locally. You can read more about the
installation process at https://docs.docker.com/get-docker/.

After installing the necessary software, in the root directory of the project run the command

`docker-compose up --build`

Django Rest Framework project will automatically start and will be available for interaction through the shell if you
use the 

`docker-compose run web bash`

The PostgreSQL database will run inside the Docker container. The added information will be stored in the automatically
created 'pgdata' folder in the project directory. If you later run the project from the container with the command

`docker-compose up`

all local changes will be saved.