# FastAPI REST vs. GraphQL Showdown

A practical demonstration project built with FastAPI to showcase the fundamental differences, strengths, and use-cases of two major API paradigms: **REST** and **GraphQL**.

This application provides identical functionality through both a RESTful API and a GraphQL API, allowing developers to compare how each approach handles data fetching, mutations, and client-server interactions.

## Project Purpose

The main goal of this project is to serve as an educational tool and a boilerplate for understanding:
-   How to implement both REST and GraphQL APIs within a single FastAPI application.
-   The core philosophical differences between the two paradigms in a real-world context.
-   When to choose one over the other based on practical examples.
-   How to structure a production-ready application with concepts like services, repositories, dependency injection, and authentication.

## Core Concepts & Structure

The application is built around a simple movie archive domain, featuring three main entities:
-   **Director**: Represents a film director.
-   **Movie**: Represents a film, which has one director and can belong to multiple genres.
-   **Genre**: Represents a film genre (e.g., Sci-Fi, Drama).

The project is organized into distinct, decoupled layers to ensure clean architecture and separation of concerns. The main `app` directory is split into two primary domains: `rest` and `graphql`, which share the core business logic, data models, and authentication mechanisms.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites
-   Python 3.11+
-   [Poetry](https://python-poetry.org/) for dependency management.
-   A running PostgreSQL database instance.

### 1. Clone the Repository
```bash
git clone https://github.com/hevalhazalkurt/fastapi-rest-vs-graphql.git
cd fastapi-rest-vs-graphql-showdown
```

### 2. Configure Environment Variables

Create an `.env` file in the project root by copying the example file. This file contains database connection strings and authentication keys.

```bash
cp .env_example .env
```

Now, open the `.env` file and update the `DATABASE_URL` to match your local PostgreSQL credentials. Ensure this database exists on your PostgreSQL server.

```bash
# .env file content
# Update user, password, and db name
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME

# Optional DB Pool Settings
POOL_SIZE=10
ECHO=False
MAX_OVERFLOW=2

# Static keys for simulated authentication
API_SECRET_KEY=fake_jwt_token
API_ADMIN_KEY=fake_admin_jwt_token
```

### 3. Install Dependencies

Use the Makefile to install all required Python packages via Poetry.

```bash
make install
```

### 4. Set Up and Migrate the Database

Run the database migrations to create all the necessary tables (directors, movies, genres, etc.).

```bash
make migrate
```

### 5. Seed the Database with Dummy Data

The project includes a script to populate the database with a significant amount of sample data (directors, movies, and genres) for realistic testing. The data is read from `data/dummy_data.csv`.

```bash
make seed
```


## Running the Application

### Running the Local Server

To start the FastAPI application, use the following command. The server will be accessible at http://localhost:8000.

```bash
make run-local
```


## API Usage: REST vs. GraphQL Showcase

This project exposes the same data through two different API endpoints. Authentication is handled via a static Bearer token.
* **Admin Token**: Use the `API_ADMIN_KEY` from your `.env` file (`fake_admin_jwt_token`) for operations requiring admin privileges (e.g., `POST`, `DELETE`).
* **User Token**: Use the `API_SECRET_KEY` (`fake_jwt_token`) for standard read-only operations.


### REST API
The REST API follows standard conventions with dedicated endpoints for each resource.
Interactive Docs: Access the Swagger UI at http://localhost:8000/docs to explore all endpoints.

**Example Requests:**

Get all directors (Authentication required):

```bash
curl -X GET "http://localhost:8000/rest/directors/" \
  -H "Authorization: Bearer fake_jwt_token"
```

Create a new director (Admin scope required):

```bash
curl -X POST "http://localhost:8000/rest/directors/director" \
  -H "Authorization: Bearer fake_admin_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Heval Hazal Kurt"}'
```

### GraphQL API

The GraphQL API provides a single, powerful endpoint for all data operations.

Interactive Playground: Access the GraphiQL interface at http://localhost:8000/graphql to write and test queries.

**Example Queries & Mutations:**
Remember to set the `Authorization: Bearer fake_jwt_token` header in your GraphQL client.

Get directors:

```graphql
query GetDirectorNames {
  directors(limit: 5) {
    name
  }
}
```

Get directors and their movies in a single request. 

```graphql
query GetDirectorsWithMovies {
  directors(limit: 5) {
    name
    movies {
      title
      releaseYear
    }
  }
}
```

Create a new director (Admin scope required). Remember to set the `Authorization: Bearer fake_admin_jwt_token` header in your GraphQL client.

```graphql
mutation CreateNewDirector {
  createDirector(directorInput: {name: "Greta Gerwig"}) {
    uuid
    name
  }
}
```

## Makefile Commands

Here's a summary of the available make commands:

* `make install`: Installs project dependencies.
* `make migrate`: Applies database migrations using Alembic.
* `make seed`: Populates the database with dummy data.
* `make run-local`: Starts the FastAPI development server.
* `make static-checks`: Runs Mypy for static type analysis.
* `make lint`: Checks code style with Ruff.
* `make format`: Formats code with Ruff.


## License
This project is licensed under the MIT License.
