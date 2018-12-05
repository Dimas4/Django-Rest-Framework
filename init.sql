CREATE DATABASE testdb;
CREATE USER useruser WITH PASSWORD 'useruser';
GRANT ALL PRIVILEGES ON DATABASE "testdb" to useruser;
\i create_tables.sql
