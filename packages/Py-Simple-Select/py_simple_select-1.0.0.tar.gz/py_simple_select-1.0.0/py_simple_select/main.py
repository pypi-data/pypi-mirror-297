import sqlite3
from json import loads, dumps, JSONDecodeError

class Database_Manager ():
	"""
	A class that manages a SQLite database.

	Attributes:
		connection (sqlite3.Connection): The SQLite database connection.
		cursor (sqlite3.Cursor): The SQLite database cursor.
		tables (tuple[str]): The names of all tables in the database.
		table_classes (dict[str, type]): A dictionary that maps each table name
			to its corresponding class.
	"""

	def __init__ (self, name : str) -> None:
		"""
		Initializes the Database_Manager class.

		Args:
			name (str): The name of the database file.
		"""
		self.connection : sqlite3.Connection = sqlite3.connect (f"{name}.db")
		self.connection.row_factory : sqlite3.Row = sqlite3.Row
		self.cursor : sqlite3.Cursor = self.connection.cursor ()

		# Enable foreign key support
		self.execute ("PRAGMA foreign_keys = ON")
		# Get all the table names in the database
		self.execute ("SELECT name FROM sqlite_master WHERE type = 'table'")

		self.tables : tuple[str] = tuple (table["name"] for table in self.fetchall () if (table["name"] != "sqlite_sequence"))

		self.table_classes : dict[str, type] = {}
		for table in self.tables:
			self.add_table_class (table)

	def disconnect (self) -> None:
		"""
		Closes the database connection.
		"""

		self.connection.close ()

	def commit (self) -> None:
		"""
		Commits all the changes made to the database.
		"""

		self.connection.commit ()

	def execute (self, query : str, *args : tuple) -> None:
		"""
		Executes a given SQL query with the given arguments.

		Args:
			query (str): The SQL query to execute.
			*args (tuple): The arguments to pass to the query.
		"""

		self.cursor.execute (f"{query};", args)

	def fetchall (self) -> tuple[dict]:
		"""
		Fetches all the rows from the last executed query.

		Returns:
			tuple[dict]: A tuple containing a dictionary for each row, where the keys are the column names and the values are the column values.
		"""

		return tuple (dict (row) for row in self.cursor.fetchall ())

	def create_table (self, _name : str, foreign_keys : dict[str, str] = {}, **columns: dict[str, type]) -> None:
		"""
		Creates a new table in the database.

		Args:
			_name (str): The name of the table to create.
			**columns (dict[str, type]): The columns of the table, where the keys are the column names and the values are the column types.

		Raises:
			RuntimeError: If the table already exists.
		"""

		if (_name not in self.tables):
			python_type_to_sql : dict[type, str] = { int : "INTEGER", float : "REAL", bool : "INTEGER" }
			self.execute (f"CREATE TABLE {_name} ({_name}_id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join (f"{column} {python_type_to_sql.get (typ, 'TEXT')}" for column, typ in columns.items ())}{' , '  + ', '.join (f"{column} INTEGER REFERENCES {foreign_keys[column]}" for column in foreign_keys) if (foreign_keys) else ''})")
			self.commit ()
			self.add_table_class (_name)
			self.tables += (_name,)

	def drop_tables (self, *names : str) -> None:
		"""
		Drops the given tables from the database.

		Args:
			*names (str): The names of the tables to drop.
		"""

		for name in names:
			if (name in self.tables):
				self.execute (f"DROP TABLE {name}")
				self.commit ()
				del self.table_classes[name]

	def add_table_class (self, name : str) -> None:
		"""
		Adds a new table class to the database manager.

		Args:
			name (str): The name of the table to add a class for.
		"""

		self.execute (f"PRAGMA table_info ({name})")

		class_attrs : dict[str, any] = { column["name"] : None for column in self.fetchall () }

		def init (self, **kwargs : dict[str, any]) -> None:
			"""
			Initializes the table class.

			Args:
				*kwargs (dict[str, any]): The keyword arguments to initialize the class with.
			"""

			for key, value in class_attrs.items ():
				if (key in kwargs):
					setattr (self, key, kwargs[key])

				elif (key != f"{name}_id"):
					raise ValueError (f"Missing required argument '{key}' for {self.__class__}")

		self.table_classes[name] : type = type (name, (object,), { "__init__" : init, "__repr__" : lambda self : f"{self.__class__.__name__} ({', '.join (f'{key} = {value}' for key, value in self.__dict__.items ())})", **class_attrs })

	def get_table_class (self, name : str) -> type:
		"""
		Gets the table class for the given table name.

		Args:
			name (str): The name of the table to get the class for.

		Returns:
			type: The table class for the given table.
		"""

		return self.table_classes[name]

	def get_class_table (self, cls : type) -> str:
		"""
		Gets the table name for the given class.

		Args:
			cls (type): The class to get the table name for.

		Returns:
			str: The table name for the given class.

		Raises:
			ValueError: If the class is not found in the database.
		"""

		if (cls in self.table_classes):
			return cls.__name__

		raise ValueError (f"Class {cls} not found in database")

	def advanced_split (self, text : str, *separators : tuple[str]) -> tuple[str]:
		"""
		Splits a given text into substrings separated by any of the given separators.

		Args:
			text (str): The text to split.
			*separators (tuple[str]): The separators to split by.

		Returns:
			tuple[str]: A tuple of the split substrings.
		"""

		result : list[str] = []
		buffer : str = ""
		i : int = 0
		length : int = len (text)

		while (i < length):
			for separator in separators:
				sep_len : int = len (separator)
				if (i + sep_len <= length and text[i:i + sep_len] == separator):
					if (buffer.strip ()):
						result.append (buffer.strip ())

					result.append (separator)
					buffer : str = ""
					i += sep_len
					break

			else:
				buffer += text[i]
				i += 1

		if (buffer.strip ()):
			result.append (buffer.strip ())

		return tuple (result)

	def separate_condition (self, condition : str) -> tuple[str, str]:
		"""
		Separates a given condition into simple and complex conditions.

		Args:
			condition (str): The condition to separate.

		Returns:
			tuple[str, str]: A tuple containing the simple condition and the complex condition.
		"""

		if (not condition):
			return None, None

		simple_conditions : list[str] = []
		complex_conditions : list[str] = []
		operators : list[str] = []

		for i, fragment in enumerate (self.advanced_split (condition, "and", "or", "AND", "OR")):
			fragment : str = fragment.strip ()

			if (fragment in ["and", "or", "AND", "OR"]):
				operators.append (fragment)

			else:
				if ("[" in fragment or "]" in fragment):
					complex_conditions.append (fragment)

				else:
					simple_conditions.append (fragment)

		simple_condition : str = self.join_conditions(simple_conditions, operators)
		complex_condition : str = self.join_conditions(complex_conditions, operators)

		return simple_condition, complex_condition

	def join_conditions (self, conditions : tuple[str], operators : tuple[str]) -> str:
		"""
		Joins a list of conditions with the given operators.

		Args:
			conditions (tuple[str]): The conditions to join.
			operators (tuple[str]): The operators to use for joining.

		Returns:
			str: The joined condition string.
		"""

		if (not conditions):
			return None

		result : str = conditions[0]
		for i, condition in enumerate (conditions[1:], 1):
			result += f" {operators[i - 1]} {condition}"
		
		return result

	def filter_complex_conditions (self, condition : str, rows : tuple[dict]) -> tuple[dict]:
		"""
		Filters a list of rows based on a complex condition.

		Args:
			condition (str): The condition to filter by.
			rows (tuple[dict]): The rows to filter.

		Returns:
			tuple[dict]: The filtered rows.
		"""

		filtered_rows : list[dict] = []

		for row in rows:
			try:
				if (eval (condition, {}, row)):
					filtered_rows.append (row)

			except Exception as e:
				print (f"Error while evaluating complex condition : {e}")

		return tuple (filtered_rows)

	def parse_condition (self, condition : str) -> tuple[str, tuple[any]]:
		"""
		Parses a condition string into a WHERE clause and parameters.

		Args:
			condition (str): The condition string.

		Returns:
			tuple[str, tuple[any]]: A tuple containing the WHERE clause and the parameters.
		"""

		condition : str = condition.replace ("==", "=")
		params : list[any] = []
		fragments : list[str] = condition.split ()

		for i, fragment in enumerate (fragments):
			if (fragment.startswith("'") or fragment.startswith('"') or fragment.isdigit ()):
				params.append (eval (fragment))
				fragments[i] : str = "?"

		condition : str = " ".join (fragments)

		return condition, tuple (params)

	def serialize_value (self, value : any) -> any:
		"""
		Serialize a value.

		Args:
			value (any): The value to serialize.

		Returns:
			any: The serialized value.
		"""

		return dumps (value) if (isinstance (value, (list, dict, tuple))) else value

	def deserialize_value (self, value : str) -> any:
		"""
		Deserialize a value.

		Args:
			value (str): The value to deserialize.

		Returns:
			any: The deserialized value.
		"""

		try:
			return loads (value)

		except (JSONDecodeError, TypeError):
			return value

	def select (self, name : str, condition : str = None, ordered : str = None) -> tuple[any]:
		"""
		Select rows from a table.

		Args:
			name (str): The table name.
			condition (str): The condition string.
			ordered (str): The column to order by.

		Returns:
			tuple[any]: The selected rows.
		"""

		simple_condition, complex_condition = self.separate_condition (condition)

		if (simple_condition):
			where_clause, condition_params = self.parse_condition (simple_condition)
			query : str = f"SELECT * FROM {name} WHERE {where_clause}"
			params : tuple[any] = tuple (condition_params)

		else:
			query : str = f"SELECT * FROM {name}"
			params : tuple[any] = ()

		if (ordered):
			query += f" ORDER BY {ordered}"

		self.execute (query, *params)

		rows : tuple[dict] = self.fetchall ()
		for row in rows:
			for key, value in row.items ():
				if (isinstance (value, str)):
					row[key] : any = self.deserialize_value (value)

		if (complex_condition):
			rows : tuple[dict] = self.filter_complex_conditions (complex_condition, rows)

		return tuple (self.table_classes[name] (**row) for row in rows)

	def advanced_select (self, name : str, condition : str = None, ordered : str = None) -> tuple:
		"""
		Select rows from a table, taking into account foreign keys.

		Args:
			name (str): The table name.
			condition (str): The condition string.
			ordered (str): The column to order by.

		Returns:
			tuple: The selected rows.
		"""

		simple_condition, complex_condition = self.separate_condition (condition)

		if (simple_condition):
			where_clause, condition_params = self.parse_condition (simple_condition)
			query : str = f"SELECT * FROM {name} WHERE {where_clause}"
			params : tuple[any] = tuple (condition_params)

		else:
			query : str = f"SELECT * FROM {name}"
			params : tuple[any] = ()

		if (ordered):
			query += f" ORDER BY {ordered}"

		self.execute (query, *params)

		rows : tuple[dict] = self.fetchall ()
		for row in rows:
			for key, value in row.items ():
				if (isinstance (value, str)):
					row[key] : any = self.deserialize_value (value)

		if (complex_condition):
			rows : tuple[dict] = self.filter_complex_conditions (complex_condition, rows)

		foreign_keys : list[tuple[str, str]] = [ column for column in rows[0].keys () if (column.endswith ('_id')) and (column != f"{name}_id") ]

		if (not foreign_keys):
			return tuple (self.table_classes[name] (**row) for row in rows)

		def group_by_foreign_key (fk_list : list[tuple[str, str]], current_rows : tuple[dict]) -> tuple:
			"""
			Group the rows by foreign key.

			Args:
				fk_list (list[tuple[str, str]]): The list of foreign keys.
				current_rows (tuple[dict]): The current rows.

			Returns:
				tuple: The grouped rows.
			"""

			if (not fk_list):
				return tuple (self.table_classes[name](**row) for row in current_rows)

			grouped : dict[any, list[dict]] = {}
			for row in current_rows:
				fk_value : any = row[fk_list[0]]
				if (fk_value not in grouped):
					grouped[fk_value] : list[dict] = []

				grouped[fk_value].append (row)

			return tuple (group_by_foreign_key (fk_list[1:], grouped_rows) for grouped_rows in grouped.values ())

		return group_by_foreign_key (foreign_keys, rows)

	def insert (self, *rows : tuple[any]) -> None:
		"""
		Insert rows into a table.

		Args:
			*rows (tuple[any]): The rows to insert.

		"""

		for row in rows:
			if (row.__class__.__name__ in self.tables):
				fields : dict[str, any] = { key : self.serialize_value (value) for key, value in row.__dict__.items () if (not key.startswith ('_') and (key != f"{row.__class__.__name__}_id")) }
				self.execute (f"INSERT INTO {row.__class__.__name__} ({', '.join (fields.keys ())}) VALUES ({', '.join ('?' * len (fields))})", *fields.values ())

			else:
				raise ValueError (f"The row is not an instance of {self.table_classes}.")

		self.commit ()

	def update (self, name : str, condition : str, **fields : dict[str, any]) -> None:
		"""
		Update rows in a table.

		Args:
			name (str): The table name.
			condition (str): The condition string.
			**fields (dict[str, any]): The fields to update.

		"""

		where_clause, condition_params = self.parse_condition (condition)
		self.execute (f"UPDATE {name} SET {', '.join ([ f'{column} = ?' for column in fields.keys () ])} WHERE {where_clause}", *(tuple (fields.values ()) + condition_params))
		self.commit ()

	def delete (self, name : str, condition : str) -> None:
		"""
		Delete rows from a table.

		Args:
			name (str): The table name.
			condition (str): The condition string.

		"""

		where_clause, condition_params = self.parse_condition (condition)
		self.execute (f"DELETE FROM {name} WHERE {where_clause}", *condition_params)
		self.commit ()

	def database_to_json (self) -> dict[str, list[dict]]:
		"""
		Convert the database to a JSON object.

		Returns:
			dict[str, list[dict]]: The JSON object.
		"""

		json_result : dict[str, list[dict]] = {}
		for table in self.tables:
			if (table != 'sqlite_sequence'):
				self.execute (f"SELECT * FROM {table}")
				rows : tuple[dict] = self.fetchall ()

				for row in rows:
					del row[f"{table}_id"]
					for key, value in row.items ():
						if (isinstance (value, str)):
							row[key] : any = self.deserialize_value (value)

				json_result[table] : list[dict] = [ dict (row) for row in rows ]

		return json_result

	def json_to_database (self, data : dict[str, list[dict]]) -> None:
		"""
		Convert a JSON object to the database.

		Args:
			data (dict[str, list[dict]]): The JSON object.
		"""

		for table_name, rows in data.items ():
			if (not isinstance (rows, list) or not all (isinstance (row, dict) for row in rows)):
				raise ValueError (f"The data for table '{table_name}' must be a list of dictionaries.")

			self.create_table (table_name, **{ key : type (value) for key, value in rows[0].items () })

			for row in rows:
				row : dict = { key : self.serialize_value (value) for key, value in row.items ()}
				self.execute (f"INSERT INTO {table_name} ({', '.join (row.keys ())}) VALUES ({', '.join ('?' for _ in row)})", *row.values ())
		
		self.commit ()