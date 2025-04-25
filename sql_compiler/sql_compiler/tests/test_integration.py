"""Integration tests for the SQL compiler."""

import pytest
from sql_compiler.lexer import Lexer
from sql_compiler.parser import Parser
from sql_compiler.analyzer import Analyzer, Database
from sql_compiler.executor import Executor


def test_create_and_query():
    """Test creating a table and querying it."""
    # Create a database
    database = Database()
    executor = Executor(database)
    
    # Create a table
    create_sql = "CREATE TABLE users (id INTEGER, name STRING, age INTEGER);"
    lexer = Lexer(create_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "create_table"
    assert result["table"] == "users"
    
    # Insert data
    insert_sql = "INSERT INTO users (id, name, age) VALUES (1, 'John', 30);"
    lexer = Lexer(insert_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "insert"
    assert result["count"] == 1
    
    # Query data
    select_sql = "SELECT * FROM users WHERE age > 25;"
    lexer = Lexer(select_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "select"
    assert result["count"] == 1
    assert len(result["rows"]) == 1
    assert result["rows"][0]["id"] == 1
    assert result["rows"][0]["name"] == "John"
    assert result["rows"][0]["age"] == 30


def test_update_and_delete():
    """Test updating and deleting data."""
    # Create a database
    database = Database()
    executor = Executor(database)
    
    # Create a table
    create_sql = "CREATE TABLE users (id INTEGER, name STRING, age INTEGER);"
    lexer = Lexer(create_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    executor.execute(statement)
    
    # Insert data
    insert_sql = "INSERT INTO users (id, name, age) VALUES (1, 'John', 30);"
    lexer = Lexer(insert_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    executor.execute(statement)
    
    # Update data
    update_sql = "UPDATE users SET name = 'Jane', age = 25 WHERE id = 1;"
    lexer = Lexer(update_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "update"
    assert result["count"] == 1
    
    # Query data to verify update
    select_sql = "SELECT * FROM users WHERE id = 1;"
    lexer = Lexer(select_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "select"
    assert result["count"] == 1
    assert result["rows"][0]["name"] == "Jane"
    assert result["rows"][0]["age"] == 25
    
    # Delete data
    delete_sql = "DELETE FROM users WHERE id = 1;"
    lexer = Lexer(delete_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "delete"
    assert result["count"] == 1
    
    # Query data to verify delete
    select_sql = "SELECT * FROM users;"
    lexer = Lexer(select_sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    analyzer = Analyzer(database)
    analyzer.analyze(statement)
    result = executor.execute(statement)
    
    assert result["type"] == "select"
    assert result["count"] == 0
    assert len(result["rows"]) == 0
