#!/bin/bash

# Скрипт для преобразования всех файлов (включая вложенные папки) в текстовый вид

# Функция для определения языка файла по расширению
get_language() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        py) echo "python" ;;
        js) echo "javascript" ;;
        ts) echo "typescript" ;;
        yaml|yml) echo "yaml" ;;
        json) echo "json" ;;
        xml) echo "xml" ;;
        html|htm) echo "html" ;;
        sql) echo "sql" ;;
        md|markdown) echo "markdown" ;;
        txt|log) echo "text" ;;
        *) echo "text" ;;
    esac
}

# Проверяем, есть ли файлы в текущей директории
if [ ! "$(ls -A . 2>/dev/null)" ]; then
    echo "В текущей папке нет файлов для обработки."
    exit 1
fi

# Создаем или очищаем выходной файл
output_file="all_files_content.md"
> "$output_file"

# Добавляем заголовок с текущей датой и временем
current_time=$(date '+%Y-%m-%d, %H:%M')
echo "Ниже мои файлы по состоянию на $current_time:" >> "$output_file"
echo >> "$output_file"

echo "Начинаю преобразование файлов в текстовый вид..."
echo "Результат будет сохранен в файл: $output_file"
echo

# Счетчик обработанных файлов
count=0

# Обходим все файлы рекурсивно, используя find
while IFS= read -r -d '' file; do
    # Пропускаем сам выходной файл
    if [ "$file" = "./$output_file" ]; then
        continue
    fi
    
    # Пропускаем сам скрипт
    if [[ "$(basename "$file")" == "+files_to_text.sh" ]] || [[ "$(basename "$file")" == "+files_to_text.txt" ]]; then
        continue
    fi
    
    # Проверяем, можно ли прочитать файл
    if [ ! -r "$file" ]; then
        echo "Предупреждение: Файл '$file' недоступен для чтения. Пропускаю..."
        continue
    fi
    
    # Проверяем, является ли файл текстовым
    if file "$file" | grep -qE 'text|empty|JSON|XML|HTML|script'; then
        # Записываем заголовок с относительным путем
        echo "Файл $file:" >> "$output_file"
        
        # Пустая строка после имени файла
        echo >> "$output_file"
        
        # Определяем язык для подсветки синтаксиса
        lang=$(get_language "$file")
        echo "\`\`\`$lang" >> "$output_file"
        
        # Записываем содержимое файла
        cat "$file" >> "$output_file"
        
        # Закрываем блок кода с новой строки
        echo '' >> "$output_file"
        echo '```' >> "$output_file"
        
        # Добавляем пустую строку для разделения
        echo >> "$output_file"
        
        # Увеличиваем счетчик
        ((count++))
        
        echo "Обработан файл: $file (язык: $lang)"
    else
        echo "Пропущен бинарный файл: $file"
    fi
done < <(find . -type f -print0)

echo
if [ $count -eq 0 ]; then
    echo "Не найдено файлов для обработки."
    rm -f "$output_file"
else
    echo "Завершено! Обработано файлов: $count"
    echo "Результат сохранен в файл: $output_file"
fi