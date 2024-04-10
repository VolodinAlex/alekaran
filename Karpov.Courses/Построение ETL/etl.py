from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
import requests
import pandas as pd
import pandahouse as ph
from datetime import datetime, timedelta
from io import StringIO

# параметры подключения к кликхаусу
connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator_20230720'
}

# параметры подключения к схеме test
test = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'database':'test',
    'user':'student-rw', 
    'password':'656e2b0c9c'
}

# дефолтные параметры
default_args = {
    'owner': 'alek-volodin',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 8, 12)
}

# интервал запуска
schedule_interval = '0 9 * * *'

@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)
def dag_alek_volodin():
    
    # выгрузка данных из ленты
    @task
    def extract_feed():
        
        q = """
            SELECT
                toDate(time) AS event_date,
                user_id,
                IF(gender=1, 'male', 'female') AS gender,
                age,
                os,
                SUM(action='like') AS likes,
                SUM(action='view') AS views
            FROM simulator_20240420.feed_actions
            WHERE toDate(time) = today() - 1
            GROUP BY event_date, user_id, gender, age, os
        """

        # продолжим работу с пандасом
        feed_cube = ph.read_clickhouse(q, connection=connection)
        
        return feed_cube
    
    
    # выгрузка данных из мессенджера
    @task
    def extract_message():
        """ чтобы не терять никакие данные, проводим полное объединение, т.е. будут выводиться
        случаи, когда, например, пользователи получают сообщения, но сами их не пишут."""

        q = """
            SELECT
                today() - 1 AS event_date,
                IF(user_id=0, reciever_id, user_id) AS user_id,
                messages_sent, users_sent,
                messages_received, users_received,
                IF(gender='', b.gender, a.gender) AS gender,
                IF(age=0, b.age, a.age) AS age,
                IF(os='', b.os, a.os) AS os
            FROM (
                SELECT
                    user_id,
                    COUNT(reciever_id) AS messages_sent,
                    COUNT(DISTINCT reciever_id) AS users_sent,
                    IF(gender=1, 'male', 'female') AS gender,
                    age,
                    os
                FROM simulator_20230720.message_actions
                WHERE toDate(time) = today() - 1
                GROUP BY user_id, gender, age, os
            ) AS a
            FULL JOIN (
                SELECT *
                FROM (
                    SELECT
                        reciever_id,
                        COUNT(user_id) AS messages_received,
                        COUNT(DISTINCT user_id) AS users_received
                    FROM simulator_20230720.message_actions
                    WHERE toDate(time) = today() - 1
                    GROUP BY reciever_id
                ) AS now
                JOIN (
                    SELECT reciever_id, age, os,
                        IF(gender=1, 'male', 'female') AS gender
                    FROM (
                        SELECT DISTINCT reciever_id
                        FROM simulator_20230720.message_actions
                    ) AS r
                    JOIN (
                        SELECT DISTINCT user_id, gender, age, os
                        FROM simulator_20230720.message_actions
                    ) AS u ON r.reciever_id=u.user_id
                ) AS all USING(reciever_id)
            ) AS b ON a.user_id=b.reciever_id
            ORDER BY user_id
        """

        # продолжим работу с пандасом
        message_cube = ph.read_clickhouse(q, connection=connection)
        
        return message_cube
    
    
    @task
    # объединеняем загрузки в один датасет
    def transform_join(feed_cube, message_cube):
        """ выводятся все пользователи, которые хоть как-то фигурировали в заданный день;
        т.е даже если пользователь не пользовался лентов, не писал сообщения, а, например,
        получил одно сообщение, он тоже попадет в выгрузку"""
        
        merged_cube = feed_cube.merge(
            message_cube, 
            how='outer',
            on=['user_id', 'gender', 'age', 'os', 'event_date']
        ).fillna(0)
        
        return merged_cube
    
    
    @task
    # получаем срез по полу
    def transform_gender(merged_cube):

        # агрегируем данные
        df_gender = merged_cube.groupby(['event_date', 'gender'], as_index=False)[['views', 'likes', 'messages_received', 'messages_sent', 'users_received', 'users_sent']].sum()
        
        # переименуем колонку 
        df_gender.rename(columns={'gender': 'dimension_value'}, inplace = True)
        
        # добавим второй по счету колонку с названием среза
        dimensions_column = 'gender'
        df_gender.insert(1, 'dimension', dimensions_column)
        
        return df_gender
    
    
    @task
    # получаем срез по возрасту
    def transform_age(merged_cube):
        
        # агрегируем данные
        df_age = merged_cube.groupby(['event_date', 'age'], as_index=False)[['views', 'likes', 'messages_received', 'messages_sent', 'users_received', 'users_sent']].sum()
        
        # переименуем колонку 
        df_age.rename(columns={'age': 'dimension_value'}, inplace=True)
        
        # добавим второй по счету колонку с названием среза
        dimensions_column = 'age'
        df_age.insert(1, 'dimension', dimensions_column)
        
        return df_age
    
    
    @task
    # получаем срез по типу операционной системы
    def transform_os(merged_cube):
        
        # агрегируем данные
        df_os = merged_cube.groupby(['event_date', 'os'], as_index=False)[['views', 'likes', 'messages_received', 'messages_sent', 'users_received', 'users_sent']].sum()
        
        # переименуем колонку 
        df_os.rename(columns={'os': 'dimension_value'}, inplace=True)
        
        # добавим второй по счету колонку с названием среза
        dimensions_column = 'os'
        df_os.insert(1, 'dimension', dimensions_column)
        
        return df_os
    
    
    @task
    def transform_concat(df_gender, df_age, df_os):
        """функция для соединения датасетов в один"""
        
        cube = pd.concat([df_gender, df_age, df_os], axis=0)
        
        return cube
        
    
    
    @task
    def load(cube):
        q = '''
            CREATE TABLE IF NOT EXISTS test.alek_volodin
                (
                event_date Date,
                dimension varchar(50),
                dimension_value varchar(50),
                views Float64,
                likes Float64,
                messages_received Float64,
                messages_sent Float64,
                users_received Float64,
                users_sent Float64
                ) ENGINE = MergeTree()
            ORDER BY event_date
        '''
        ph.execute(q, connection=test) 
        ph.to_clickhouse(cube, 'alek_volodin', index=False, connection=test)

        
    # выполням таски
    feed_cube = extract_feed()
    message_cube = extract_message()
    merged_cube = transform_join(feed_cube, message_cube)
    df_gender = transform_gender(merged_cube)
    df_age = transform_age(merged_cube)
    df_os = transform_os(merged_cube)
    cube = transform_concat(df_gender, df_age, df_os)
    load(cube)

dag_alek_volodin = dag_alek_volodin()