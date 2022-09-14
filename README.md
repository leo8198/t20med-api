<a href="https://drive.google.com/uc?export=view&id=1-yA25u3ELXT_-HWGcNuR1HRYeI-fZHuD"><img src="https://drive.google.com/uc?export=view&id=1-yA25u3ELXT_-HWGcNuR1HRYeI-fZHuD" style="width: 200px; max-width: 100%; height: auto" title="Click to enlarge picture" />


# T20Med API

![Build status](https://github.com/leo8198/t20med-api/actions/workflows/python-app.yml/badge.svg)

T20Med API for the mobile and web applications


Available services:

- Authentication
- Sign up
- Scheduling appointments
- Payment system
- Save file exams
- Digital signing for prescriptions


### Deploy in local environment

Copy the .env.example to .env:

`cp .env.example .env`

Use docker compose:

`docker compose up`

### Testing

For running the tests locally using pytest just start the container, change the database host to localhost instead of postgres and run:

`bash tests.sh`

### Documentation

#### Database schema

The database schema can be found [here](https://drive.google.com/file/d/1C5Iv-LBZu_vZdSuwWXBcBA4-sgaXaQvk/view?usp=sharing).

#### API documentation

API documentation can be found [here](https://documenter.getpostman.com/view/10980235/VVQix2aJ).

#### Production architecture

Production architecture diagram can be found [here](https://drive.google.com/file/d/12CVwjbDr5v3IEJZHh8PUdEcjfWypydzd/view?usp=sharing)

### Deploy in production

It's recommended to use docker swarm and get the image from the company AWS ECR.

`docker stack deploy -c docker-compose.prod.yml t20med-api`

### Logging

Access sentry dashboard