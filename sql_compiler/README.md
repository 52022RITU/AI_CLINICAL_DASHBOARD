# SQL Query Compiler

A Python-based SQL query compiler that can parse, analyze, and execute SQL queries. This project provides a simple implementation of a SQL compiler with lexical analysis, parsing, semantic analysis, and execution capabilities.

## Features

- **Lexical Analysis**: Tokenizes SQL queries into meaningful tokens
- **Parsing**: Converts tokens into an Abstract Syntax Tree (AST)
- **Semantic Analysis**: Validates SQL queries against a database schema
- **Execution**: Executes SQL queries against an in-memory database
- **Command-line Interface**: Easy-to-use CLI for interacting with the compiler

## Supported SQL Operations

- `SELECT`: Query data from tables
- `INSERT`: Add new records to tables
- `UPDATE`: Modify existing records
- `DELETE`: Remove records from tables
- `CREATE TABLE`: Create new tables
- `DROP TABLE`: Remove existing tables

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sql_compiler.git
   cd sql_compiler
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

### Command-line Interface

The SQL compiler can be used from the command line:

```bash
# Execute a SQL query from a file
sqlcompile path/to/query.sql

# Execute a SQL query directly
sqlcompile --query "SELECT * FROM users WHERE age > 18"

# Save the result to a file
sqlcompile --query "SELECT * FROM users" --output result.json

# Use a specific database file
sqlcompile --query "SELECT * FROM users" --db database.json

# Enable verbose output
sqlcompile --query "SELECT * FROM users" --verbose
```

### Python API

You can also use the SQL compiler as a Python library:

```python
from sql_compiler.lexer import Lexer
from sql_compiler.parser import Parser
from sql_compiler.analyzer import Analyzer, Database
from sql_compiler.executor import Executor

# Create a database
database = Database()

# Create an executor
executor = Executor(database)

# Execute a SQL query
sql = "CREATE TABLE users (id INTEGER, name STRING, age INTEGER)"

# Tokenize
lexer = Lexer(sql)
tokens = lexer.tokenize()

# Parse
parser = Parser(tokens)
statement = parser.parse()

# Analyze
analyzer = Analyzer(database)
analyzer.analyze(statement)

# Execute
result = executor.execute(statement)
print(result)
```

## Project Structure

```
sql_compiler/
├── sql_compiler/
│   ├── __init__.py
│   ├── lexer.py       # SQL tokenizer
│   ├── parser.py      # SQL parser
│   ├── analyzer.py    # Semantic analyzer
│   ├── executor.py    # Query executor
│   ├── cli.py         # Command-line interface
│   └── tests/         # Test directory
├── setup.py           # Package setup file
└── README.md          # This file
```

## Components

### Lexer

The lexer breaks down SQL queries into tokens such as keywords, identifiers, operators, and literals.

### Parser

The parser converts tokens into an Abstract Syntax Tree (AST) that represents the structure of the SQL query.

### Analyzer

The analyzer validates the SQL query against a database schema to ensure it is semantically correct.

### Executor

The executor executes the SQL query against an in-memory database and returns the result.

## Examples

### Creating a Table

```sql
CREATE TABLE users (id INTEGER, name STRING, age INTEGER);
```

### Inserting Data

```sql
INSERT INTO users (id, name, age) VALUES (1, 'John', 30);
```

### Querying Data

```sql
SELECT * FROM users WHERE age > 25;
```

### Updating Data

```sql
UPDATE users SET age = 31 WHERE id = 1;
```

### Deleting Data

```sql
DELETE FROM users WHERE id = 1;
```

## Testing

Run the tests using pytest:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as a learning exercise for compiler design principles
- Inspired by various SQL implementations and compiler design patterns
