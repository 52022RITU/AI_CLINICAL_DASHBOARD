"""Tests for the SQL parser."""

import pytest
from sql_compiler.lexer import Lexer
from sql_compiler.parser import Parser, SelectStatement, CreateTableStatement, InsertStatement


def test_parser_select():
    """Test parsing a SELECT statement."""
    sql = "SELECT id, name FROM users WHERE age > 18;"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    
    assert isinstance(statement, SelectStatement)
    assert statement.columns == ["id", "name"]
    assert statement.table == "users"
    assert statement.where_clause is not None


def test_parser_select_all():
    """Test parsing a SELECT * statement."""
    sql = "SELECT * FROM users;"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    
    assert isinstance(statement, SelectStatement)
    assert statement.columns == ["*"]
    assert statement.table == "users"
    assert statement.where_clause is None


def test_parser_create_table():
    """Test parsing a CREATE TABLE statement."""
    sql = "CREATE TABLE users (id INTEGER, name STRING, age INTEGER);"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    
    assert isinstance(statement, CreateTableStatement)
    assert statement.table == "users"
    assert statement.columns == {
        "id": "INTEGER",
        "name": "STRING",
        "age": "INTEGER",
    }


def test_parser_insert():
    """Test parsing an INSERT statement."""
    sql = "INSERT INTO users (id, name, age) VALUES (1, 'John', 30);"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    statement = parser.parse()
    
    assert isinstance(statement, InsertStatement)
    assert statement.table == "users"
    assert statement.columns == ["id", "name", "age"]
    assert statement.values == [1, "John", 30]
