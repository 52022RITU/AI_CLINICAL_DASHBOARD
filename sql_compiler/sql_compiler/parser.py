"""SQL Parser module for parsing SQL tokens into an AST."""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .lexer import Token, TokenType


class ParseError(Exception):
    """Exception raised for errors during parsing."""
    
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(f"Parse error at line {token.line}, column {token.column}: {message}")


@dataclass
class SelectStatement:
    """Class representing a SELECT statement in the AST."""
    
    columns: List[str]
    table: str
    where_clause: Optional['Expression'] = None


@dataclass
class InsertStatement:
    """Class representing an INSERT statement in the AST."""
    
    table: str
    columns: List[str]
    values: List[Any]


@dataclass
class UpdateStatement:
    """Class representing an UPDATE statement in the AST."""
    
    table: str
    assignments: Dict[str, Any]
    where_clause: Optional['Expression'] = None


@dataclass
class DeleteStatement:
    """Class representing a DELETE statement in the AST."""
    
    table: str
    where_clause: Optional['Expression'] = None


@dataclass
class CreateTableStatement:
    """Class representing a CREATE TABLE statement in the AST."""
    
    table: str
    columns: Dict[str, str]  # column_name -> data_type


@dataclass
class DropTableStatement:
    """Class representing a DROP TABLE statement in the AST."""
    
    table: str


@dataclass
class BinaryExpression:
    """Class representing a binary expression in the AST."""
    
    left: Union['Expression', str]
    operator: str
    right: Union['Expression', Any]


@dataclass
class Literal:
    """Class representing a literal value in the AST."""
    
    value: Any
    type: str  # 'string', 'number', etc.


# Type alias for all possible expressions
Expression = Union[BinaryExpression, Literal, str]

# Type alias for all possible statements
Statement = Union[
    SelectStatement,
    InsertStatement,
    UpdateStatement,
    DeleteStatement,
    CreateTableStatement,
    DropTableStatement,
]


