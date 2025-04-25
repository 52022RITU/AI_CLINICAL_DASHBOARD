"""SQL Lexer module for tokenizing SQL queries."""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Enum representing different types of SQL tokens."""
    
    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AND = auto()
    OR = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    UPDATE = auto()
    SET = auto()
    DELETE = auto()
    CREATE = auto()
    TABLE = auto()
    DROP = auto()
    
    # Operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    
    # Punctuation
    COMMA = auto()
    SEMICOLON = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    DOT = auto()
    
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    
    # Other
    WHITESPACE = auto()
    COMMENT = auto()
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    """Class representing a token in a SQL query."""
    
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    """SQL Lexer class for tokenizing SQL queries."""
    
    def __init__(self, text: str):
        """Initialize the lexer with the input text.
        
        Args:
            text: The SQL query text to tokenize.
        """
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None
        
        # Define token patterns
        self.patterns = [
            # Keywords (case insensitive)
            (r'(?i)SELECT', TokenType.SELECT),
            (r'(?i)FROM', TokenType.FROM),
            (r'(?i)WHERE', TokenType.WHERE),
            (r'(?i)AND', TokenType.AND),
            (r'(?i)OR', TokenType.OR),
            (r'(?i)INSERT', TokenType.INSERT),
            (r'(?i)INTO', TokenType.INTO),
            (r'(?i)VALUES', TokenType.VALUES),
            (r'(?i)UPDATE', TokenType.UPDATE),
            (r'(?i)SET', TokenType.SET),
            (r'(?i)DELETE', TokenType.DELETE),
            (r'(?i)CREATE', TokenType.CREATE),
            (r'(?i)TABLE', TokenType.TABLE),
            (r'(?i)DROP', TokenType.DROP),
            
            # Operators
            (r'=', TokenType.EQUAL),
            (r'!=|<>', TokenType.NOT_EQUAL),
            (r'>', TokenType.GREATER),
            (r'<', TokenType.LESS),
            (r'>=', TokenType.GREATER_EQUAL),
            (r'<=', TokenType.LESS_EQUAL),
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULTIPLY),
            (r'/', TokenType.DIVIDE),
            
            # Punctuation
            (r',', TokenType.COMMA),
            (r';', TokenType.SEMICOLON),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\.', TokenType.DOT),
            
            # Literals
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            (r"'[^']*'", TokenType.STRING),
            (r'"[^"]*"', TokenType.STRING),
            (r'\d+(\.\d+)?', TokenType.NUMBER),
            
            # Whitespace and comments
            (r'\s+', TokenType.WHITESPACE),
            (r'--[^\n]*', TokenType.COMMENT),
            (r'/\*[\s\S]*?\*/', TokenType.COMMENT),
        ]
        
        # Compile patterns
        self.regex_patterns = [(re.compile(pattern), token_type) for pattern, token_type in self.patterns]
    
    def advance(self):
        """Advance the position pointer and set the current character."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
    
    def tokenize(self) -> List[Token]:
        """Tokenize the input text into a list of tokens.
        
        Returns:
            A list of Token objects.
        """
        tokens = []
        
        while self.pos < len(self.text):
            # Try to match a token at the current position
            match_found = False
            
            for pattern, token_type in self.regex_patterns:
                match = pattern.match(self.text[self.pos:])
                if match:
                    value = match.group(0)
                    
                    # Skip whitespace and comments
                    if token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                        tokens.append(Token(token_type, value, self.line, self.column))
                    
                    # Update position and current character
                    for char in value:
                        if char == '\n':
                            self.line += 1
                            self.column = 1
                        else:
                            self.column += 1
                    
                    self.pos += len(value)
                    if self.pos < len(self.text):
                        self.current_char = self.text[self.pos]
                    else:
                        self.current_char = None
                    
                    match_found = True
                    break
            
            if not match_found:
                # If no match is found, add an unknown token and advance
                tokens.append(Token(TokenType.UNKNOWN, self.current_char, self.line, self.column))
                self.advance()
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        
        return tokens
