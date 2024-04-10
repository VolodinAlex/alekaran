import telegram
from datetime import datetime
import io
import pandas as pd
import pandahouse as ph
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# параметры подключения к кликхаусу
connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator_20230720'
}

# дефолтные параметры
default_args = {
    'owner': 'alek-volodin',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 8, 12)
}

# bot
my_token = '6521835945:AAHWzxWP3HZiqu9Tv11gdGvfBelouNDyNjY'
bot = telegram.Bot(token=my_token)
chat_id=-927780322

# интервал запуска
schedule_interval = '0 14 * * *'

@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)
def dag_alekaran_report_1():
    
    @task()
    def export():
        """выгружаем необходимые данные"""
    
        q = """
            SELECT
                toDate(time) AS date,
                COUNT(DISTINCT user_id) AS DAU,
                SUM(action='view') AS views,
                SUM(action='like') AS likes,
                ROUND(likes/views, 4) AS CTR
            FROM simulator_20230720.feed_actions
            WHERE toDate(time) >= today() - 7 AND toDate(time) < today()
            GROUP BY date
            ORDER BY date DESC
        """
    
        df = ph.read_clickhouse(query=q, connection=connection)
        
        return df
    
    @task()
    def transfrom(df):
        """изменим тип вывода даты"""
        
        date = df['date'].loc[0]
        date_str = date.strftime('%d %B %Y года')
        
        return date_str
    
    
    @task()
    def load_text(df, date_str, chat_id):
        """отправляем текстовую часть сообщения"""
    
        # составляем текст
        msg = (
            f"***Отчет за {date_str}***\n"
            f"- DAU: {df['DAU'].loc[0]}\n"
            f"- Просмотров: {df['views'].loc[0]}\n"
            f"- Лайков: {df['likes'].loc[0]}\n"
            f"- CTR: {df['CTR'].loc[0]}\n"
        )
        
        # отправка текста
        bot.sendMessage(chat_id=chat_id, text=msg)
        
        
    @task()
    def load_plot(df, chat_id):
        """отправляем график"""

        # строим графики
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(21,10))

        # график для dau
        sns.lineplot(df, x='date', y='DAU', color='blue', markers=True, dashes=False, ax=axes[0][0])
        axes[0][0].set_title('DAU', fontsize=16)
        axes[0][0].set(xlabel='', ylabel='')

        # график для просмотров
        sns.lineplot(df, x='date', y='views', color='green', markers=True, dashes=False, ax=axes[0][1])
        axes[0][1].set_title('Просмотры', fontsize=16);
        axes[0][1].set(xlabel='', ylabel='')

        # график для лайков
        sns.lineplot(df, x='date', y='CTR', color='brown', markers=True, dashes=False, ax=axes[1][0])
        axes[1][0].set_title('CTR', fontsize=16);
        axes[1][0].set(xlabel='', ylabel='')

        # график для CTR
        sns.lineplot(df, x='date', y='likes', color='red', markers=True, dashes=False, ax=axes[1][1])
        axes[1][1].set_title('Лайки', fontsize=16)
        axes[1][1].set(xlabel='', ylabel='');

        # отправляем графики
        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'plot_report.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
    
    
    df = export()
    date_str = transform(df)
    load_text(df, date_str, chat_id=-927780322)
    load_plot(df, chat_id=-927780322)

dag_alekaran_report_1 = dag_alekaran_report_1()