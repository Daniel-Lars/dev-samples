# dev-samples

A sample development environment for data engineering and analytics, featuring:
- Local PostgreSQL databases representing different environemnts (dev and cprod) via Docker Compose
- Python utilities for generating mock data
- A dbt project set-up with dedicated dev_ schemas for individual developers 
- Task automation with Taskfile

## Project Structure

```
dev-samples/
│
├── dbt_dev_samples/         # dbt project (models, macros, seeds, snapshots, etc.)
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── ...
├── src/dev_samples/         # Python source code
│   └── mockdata/
│       └── mockdata.py      # Script to generate mock data in PostgreSQL
├── docker-compose.yml       # Defines local PostgreSQL containers
├── Taskfile.yml             # Task automation (start DBs, generate mock data)
├── pyproject.toml           # Python project metadata and dependencies
├── uv.lock                  # Python dependency lock file
├── README.md                # Project documentation (this file)
└── ...
```

## Getting Started

### 1. Requirements

- Docker & Docker Compose
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) or pip for dependency management
- dbt-core (installed via Python dependencies)

### 2. Setup

#### Install Python dependencies

```sh
uv pip install -r pyproject.toml
# or
pip install -r pyproject.toml
```

#### Start PostgreSQL databases

```sh
task start-databases
# or manually:
docker-compose up -d
```

#### Set environment variables

Create a .env file or export the following variables for database access (change sensitive data accordingly):

```
DEV_POSTGRES_USER=postgres
DEV_POSTGRES_PASSWORD=password
DEV_POSTGRES_DB=dev_db
CPROD_POSTGRES_USER=postgres
CPROD_POSTGRES_PASSWORD=password
CPROD_POSTGRES_DB=cprod_db
# The developers name used to prefix dedicated dev schema 
DEV_NAME=myname
```

### 3. Generate Mock Data

Populate the dev database with fake user signup data:

```sh
# creates 50 rows of mock data, can be customized with the argument rows=n 
task mock-data
# or manually:
python src/dev_samples/mockdata/mockdata.py -n 100
```

### 4. Using dbt

Navigate to the dbt project directory:

```sh
cd dbt_dev_samples
```

Run dbt models:

```sh
dbt run
```

## Project Details

- **dbt**: Models are in models. Configuration is in dbt_project.yml and profiles.yml.
- **Mock Data**: The script in mockdata.py generates fake user signup data using Faker and SQLAlchemy.
- **Docker Compose**: Spins up two PostgreSQL containers for dev and cprod environments.
- **Taskfile**: Provides shortcuts for common tasks (`start-databases`, `refresh-databases`, `mock-data`).

## Resources

- [dbt Documentation](https://docs.getdbt.com/docs/introduction)
- [Faker Documentation](https://faker.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Taskfile Documentation](https://taskfile.dev/)
