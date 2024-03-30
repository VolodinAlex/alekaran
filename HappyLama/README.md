# __HappyLama__

### __О компании__
[HappyLama](https://t.me/HappyLama_vetproducts) — ветеринарная онлайн-аптека в Тбилиси (Грузия).  
Создана автоматизированная система учета препаратов на базе [Google Sheets](https://www.google.com/sheets/about/) с учетом остатков, списывания проданных и добавления новых, а также полноценная система аналитики. Предоставлена демонстративная версия созданной мной системы учета. 
* Все данные внутри созданы искусственно и не отражают реальные метрики продукта!
[![image.png](https://i.postimg.cc/Xq0B5C3F/image.png)](https://postimg.cc/KkJYS41v)

[Ветеринарная онлайн-аптека Демо](https://docs.google.com/spreadsheets/d/1Sn59xFjlPfg8_xuweihIqL_it1Y7l3HHdHXW6qaaM_c/edit?usp=sharing)

### __Структура__  
**Блок 1. Учет**  
Наименование товара, рассчет количества доступных к продаже препаратов с учетом текущих закупков, остатков с прошлого месяца и проданных в этом месяц

**Блок 2. Продажи**  
При вводе наименования препарата выводится его цена, а при указании количества проданных единиц происходит рассчет дохода и прибыли с учетом скидки и цены закупки. При этом изменяется информация в блоке 1. 

**Блок 3. Закупка**  
При добавлении товара (а также его закупочной стоимости и количества) происходит обновление данных в блоке 1.

**Блок 4. Инвентаризация**  
Здесь происходят рассчеты закупочной цены и маржинальность на каждое наименование, а также рассчет рекомендуемой цены с учетом желаемой маржинальности. 

### __Используемые функции__
- [vlookup](https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1)
- [hlookup](https://support.microsoft.com/en-au/office/hlookup-function-a3034eec-b719-4ba3-bb65-e1ad662ed95f)
- [arrayformula](https://support.google.com/docs/answer/3093275?hl=ru)
- [sumifs](https://support.microsoft.com/en-gb/office/sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b)
- [countifs](https://support.microsoft.com/en-gb/office/countifs-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842)
- [iferror](https://support.microsoft.com/en-au/office/iferror-function-c526fd07-caeb-47b8-8bb6-63f3e417f611)
- [ifs](https://support.microsoft.com/en-gb/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45)
- [isblank](https://support.google.com/docs/answer/3093290?hl=ru)
- прочие стандартные арифметические и логические функции.
