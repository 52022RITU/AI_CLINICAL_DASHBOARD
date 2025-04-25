"""Tests for the SQL lexer."""

import pytest
from sql_compiler.lexer import Lexer, TokenType


def test_lexer_select():
    """Test lexing a SELECT statement."""
    sql = "SELECT id, name FROM users WHERE age > 18;"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    
    # Check token types (excluding whitespace and EOF)
    token_types = [token.type for token in tokens]
    expected_types = [
        TokenType.SELECT,
        TokenType.IDENTIFIER,  # id
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # name
        TokenType.FROM,
        TokenType.IDENTIFIER,  # users
        TokenType.WHERE,
        TokenType.IDENTIFIER,  # age
        TokenType.GREATER,
        TokenType.NUMBER,      # 18
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    
    assert token_types == expected_types
    
    # Check token values
    token_values = [token.value for token in tokens]
    expected_values = [
        "SELECT",
        "id",
        ",",
        "name",
        "FROM",
        "users",
        "WHERE",
        "age",
        ">",
        "18",
        ";",
        "",
    ]
    
    assert token_values == expected_values


def test_lexer_create_table():
    """Test lexing a CREATE TABLE statement."""
    sql = "CREATE TABLE users (id INTEGER, name STRING, age INTEGER);"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    
    # Check token types (excluding whitespace and EOF)
    token_types = [token.type for token in tokens]
    expected_types = [
        TokenType.CREATE,
        TokenType.TABLE,
        TokenType.IDENTIFIER,  # users
        TokenType.LEFT_PAREN,
        TokenType.IDENTIFIER,  # id
        TokenType.IDENTIFIER,  # INTEGER
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # name
        TokenType.IDENTIFIER,  # STRING
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # age
        TokenType.IDENTIFIER,  # INTEGER
        TokenType.RIGHT_PAREN,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    
    assert token_types == expected_types


def test_lexer_insert():
    """Test lexing an INSERT statement."""
    sql = "INSERT INTO users (id, name, age) VALUES (1, 'John', 30);"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    
    # Check token types (excluding whitespace and EOF)
    token_types = [token.type for token in tokens]
    expected_types = [
        TokenType.INSERT,
        TokenType.INTO,
        TokenType.IDENTIFIER,  # users
        TokenType.LEFT_PAREN,
        TokenType.IDENTIFIER,  # id
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # name
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # age
        TokenType.RIGHT_PAREN,
        TokenType.VALUES,
        TokenType.LEFT_PAREN,
        TokenType.NUMBER,      # 1
        TokenType.COMMA,
        TokenType.STRING,      # 'John'
        TokenType.COMMA,
        TokenType.NUMBER,      # 30
        TokenType.RIGHT_PAREN,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    
    assert token_types == expected_types


def test_lexer_update():
    """Test lexing an UPDATE statement."""
    sql = "UPDATE users SET name = 'Jane', age = 25 WHERE id = 1;"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    
    # Check token types (excluding whitespace and EOF)
    token_types = [token.type for token in tokens]
    expected_types = [
        TokenType.UPDATE,
        TokenType.IDENTIFIER,  # users
        TokenType.SET,
        TokenType.IDENTIFIER,  # name
        TokenType.EQUAL,
        TokenType.STRING,      # 'Jane'
        TokenType.COMMA,
        TokenType.IDENTIFIER,  # age
        TokenType.EQUAL,
        TokenType.NUMBER,      # 25
        TokenType.WHERE,
        TokenType.IDENTIFIER,  # id
        TokenType.EQUAL,
        TokenType.NUMBER,      # 1
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    
    assert token_types == expected_types


def test_lexer_delete():
    """Test lexing a DELETE statement."""
    sql = "DELETE FROM users WHERE id = 1;"
    lexer = Lexer(sql)
    tokens = lexer.tokenize()
    
    # Check token types (excluding whitespace and EOF)
    token_types = [token.type for token in tokens]
    expected_types = [
        TokenType.DELETE,
        TokenType.FROM,
        TokenType.IDENTIFIER,  # users
        TokenType.WHERE,
        TokenType.IDENTIFIER,  # id
        TokenType.EQUAL,
        TokenType.NUMBER,      # 1
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    
    assert token_types == expected_types
