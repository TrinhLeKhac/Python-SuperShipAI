import psycopg2
from psycopg2 import sql
from config import settings


def check_tbl_exists_in_postgres(schema_name, table_name, cursor):

    # Check if the table exists
    check_table_query = sql.SQL("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = {} AND table_name = {}
        )
    """).format(sql.Literal(schema_name), sql.Literal(table_name))

    cursor.execute(check_table_query)
    table_exists = cursor.fetchone()[0]

    # Table doesn't exist, create it
    if not table_exists:
        if table_name == 'zns':
            create_table_query = sql.SQL("""
                CREATE TABLE {}.{} (
                    receiver_province VARCHAR(30),
                    receiver_district VARCHAR(30),
                    carrier_id SMALLINT,
                    message_count INTEGER,
                    star INTEGER,
                    feedbacks TEXT [],
                    note VARCHAR(100),
                    submitted_at VARCHAR(20),
                    date VARCHAR(10)
                )
            """).format(sql.Identifier(schema_name), sql.Identifier(table_name))
            cursor.execute(create_table_query)

        elif table_name == 'order':
            create_table_query = sql.SQL("""
                CREATE TABLE {}.{} (
                    order_code VARCHAR(30),
                    created_at VARCHAR(20),
                    sent_at VARCHAR(20),
                    order_status VARCHAR(30),
                    carrier_id SMALLINT,
                    carrier_status VARCHAR(30),
                    sender_province VARCHAR(30),
                    sender_district VARCHAR(30),
                    receiver_province VARCHAR(30),
                    receiver_district VARCHAR(30),
                    delivery_count INTEGER,
                    pickup VARCHAR(1),
                    barter VARCHAR(1),
                    carrier_delivered_at VARCHAR(20),
                    picked_at VARCHAR(20),
                    last_delivering_at VARCHAR(20),
                    carrier_updated_at VARCHAR(20),
                    date VARCHAR(10)
                )
            """).format(sql.Identifier(schema_name), sql.Identifier(table_name))
            cursor.execute(create_table_query)


def check_row_exists_in_postgres(row, schema_name, table_name, cursor):

    # Build the SELECT query dynamically based on the provided data
    select_query = sql.SQL("""
            SELECT * 
            FROM {}.{}
            WHERE {}
        """).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(" AND ").join(
            sql.SQL("{} = %s").format(sql.Identifier(column))
            for column in row.keys()
        )
    )

    # Execute the SELECT query
    cursor.execute(select_query, tuple(row.values()))

    # Check if the row exists
    existing_row = cursor.fetchone()

    return existing_row


def _insert_data_to_postgres(data, schema_name, table_name, cursor):

    # Assuming data is a list of dictionaries where each dictionary represents a row
    for row in data:
        if check_row_exists_in_postgres(row, schema_name, table_name, cursor):
            print('Row already exists, skipping insertion.')
        else:
            columns = row.keys()
            values = [row[column] for column in columns]

            insert_query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(sql.Placeholder() for _ in values)
            )
            print(insert_query)
            cursor.execute(insert_query, values)


def insert_data_to_postgres(data, schema_name, table_name):
    # Create connection
    connection = psycopg2.connect(
        settings.SQLALCHEMY_DATABASE_URI
    )

    cursor = connection.cursor()

    check_tbl_exists_in_postgres(schema_name, table_name, cursor)
    _insert_data_to_postgres(data, schema_name, table_name, cursor)

    # Commit the transaction
    connection.commit()

    cursor.close()
    connection.close()
