# simpleAPI
This is a Python Flask simple API to demonstrate HOW RESTFUL API works 

### Organization:
- Name
- Address
- Phone


### User:
- First Name
- Email
- Address
- Phone
- Last Name

### Instructions

Design and implement a simple application serving a RESTful API to perform operations on Organization as well as
Users. You may use any language, framework, or object-relational mapping of your choice and create any additional
fields and classes you desire. We are looking to see how you design and implement your model as well as your
application. We expect to be able to trace an endpoint down to the data transfer objects (DTO) that represent
Organizations and Users. Feel free to provide additional documentation (UML, SQL scripts, comments, etc) that may
communicate your design choices. We expect your API to support the following operations:

- Create a single Organization
- Create a single User
- Add a User to an Organization
- Delete a User from an Organization
- Read all Users who belong to a specific Organization
- Read all Organizations to which a User belongs

### How to run API:

- local server:
  ###### CREATE virtualenv by installing pip packages:
    <pre>pip install -r requirements.txt</pre>
  ###### ADD current folder into PYTHONPATH:
  e.g.  
    <pre>export PYTHONPATH=/c/Users/kawoukaka/workspace/simpleAPI</pre>
  ###### RUN server:
    <pre>python api_server/server.py</pre>
  ###### Check server url 127.0.0.1:5000

- Docker:
  ###### Build docker image:
  e.g.
    <pre>docker build -t xxxx/simple_api:latest</pre>
  docker is running on 127.0.0.1:8001 if you are running with docker desktop version.
  The port number is able to change in Dockerfile and docker-compose file for mapping. 
  ###### RUN docker compose to run container: 
    <pre>docker compose up</pre>
  ###### Check server url 127.0.0.1:8001

### How to run Tests:
  ###### RUN flake8 and unit tests in the folder
    . ./bin/run_tests.sh
