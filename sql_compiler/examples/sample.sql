-- Create a users table
CREATE TABLE users (
    id INTEGER,
    name STRING,
    email STRING,
    age INTEGER
);

-- Insert some sample data
INSERT INTO users (id, name, email, age) VALUES (1, 'John Doe', 'john@example.com', 30);
INSERT INTO users (id, name, email, age) VALUES (2, 'Jane Smith', 'jane@example.com', 25);
INSERT INTO users (id, name, email, age) VALUES (3, 'Bob Johnson', 'bob@example.com', 40);

-- Query the data
SELECT * FROM users WHERE age > 25;
