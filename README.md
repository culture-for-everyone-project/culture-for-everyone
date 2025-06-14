=======
<p align="center"> 
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png" alt="HAR Logo" width="80px" height="80px">
</p>
<h1 align="center"> КДК - Культура Для Каждого </h1>
<h3 align="center"> Сервис для поиска информации о картинах музея «Эрмитаж-Урал» через Telegram-бот  </h3>  

</br>

<p align="center"> 
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjZvOTUwcml6d3YxcTZudDQxY3pwOGptY2dnd3hnYWIwZTIzbTZwZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oEduGYoe2rHKbi55m/giphy.gif" alt="Sample signal" width="40%" height="40%">
</p>

<h2 id="table-of-contents"> :book: Навигация</h2>

<details open="open">
  <summary>Навигация</summary>
  <ol>
    <li><a href="#about"> ➤ О проекте</a></li>
    <li><a href="#func_description"> ➤ Описание функционала</a></li>
    <li><a href="#folder-structure"> ➤ Структура проекта</a></li>
    <li><a href="#file_description"> ➤ Описание файлов</a></li>
    <li><a href="#technology stack"> ➤ Стек технологий</a></li>
    <li><a href="#requirements_instruction"> ➤ Требования и инструкция по запуску</a></li>
    <li><a href="#datasets"> ➤ Датасеты</a></li>
    <li><a href="#links"> ➤ Ссылки</a></li>
    <li><a href="#contributors"> ➤ Участники</a></li>
  </ol>
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 id="about"> :small_orange_diamond: О проекте</h2>
<p align="justify">
  Современные любители искусства, студенты и просто любопытные зрители часто сталкиваются с трудностями при попытке быстро получить информацию о картинах и художниках в музейных пространствах. <br>
</p>
<p align="justify">
<ul>
  <li>
    При большом количестве людей нет времени или возможности вручную искать сведения об экспонатах. <br>
  </li>
  <li>
    Нахождение информации о произведения искусства в интернете или книгах затруднительно, особенно если это малоизвестное произведение или автор.
  </li>
</ul>
</p>

<p align="justify"> 
  Нужен способ открывать для себя новое, не затрачивая время на долгий поиск.
</p>
<p align="justify"> 
  Для устранения указанных проблем мы разрабатываем Telegram-бота, который позволяет пользователю узнать информацию о картинах по фотографии и не только.
  Достаточно отправить фото или название картины, чтобы получить краткую справку: название, автор, год создания, описание.
  Если пользователь не знает название или не может сделать фотографию (например, из-за большого скопления людей возле экспоната), он может воспользоваться встроенным каталогом. Все картины в базе распределены по коллекциям музея. 
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="func_description"> :small_orange_diamond: Описание функционала</h2>

1. **Найти картину по коллекциям музея**  
   - Пользователю отправляется список доступных коллекций музея.  
   - После выбора коллекции бот показывает список картин, которые в неё входят.  
   - Пользователь может выбрать любую картину и получить о ней подробную информацию.

2. **Найти картину по названию**  
   - Пользователь вводит название картины (или часть названия).  
   - Бот ищет совпадения в базе данных и выводит список подходящих вариантов.  
   - При выборе конкретной картины пользователь получает полную информацию о ней.  

3. **Найти картину по фото**  
   - Пользователь выбирает коллекцию, в которой нужно выполнить поиск.  
   - Затем загружает фотографию картины.  
   - Бот обрабатывает изображение с помощью компьютерного зрения и ищет совпадения в выбранной коллекции.  
   - Если картина найдена, пользователь получает о ней полную информацию.  
   - Если точного совпадения нет, бот может предложить похожие варианты или уточнить запрос.  

---

### Структура информационного сообщения о картине

- **Фотография**
- **Название**
- **Автор**
- **Время создания**
- **Материал и техника**: _[Холст/дерево/бумага, масло/акварель/темпера и т. д.]_
- **Размеры**: _[Ширина × высота в см]_
- **Ссылка на картину** (официальный сайт Эрмитаж-Урал)
- **Аудиолекция** (если доступна) и ссылка на сайт со всеми аудиолекциями
- **Описание картины**
- **Кнопка повторного поиска**
<img src="https://i.ibb.co/1Ydp5K31/photo-2025-06-12-00-46-16.jpg" height="640px" height="640px">
<img src="https://i.ibb.co/PvvNVY1k/photo-2025-06-12-00-46-16-2.jpg" width="305px" height="640px">


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 id="folder-structure"> :small_orange_diamond: Структура проекта</h2>

    project/
    ├── bot/
    │   ├── handlers.py
    │   └── keyboards.py
    ├── database/
    │   ├── db_requests.py
    │   └── db_tables.py
    ├── datasets/
    ├── models/
    │   ├── class_labels.py
    │   ├── configuration.py
    │   ├── model_1.h5
    │   ├── model_2.h5
    │   ├── model_3.h5
    │   ├── model_4.h5
    │   ├── model_training.py
    │   └── predictions.py
    ├── db.sqlite3
    └── main.py


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="file_description"> :small_orange_diamond: Описание файлов</h2>

- `main.py` — запускает Telegram-бота
- `bot/handlers.py` — логика диалога с пользователем
- `bot/keyboards.py` — кнопки для Telegram-интерфейса
- `database/db_requests.py` — функции добавления и получения данных из БД
- `database/db_tables.py` — инициализация таблиц MySQL/SQLite
- `models/predictions.py` — загрузка модели и получение предсказаний
- `models/model_training.py` — обучение MobileNetV2 на картинках
- `models/configuration.py` — параметры обучения
- `models/class_labels.py` — соответствие классов и названий картин
- `model_X.h5` — сохранённые модели для разных коллекций


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="requirements_instruction"> :small_orange_diamond: Cтек технологий</h2>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) <br>

