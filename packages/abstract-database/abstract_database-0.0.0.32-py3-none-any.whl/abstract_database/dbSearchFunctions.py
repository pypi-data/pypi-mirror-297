from templates import getInsertType
import json,asyncio,asyncpg
from .db_config import getQuery
from .templates import getInsertList
from abstract_apis import asyncPostRpcRequest, asyncPostRequest
from abstract_utilities import SingletonMeta
from abstract_solcatcher import makeLimitedCall
from abstract_solana import Pubkey
class TableManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.tables = []

    async def create_table(self, tableName):
        tableName = tableName.lower()
        if tableName not in self.tables:
            query_result = await create_table(tableName)
            if query_result:
                self.tables.append(tableName)
        return getInsertType(tableName)

async def create_table(tableName):
    insertType = getInsertType(tableName)
    if insertType and insertType.get("table"):
        try:
            await getQuery(insertType["table"])
        except Exception as e:
            print(f"Error creating table {tableName}: {str(e)}")
    else:
        print(f"No creation query found for {tableName}")

async def insert_Db(tableName, searchValue, insertValue,**kwargs):
    tableName = tableName.lower()
    insertType = await TableManager().create_table(tableName)
    if not insertType:
        print(f"No insert type found for table: {tableName}")
        return

    # Check if entry exists
    existing_entry = await search_Db(tableName, searchValue)
    if existing_entry:
        print(f"Entry already exists in {tableName} with value {searchValue}")
        return existing_entry

    if not isinstance(insertValue, tuple):
        insertValue = (searchValue, dump_if_json(insertValue))

    instype = insertType['insertQuery']
    query = getInsertQueryS(insertType['insertQuery'])
    
    insert_query = "INSERT INTO {} ({}) VALUES ({})".format(tableName, instype, query)
    try:
        await getQuery(insert_query, insertValue)
        print(f"Inserted into {tableName}: {searchValue}")
    except Exception as e:
        print(f"Error using {insert_query} inserting {instype} with a value of {query} into {tableName}: {str(e)}")

async def search_Db(tableName, searchValue,**kwargs):
    tableName = tableName.lower()
    insertType = await TableManager().create_table(tableName)
    if not insertType:
        print(f"No data structure for {tableName}")
        return

    search_query = getSearchQuery(tableName, '*', insertType['columnSearch'])
    try:
        result = await getQuery(search_query, (searchValue,))
        if result:
            print(f"Found in {tableName}: {result}")
            return result
        else:
            print(f"No data found in {tableName} for {searchValue}")
    except Exception as e:
        print(f"Error searching in {tableName}: {str(e)}")


async def universal_db_function(method,  params, check_identical_params=None, doNotCall=None, url=None, data={}):
    # Ensure the table is ready for operations
    tableName = method
    inputs = await TableManager().create_table(tableName)
    if not inputs:
        print(f"Unable to find or create table: {tableName}")
        return

    # Extract the unique identifier for database operations
    unique_identifier = params[0]

    # Attempt to find an existing entry in the database
    existing_entry = await search_Db(tableName, unique_identifier)

    # Determine if the existing entry should be ignored based on the parameters
    if check_identical_params and existing_entry:
        all_match = all(params[k] == existing_entry.get(k, None) for k in params if k in existing_entry)
        if not all_match:
            existing_entry = None

    # If instructed not to make external calls and an entry exists, return it
    if doNotCall and existing_entry:
        return existing_entry

    # If there's no existing entry or it's ignored based on parameters, make an external call if allowed
    if not existing_entry and not doNotCall:
        response_data = await (asyncPostRequest(url=url, data=data, endpoint=method) if url else makeLimitedCall(method, params))

        # Handle unsuccessful responses or errors
        if not response_data or (isinstance(response_data, dict) and response_data.get('error')):
            print(f"Failed to get a valid response for {unique_identifier} in {tableName}: {response_data}")
            return response_data

        # If the response is successful, insert it into the database
        await insert_Db(tableName, unique_identifier, (unique_identifier, dump_if_json(response_data)))
        print(f"Inserted {unique_identifier} in {tableName}")
        return response_data

    # Return the existing entry if all checks pass and no external call is made
    return existing_entry


def check_table_mgr(tableName):
    tableName = tableName.lower()
    return TableManager().create_table(tableName)

def getSearchQuery(tableName, valueSelect='*', columnName=''):
    return f"SELECT {valueSelect} FROM {tableName} WHERE {columnName} = $1"

def getsearchquery(tableName):
    insertType = check_table_mgr(tableName)
    return getSearchQuery(insertType.get('tableName'), '*', insertType['columnSearch'])

def getInsertQueryS(insertQuery):
    parts = [part.strip() for part in insertQuery[1:-1].split(',')]
    placeholders = ', '.join(f'${i + 1}' for i in range(len(parts)))
    return placeholders

def getInsertType(tableName):
    insertList = [ls for ls in getInsertList() if ls.get("tableName") == tableName.lower()]
    return insertList[0] if insertList else None

def setup_database(tables, conn):
    """ Create database tables based on provided configurations """
    cur = conn.cursor()
    try:
        for table in tables:
            cur.execute(table['table'])
        conn.commit()
    except psycopg2.Error as e:
        print("Error setting up database tables:", e)
        conn.rollback()
    finally:
        cur.close()

def fetch_data(search_query, search_value, conn):
    """ Fetch data from the database using the specified query and value """
    cur = conn.cursor()
    try:
        cur.execute(search_query, (search_value,))
        return cur.fetchone()
    finally:
        cur.close()

def insert_data(insert_query, values, conn):
    """ Insert data into the database using the specified query and values """
    cur = conn.cursor()
    try:
        cur.execute(insert_query, values)
        conn.commit()
    except psycopg2.Error as e:
        print("Failed to insert data:", e)
        conn.rollback()
    finally:
        cur.close()

def perform_database_operations(operation_type, table_info, value, conn):
    """ Perform dynamic database operations based on type and table info """
    if operation_type == 'fetch':
        return fetch_data(table_info['searchQuery'], value, conn)
    elif operation_type == 'insert':
        insert_data(table_info['insertQuery'], value, conn)

def fetchFromDb(tableName,searchValue,conn):
    cached_response =perform_database_operations('fetch', getInsertType(tableName.lower()), searchValue, conn)
    if cached_response:
        return cached_response

def insert_intoDb(tableName,searchValue,insertValue,conn):
    if isinstance(insertValue,dict):
        insertValue = json.dumps(insertValue)
    perform_database_operations('insert', getInsertType(tableName.lower()), (params[0],insertValue),conn )
