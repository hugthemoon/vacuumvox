# Vacuumvox

**Vacuumvox** — это утилита для создания кастомных озвучек пылесосов. Проект предоставляет инструменты для транскрипции, конвертации аудио в формат mp3 и упаковки в tar.gz архив.

### Возможности
- **Транскрипция аудиофайлов**: автоматическое преобразование аудиофайлов в текст.
- **Конвертация в mp3**: поддержка различных аудиоформатов с возможностью настройки частоты, битрейта и каналов.
- **Упаковка в tar.gz**: удобная сборка готовой озвучки для передачи на устройство.

### Требования
Для работы проекта необходим [Python](https://www.python.org/downloads/) 3.12+.

### ️Установка
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/hugthemoon/vacuumvox.git
   cd vacuumvox
   ```
2. Установите зависимости
   ```bash
   pip install poetry 
   poetry install
   poetry run ffdl install --add-path
   ```
3. Перезапустите терминал, чтобы применить настройки окружения
4. Откройте виртуальное окружение
   ```bash
   poetry shell
   ```
### Использование
Транскрипция аудиофайлов
   ```bash
  python manage.py transcribe --input <папка_с_аудио> --out <файл_с_текстом> [--lang <язык>]
   ```

Пример
   ```bash
   python manage.py transcribe --input .\example --out transcribe.txt --lang ru-RU
   ```
   
Конвертация и упаковка в архив
   ```bash
  python manage.py pack --input <папка_с_аудио> --out <имя_архива.tgz> [--codec <кодек>] [--frequency <частота>] [--bitrate <битрейт>] [--channels <каналы>]
   ```
Пример
   ```bash
   python manage.py pack --input .\example --out custom.tgz --frequency 22050 --bitrate 256k --channels 1
   ```
