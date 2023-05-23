# Auto Avia Offer

### 1. Intro
-----

The aim of project is creating an offer ranking service (task from hack [Aeroclub
Challenge 2023](https://codenrock.com/contests/aeroclub-challenge-2023#/info))


### 2. Project structure
-----

- `notebooks` contains script (.py format):
  - `research`: EDA, data cleaning, feature engineering
- `data` contains .xlsx / .csv files with initial data from hack, processed data after feature engineering
- `service` contains core of FastAPI service.
- `requirements.txt` is list of necessary packages
- `tests` contains test script for service api.


### 3. Installation
-----

Be sure that Docker is installed on your local machine. If not, go [there](https://docs.docker.com/get-docker/) and do following instructions. Then go to command line and execute commands:

1. <code>git clone https://github.com/unknowngfonovich/avia_hack_2023.git</code>
2. Go to `/service` folder
3. Create `.env` file with two variables

    `SERVICE_HOST`=0.0.0.0

    `SERVICE_PORT`=8001

4. <code>docker build -t ranking_service .</code>

### 4. Running
-----

Just go to command line and type next command:

<code>docker run --rm -d --env-file .env -p 8001:8001 ranking_service</code>


### 5. Examples of usage
-----

If you have Postman try to make POST request to `http://0.0.0.0:8001/predict_batch` with body from `test_request.json` from `notebooks/service_api_test`

You will recieve JSON with proba (if offer is likely to be sent) and ranking level within a single request (position).
