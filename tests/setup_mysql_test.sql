-- Create the test database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user if it doesn't exist and set the password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges to the test user on the test database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to the test user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

