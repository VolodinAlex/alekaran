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

# интервал запуска
schedule_interval = '0 14 * * *'

# bot and chats
my_token = '6521835945:AAHWzxWP3HZiqu9Tv11gdGvfBelouNDyNjY'
bot = telegram.Bot(token=my_token)
chat_id=-927780322

# автоматизируем отправку
@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False, chat_id=-927780322)
def dag_alekaran_report_2():
    
    # выгрузка данных
    @task()
    def extract_feed():
        # формируем запрос
        q = """
            WITH both_main AS (
                SELECT
                    date,
                    COUNT(DISTINCT user_id) AS dau_both,
                    SUM(likes) AS likes_total,
                    SUM(views) AS views_total,
                    SUM(recievers) AS recievers_total,
                    SUM(msg) AS msg_total
                FROM (
                    SELECT
                        IF(f.date='1970-01-01', m.date, f.date) AS date,
                        IF(f.user_id=0, m.user_id, f.user_id) AS user_id,
                        likes,
                        views,
                        recievers,
                        msg
                    FROM (
                        SELECT
                            toDate(time) AS date,
                            user_id,
                            SUM(action='like') AS likes,
                            SUM(action='view') AS views
                        FROM simulator_20230720.feed_actions
                        WHERE toDate(time) >= today() - 14 AND toDate(time) < today()
                        GROUP BY date, user_id
                    ) AS f
                    FULL JOIN (
                        SELECT
                            toDate(time) AS date,
                            user_id,
                            COUNT(DISTINCT reciever_id) AS recievers,
                            COUNT(reciever_id) AS msg
                        FROM simulator_20230720.message_actions
                        WHERE toDate(time) >= today() - 14 AND toDate(time) < today()
                        GROUP BY date, user_id
                    ) AS m ON f.user_id=m.user_id AND f.date=m.date
                ) AS all
                GROUP BY date
            ), 
            new AS (
                SELECT
                    first_act AS date,
                    feed_new_users, 
                    msg_new_users
                FROM (
                    SELECT
                        first_act,
                        COUNT(DISTINCT user_id) AS feed_new_users
                    FROM (
                        SELECT
                            user_id,
                            MIN(toDate(time)) AS first_act
                        FROM simulator_20230720.feed_actions
                        GROUP BY user_id
                        ORDER BY user_id
                    ) AS min_f
                    WHERE first_act < today() AND first_act >= today() - 14
                    GROUP BY first_act
                ) AS f
                JOIN (
                    SELECT
                        first_act,
                        COUNT(DISTINCT user_id) AS msg_new_users
                    FROM (
                        SELECT
                            user_id,
                            MIN(toDate(time)) AS first_act
                        FROM simulator_20230720.message_actions
                        GROUP BY user_id
                        ORDER BY user_id
                    ) AS min_f
                    WHERE first_act < today() AND first_act >= today() - 14

                    GROUP BY first_act
                ) AS m USING(first_act)
            ), 
            dau AS (
                SELECT
                    date,
                    dau_feed,
                    dau_msg
                FROM (
                    SELECT
                        toDate(time) AS date,
                        COUNT(DISTINCT user_id) AS dau_feed
                    FROM simulator_20230720.feed_actions
                    WHERE toDate(time) >= today() - 14 AND toDate(time) < today()
                    GROUP BY date
                ) AS f_dau
                JOIN (
                    SELECT
                        toDate(time) AS date,
                        COUNT(DISTINCT user_id) AS dau_msg
                    FROM simulator_20230720.message_actions
                    WHERE toDate(time) >= today() - 14 AND toDate(time) < today()
                    GROUP BY date
                ) AS m_dau USING(date)
            )

            SELECT
                a.date AS date, 
                dau_both, dau_feed, dau_msg,
                feed_new_users, msg_new_users,
                likes_total, views_total, msg_total,
                ROUND(likes_total/views_total, 3) AS CTR,
                ROUND(likes_total / dau_feed, 2) AS likes_per_user,
                ROUND(views_total / dau_feed, 2) AS views_per_user,
                ROUND(recievers_total / dau_msg, 2) AS recievers_per_user,
                ROUND(msg_total / dau_msg ,2) as msg_per_user
            FROM both_main AS a
            JOIN new AS b ON a.date=b.date
            JOIN dau AS c ON a.date=c.date
            ORDER BY a.date DESC
        """

        # перейдем в датафрейм
        df = ph.read_clickhouse(query=q, connection=connection)
        
        return df
    
    
    @task()
    # преобразование
    def transform_join(df):
        """функция для преобразования даты"""
        
        # за день до дня отчета
        day_before = df['date'].loc[1]
        day_before = day_before.strftime('%d.%m')
        
        # день отчета
        date = df['date'].loc[0]
        date_str = date.strftime('%d.%m.%Y')
        
        return date_str, day_before
    
    
    @task()
    # график по dau
    def load_first_plot(df, date_str, day_before, chat_id):
        
        # старт
        msg = (
            f"***Отчет за {date_str}***\n"
            "__________________________\n"
        )
        bot.sendMessage(chat_id=chat_id, text=msg)
        
        # график 1
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))

        # график dau
        sns.lineplot(df, y='dau_both', x='date', color='blue', markers=True, label='DAU приложения', ax=axes[0])
        sns.lineplot(df, y='dau_feed', x='date', color='green', markers=True, label='DAU ленты новостей', ax=axes[0])
        sns.lineplot(df, y='dau_msg', x='date', color='red', markers=True, label='DAU мессенджера', ax=axes[0])
        axes[0].set(title='Активные пользователи', xlabel='', ylabel='');

        # график новых пользователей
        sns.lineplot(df, y='feed_new_users', x='date', color='green', markers=True, label='Лента', ax=axes[1])
        sns.lineplot(df, y='msg_new_users', x='date', color='red', markers=True, label='Мессенджер', ax=axes[1])
        axes[1].set(title='Новые пользователи', xlabel='', ylabel='');

        # сделаем адекватную визуализацию дат
        axes[0].tick_params(axis='x', rotation=45)
        axes[1].tick_params(axis='x', rotation=45)
        plt.tight_layout()

        # отправляем график
        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'dau.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
    
    
    @task()
    # аналитика по dau
    def load_first_text(df, date_str, day_before, chat_id):
        
        # общая аудитория
        if df['dau_both'].loc[0] < df['dau_both'].loc[1]:
            dau_both = round(100 - df['dau_both'].loc[0] / df['dau_both'].loc[1] * 100, 2) 
            msg_1 = f"Общая аудитория: {df['dau_both'].loc[0]} ( -{dau_both}% от {day_before})\n"
        else:
            dau_both = round(df['dau_both'].loc[0] / df['dau_both'].loc[1] * 100, 2) 
            msg_1 = f"Общая аудитория: {df['dau_both'].loc[0]} (+{dau_both}% от {day_before})\n"
            
        # лента
        if df['dau_feed'].loc[0] < df['dau_feed'].loc[1]:
            dau_feed = round(100 - df['dau_feed'].loc[0] / df['dau_feed'].loc[1] * 100, 2) 
            msg_2 = f"Лента: {df['dau_feed'].loc[0]} ( -{dau_feed}% от {day_before})\n"
        else:
            dau_feed = round(df['dau_feed'].loc[0] / df['dau_feed'].loc[1] * 100, 2) 
            msg_2 = f"Лента: {df['dau_feed'].loc[0]} (+{dau_feed}% от {day_before})\n"

        # мессенджер
        if df['dau_msg'].loc[0] < df['dau_msg'].loc[1]:
            dau_msg = round(100 - df['dau_msg'].loc[0] / df['dau_msg'].loc[1] * 100, 2) 
            msg_3 = f"Мессенджер: {df['dau_msg'].loc[0]} ( -{dau_msg}% от {day_before})\n"

        else:
            dau_msg = round(df['dau_msg'].loc[0] / df['dau_msg'].loc[1] * 100, 2) 
            msg_3 = f"Мессенджер: {df['dau_msg'].loc[0]} (+{dau_msg}% от {day_before})\n"

        # текст сообщения
        msg = (
            f"<b>Активные пользователи</b>\n"
            + msg_1
            + msg_2
            + msg_3
            + '\n'
            "<b>Новые пользователи</b>\n"
            f"Лента: {df['feed_new_users'].loc[0]}\n"
            f"Мессенджер: {df['msg_new_users'].loc[0]}"
        )

        # отправляем сообщение
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')
        
        
    @task()
    # график по ленте
    def load_second_plot(df, date_str, day_before, chat_id):
        
        # график 2
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,8))

        # график dau
        sns.lineplot(df, y='likes_total', x='date', color='red', markers=True, ax=axes[0][0])
        axes[0][0].set(title='Лайки', xlabel='', ylabel='');
        axes[0][0].tick_params(axis='x', rotation=45)

        # график новых пользователей
        sns.lineplot(df, y='views_total', x='date', color='purple', markers=True, ax=axes[0][1])
        axes[0][1].set(title='Просмотры', xlabel='', ylabel='');
        axes[0][1].tick_params(axis='x', rotation=45)

        # график ctr
        sns.lineplot(df, y='CTR', x='date', color='blue', markers=True, ax=axes[1][0])
        axes[1][0].set(title='CTR', xlabel='', ylabel='');
        axes[1][0].tick_params(axis='x', rotation=45)

        # график лайков и просмотров на 1 юзера
        sns.lineplot(df, y='likes_per_user', x='date', color='red', markers=True, ax=axes[1][1], label='Лайки')
        sns.lineplot(df, y='views_per_user', x='date', color='purple', markers=True, ax=axes[1][1], label='Просмотры')
        axes[1][1].set(title='На одного пользователя', xlabel='', ylabel='');
        axes[1][1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # отправляем график
        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'feed_actions.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
    
    
    @task()
    # аналитика по ленте
    def load_second_text(df, date_str, day_before, chat_id):
        
        # лайки
        if df['likes_total'].loc[0] < df['likes_total'].loc[1]:
            likes_total = round(100 - df['likes_total'].loc[0] / df['likes_total'].loc[1] * 100, 2) 
            msg_4 = f"Лайков: {df['likes_total'].loc[0]} ( -{likes_total}% от {day_before})\n"
        else:
            likes_total = round(df['likes_total'].loc[0] / df['likes_total'].loc[1] * 100, 2) 
            msg_4 = f"Лайков: {df['likes_total'].loc[0]} (+{likes_total}% от {day_before})\n"

        # просмотры
        if df['views_total'].loc[0] < df['views_total'].loc[1]:
            views_total = round(100 - df['views_total'].loc[0] / df['views_total'].loc[1] * 100, 2) 
            msg_5 = f"Просмотров: {df['views_total'].loc[0]} ( -{views_total}% от {day_before})\n"
        else:
            views_total = round(df['views_total'].loc[0] / df['views_total'].loc[1] * 100, 2) 
            msg_5 = f"Просмотров: {df['views_total'].loc[0]} (+{views_total}% от {day_before})\n"

        # формируем текст
        msg = (
            "<b>Лента новостей</b>\n"
            + msg_4
            + msg_5
            + f"CTR: {df['CTR'].loc[0]}\n"
            '\n'
            "<b>На одного пользователя </b>\n"
            f"Лайки: {df['likes_per_user'].loc[0]}\n"
            f"Просмотры: {df['views_per_user'].loc[0]}"
        )

        # отправляем сообщение
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')
        
    
    @task()
    # график по мессенджеру
    def load_third_plot(df, date_str, day_before, chat_id):
        
        # график 3
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))

        # всего сообщений
        sns.lineplot(df, y='msg_total', x='date', color='yellow', markers=True, ax=axes[0])
        axes[0].set(title='Сообщений за день', xlabel='', ylabel='');
        axes[0].tick_params(axis='x', rotation=45)

        # на одного
        sns.lineplot(df, y='recievers_per_user', x='date', color='green', label='Получатели', ax=axes[1])
        sns.lineplot(df, y='msg_per_user', x='date', color='yellow', label='Сообщения', ax=axes[1])
        axes[1].set(title='На одного пользователя', xlabel='', ylabel='');
        axes[1].tick_params(axis='x', rotation=45)
        plt.tight_layout()

        # отправляем график
        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'msg_actions.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
    
    
    @task()
    # аналитика по мессенджеру
    def load_third_text(df, date_str, day_before, chat_id):
        
        # всего сообщений
        if df['msg_total'].loc[0] < df['msg_total'].loc[1]:
            msg_total = round(100 - df['msg_total'].loc[0] / df['msg_total'].loc[1] * 100, 2) 
            msg_6 = f"Всего сообщений: {df['msg_total'].loc[0]} ( -{msg_total}% от {day_before})\n"
        else:
            msg_total = round(df['msg_total'].loc[0] / df['msg_total'].loc[1] * 100, 2) 
            msg_6 = f"Всего сообщений: {df['msg_total'].loc[0]} (+{msg_total}% от {day_before})\n"

        # формируем текст
        msg = (
            "<b>Мессенджер</b>\n"
            + msg_6
            + '\n'
            "<b>На одного пользователя</b>\n"
            f"Получателей: {df['recievers_per_user'].loc[0]}\n"
            f"Сообщений: {df['msg_per_user'].loc[0]}"
        )

        # Используйте метод parse_mode для указания HTML
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')
    
    
    df = extract_feed()
    date_str, day_before = transform_join(df)
    load_first_plot(df, date_str, day_before, chat_id=-927780322)
    load_first_text(df, date_str, day_before, chat_id=-927780322)
    load_second_plot(df, date_str, day_before, chat_id=-927780322)
    load_second_text(df, date_str, day_before, chat_id=-927780322)
    load_third_plot(df, date_str, day_before, chat_id=-927780322)
    load_third_text(df, date_str, day_before, chat_id=-927780322)
    
dag_alekaran_report_2 = dag_alekaran_report_2()