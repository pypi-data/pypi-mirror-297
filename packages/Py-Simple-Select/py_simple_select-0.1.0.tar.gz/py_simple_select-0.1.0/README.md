<h1 align = "center">
	<img alt = "Py_Simple_Select" src = "img/logo.png"/>
	<br/>
	Py_Simple_Select
</h1>
<br/>

**Py_Simple_Select** is a lightweight Python library designed to simplify interactions with SQLite databases. It provides a minimalistic ORM (Object-Relational Mapping) system that enables advanced querying and flexible data selection. This library is tailored to offer an easy-to-use interface while abstracting away database internals, such as primary keys and foreign keys, when they are not needed by the user.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
	- [Create and Connect to a Database](#create-and-connect-to-a-database)
	- [Insert Data into Tables](#insert-data-into-tables)
	- [Perform Advanced Queries](#perform-advanced-queries)
- [Examples](#examples)
- [License](#license)
- [Documentation](#documentation)

---

## Features

- **Lightweight ORM**: Interact with SQLite databases using Python objects, making database operations more intuitive and Pythonic.
- **Advanced Querying**: Perform advanced selections that allow grouping results based on foreign keys, offering a powerful way to organize related data.
- **Object Simplification**: Automatically filters out primary and foreign keys, returning only the relevant attributes in your objects.
- **Foreign Key Support**: Full support for foreign keys, including automatic detection and grouping of results based on these relationships.
- **Ease of Use**: Designed for simplicity, allowing users to focus on the data they care about without worrying about the underlying database structure.

---

## Installation

You can install **Py_Simple_Select** directly from PyPI using `pip`:

```bash
pip install Py_Simple_Select
```

---

## Usage

### Create and Connect to a Database

First, let's create a database manager instance and set up our tables, including those with foreign keys:

```python

from py_simple_select import Database_Manager

# Create a database manager instance
db : Database_Manager = Database_Manager("my_database")

# Create a table without foreign keys
db.create_table ("user", name = str, email = str)

# Create a table with a foreign key referencing the "users" table
db.create_table ("order", amount = float, user_id = int)

```

---

### Insert Data into Tables

Next, we can insert data into our tables. The ORM makes it simple to add entries:

```python

# Get the "users" table class
User : type = db.get_table_class ("user")
Order : type = db.get_table_class ("order")

# Insert records into the "users" table and records into the "orders" table with a reference to "users"
db.insert (
	User (name = "Alice", email = "alice@example.com"),
	User (name = "Bob", email = "bob@example.com"),
	Order (amount = 250.75, user_id = 1),
	Order (amount = 125.50, user_id = 2)
)

```

---

### Perform Advanced Queries

You can perform advanced queries that group results based on foreign keys:

```python

# Get the "orders" table class
grouped_orders = db.advanced_select ("orders")
for group in grouped_orders:
    print (group)

```

This will return a nested tuple structure where the orders are grouped by the values of their foreign keys (e.g., user_id).

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Documentation

For more detailed documentation, including API references and advanced usage, please visit the official documentation.

---

Thanks you for using Py_Simple_Select! I hope you find it useful.
