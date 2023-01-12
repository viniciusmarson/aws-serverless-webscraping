# aws-serverless-webscraping

This is a basic project to collect notices from a web page and save the information in a MongoDB database. 

You can use this project as a guideline for your webscrapings projects that needs to go to a page, collect things that are new and maybe if the first collection was not enough invoke a process to collect the full information about it.

This project uses the [Serverless Framework](https://www.serverless.com/) as a [IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code) to create all infrastructure necessary to complete the job. 

## Architeture

The CI/CD for this project was created using de Bitbucket Pipeline. (If you are using a different CI/CD you only need to check the steps used in the `bitbucket-pipelines.yml` file to create your own steps in your CI/CD Server)

The Docker image with all necessary environment configs to run the webscrap will be stored in the [AWS ECR](https://aws.amazon.com/pt/ecr/).

All the code to do the scrap will be runned in a [Lambda Function](https://aws.amazon.com/pt/lambda/). 

The code will store the data in a [MongoDB](https://www.mongodb.com/) database.

The new information collected will be sent to a queue ([AWS SQS](https://aws.amazon.com/pt/sqs/)) to be consumed by the code responsible for collect the complete information about the notice.

See the architecture bellow:

![Architecture](img/Architecture.png?raw=true "Architecture")

## Codebase

```yaml
- img
# - "/img" folder contains images used to construct this documentation
- /src
# - "/src" folder contains the application source code
    - /handlers
    # The /handlers folder contains all fonders with the respective set of functions
    # responsible for collect data from the page of the context inserted
    # For example in this project you will find only the camara_news folder
    # where I have all functions responsible for collect data from Brazilian Camara page
    # if I wanted to collect that for more sites I could, for example, have  the bbc_news folder
    # With all codes responsible for collect data from BBC Page
    - /lib
    # The /lib folder contains reusable code between my handlers
    # in this example you will find the scraping and data module
    # who are responsible respectively for collecting and storing data
```

---

## Environment variables

`ENVIRONMENT`: Environment where the code is running, for example:  `dev`, `test`, `production`, `local`

`AWS_REGION`: Region in AWS where your infraestructure is running

`AWS_ACCOUNT_ID`: Your AWS account ID

`MONGO_URI`: Your MongoDB connection string URI, if not informed the application will use `localhost`

## Running

Go inside de `src/` folder.

`make install`
Install project and dev dependencies.

`make test`
Run the unit tests of this project located in `tests/` folder

`make run handler=camara_news file=insert`
Run the project local in your machine. The first argument is the name of the handler and the second the file inside the handler that you wanna run. 

WARNING:
- In your environment variable you will need to have de DATABASE_URI seted or have a running MongoDB in your machine. To install and run MongoDB Localy check this [article](https://www.mongodb.com/docs/manual/installation/)
- You also need the [chrome driver](https://chromedriver.chromium.org/downloads) in your computer. Download and put the file in `/opt/chromedriver`

`make docker-build`
Build docker image

`make docker-run handler=camara_news file=insert`
Run the application inside a docker container. For this command work, you need to have the [Docker](https://www.docker.com/) installed and runing in your machine.

`make signal`
Send a signal to docker container endpoint to run the handle function.

## References

Lambda Web Scraping with ECS
https://github.com/umihico/docker-selenium-lambda

Serverless + Lambda Container
https://www.serverless.com/blog/container-support-for-lambda