class Parser:
    """SQL Parser class for parsing tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        """Initialize the parser with a list of tokens.
        
        Args:
            tokens: A list of Token objects from the lexer.
        """
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Statement:
        """Parse the tokens into an AST.
        
        Returns:
            An AST representing the SQL statement.
            
        Raises:
            ParseError: If the SQL statement is invalid.
        """
        # Check the first token to determine the type of statement
        token = self.peek()
        
        if token.type == TokenType.SELECT:
            return self.parse_select()
        elif token.type == TokenType.INSERT:
            return self.parse_insert()
        elif token.type == TokenType.UPDATE:
            return self.parse_update()
        elif token.type == TokenType.DELETE:
            return self.parse_delete()
        elif token.type == TokenType.CREATE:
            return self.parse_create_table()
        elif token.type == TokenType.DROP:
            return self.parse_drop_table()
        else:
            raise ParseError(token, f"Unexpected token: {token.value}")
    
    def peek(self) -> Token:
        """Return the current token without consuming it."""
        return self.tokens[self.current]
    
    def advance(self) -> Token:
        """Consume the current token and return it."""
        token = self.peek()
        self.current += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        """Check if the current token matches any of the given types.
        
        If it matches, consume the token and return True.
        Otherwise, return False without consuming the token.
        """
        if self.peek().type in types:
            self.advance()
            return True
        return False
    
    def expect(self, *types: TokenType) -> Token:
        """Expect the current token to be of one of the given types.
        
        If it matches, consume the token and return it.
        Otherwise, raise a ParseError.
        """
        token = self.peek()
        if token.type in types:
            return self.advance()
        
        expected = " or ".join(str(t) for t in types)
        raise ParseError(token, f"Expected {expected}, got {token.type}")
    
    def parse_select(self) -> SelectStatement:
        """Parse a SELECT statement."""
        # Consume SELECT keyword
        self.expect(TokenType.SELECT)
        
        # Parse column list
        columns = self.parse_column_list()
        
        # Expect FROM keyword
        self.expect(TokenType.FROM)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Parse optional WHERE clause
        where_clause = None
        if self.match(TokenType.WHERE):
            where_clause = self.parse_expression()
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return SelectStatement(columns=columns, table=table, where_clause=where_clause)
    
    def parse_column_list(self) -> List[str]:
        """Parse a comma-separated list of column names."""
        columns = []
        
        # Handle * for all columns
        if self.match(TokenType.MULTIPLY):
            return ["*"]
        
        # Parse first column
        column_token = self.expect(TokenType.IDENTIFIER)
        columns.append(column_token.value)
        
        # Parse additional columns
        while self.match(TokenType.COMMA):
            column_token = self.expect(TokenType.IDENTIFIER)
            columns.append(column_token.value)
        
        return columns
    
    def parse_expression(self) -> Expression:
        """Parse an expression (e.g., in a WHERE clause)."""
        left = self.parse_primary()
        
        # Check for binary operators
        if self.peek().type in (
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.GREATER, TokenType.LESS,
            TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
            TokenType.AND, TokenType.OR,
        ):
            operator = self.advance().value
            right = self.parse_expression()
            return BinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def parse_primary(self) -> Union[Expression, str, Literal]:
        """Parse a primary expression (identifier, literal, or parenthesized expression)."""
        token = self.peek()
        
        if token.type == TokenType.IDENTIFIER:
            return self.advance().value
        elif token.type == TokenType.STRING:
            value = self.advance().value
            # Remove quotes
            return Literal(value=value[1:-1], type="string")
        elif token.type == TokenType.NUMBER:
            value = self.advance().value
            # Convert to appropriate numeric type
            if "." in value:
                return Literal(value=float(value), type="float")
            else:
                return Literal(value=int(value), type="integer")
        elif token.type == TokenType.LEFT_PAREN:
            self.advance()  # Consume '('
            expr = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN)  # Expect ')'
            return expr
        else:
            raise ParseError(token, f"Unexpected token in expression: {token.value}")
    
    def parse_insert(self) -> InsertStatement:
        """Parse an INSERT statement."""
        # Consume INSERT INTO keywords
        self.expect(TokenType.INSERT)
        self.expect(TokenType.INTO)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Parse optional column list
        columns = []
        if self.match(TokenType.LEFT_PAREN):
            columns = self.parse_column_list()
            self.expect(TokenType.RIGHT_PAREN)
        
        # Parse VALUES keyword and value list
        self.expect(TokenType.VALUES)
        self.expect(TokenType.LEFT_PAREN)
        
        values = []
        # Parse first value
        values.append(self.parse_value())
        
        # Parse additional values
        while self.match(TokenType.COMMA):
            values.append(self.parse_value())
        
        self.expect(TokenType.RIGHT_PAREN)
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return InsertStatement(table=table, columns=columns, values=values)
    
    def parse_value(self) -> Any:
        """Parse a value in an INSERT statement."""
        token = self.peek()
        
        if token.type == TokenType.STRING:
            value = self.advance().value
            # Remove quotes
            return value[1:-1]
        elif token.type == TokenType.NUMBER:
            value = self.advance().value
            # Convert to appropriate numeric type
            if "." in value:
                return float(value)
            else:
                return int(value)
        else:
            raise ParseError(token, f"Expected string or number, got {token.type}")
    
    def parse_update(self) -> UpdateStatement:
        """Parse an UPDATE statement."""
        # Consume UPDATE keyword
        self.expect(TokenType.UPDATE)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Parse SET keyword and assignments
        self.expect(TokenType.SET)
        
        assignments = {}
        # Parse first assignment
        column, value = self.parse_assignment()
        assignments[column] = value
        
        # Parse additional assignments
        while self.match(TokenType.COMMA):
            column, value = self.parse_assignment()
            assignments[column] = value
        
        # Parse optional WHERE clause
        where_clause = None
        if self.match(TokenType.WHERE):
            where_clause = self.parse_expression()
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return UpdateStatement(table=table, assignments=assignments, where_clause=where_clause)
    
    def parse_assignment(self) -> tuple:
        """Parse an assignment in an UPDATE statement."""
        # Parse column name
        column_token = self.expect(TokenType.IDENTIFIER)
        column = column_token.value
        
        # Parse equals sign
        self.expect(TokenType.EQUAL)
        
        # Parse value
        value = self.parse_value()
        
        return column, value
    
    def parse_delete(self) -> DeleteStatement:
        """Parse a DELETE statement."""
        # Consume DELETE FROM keywords
        self.expect(TokenType.DELETE)
        self.expect(TokenType.FROM)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Parse optional WHERE clause
        where_clause = None
        if self.match(TokenType.WHERE):
            where_clause = self.parse_expression()
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return DeleteStatement(table=table, where_clause=where_clause)
    
    def parse_create_table(self) -> CreateTableStatement:
        """Parse a CREATE TABLE statement."""
        # Consume CREATE TABLE keywords
        self.expect(TokenType.CREATE)
        self.expect(TokenType.TABLE)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Parse column definitions
        self.expect(TokenType.LEFT_PAREN)
        
        columns = {}
        # Parse first column definition
        column, data_type = self.parse_column_definition()
        columns[column] = data_type
        
        # Parse additional column definitions
        while self.match(TokenType.COMMA):
            column, data_type = self.parse_column_definition()
            columns[column] = data_type
        
        self.expect(TokenType.RIGHT_PAREN)
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return CreateTableStatement(table=table, columns=columns)
    
    def parse_column_definition(self) -> tuple:
        """Parse a column definition in a CREATE TABLE statement."""
        # Parse column name
        column_token = self.expect(TokenType.IDENTIFIER)
        column = column_token.value
        
        # Parse data type
        data_type_token = self.expect(TokenType.IDENTIFIER)
        data_type = data_type_token.value
        
        return column, data_type
    
    def parse_drop_table(self) -> DropTableStatement:
        """Parse a DROP TABLE statement."""
        # Consume DROP TABLE keywords
        self.expect(TokenType.DROP)
        self.expect(TokenType.TABLE)
        
        # Parse table name
        table_token = self.expect(TokenType.IDENTIFIER)
        table = table_token.value
        
        # Expect semicolon (optional)
        self.match(TokenType.SEMICOLON)
        
        return DropTableStatement(table=table)
