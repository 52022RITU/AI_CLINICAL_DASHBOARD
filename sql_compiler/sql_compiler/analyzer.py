"""SQL Semantic Analyzer module for validating SQL queries."""

from typing import Dict, List, Set, Any, Optional

from .parser import (
    Statement,
    SelectStatement,
    InsertStatement,
    UpdateStatement,
    DeleteStatement,
    CreateTableStatement,
    DropTableStatement,
    BinaryExpression,
    Literal,
    Expression,
)


class SemanticError(Exception):
    """Exception raised for semantic errors during analysis."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Semantic error: {message}")


class Database:
    """Simple in-memory database schema representation."""
    
    def __init__(self):
        """Initialize an empty database schema."""
        self.tables: Dict[str, Dict[str, str]] = {}  # table_name -> {column_name -> data_type}
    
    def create_table(self, table: str, columns: Dict[str, str]):
        """Create a new table in the database.
        
        Args:
            table: The name of the table to create.
            columns: A dictionary mapping column names to data types.
            
        Raises:
            SemanticError: If the table already exists.
        """
        if table in self.tables:
            raise SemanticError(f"Table '{table}' already exists")
        
        self.tables[table] = columns
    
    def drop_table(self, table: str):
        """Drop a table from the database.
        
        Args:
            table: The name of the table to drop.
            
        Raises:
            SemanticError: If the table does not exist.
        """
        if table not in self.tables:
            raise SemanticError(f"Table '{table}' does not exist")
        
        del self.tables[table]
    
    def table_exists(self, table: str) -> bool:
        """Check if a table exists in the database.
        
        Args:
            table: The name of the table to check.
            
        Returns:
            True if the table exists, False otherwise.
        """
        return table in self.tables
    
    def get_columns(self, table: str) -> Dict[str, str]:
        """Get the columns of a table.
        
        Args:
            table: The name of the table.
            
        Returns:
            A dictionary mapping column names to data types.
            
        Raises:
            SemanticError: If the table does not exist.
        """
        if not self.table_exists(table):
            raise SemanticError(f"Table '{table}' does not exist")
        
        return self.tables[table]
    
    def column_exists(self, table: str, column: str) -> bool:
        """Check if a column exists in a table.
        
        Args:
            table: The name of the table.
            column: The name of the column.
            
        Returns:
            True if the column exists, False otherwise.
            
        Raises:
            SemanticError: If the table does not exist.
        """
        columns = self.get_columns(table)
        return column in columns or column == "*"


class Analyzer:
    """SQL Semantic Analyzer class for validating SQL queries."""
    
    def __init__(self, database: Database):
        """Initialize the analyzer with a database schema.
        
        Args:
            database: A Database object representing the schema.
        """
        self.database = database
    
    def analyze(self, statement: Statement):
        """Analyze a SQL statement for semantic errors.
        
        Args:
            statement: The SQL statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        if isinstance(statement, SelectStatement):
            self.analyze_select(statement)
        elif isinstance(statement, InsertStatement):
            self.analyze_insert(statement)
        elif isinstance(statement, UpdateStatement):
            self.analyze_update(statement)
        elif isinstance(statement, DeleteStatement):
            self.analyze_delete(statement)
        elif isinstance(statement, CreateTableStatement):
            self.analyze_create_table(statement)
        elif isinstance(statement, DropTableStatement):
            self.analyze_drop_table(statement)
        else:
            raise SemanticError(f"Unknown statement type: {type(statement)}")
    
    def analyze_select(self, statement: SelectStatement):
        """Analyze a SELECT statement for semantic errors.
        
        Args:
            statement: The SELECT statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table exists
        if not self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' does not exist")
        
        # Check if all columns exist
        for column in statement.columns:
            if not self.database.column_exists(statement.table, column):
                raise SemanticError(f"Column '{column}' does not exist in table '{statement.table}'")
        
        # Check the WHERE clause if it exists
        if statement.where_clause:
            self.analyze_expression(statement.where_clause, statement.table)
    
    def analyze_insert(self, statement: InsertStatement):
        """Analyze an INSERT statement for semantic errors.
        
        Args:
            statement: The INSERT statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table exists
        if not self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' does not exist")
        
        # Get the columns of the table
        table_columns = self.database.get_columns(statement.table)
        
        # If no columns are specified, use all columns
        if not statement.columns:
            statement.columns = list(table_columns.keys())
        
        # Check if all specified columns exist
        for column in statement.columns:
            if not self.database.column_exists(statement.table, column):
                raise SemanticError(f"Column '{column}' does not exist in table '{statement.table}'")
        
        # Check if the number of values matches the number of columns
        if len(statement.columns) != len(statement.values):
            raise SemanticError(
                f"Number of values ({len(statement.values)}) does not match "
                f"number of columns ({len(statement.columns)})"
            )
    
    def analyze_update(self, statement: UpdateStatement):
        """Analyze an UPDATE statement for semantic errors.
        
        Args:
            statement: The UPDATE statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table exists
        if not self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' does not exist")
        
        # Check if all columns in the assignments exist
        for column in statement.assignments:
            if not self.database.column_exists(statement.table, column):
                raise SemanticError(f"Column '{column}' does not exist in table '{statement.table}'")
        
        # Check the WHERE clause if it exists
        if statement.where_clause:
            self.analyze_expression(statement.where_clause, statement.table)
    
    def analyze_delete(self, statement: DeleteStatement):
        """Analyze a DELETE statement for semantic errors.
        
        Args:
            statement: The DELETE statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table exists
        if not self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' does not exist")
        
        # Check the WHERE clause if it exists
        if statement.where_clause:
            self.analyze_expression(statement.where_clause, statement.table)
    
    def analyze_create_table(self, statement: CreateTableStatement):
        """Analyze a CREATE TABLE statement for semantic errors.
        
        Args:
            statement: The CREATE TABLE statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table already exists
        if self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' already exists")
        
        # Check for duplicate column names
        column_names = set()
        for column in statement.columns:
            if column in column_names:
                raise SemanticError(f"Duplicate column name: '{column}'")
            column_names.add(column)
    
    def analyze_drop_table(self, statement: DropTableStatement):
        """Analyze a DROP TABLE statement for semantic errors.
        
        Args:
            statement: The DROP TABLE statement to analyze.
            
        Raises:
            SemanticError: If the statement has semantic errors.
        """
        # Check if the table exists
        if not self.database.table_exists(statement.table):
            raise SemanticError(f"Table '{statement.table}' does not exist")
    
    def analyze_expression(self, expression: Expression, table: str):
        """Analyze an expression for semantic errors.
        
        Args:
            expression: The expression to analyze.
            table: The name of the table the expression is used with.
            
        Raises:
            SemanticError: If the expression has semantic errors.
        """
        if isinstance(expression, BinaryExpression):
            # Analyze the left and right sides of the expression
            if isinstance(expression.left, str):
                # If the left side is a column name, check if it exists
                if not self.database.column_exists(table, expression.left):
                    raise SemanticError(f"Column '{expression.left}' does not exist in table '{table}'")
            elif isinstance(expression.left, (BinaryExpression, Literal)):
                # If the left side is an expression, analyze it recursively
                self.analyze_expression(expression.left, table)
            
            if isinstance(expression.right, str):
                # If the right side is a column name, check if it exists
                if not self.database.column_exists(table, expression.right):
                    raise SemanticError(f"Column '{expression.right}' does not exist in table '{table}'")
            elif isinstance(expression.right, (BinaryExpression, Literal)):
                # If the right side is an expression, analyze it recursively
                self.analyze_expression(expression.right, table)
        elif isinstance(expression, str):
            # If the expression is a column name, check if it exists
            if not self.database.column_exists(table, expression):
                raise SemanticError(f"Column '{expression}' does not exist in table '{table}'")
        # Literals don't need to be analyzed
