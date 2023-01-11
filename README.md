# aws-serverless-webscraping

This is a basic project to collect notices from a web page and save the information in a MongoDB database. 

You can use this basic project as a guideline for your webscrapings projects that needs to go to a page, collect things that are new and maybe if the first collection was not enough invoke a process to collect the full information about it.

This project uses the [Serverless Framework](https://www.serverless.com/) as a [IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code) to create all infrastructure necessary to complete the job. 

## Architeture

The CI/CD for this project was created using de Bitbucket Pipeline. (If you are using a different CI/CD you only need to check the steps used in the `bitbucket-pipelines.yml` file to create your own steps in your CI/CD Server)

The Docker image with all necessary environment configs to run the webscrap will be stored in the AWS ECR.

All the code to do the scrap will be runned in a Lambda Function. 

The code will store the data in a MongoDB database.

The new information collected will be sent to a queue (AWS SQS) to be consumed by the code responsible for collect the complete information about the notice.

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
    # who are responsible respectively for collecting and storing
```

---

## Running in your machine

Firt of all you will need to install the dependencies of this project. 

Run: `pip install -r src/requirements.txt`

In your environment variable you will need to have de DATABASE_URI seted or have a running MongoDB in your machine. 

To install and run MongoDB Localy check this [article](https://www.mongodb.com/docs/manual/installation/)

## Running in Docker
Inside the `src/` folder where Dockerfile is located run:

`docker build --platform linux/amd64 -t scrapper:latest .`

After that run the container: 

`docker run -p 9000:8080  scrapper:latest insert.handler`

And then, call the function:

`curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`


## References

Lambda Web Scraping with ECS
https://github.com/umihico/docker-selenium-lambda

Serverless + Lambda Container
https://www.serverless.com/blog/container-support-for-lambda