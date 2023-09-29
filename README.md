# scavenger
Скрипт поиска мусорных файлов.

## Запуск

1. Перейдите в папку **scripts** и запустите скрипт:

   - **install.bat**, если Вы работаете в *Windows*;

   - **install.sh**, если Вы работаете в *Linux/macOS*:

     ```bash
     bash install.sh
     ```

2. Перейдите в папку **scripts** и запустите скрипт:

   - **run.bat**, если Вы работаете в *Windows*;

   - **run.sh**, если Вы работаете в *Linux/macOS*:

     ```bash
     bash run.sh
     ```

3. Вместо предыдущего пункта можете в терминале перейти в корневую папку репозитория и выполнить команду:

   - если Вы работаете в *Windows*:

     ```batch
     venv\Scripts\python run.py --dir DIR --verbose
     ```

   - если Вы работаете в *Linux/macOS*:

     ```bash
     venv/bin/python run.py --dir DIR --verbose
     ```

   В указанных командах используется опциональный флаг:

   - *--dir* - путь до директории, в которой нужно найти мусор;
   - *--verbose* - скрипт будет выводить пути до найденных мусорных файлов в реальном времени.

## Запуск тестов

1. Перейдите в папку **scripts** и запустите скрипт:

   - **install.bat**, если Вы работаете в *Windows*;

   - **install.sh**, если Вы работаете в *Linux/macOS*:

     ```bash
     bash install.sh
     ```

2. Перейдите в папку **scripts** и запустите скрипт:

   - **run_tests.bat**, если Вы работаете в *Windows*;

   - **run_tests.sh**, если Вы работаете в *Linux/macOS*:

     ```bash
     bash run_tests.sh
     ```

## Конфигурационные файлы

В папке **config** находятся конфигурационные файлы **junk.txt** и **exceptions.txt**. Каждая строка в этих файлах задает шаблон. Скрипт ищет в файловой системе каталоги и файлы, которые соответствуют отдельным шаблонам из файла **junk.txt** и не соответствуют ни одному шаблону из файла **exceptions.txt**. Такие файлы и каталоги считаются мусорными.

#### Формат шаблона

- Пустая строка не соответствует ни одному файлу. Поэтому пустая строка может использоваться в качестве разделителя для удобства чтения.

- Строка, начинающаяся с символа "#", служит комментарием. Если Вы хотите задать шаблон, который начинается с символа "#", поставьте обратную косую черту "\\" перед "#".

- Косая черта "/" используется в качестве разделителя каталогов. Разделители могут встречаться в начале, середине или конце шаблона поиска.

- Если в конце шаблона есть косая черта "/", то шаблон будет соответствовать только каталогам. В противном случае шаблон может может соответствовать как файлам, так и каталогам.

- Звездочка "*" соответствует всему.

- Для обозначения набора символов, которые могут находиться в определенной позиции, используйте квадратные скобки "[]". Например, шаблону "som[ae]pattern" будут соответствовать строки "somepattern" и "somapattern".

- Для шаблона можно задать сообщение, которое будет выводиться на экран, когда для данного шаблона находится совпадение. Для этого в конфигурационный файл нужно написать строку вида:

  ```
  шаблон | Здесь можно написать любое сообщение
  ```

  