В проекте используются следующие ключевые технологии и библиотеки с открытым исходным кодом:

- **Python 3.9+** — основной язык программирования проекта  
- **TensorFlow** — фреймворк для построения и запуска нейросетевых моделей  
- **Keras** — высокоуровневый API над TensorFlow для создания и обучения моделей  
- **NumPy** — работа с многомерными массивами и числовыми данными  
- **Scikit-learn (sklearn)** — оценка качества моделей, предобработка данных и метрики  
- **Aiogram** — асинхронный фреймворк для создания Telegram-бота  
- **SQLAlchemy** — ORM для взаимодействия с базой данных  
- **SQLite** — встроенная легковесная база данных для хранения информации о картинах и пользователях  



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="about"> :small_orange_diamond: Требования и инструкции по запуску</h2>

### Системные требования:
- **Python 3.9+**
- **pip** — менеджер пакетов Python  
- **Git** — (опционально, для клонирования репозитория)
  
### Инструкция по запуску:
Клонируйте репозиторий:
```
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```
Создайте и активируйте виртуальное окружение (рекомендуется):
```
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```
Установите зависимости:
```
pip install -r requirements.txt
```
Заполните файл конфигурации `configuration.py`:
```
BOT_TOKEN=ваш_токен_бота
```
Запустите бота:
```
python main.py
```
### Работа с моделями:
Если вы хотите обучить модели на своём датасете, укажите пути в файле `configuration.py`:
```
DATASET_PATH = "путь к основному датасету для обучения"
TEST_DATASET_PATH = "путь к тестовому датасету (примерно 25% от основного)"
VALIDATION_DATASET_PATH = "путь к валидационному датасету (примерно 10% от основного)"
```
Запустите обучение:
```
python model_training.py
```
### Работа с БД:
Для первоначальной инициализации таблиц используется файл `db_tables.py`.При первом запуске, если файл `db.sqlite3` отсутствует, он будет создан автоматически.
Для инициализации таблиц используется скрипт:
```
python db_tables.py
```


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="datasets"> :small_orange_diamond: Датасеты</h2>
<p>
Для обучения моделей был самостоятельно собран кастомный датасет по 4 коллекциям музея «Эрмитаж-Урал».
Каждая коллекция представлена отдельной папкой, в которой содержатся три подкаталога:

- `ds` — основной набор изображений для обучения модели  
- `ds_test` — изображения для тестирования  
- `ds_validation` — изображения для валидации модели
</p>

<p>Модели обучаются отдельно для каждой коллекции, что позволяет повысить точность классификации внутри определённого набора данных.</p>
Скачать датасеты можно по ссылке:

- 📁 [Яндекс Диск](https://disk.yandex.ru/d/ZMdzPGthYJdx5w)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="links"> :small_orange_diamond: Ссылки</h2>

- [Презентация проекта](https://docs.google.com/presentation/d/1Vi3PQfl1g88crGU1cfIGv1wuJnUB_Aj-/edit?usp=drive_link&ouid=103828314448526200968&rtpof=true&sd=true)
- [Видео-демонстрация](https://drive.google.com/file/d/1yiXJ_PzVEevlAcIh1yh_5hBn-P17FouF/view?usp=drive_link)
- [Google Drive](https://drive.google.com/drive/u/1/folders/1SqW4DWadmEfX75dRZIVHQgjVDyDJr1gC)
- [Эрмитаж-Урал](https://i-z-o.art/constitutor/centr-ermitazh-ural/)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="contributors"> :small_orange_diamond: Участники</h2>

<p>
  <i>:mortar_board: Все участники этого проекта являются студентами программы <a href="https://programms.edu.urfu.ru/ru/10591/"> «Алгоритмы искусственного интеллекта»</a> <b> </b> <a href="https://rtf.urfu.ru/ru/"> Института радиоэлектроники и информационных технологий — РТФ Уральского федерального университета имени Б. Н. Ельцина.</a></i> <br> <br>
   
  :diamond_shape_with_a_dot_inside: <b>Молчанова Полина Алексеевна</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>07lllllll07lllllll@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/aaaaaaa0">@aaaaaaa0</a> <br>
  
  :diamond_shape_with_a_dot_inside: <b>Пластеева Ксения Евгеньевна</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>kseniaplasteeva45561@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/KseniaPlasteeva">@KseniaPlasteeva</a> <br>

  :diamond_shape_with_a_dot_inside: <b>Ступаченко Екатерина Евгеньевна</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>katya.62442@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/tnixf">@tnixf</a> <br>

  :diamond_shape_with_a_dot_inside: <b>Тетенькина Екатерина Владимировна</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>fikusekaterina8@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/f-f-i">@f-f-i</a> <br>

  :diamond_shape_with_a_dot_inside: <b>Филипович Илья Андреевич</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>llilay293@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/IlyaF7">@IlyaF7</a> <br>

  :diamond_shape_with_a_dot_inside: <b>Шитникова Анастасия Сергеевна</b> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>shitnikovanastya2006@gmail.com</a> <br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/shitnikov-a">@shitnikov-a</a> <br>
</p>

<i>
  Учебный проект, реализованный в рамках дисциплины «Проектный практикум».<br>
  Команда «Генератор букв».<br>
  Июнь 2025 г.
</i>

