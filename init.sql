CREATE DATABASE testdbb;
CREATE USER useruser WITH PASSWORD 'useruser';
GRANT ALL PRIVILEGES ON DATABASE "testdbb" to useruser;
\i create_tables.sql
