import pandas as pd
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas

# Requirements
# Currently, the pandas-oriented API methods in the Python connector API work with:
# Snowflake Connector 2.1.2 (or higher) for Python.
# PyArrow library version 3.0.x.
# If you do not have PyArrow installed, you do not need to install PyArrow yourself; installing the Python Connector as documented below automatically installs the appropriate version of PyArrow.
# Caution
# If you already have any version of the PyArrow library other than the recommended version listed above, please uninstall PyArrow before installing the Snowflake Connector for Python. Do not re-install a different version of PyArrow after installing the Snowflake Connector for Python.
# For more information, see the PyArrow library documentation.
# pandas 0.25.2 (or higher). Earlier versions might work, but have not been tested.


class CustomException(Exception):
    """Custom exception class for Snowflake connector errors."""
    def __init__(self, e, operation):
        self.message = f"Error in {operation}: {e}"
        super().__init__(self.message)

class Connector:
    """Snowflake connector class for python pandas."""
    def __init__(self, 
                 snowflake_user, 
                 snowflake_password, 
                 snowflake_account, 
                 snowflake_warehouse, 
                 snowflake_database, 
                 snowflake_schema,
                 pool_size=10, 
                 max_overflow=10, 
                 pool_timeout=30):
        """
        Initialize the Snowflake connector with connection pool parameters.
        Args:
            snowflake_user (str): Snowflake username.
            snowflake_password (str): Snowflake password.
            snowflake_account (str): Snowflake account name.
            snowflake_warehouse (str): Snowflake warehouse name.
            snowflake_database (str): Snowflake database name.
            snowflake_schema (str): Snowflake schema name.
            pool_size (int, optional): Connection pool size. Defaults to 10.
            max_overflow (int, optional): Maximum overflow for the pool. Defaults to 10.
            pool_timeout (int, optional): Timeout for acquiring connections from the pool. Defaults to 30 seconds.
        """
        self.user = snowflake_user
        self.password = snowflake_password
        self.account = snowflake_account
        self.warehouse = snowflake_warehouse
        self.database = snowflake_database
        self.schema = snowflake_schema
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool = self._create_pool()

    def _create_pool(self):
        """
        Create a connection pool with the provided parameters.
        """
        return snowflake.connector.SnowflakeConnectionPool(
            creator=sf.connect,
            pool_size=self.pool_size,  # Use pool_size from initialization
            max_overflow=self.max_overflow,  # Use max_overflow from initialization
            pool_timeout=self.pool_timeout,  # Use pool_timeout from initialization
            user=self.user,
            password=self.password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema
        )

    def _get_connection(self):
        """
        Get a connection from the pool.
        """
        return self.pool.connect()

    def add_column(self, table_name, column_name):
        """
        Add a column to a Snowflake table.
        Args:
            table_name (str): Name of the table to add the column to.
            column_name (str): Name of the column to add.
        Raises:
            CustomException: If the operation fails.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = f'ALTER TABLE {table_name} ADD COLUMN "{column_name}" VARCHAR(16777216)'
            cursor.execute(query)
            cursor.close()
            conn.close()
            return
        except Exception as e:
            raise CustomException(e, "addColumn")

    def run_sql_query(self, query):
        """
        Run any SQL query on Snowflake and return the result as a DataFrame.
        Args:
            query (str): SQL query to run.
        Returns:
            pd.DataFrame: DataFrame containing the result of the query.
        Raises:
            CustomException: If the operation fails.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
            cursor.close()
            conn.close()
            return df
        except Exception as e:
            raise CustomException(e, "run_sql_query")

    def write_df(self, df, table_name, auto_create_table=True):
        """
        Write a Pandas DataFrame to a Snowflake table.
        Args:
            df (pd.DataFrame): DataFrame to write to Snowflake.
            table_name (str): Name of the table to write to.
            auto_create_table (bool, optional): Whether to create the table if it doesn't exist. Defaults to True.
        Raises:
            CustomException: If the operation fails.
        """
        try:
            df = df.fillna("")
            if df.empty:
                return None
            conn = self._get_connection()
            res = write_pandas(
                conn=conn,
                df=df,
                table_name=table_name,
                database=self.database,
                schema=self.schema,
                auto_create_table=auto_create_table
            )
            conn.commit()
            conn.close()
            return res
        except Exception as e:
            raise CustomException(e, "write_df")

    def get_table_columns(self, table_name):

        """
        Get the columns of a Snowflake table.

        Args:
            table_name (str): Name of the table to get columns for.

        Returns:
            pd.DataFrame: DataFrame containing the table columns.

        Raises:
            CustomException: If the operation fails.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = f"DESCRIBE TABLE {table_name}"
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
            cursor.close()
            conn.close()
            return df
        except Exception as e:
            raise CustomException(e, "getTableColumns")
