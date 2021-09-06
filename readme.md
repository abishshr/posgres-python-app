# Data Engineering Take Home

For this exercise you will create and populate Postgres tables using Python and SQL. We have provided 4 csv files. The `dictionary.csv` contains the schema for the other 3 files. The data in these files is real GameChanger data that has been cleaned and anonymized. **You can use google** for this exercise. We do not expect candidates to remember specifics for any libraries they are using. We want this to mimic normal day to day programing and problem solving. Once you have read through this `README.md` you can find the steps for this take home in the `take_home_steps.md` file.

Postgres will be run in a Docker container. We have provided a docker-compose file to simplify creating and deleting the database. Please create a Dockerfile to run your code and add it as a service to the docker-compose so that we can run your submission locally using the commands in **Usage Notes**.
**Note:** Data within your postgres container will not persist between container restarts. To clear the state, restart the container using the `down` and `up` commands specified in the **Usage Notes** section.

## Pre take home prep

**Folder structure**:

```
.
├── candidate_code
│   ├── Dockerfile
│   ├── app
│   │   └── main.py
│   ├── data
│   │   ├── dictionary.csv
│   │   ├── person_team_association.csv
│   │   ├── persons.csv
│   │   └── teams.csv
│   └── requirements.txt
├── docker-compose.yml
├── readme.md
└── take_home_steps.md

```

For this exercise we will use a Postgres Docker image.
**Note:** you will need Docker, docker compose and psql installed on your computer.

**Usage Notes**

The following terminal commands are for Mac. If you use a different OS, you may need to google for equivalent commands.

**instructions on how to run the app**
To run the app simply go to the location of the app and run the below command this will build and run the docker container
```
 docker-compose up --build 
```

**Tables created for Step 1:**
1.)persons
2.)person_team_association
3.)teams 

**Tables created for Step 2:**
4.)persons_no_team


**Validating the results**

[documentation for up](https://docs.docker.com/engine/reference/commandline/compose_up/)

You can run queries against the Postgres container with:
```
psql -h localhost -p 5432 -U username database
```
The password is `secret`

To run a specific service within the `docker-compose` use:
```
docker-compose run <service_name>
```
[documentation for run](https://docs.docker.com/engine/reference/commandline/compose_run/)

Finally, to kill the Postgres container run:
```
docker-compose down
```
[documentation for down](https://docs.docker.com/engine/reference/commandline/compose_down/)

Once you have finished and submitted the take-home, run this command to remove all unused containers and images:
```
docker system prune
```
[documentation for system prune](https://docs.docker.com/engine/reference/commandline/system_prune/)

It is helpful to create a `requirements.txt` file to simplify dependency installation within the dockerfile. See the [Docker documentation](https://docs.docker.com/language/python/build-images/#create-a-dockerfile-for-python) for more information.

To make sure your development setup wont cause issues, we have provided the `candidate_code` folder which contains a python file to test the connection with the postgres docker container, and a requirements file containing dependencies. Please run this in advance.



1. What ways can this be improved for a production environment?
  - a.) In production we should check if the files are present in the right directory / if the files have 0 bytes / are the files in the expected 
  format before running the job 
  - b.) Also we should check if the database is up and running before starting the loading job 
  - c.) Unit test cases should also be included as part of the build 

2. How does your solution scale?
  - a.) if the data volume gets huge a bulk loader should be used 
  - b.) To scale the solution horizontally parallel computation framework like Apache spark should be used if there are 
  transformations involved 
  - c.) increasing the hardware components like memory sizes 
