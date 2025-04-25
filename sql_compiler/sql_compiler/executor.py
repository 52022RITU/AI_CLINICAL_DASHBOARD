"""SQL Executor module for executing SQL queries."""

from typing import Dict, List, Any, Optional, Union
import json

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
from .analyzer import Database


class ExecutionError(Exception):
    """Exception raised for errors during execution."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Execution error: {message}")


class Table:
    """Class representing a table in the in-memory database."""
    
    def __init__(self, name: str, columns: Dict[str, str]):
        """Initialize a table with a name and column definitions.
        
        Args:
            name: The name of the table.
            columns: A dictionary mapping column names to data types.
        """
        self.name = name
        self.columns = columns
        self.rows: List[Dict[str, Any]] = []
    
    def insert(self, row: Dict[str, Any]):
        """Insert a row into the table.
        
        Args:
            row: A dictionary mapping column names to values.
            
        Raises:
            ExecutionError: If the row has invalid columns or values.
        """
        # Check if all columns exist
        for column in row:
            if column not in self.columns:
                raise ExecutionError(f"Column '{column}' does not exist in table '{self.name}'")
        
        # Add the row
        self.rows.append(row)
    
    def select(self, columns: List[str], where_clause: Optional[Expression] = None) -> List[Dict[str, Any]]:
        """Select rows from the table.
        
        Args:
            columns: A list of column names to select.
            where_clause: An optional WHERE clause to filter rows.
            
        Returns:
            A list of dictionaries representing the selected rows.
            
        Raises:
            ExecutionError: If a column does not exist.
        """
        # Check if all columns exist
        for column in columns:
            if column != "*" and column not in self.columns:
                raise ExecutionError(f"Column '{column}' does not exist in table '{self.name}'")
        
        # Filter rows based on the WHERE clause
        filtered_rows = []
        for row in self.rows:
            if where_clause is None or self.evaluate_expression(where_clause, row):
                filtered_rows.append(row)
        
        # Select only the requested columns
        if "*" in columns:
            return filtered_rows
        else:
            result = []
            for row in filtered_rows:
                selected_row = {}
                for column in columns:
                    selected_row[column] = row.get(column)
                result.append(selected_row)
            return result
    
    def update(self, assignments: Dict[str, Any], where_clause: Optional[Expression] = None) -> int:
        """Update rows in the table.
        
        Args:
            assignments: A dictionary mapping column names to new values.
            where_clause: An optional WHERE clause to filter rows.
            
        Returns:
            The number of rows updated.
            
        Raises:
            ExecutionError: If a column does not exist.
        """
        # Check if all columns exist
        for column in assignments:
            if column not in self.columns:
                raise ExecutionError(f"Column '{column}' does not exist in table '{self.name}'")
        
        # Update rows based on the WHERE clause
        count = 0
        for row in self.rows:
            if where_clause is None or self.evaluate_expression(where_clause, row):
                for column, value in assignments.items():
                    row[column] = value
                count += 1
        
        return count
    
    def delete(self, where_clause: Optional[Expression] = None) -> int:
        """Delete rows from the table.
        
        Args:
            where_clause: An optional WHERE clause to filter rows.
            
        Returns:
            The number of rows deleted.
        """
        # Delete rows based on the WHERE clause
        original_count = len(self.rows)
        if where_clause is None:
            self.rows = []
            return original_count
        else:
            self.rows = [row for row in self.rows if not self.evaluate_expression(where_clause, row)]
            return original_count - len(self.rows)
    
    def evaluate_expression(self, expression: Expression, row: Dict[str, Any]) -> bool:
        """Evaluate an expression against a row.
        
        Args:
            expression: The expression to evaluate.
            row: The row to evaluate the expression against.
            
        Returns:
            The result of the expression.
            
        Raises:
            ExecutionError: If the expression is invalid.
        """
        if isinstance(expression, BinaryExpression):
            # Evaluate the left and right sides of the expression
            left_value = self.evaluate_operand(expression.left, row)
            right_value = self.evaluate_operand(expression.right, row)
            
            # Evaluate the operator
            if expression.operator.upper() == "=":
                return left_value == right_value
            elif expression.operator.upper() in ("!=", "<>"):
                return left_value != right_value
            elif expression.operator.upper() == ">":
                return left_value > right_value
            elif expression.operator.upper() == "<":
                return left_value < right_value
            elif expression.operator.upper() == ">=":
                return left_value >= right_value
            elif expression.operator.upper() == "<=":
                return left_value <= right_value
            elif expression.operator.upper() == "AND":
                return left_value and right_value
            elif expression.operator.upper() == "OR":
                return left_value or right_value
            else:
                raise ExecutionError(f"Unknown operator: {expression.operator}")
        elif isinstance(expression, str):
            # If the expression is a column name, return its value
            if expression not in row:
                raise ExecutionError(f"Column '{expression}' does not exist in row")
            return row[expression]
        elif isinstance(expression, Literal):
            # If the expression is a literal, return its value
            return expression.value
        else:
            raise ExecutionError(f"Unknown expression type: {type(expression)}")
    
    def evaluate_operand(self, operand: Union[Expression, str, Any], row: Dict[str, Any]) -> Any:
        """Evaluate an operand in an expression.
        
        Args:
            operand: The operand to evaluate.
            row: The row to evaluate the operand against.
            
        Returns:
            The value of the operand.
            
        Raises:
            ExecutionError: If the operand is invalid.
        """
        if isinstance(operand, (BinaryExpression, Literal)):
            return self.evaluate_expression(operand, row)
        elif isinstance(operand, str):
            # If the operand is a column name, return its value
            if operand not in row:
                raise ExecutionError(f"Column '{operand}' does not exist in row")
            return row[operand]
        else:
            # If the operand is a literal value, return it as is
            return operand


class Executor:
    """SQL Executor class for executing SQL queries."""
    
    def __init__(self, database: Database):
        """Initialize the executor with a database schema.
        
        Args:
            database: A Database object representing the schema.
        """
        self.database = database
        self.tables: Dict[str, Table] = {}
    
    def execute(self, statement: Statement) -> Dict[str, Any]:
        """Execute a SQL statement.
        
        Args:
            statement: The SQL statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        if isinstance(statement, SelectStatement):
            return self.execute_select(statement)
        elif isinstance(statement, InsertStatement):
            return self.execute_insert(statement)
        elif isinstance(statement, UpdateStatement):
            return self.execute_update(statement)
        elif isinstance(statement, DeleteStatement):
            return self.execute_delete(statement)
        elif isinstance(statement, CreateTableStatement):
            return self.execute_create_table(statement)
        elif isinstance(statement, DropTableStatement):
            return self.execute_drop_table(statement)
        else:
            raise ExecutionError(f"Unknown statement type: {type(statement)}")
    
    def execute_select(self, statement: SelectStatement) -> Dict[str, Any]:
        """Execute a SELECT statement.
        
        Args:
            statement: The SELECT statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table exists
        if statement.table not in self.tables:
            raise ExecutionError(f"Table '{statement.table}' does not exist")
        
        # Select rows from the table
        table = self.tables[statement.table]
        rows = table.select(statement.columns, statement.where_clause)
        
        return {
            "type": "select",
            "rows": rows,
            "count": len(rows),
        }
    
    def execute_insert(self, statement: InsertStatement) -> Dict[str, Any]:
        """Execute an INSERT statement.
        
        Args:
            statement: The INSERT statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table exists
        if statement.table not in self.tables:
            raise ExecutionError(f"Table '{statement.table}' does not exist")
        
        # Get the table
        table = self.tables[statement.table]
        
        # If no columns are specified, use all columns
        columns = statement.columns
        if not columns:
            columns = list(table.columns.keys())
        
        # Create a row from the values
        row = {}
        for i, column in enumerate(columns):
            if i < len(statement.values):
                row[column] = statement.values[i]
        
        # Insert the row
        table.insert(row)
        
        return {
            "type": "insert",
            "count": 1,
        }
    
    def execute_update(self, statement: UpdateStatement) -> Dict[str, Any]:
        """Execute an UPDATE statement.
        
        Args:
            statement: The UPDATE statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table exists
        if statement.table not in self.tables:
            raise ExecutionError(f"Table '{statement.table}' does not exist")
        
        # Update rows in the table
        table = self.tables[statement.table]
        count = table.update(statement.assignments, statement.where_clause)
        
        return {
            "type": "update",
            "count": count,
        }
    
    def execute_delete(self, statement: DeleteStatement) -> Dict[str, Any]:
        """Execute a DELETE statement.
        
        Args:
            statement: The DELETE statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table exists
        if statement.table not in self.tables:
            raise ExecutionError(f"Table '{statement.table}' does not exist")
        
        # Delete rows from the table
        table = self.tables[statement.table]
        count = table.delete(statement.where_clause)
        
        return {
            "type": "delete",
            "count": count,
        }
    
    def execute_create_table(self, statement: CreateTableStatement) -> Dict[str, Any]:
        """Execute a CREATE TABLE statement.
        
        Args:
            statement: The CREATE TABLE statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table already exists
        if statement.table in self.tables:
            raise ExecutionError(f"Table '{statement.table}' already exists")
        
        # Create the table in the database schema
        self.database.create_table(statement.table, statement.columns)
        
        # Create the table in memory
        self.tables[statement.table] = Table(statement.table, statement.columns)
        
        return {
            "type": "create_table",
            "table": statement.table,
        }
    
    def execute_drop_table(self, statement: DropTableStatement) -> Dict[str, Any]:
        """Execute a DROP TABLE statement.
        
        Args:
            statement: The DROP TABLE statement to execute.
            
        Returns:
            A dictionary with the result of the execution.
            
        Raises:
            ExecutionError: If the statement cannot be executed.
        """
        # Check if the table exists
        if statement.table not in self.tables:
            raise ExecutionError(f"Table '{statement.table}' does not exist")
        
        # Drop the table from the database schema
        self.database.drop_table(statement.table)
        
        # Drop the table from memory
        del self.tables[statement.table]
        
        return {
            "type": "drop_table",
            "table": statement.table,
        }
    
    def to_json(self) -> str:
        """Convert the database to a JSON string.
        
        Returns:
            A JSON string representing the database.
        """
        data = {}
        for table_name, table in self.tables.items():
            data[table_name] = {
                "columns": table.columns,
                "rows": table.rows,
            }
        
        return json.dumps(data, indent=2)
    
    def from_json(self, json_str: str):
        """Load the database from a JSON string.
        
        Args:
            json_str: A JSON string representing the database.
            
        Raises:
            ExecutionError: If the JSON string is invalid.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ExecutionError(f"Invalid JSON: {e}")
        
        # Clear existing tables
        self.tables = {}
        
        # Create tables from the JSON data
        for table_name, table_data in data.items():
            columns = table_data.get("columns", {})
            rows = table_data.get("rows", [])
            
            # Create the table in the database schema
            self.database.create_table(table_name, columns)
            
            # Create the table in memory
            table = Table(table_name, columns)
            self.tables[table_name] = table
            
            # Insert rows
            for row in rows:
                table.insert(row)
