"""Command-line interface for the SQL compiler."""

import argparse
import sys
import json
from pathlib import Path

from .lexer import Lexer
from .parser import Parser
from .analyzer import Analyzer, Database
from .executor import Executor


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="SQL Compiler")
    
    # Add arguments
    parser.add_argument("file", nargs="?", help="SQL file to compile")
    parser.add_argument("--query", "-q", help="SQL query to compile")
    parser.add_argument("--output", "-o", help="Output file for the result")
    parser.add_argument("--db", "-d", help="Database file to use")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a file or query is provided
    if not args.file and not args.query:
        parser.print_help()
        sys.exit(1)
    
    # Get the SQL query
    sql = ""
    if args.file:
        try:
            with open(args.file, "r") as f:
                sql = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sql = args.query
    
    # Create a database
    database = Database()
    
    # Load database from file if provided
    if args.db and Path(args.db).exists():
        try:
            with open(args.db, "r") as f:
                db_json = f.read()
            
            executor = Executor(database)
            executor.from_json(db_json)
            
            if args.verbose:
                print(f"Loaded database from {args.db}")
        except Exception as e:
            print(f"Error loading database: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        executor = Executor(database)
    
    try:
        # Tokenize the SQL query
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        
        if args.verbose:
            print("Tokens:")
            for token in tokens:
                print(f"  {token}")
        
        # Parse the tokens
        parser = Parser(tokens)
        statement = parser.parse()
        
        if args.verbose:
            print(f"Statement: {statement}")
        
        # Analyze the statement
        analyzer = Analyzer(database)
        analyzer.analyze(statement)
        
        if args.verbose:
            print("Analysis: OK")
        
        # Execute the statement
        result = executor.execute(statement)
        
        # Print the result
        if args.output:
            try:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                
                if args.verbose:
                    print(f"Result written to {args.output}")
            except Exception as e:
                print(f"Error writing result: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(json.dumps(result, indent=2))
        
        # Save the database if a file is provided
        if args.db:
            try:
                with open(args.db, "w") as f:
                    f.write(executor.to_json())
                
                if args.verbose:
                    print(f"Database saved to {args.db}")
            except Exception as e:
                print(f"Error saving database: {e}", file=sys.stderr)
                sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
