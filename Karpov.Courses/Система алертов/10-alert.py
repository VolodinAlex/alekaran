import telegram
from datetime import datetime, timedelta
import io

import pandas as pd
import pandahouse as ph
import numpy as np

# визуализация
import matplotlib.pyplot as plt
import seaborn as sns

# параметры подключения к кликхаусу
connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator_20230720'
}

# бот и чат
my_token = '6521835945:AAHWzxWP3HZiqu9Tv11gdGvfBelouNDyNjY'
bot = telegram.Bot(token=my_token)
chat_id = -927780322

# проверка последних значений метрик
def get_outliers(df, metric, left=3, right=4, window=5):
    """функция для поиска выбросов

    Args:
        df: датасет из загрузки
        metric: какую метрику проверяем
        left (int, optional): левый коэф для iqr. Defaults to 3.
        right (int, optional): правый коэф для iqr. Defaults to 3.
        window (int, optional): размер окна для сглаживания данных. Defaults to 5.

    Returns:
        df: датасет с границами
        is_outlier: наличие выбросов
    """
    df['q25'] = df[metric].shift(1).rolling(window).quantile(0.25)
    df['q75'] = df[metric].shift(1).rolling(window).quantile(0.75)
    df['iqr'] = df['q75'] - df['q25']
    
    # определяем границы
    df['upper_bound'] = df['q75'] + right*df['iqr']
    df['lower_bound'] = df['q25'] - left*df['iqr']
    
    # дополнительно сгладим
    df['upper_bound'] = df['upper_bound'].rolling(window).mean()
    df['lower_bound'] = df['lower_bound'].rolling(window).mean()
    
    # проверяем последнее значение метрики
    # возьмем обе ситуации - когда меньше нижней границы
    if df[metric].iloc[-1] < df['lower_bound'].iloc[-1]:
        is_outlier = 1
    
    # и когда больше верхней границы
    if df[metric].iloc[-1] > df['upper_bound'].iloc[-1]:
        is_outlier = 2
    
    # если все ок тоже сохраним результат
    else:
        is_outlier = 0
    
    return is_outlier, df


def get_title(df, metric):
    """функция для оформления подписи графика и вывода сообщения"""
    
    if metric == 'feed_users':
        return 'Активные пользователи ленты'
    
    if metric == 'likes':
        return 'Лайки'
    
    if metric == 'views':
        return 'Просмотры'
    
    if metric == 'ctr':
        return 'CTR'
    
    if metric == 'msg_users':
        return 'Активные пользователи мессенджера'
    
    if metric == 'messages':
        return 'Количество сообщений'

    
def build_plot(df, metric):
    """ф-я для построения графика с отклонением в сравнении с вчерашним днем и неделей назад
    добавим и доверительные интервалы """
    
    # выделим данные, которые были неделю назад
    week_ago = df['date'].iloc[-1] - timedelta(weeks=1)
    week_df = df[df['date'] == week_ago]
    
    # выделим данные за вчера
    yesterday = df['date'].iloc[-1] - timedelta(days=1)
    yesterday_df = df[df['date'] == yesterday]
    
    # данные за сегодня
    today = df['date'].iloc[-1]
    today_df = df[df['date'] == today]
    
    # строим график
    fig = plt.figure(figsize=(20, 8))

    # строим графики за сегодня, вчера и неделю назад
    sns.lineplot(today_df, x='dt', y=df[metric], color='green', linewidth=2, label='Сегодня')
    sns.lineplot(yesterday_df, x='dt', y=df[metric], color='green', linestyle='dashed', linewidth=1, label='Вчера')
    sns.lineplot(week_df, x='dt', y=df[metric], color='purple', linestyle='dotted', linewidth=1, label='Неделю назад')
            
    # строим графики доверительных интервалов
    sns.lineplot(df['upper_bound'], color='red', linewidth=1)
    sns.lineplot(df['lower_bound'], color='red', linewidth=1, label='Доверительные интервалы').set(xlabel='', ylabel='')

    # отметим аномальное значение
    plt.plot(today_df['dt'].iloc[-1], today_df[metric].iloc[-1], marker='o', markersize=10, color='red', label='Last Point')

