# Postgres for persistence; SQLite only in tests

MVP runtime data lives in PostgreSQL (Docker Compose for local). SQLite is allowed only for fast unit tests so production-shaped SQL and migrations stay honest. Migrating later should not require a redesign of entities.
