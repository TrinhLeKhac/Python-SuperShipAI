from sqlalchemy import create_engine
from scripts.api.out_data_final import *
from scripts.database.dtypes import *


def ingest_data_to_db():
    port = create_engine('postgresql://postgres:123456@localhost:5432/supership_ai_db')
    engine = create_engine(port)

    print('1. Ingest processed_data...')
    processed_data_path = './processed_data'
    for f, schema in TABLE_SCHEMA.values():
        if f not in ['data_api', 'data_api_full', 'data_check_output']:
            tmp_df = pd.read_parquet(os.path.join(processed_data_path, f))
            tmp_df.to_sql(name=f, con=engine, schema="db_schema", index=False, dtype=schema)

    print('2. Ingest output API')
    data_api_df = pd.read_parquet('./output/data_api.parquet')
    data_api_df.to_sql(name='data_api', con=engine, schema="db_schema", index=False, dtype=TABLE_SCHEMA['data_api'])

    print('3. Ingest output API full')
    data_api_full_df = out_data_api(return_full_cols_df=True)
    data_api_full_df.to_sql(name='data_api_full', con=engine, schema="db_schema", index=False, dtype=TABLE_SCHEMA['data_api_full'])

    print('4. Ingest data check output')
    check_df = out_data_final()
    check_df.to_sql(name='data_check_output', con=engine, schema="db_schema", index=False, dtype=TABLE_SCHEMA['data_check_output'])


if __name__ == '__main__':
    ingest_data_to_db()
