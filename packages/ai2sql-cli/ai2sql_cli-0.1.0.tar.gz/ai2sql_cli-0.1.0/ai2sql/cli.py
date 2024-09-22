import argparse
import json
import os
from .core import AI2SQL
from .db_manager import DatabaseManager

CONFIG_FILE = os.path.expanduser("~/.ai2sql_config.json")

def main():
    parser = argparse.ArgumentParser(description="AI2SQL CLI")
    parser.add_argument("--username", help="AI2SQL username")
    parser.add_argument("--password", help="AI2SQL password")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate SQL command
    generate_parser = subparsers.add_parser("generate", help="Generate SQL from natural language")
    generate_parser.add_argument("prompt", help="Natural language description of the SQL query")
    generate_parser.add_argument("--dialect", default="mysql", choices=["mysql", "postgresql", "sqlite"], help="SQL dialect")
    generate_parser.add_argument("--connection", help="Name of the database connection to use")
    generate_parser.add_argument("--run", action="store_true", help="Execute the generated SQL query")

    # Execute SQL command
    execute_parser = subparsers.add_parser("execute", help="Execute SQL on connected database")
    execute_parser.add_argument("sql", help="SQL query to execute")
    execute_parser.add_argument("--connection", required=True, help="Name of the database connection")

    # Connection management commands
    conn_parser = subparsers.add_parser("connection", help="Manage database connections")
    conn_subparsers = conn_parser.add_subparsers(dest="conn_command", required=True)

    add_conn_parser = conn_subparsers.add_parser("add", help="Add a new database connection")
    add_conn_parser.add_argument("--name", required=True, help="Name of the connection")
    add_conn_parser.add_argument("--dialect", required=True, choices=["mysql", "postgresql", "sqlite"], help="Database dialect")
    add_conn_parser.add_argument("--connection-string", required=True, help="Database connection string")

    list_conn_parser = conn_subparsers.add_parser("list", help="List all saved connections")

    remove_conn_parser = conn_subparsers.add_parser("remove", help="Remove a saved connection")
    remove_conn_parser.add_argument("--name", required=True, help="Name of the connection to remove")

    args = parser.parse_args()

    if args.command == "generate":
        generate_sql(args)
    elif args.command == "execute":
        execute_sql(args)
    elif args.command == "connection":
        if args.conn_command == "add":
            add_connection(args)
        elif args.conn_command == "list":
            list_connections(args)
        elif args.conn_command == "remove":
            remove_connection(args)

def generate_sql(args):
    ai2sql = AI2SQL(args.username, args.password)
    sql = ai2sql.generate_sql(args.prompt, args.dialect)
    print(f"Generated SQL:\n{sql}")
    
    if args.run:
        if not args.connection:
            print("Error: --connection is required when using --run")
            return
        config = load_config()
        if args.connection not in config["connections"]:
            print(f"Connection '{args.connection}' not found.")
            return
        conn_details = config["connections"][args.connection]
        db_manager = DatabaseManager(conn_details["dialect"], conn_details["connection_string"])
        try:
            result = db_manager.execute_query(sql)
            print("Query Result:")
            for row in result:
                print(row)
        except Exception as e:
            print(f"Error executing query: {str(e)}")

def execute_sql(args):
    config = load_config()
    if args.connection not in config["connections"]:
        print(f"Connection '{args.connection}' not found.")
        return
    conn_details = config["connections"][args.connection]
    db_manager = DatabaseManager(conn_details["dialect"], conn_details["connection_string"])
    result = db_manager.execute_query(args.sql)
    print("Query Result:")
    print(result)

def add_connection(args):
    config = load_config()
    config["connections"][args.name] = {
        "dialect": args.dialect,
        "connection_string": args.connection_string
    }
    save_config(config)
    print(f"Connection '{args.name}' added successfully.")

def list_connections(args):
    config = load_config()
    if not config["connections"]:
        print("No connections found.")
    else:
        for name, details in config["connections"].items():
            print(f"Name: {name}, Dialect: {details['dialect']}")

def remove_connection(args):
    config = load_config()
    if args.name in config["connections"]:
        del config["connections"][args.name]
        save_config(config)
        print(f"Connection '{args.name}' removed successfully.")
    else:
        print(f"Connection '{args.name}' not found.")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"connections": {}}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
