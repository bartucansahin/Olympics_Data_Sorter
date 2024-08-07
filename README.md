# Olympics Data Sorter

This project is designed to sort and analyze data related to the Olympics. The application is built using Python, Flask, and SQLAlchemy, and it leverages Docker for containerization.

## API Endpoints
The Olympics Data Sorter API provides several endpoints to interact with the Olympics data returning in JSON format. Below are the available endpoints and their capabilities:

### 1. Get All Athletes
- **Endpoint**: `/athletes`
- **Method**: `GET`
- **Description**: Retrieves a list of all athletes in a sorted list.

### 2. Get All Countries
- **Endpoint**: `/countries`
- **Method**: `GET`
- **Description**: Retrieves a list of all countries in a sorted list.

### 3. Get All Sports
- **Endpoint**: `/sports`
- **Method**: `GET`
- **Description**: Retrieves a list of all sports in a sorted list.

### 3. Get All Countries sorted by Medals
- **Endpoint**: `/countries/medals`
- **Method**: `GET`
- **Description**: Retrieves a list of all countries in sorted order by most medal winners.

### 4. Search Endpoint
- **Endpoint**: `/countries/medals`
- **Method**: `GET`
- **Description**: Searches for athletes, countries, or sports based on the query parameter `q`. Returns 30 values in an array, sorted by exact matches first.

**Query Parameters**:
- `q` (string): The search query

**Example Request**:
```sh
curl -X GET "http://localhost:5000/search?q=athlete_name"
```
### 5. Info Endpoint
- **Endpoint**: `/info`
- **Method**: `GET`
- **Description**: Retrieves information about an athlete, country, or sport based on the query parameter `value`.

**Query Parameters**:
- `value` (string): The value to get information for

**Example Request**:
```sh
curl -X GET "http://localhost:5000/info?value=athlete_name"
```


## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or later
- Docker and Docker Compose installed
- Git installed
- MySQL installed

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Step 1: Clone the Repository

Clone this repository to your local machine using:
```sh
git clone https://github.com/your-repo/Olympics_Data_Sorter.git
cd Olympics_Data_Sorter
```

### Step 2: Create and Activate a Virtual Environment

python3 -m venv venv
source venv/bin/activate

### Step 3: Install the Required Packages
```sh
pip install -r requirements.txt
```
### Step 4: Set Up the Database

You need to have a MySQL database set up. You can run MySQL in a Docker container for this purpose.
```sh
docker run --name olympics-mysql -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=olympics -p 3306:3306 -d mysql:5.7
```
Update the config.py file with your database credentials:
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yourpassword@localhost/olympics'

### Step 5: Load Initial Data

Load your initial data into the database using the provided script:
```sh
python load_data.py
```
### Step 6: Run the Flask Application
```sh
flask run --host=0.0.0.0
```
The application should now be accessible at http://127.0.0.1:5000.

### Docker Setup (Optional)

If you prefer to use Docker:

```sh
docker-compose up --build
```
The application will be accessible at http://localhost:5000.

# Useful Commands

### Deactivate the Virtual Environment:
```sh
deactivate
```
### Stop Docker Containers:

```sh
docker-compose down
```
### Check Docker Container Logs:

```sh
docker logs olympics_data_sorter-web-1
```

# Project Structure
```arduino
Olympics_Data_Sorter/
├── config.py
├── data_sorter.py
├── docker-compose.yml
├── Dockerfile
├── load_data.py
├── .env
├── alembic
├── Olympics_Data.py
├── nginx.conf
├── models.py
├── requirements.txt
├── wait-for-it.sh
├── api.py
└── README.md
```

# Dependencies
The project dependencies are listed in the `requirements.txt` file and include:

- Flask
- SQLAlchemy
- mysqlclient
- pandas
- pymysql





