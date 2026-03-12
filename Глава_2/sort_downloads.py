# Импортируем необходимые библиотеки
import shutil
from pathlib import Path

# 1. Указываем путь к папке, в которой нужно навести порядок
# ВНИМАНИЕ: Замените "Михаил" на имя вашего пользователя в системе!
# Префикс r'...' важен для Windows, он гарантирует корректное чтение пути.
downloads_path = Path(r"C:\Users\Михаил\Downloads")

# 2. Описываем "правила сортировки" в виде словаря
# Ключ — это название папки, а значение — список расширений.
file_categories = {
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Документы": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".pptx"],
    "Архивы": [".zip", ".rar", ".7z"],
    "Музыка и Видео": [".mp3", ".wav", ".mp4", ".mov", ".avi"],
    "Прочее": []  # Сюда попадет все, что не подошло в другие категории
}

# 3. Создаем целевые папки, если они еще не существуют
for category in file_categories.keys():
    category_path = downloads_path / category
    # Метод .mkdir() с параметром exist_ok=True очень удобен:
    # он создает папку и не выдает ошибку, если она уже есть.
    category_path.mkdir(exist_ok=True)

# 4. Главный цикл: проходим по каждому элементу в папке "Загрузки"
print(f"Начинаю сортировку в папке: {downloads_path}")
for file_path in downloads_path.iterdir():
    # Нам нужны только файлы, папки мы пропускаем
    if file_path.is_file():
        # Определяем категорию файла по его расширению
        file_extension = file_path.suffix.lower() # .suffix получает расширение, .lower() приводит его к нижнему регистру
        target_category = "Прочее"  # Категория по умолчанию

        # Ищем, в какую категорию попадает наше расширение
        for category, extensions in file_categories.items():
            if file_extension in extensions:
                target_category = category
                break # Нашли подходящую категорию, выходим из внутреннего цикла

        # 5. Перемещаем файл в нужную папку
        target_folder = downloads_path / target_category
        shutil.move(str(file_path), str(target_folder))
        print(f"Файл '{file_path.name}' перемещен в папку '{target_category}'")

print("Сортировка завершена! В папке 'Загрузки' теперь идеальный порядок.")