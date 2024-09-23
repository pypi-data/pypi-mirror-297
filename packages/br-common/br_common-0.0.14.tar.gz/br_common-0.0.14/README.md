# **br-common**

`br-common` is a reusable Python package designed to centralize common utilities, SQLAlchemy models, and shared logic. It simplifies the management of shared functionality across multiple microservices, ensuring consistency, scalability, and ease of development.

## **Key Features**

- **Centralized Utility Functions:** Access reusable utility functions across all microservices from a single location, reducing redundancy and promoting clean code.
- **SQLAlchemy Models:** Maintain and share common database models easily across services.
- **Reusable Across Microservices:** Ideal for microservice architectures that require shared utilities and models across various services.

## **Installation**

Install the `br-common` package directly from PyPI using pip:

```bash
pip install br-common
```

## Migration

- Please set the environment variable in your .env file
```bash
DATABASE_URI="postgresql://user:password@host/db_name"
```

- Install the dependencies using below command
```bash
pip install -r requirements.txt 
```

- Create new migration files use below command
```bash
inv migration-create -m "migration message"
```

- Apply the migration
```bash
inv migration-upgrade
```

- Remove latest applied migration
```bash
inv migration-downgrade
``` 
