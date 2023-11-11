from sqlalchemy import create_engine
from scripts.utilities.helper import *
from scripts.api.out_data_api import *
from scripts.api.out_data_final import *


def ingest_data_to_db():
    engine = create_engine('postgresql://postgres:123456@localhost:5432/supership_ai_db')

    print('1. Ingest processed_data...')
    processed_data_path = './processed_data'
    for f in os.listdir(processed_data_path):
        tmp_df = pd.read_parquet(os.path.join(processed_data_path, f))
        tmp_df.to_sql(file, engine)

    print('2. Ingest output API')
    data_api_df = pd.read_parquet('./output/data_api.parquet')
    data_api_df.to_sql("data_api", engine)

    print('3. Ingest output API full')
    data_api_full_df = out_data_api(return_full_cols_df=True)
    data_api_full_df.to_sql("data_api_full", engine)

    print('4. Ingest data check output')
    final_df = out_data_final()
    data_api_full_df.to_sql('data_check_output', engine)


if __name__ == '__main__':
    ingest_data_to_db()
