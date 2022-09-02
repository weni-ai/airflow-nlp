from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from simplet5 import SimpleT5
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import re
import glob
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {
    'owner': 'mmt93',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet():
    path = '/opt/airflow/dags/data'
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

    df = pd.read_csv('/opt/airflow/dags/teste33.csv')

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df.to_csv('/opt/airflow/dags/data/train_df.csv')
    test_df.to_csv('/opt/airflow/dags/data/test_df.csv')

def bye():
    model = SimpleT5()
    model.from_pretrained(model_type="t5", model_name="unicamp-dl/ptt5-base-portuguese-vocab")
    train_df = pd.read_csv('/opt/airflow/dags/data/train_df.csv')
    test_df = pd.read_csv('/opt/airflow/dags/data/test_df.csv')

    model.train(train_df=train_df,
                eval_df=test_df, 
                source_max_token_len=100, 
                target_max_token_len=100, 
                batch_size=2, max_epochs=2, use_gpu=False)
    
    directory = '/'
    dirs = os.walk(directory)
    dir_ = list(dirs)
    print('#############25', dir_)
    print(glob.glob("/"))

    dir_ = list(dirs)
    dir_ = dir_[0][1]
    lowest_val = 100
    for fold_nam in dir_:
        val_loss = re.findall('[0-9][,.][0-9]{3}', fold_nam)[1]
        if float(val_loss) < lowest_val:
            lowest_val = float(val_loss)
            model_path = 'outputs/' + fold_nam    
    model = SimpleT5()
    model.load_model("t5", model_path, use_gpu=False)
    res = model.predict('qual o nome da autora ? Ana')
    print('teste_teste_teste', res)

def hi():
    print('hi')

with DAG(
    default_args=default_args,
    dag_id='dag_number_1',
    description='First dag',
    start_date=datetime(2022, 9, 2),
    schedule_interval='@daily'
) as dag:

    # task1= S3KeySensor(
    #     task_id='sensor_minio_s3',
    #     bucket_name='allfiles',
    #     bucket_key='teste3.csv',
    #     aws_conn_id='minio_conn'
    # )

    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id='bye',
        python_callable=bye
    )

    task1 >> task2
