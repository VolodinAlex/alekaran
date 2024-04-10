# __Система алертов__

### __Разделы__
[1. Задача](https://github.com/VolodinAlex/alekaran/blob/AlekaranDS/Karpov.Courses/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D0%BE%D0%B2/README.md#1-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0)<br>

[2. Метрики](https://github.com/VolodinAlex/alekaran/blob/AlekaranDS/Karpov.Courses/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D0%BE%D0%B2/README.md#2-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA%D0%B8)<br>

[3. Этапы](https://github.com/VolodinAlex/alekaran/blob/AlekaranDS/Karpov.Courses/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D0%BE%D0%B2/README.md#3-%D1%8D%D1%82%D0%B0%D0%BF%D1%8B)<br>

[4. Результаты](https://github.com/VolodinAlex/alekaran/blob/AlekaranDS/Karpov.Courses/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D0%BE%D0%B2/README.md#4-%D1%80%D0%B5%D0%B7%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82%D1%8B)<br>

![](https://www.virtualmetric.com/blog/wp-content/uploads/2021/03/Blog-post-37_2.jpg)

### __1. Задача__
Настроить систему алертов - каждые 15 минут происходит проверка ключевых метрик. В случае обнаружения аномального значения TG-бот должен отправлять алерт с информацией.

### __2. Метрики__
- DAU в ленте и мессенджере
- views
- likes
- CTR 
- messages

### __3. Этапы__
- Создание телеграм-бота с помощью [@BotFather](https://t.me/BotFather)
- Рассчет оптимальных доверительных интервалов для каждой метрики в разные промежутки
- Построение ETL-пайплайн с отправлением алерта при отклонении 

### __4. Результаты__
Создан ETL-пайплайн для автоматизации системы алертов.  
Данная система имеет только демонстративное назначение, поскольку улушать доверительные интервалы с помощью различных методов, в т.ч. ML, можно до бесконечности в реальном продукте.

[![1.jpg](https://i.postimg.cc/kgcJpcPv/1.jpg)](https://postimg.cc/DSS3W1ZS)

:arrow_up:[back to contents](https://github.com/VolodinAlex/alekaran/blob/AlekaranDS/Karpov.Courses/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D0%BE%D0%B2/README.md#%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B)
