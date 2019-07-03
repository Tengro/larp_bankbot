# larp_bankbot
LARP BankBot: бот загального користування для імплементації банкінгу на рольових іграх живої дії

## Для чого це потрібно?
Мета розробки даного проекту - поширення використання сучасних технологій у РІЖД; найбільш очевидна система, що часто стає у нагоді у грі - банківська система. Даний код дозволяє заощадити масу зусиль і розвернути типовий банкінг для будь-якої гри за півгодини, використовуючи ботів Telegram.

Деталі про використання програмних продуктів у рольвих іграх живої дії дивіться у [матеріалах моєї лекції для конвенту d!RDay-2019](https://docs.google.com/presentation/d/14e2WuS1jtmjxMIZkIlZ0sjbuK5w5bhYXUW2XqQo1IlI/edit?usp=sharing)

## Встановлення
### Завантаження
Завантажте код з репозиторію в будь-яку зручну для вас папку на вашому комп'ютері. Переконайтеся, що в вас встановлено Python версії 3.6.3 або новіше і остання версія PIP. Після встановлення Python та PIP у папці, в яку ви завантажили код, виконайте команду:

`pip install -r requirements.txt`

для встановлення необхідних пакетів.

[Інструкція з встановлення Python](https://uk.wikibooks.org/wiki/%D0%9F%D0%BE%D1%80%D0%B8%D0%BD%D1%8C%D1%82%D0%B5_%D1%83_Python_3/%D0%92%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F)\
[Інструкція з встановлення PIP](http://programming.in.ua/programming/python/248-install-pip-python.html)

### Отримання токену
Перш ніж запускати LARP BankBot, вам буде необхідно зареєструвати бота у Telegram та отримати унікальний ID бота (він працює і як токен)
Для цього в Telegram існує спеціальний бот — @BotFather.

Напишіть йому /start щоб отримати список команд.
Головна команда — /newbot — відправте його цьому боту і він попросить вказати ім'я вашого бота (воно обов'язково має закінчуватися на "bot"). Якщо все вийшло, BotFather поверне повідомлення з токеном бота та лінкою на нього. Тут можна вказати аватар бота.

### Запуск бота
Отриманий токен вставте у файл settings.py (лежить у папці "bank_bot") в якості значення змінної. Ви маєте отримати у файлі наступний рядок:

`BOT_TOKEN = "(ваш токен бота, лапки обов'язкові)"`

Після цього запустіть через python файл run_bank_bot.py:

`python run_bank_bot.py`

І напишіть вашому боту команду /start

Вітаю! Ви запустили активного бота для банкінгу!

Якщо ви - майстер гри, для якої ви створили цього бота, одразу ж введіть команду
`/create_admin`

Ця команда прив'яже ваш аккаунт у Telegram до цього бота в якості адміністративного аккаунту.

## Налаштування
Даний бот має відносно малу кількість налаштувань переважно косметичного характеру; у даній інструкції будуть розглянуті основні з них. Усі налаштування знаходяться у файлі settings.py у папці bank_bot
### Основні налаштування
BOT_TOKEN = "" - Токен бота. Необхідно вказати для роботи\
DATABASE_FILE = "bot_base.db" - Адреса бази даних. Не змінюйте, якщо не певні у тому, що робите!\
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S" - Формат виведення дати та часу.\
HACKING_ALLOWED = True - Вказує, чи активний додатковий модуль "хакінгу". Вкажіть True для ввімкнення, False для вимкнення

### Текст повідомлень
У тому ж файлі існує набір текстів повідомлень бота. Їх також можна редагувати - наприклад, для перекладу або більшої відповідності стилістиці гри.

## Загальний список команд
Повний список команд, доступ до яких є у всіх зареєстрованих у системі користувачів. Тут і далі квадратні дужки використовуться лише як означення того, що замість них має бути вказане те, що в них згадується.

`/start` - прочитати привітання\
`/help` - довідка/список загальних команд\
`/admin_help` - довідка/список адміністративних команд\
`/hacker_help` -  довідка/список хакерських команд\
`/register [ім'я персонажа]` - реєстрація персонажа (1 персонаж на 1 користувача на 1 бота)\
`/inspect` - дані про персонажа (якщо його зареєстровано)\
`/message [хеш персонажа] [текст повідомлення]` - передати повідомлення через бота (підписане хешем вашого персонажа)\
`/list_sent` - вивести список надісланих транзакцій \
`/list_recieved` - вивести список отриманих транзакцій\
`/send [хеш персонажа] [сума]` - надіслати вказану суму персонажу з вказаним хешем з рахунку свого персонажа\

### Приклади використання
`/register Морган Кларк` - рєеструє у системі персонажа під ім'ям "Морган Кларк"; повертає користувачу хеш цього персонажа. Саме хеш є основним ідентифікатором і дозволяє взаємодіяти з іншими персонажами у системі. 
Якщо спробувати зареєструватися другий раз, система видасть повідомлення про те, що на ваш юзернейм уже прив'язано персонажа (або, якщо ви спробуєте зареєструвати такого ж персонажа з іншого юзернейму - про те, що такий персонаж уже існує)
`/inspect` - повертає дані про персонажа "Морган Кларк"
`/send 0000000000 1000` - надсилає 1000 одиниць фінансів з рахунку персонажа "Морган Кларк" (вашого персонажа) на рахунок персонажа з хешем "0000000000" (це - службовий хеш, що встановлюється головному адміністратору гри при його створенні). Якщо у персонажа "Морган Кларк" недостатньо фінансів - транзакція не відбудеться, а система повідомить вас про це.

## Підсистема хакерської активності
У випадку, якщо у налаштуваннях встановлено `HACKING_ALLOWED = True` (за замовчуванням це саме так), окрім системи банкінгу і обміну повідомленнями активується підсистема хакерства. Вона скоріш рудиментарна на даному етапі розробки, але дозволяє надати певного флеру хакерства грі.

### Можливості хакера
Отже, хакер (будь-який персонаж, у якого параметр *Рівень хакерських здібностей* більше за 1) має наступний список можливостей:

- Надсилання анонімного повідомлення\
- Отримання доступу до загальних даних про користувача\
- Отримання доступу до списку транзакцій (як надісланих, так і отриманих)\

Основне обмеження: у випадку, якщо рівень захисту від зламу у цілі більший або рівний за рівень хакерських здібностей хакера, ціль отримує повідомлення про те, яку саме інформацію і хто саме (вказується хеш, а не ім'я персонажа) отримав.

### Список хакерських команд
Доступ до будь-якої з команд цього списку потребує, щоб рівень хакерських здібностей персонажа був більший за 0
`/hacker_help` -  довідка/список хакерських команд;\
`/h@ck_user [хеш персонажа]` - отримайте дані про профіль вказаного персонажа\
`/h@ck_list_recieved [хеш персонажа]` - вивести список отриманих транзакцій для обраного персонажа\
`/h@ck_list_sent [хеш персонажа]` - вивести список надісланих транзакцій для обраного персонажа\
`/mess@ge [хеш персонажа] [текст повідомлення]` - надішліть анонімне повідомлення персонажу\


## Адміністративні команди
Адміністратори гри (майстри) мають певний набір команд, що дають їм додатковий доступ до гри. Список команд адміністратора (для доступу до них флаг is_admin у персонажа має бути більше 0 - окрім команди `/create_admin`)

`/admin_help` - довідка/список адміністративних команд\
`/create_admin` - створення адміністративного користувача (якщо його ще не існує)\
`/delete [хеш персонажа]` - видалення персонажа\
`/inspect_all` - дані про всіх зареєстрованих персонажів гри\
`/set_attribute [хеш персонажа] [назву атрибуту; одне зі списку - finances|hacker_level|hacker_defence|is_admin] [нове значення атрибуту]` - встановити атрибут персонажа рівним значенню\


## Плани розвитку
- Покращити роботу з базою даних
- Покрити код боту достатньо щільними тестами
- Розвивати бота відповідно до запитів спільноти

Щиро ваш, Андрій Лящук a.k.a. Tengro
