FROM umihico/aws-lambda-selenium-python:latest

# Install dependecies
RUN pip3 install -U pip selenium==4.4.3 bs4 mongoengine boto3 "pymongo[srv]"

# Copy lambda's main script
COPY ./lib/* ./
COPY ./handlers/* ./