# наведем красоту
    plt.tick_params(axis='x', rotation=90)
    plt.xlim(yesterday_df['dt'].iloc[0], yesterday_df['dt'].iloc[-1])
    plt.title('Активные пользователи ленты', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout();


# автоматизируем
@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)
def dag_alekaran_alert():
    
    @task()
    def extract_data():
        """выгружаем необходимые метрики, время и дату переводим в удобные форматы"""
        
        q = """
            SELECT *
            FROM (
                SELECT
                    toStartOfInterval(time, interval 15 minute) AS period,
                    toDate(time) AS date,
                    formatDateTime(toStartOfInterval(time, interval 15 minute), '%R') AS dt,
                    COUNT(DISTINCT user_id) AS feed_users,
                    SUM(action='like') AS likes,
                    SUM(action='view') AS views,
                    ROUND(likes / views, 3) AS ctr
                FROM simulator_20230720.feed_actions
                WHERE time >= today() - 7 and time < toStartOfFifteenMinutes(now())
                GROUP BY period, date, dt
            ) AS f
            JOIN (
                SELECT
                    toStartOfInterval(time, interval 15 minute) AS period,
                    COUNT(DISTINCT user_id) AS msg_users,
                    COUNT(reciever_id) AS messages
                FROM simulator_20230720.message_actions
                WHERE time >= today() - 7 and time < toStartOfFifteenMinutes(now())
                GROUP BY period
            ) AS m USING(period)
            ORDER BY period
        """
        
        df = ph.read_clickhouse(query=q, connection=connection)
        
        return df
    
    
    @task()
    def send_warning(df):
        """ф-я для отправление отчета об отличии в метрике"""
        
        # наши метрики
        metrics = ['feed_users', 'likes', 'views', 'ctr', 'msg_users', 'messages'] 
        
        # пройдемся по каждой метрике отдельно
        for metric in metrics:
            
            # вызываем функция получения названия метрики 
            title = get_title(df, metric)
                
            # формируем датасет только с нужными столбцами
            df_copy = df[['period', 'date', 'dt', metric]].copy()
            
            # проверяем на наличие отклонений
            is_outlier, df_bounds = get_outliers(df, metric)
            
            # в случае наличия отклонения в метрике - отправляем отчет
            if is_outlier in (1, 2):
                
                if is_outlier == 1:
                    add_msg_1 = 'нижней'
                    add_msg_2 = round(100 - df_bounds[metric].iloc[-1] / df_bounds['lower_bound'].iloc[-1]*100, 2)
                
                else:
                    add_msg_1 = 'верхней'
                    add_msg_2 = round(df_bounds[metric].iloc[-1] / df_bounds['lower_bound'].iloc[-1]*100, 2)
                
                # составляем текст и отправляем сообщение
                msg = (
                    f'<b>Метрика "{title}" в {df_bounds["period"].iloc[-1]}:</b>\n'
                    f'Текущее значение: {df_bounds[metric].iloc[-1]}\n'
                    f'Отклонение от {add_msg_1} границы доверительного интервала: {add_msg_2}%\n'
                    f'---ссылка на график---'
                )
                bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')
                
                # вызываем функцию построения графика
                build_plot(df, metric)
                
                # отправляем график через бот
                plot_object = io.BytesIO()
                plt.savefig(plot_object)
                plot_object.seek(0)
                plot_object.name = 'alert.png'
                plt.close()
                bot.sendPhoto(chat_id=chat_id, photo=plot_object)
                
            else:
                return None
    
    df = extract_data()
    send_warning(df)

dag_alekaran_alert = dag_alekaran_alert()