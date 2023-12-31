# Romantik
Цей проєкт — код [веб-сайту туристичного клубу "Романтик"](https://www.romantik.pp.ua/news/). Написаний на Django, він знаходиться у вільному доступі та розповсюджується за відкритою ліцензією [Apache 2.0](https://snyk.io/learn/apache-license/), що дає повне право іншим розробникам на подальше використання цієї кодової бази.

Ви також можете самі прийняти участь у розробці цього проєкту. Задля цього, ви можете розгорнути веб-сайт на локальній машині, внести зміни та відправити Pull Request в main. Як розгорнути проєкт на локальній машині — вказано нижче. Будемо вдячні за будь-яку співпрацю!
## Як розгорнути на локальній машині?
1. Клонувати цей репозиторій
   
   У консолі, перейдіть у папку, де ви хочете розгорнути проєкт. На більшості систем, це відбувається за допомогою команди

       cd <your_folder>
   
   Пропишіть
   
       git clone https://github.com/Casy7/Romantik.git
   
   Зачекайте, допоки проєкт завантажиться на вашу машину.
   
2. Перейдіть у папку проєкту.

   Задля цього, напишіть

       cd Romantik

3. Встановіть Python

   Для Unix-подібних систем пропишіть 

       apt install python

   Для Windows — завантажте останню версію з [офіційного дистрибутиву Python](https://www.python.org/downloads/) та встановіть її. Під час встановлення, оберіть пункт `Add Python to PATH`.

4. Встановіть необхідні бібліотеки для роботи сайту з `requirements.txt`.

   Щоб зробити це в автоматичному режимі, пропишіть команду

       pip install -r requirements.txt

5. Підготуйте проєкт до першого запуску.

   Для цього виконайте таку команду:

       python manage.py migrate

6. Запустіть проєкт.

   Пропишіть

       python manage.py runserver 8000

   В консолі повинно відображатись щось на кшталт цього:

       System check identified no issues (0 silenced).
       August 20, 2023 - 13:22:04
       Django version 4.2, using settings 'romantik.settings'
       Starting development server at http://127.0.0.1:8000/
       Quit the server with CTRL-BREAK.
   
7. Перевірте, чи працює сайт у вашій петлі зворотнього зв'язку.
Перейдіть у бровзері за посиланням [127.0.0.1:8000](http://127.0.0.1:8000/). Якщо там відображається головна сторінка веб-сайту, то вітаємо, ви це зробили!
   
