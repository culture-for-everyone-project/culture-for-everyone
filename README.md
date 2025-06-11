<p align="center"> 
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png" alt="HAR Logo" width="80px" height="80px">
</p>
<h1 align="center"> КДК - Культура Для Каждого </h1>
<h3 align="center"> Сервис для поиска информации о картинах музея "Эрмитаж-Урал" через Telegram-bot  </h3>  

</br>

<p align="center"> 
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjZvOTUwcml6d3YxcTZudDQxY3pwOGptY2dnd3hnYWIwZTIzbTZwZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oEduGYoe2rHKbi55m/giphy.gif" alt="Sample signal" width="70%" height="70%">
</p>

<h2 id="table-of-contents"> :book: Навигация</h2>

<details open="open">
  <summary>Оглавление</summary>
  <ol>
    <li><a href="#about"> ➤ О проекте</a></li>
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

<h2 id="about"> :pencil: О проекте</h2>

<p align="justify"> 
  Современные любители искусства, студенты и просто любопытные зрители сталкиваются с трудностями при попытке быстро получить информацию о картинах и художниках.
  - При большом количестве людей в  музеях нет времени или возможности вручную искать сведения об экспонатах.
  - Нахождение информации о произведения  искусства в интернете или книгах затруднительно, особенно если это малоизвестное произведение или автор.
  - Посетители сталкиваются с необходимостью быстро находить справочные данные о произведениях. 
  Нужен способ открывать для себя новое, не затрачивая время на долгий поиск.

  Для устранения указанных проблем мы разрабатываем Telegram-бота, который позволяет пользователю узнать информацию о картинах по фотографии и не только.
  Достаточно отправить фото или название картины, чтобы получить краткую справку: название, автор, год создания, описание.
  Если пользователь не знает название или не может сделать фотографию (например, из-за большого скопления людей возле экспоната), он может воспользоваться встроенным каталогом. Все картины в базе распределены по коллекциям  музея. 

</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2 id="folder-structure"> :large_blue_diamond: Структура проекта</h2>

    code
    .
    ├── bot
    │   ├── handlers.py
    |   └── keyboards.py
    |── database
    |   |── db_requests.py
    |   └── db_tabels.py
    |── datasets
    |── models
    |   |── class_labels.py
    |   |── configuration.py
    |   |── model_1.h5
    |   |── model_2.h5
    |   |── model_3.h5
    |   |── model_4.h5
    |   |── model_training.py
    |   └── predictions.py
    |── db.sqlite3
    |── main.py


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="file_description"> :pencil: Описание файлов</h2>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="requirements_instruction"> :large_blue_diamond: Cтек технологий</h2>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) <br>

В этом проекте используются следующие пакеты с открытым исходным кодом:
* TensorFlow


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="about"> :pencil: Требования и инструкции по запуску</h2>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="datasets"> :floppy_disk: Датасеты</h2>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="links"> :books: Ссылки</h2>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="contributors"> :scroll: Участники</h2>

<p>
  :mortar_board: <i> Все участники этого проекта являются студентами программы <a href="https://programms.edu.urfu.ru/ru/10591/"> «Алгоритмы искусственного интеллекта»</a> <b>@</b> <a href="https://rtf.urfu.ru/ru/"> Института радиоэлектроники и информационных технологий — РТФ Уральского федерального университета имени Б. Н. Ельцина.</a></i> <br> <br>
  
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

<br>
<i>Учебный проект, реализованный в рамках дисциплины «Проектный практикум».<i>
<i><a>Команда «Генератор букв»</a><i>
<i><a>Июнь 2025 г.</a><i>
