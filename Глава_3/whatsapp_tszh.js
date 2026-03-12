/**
 * Система автоматических уведомлений через WhatsApp для ТСЖ и УК
 *
 * Данный скрипт загружает список жильцов из Excel-файла и отправляет им сообщения через WhatsApp.
 * Используется библиотека whatsapp-web.js для взаимодействия с WhatsApp Web.
 *
 * Подготовка окружения *
 * 1. Установите Node.js:
 *    - Скачайте LTS версию с официального сайта nodejs.org
 *    - Проверьте установку командой: `node -v`
 *
 * 2. Установите необходимые библиотеки:
 *    npm install whatsapp-web.js xlsx qrcode-terminal
 *
 * Подготовка данных *
 * Создайте Excel-файл `TSZH.xlsx` со следующими колонками:
 * - Name (Имя жильца)
 * - Phone number (Номер телефона)
 * - Car (Марка автомобиля, опционально)
 * 
 * Подробнее о скрипте: https://habr.com/ru/articles/876216/
 * 
 */

// Импорт необходимых библиотек
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const xlsx = require('xlsx');
const path = require('path');

// Путь к Excel-файлу с данными
const excelFilePath = path.join(__dirname, 'TSZH.xlsx');

// Читаем данные из Excel-файла
console.log("Чтение данных из Excel-файла...");
const workbook = xlsx.readFile(excelFilePath);
const sheetName = workbook.SheetNames[0];
const data = xlsx.utils.sheet_to_json(workbook.Sheets[sheetName]);

// Вывод данных в консоль сразу после чтения
console.log("Данные из Excel-файла:", data);

// Настройка клиента WhatsApp
console.log("Инициализация клиента WhatsApp...");
const client = new Client({
    authStrategy: new LocalAuth()
});

// Генерация QR-кода
client.on('qr', qr => {
    console.log("Сканируйте этот QR-код в приложении WhatsApp:");
    qrcode.generate(qr, { small: true });
});

// Когда клиент готов
client.on('ready', async () => {
    console.log("Клиент WhatsApp готов к отправке сообщений.");

    // Функция для отправки сообщения с задержкой
    const sendMessageWithDelay = async (person, delay) => {
        return new Promise(resolve => {
            setTimeout(async () => {
                // Проверка наличия имени и номера телефона, чтобы избежать ошибок
                if (!person.Name || !person['Phone number']) {
                    console.error(`Ошибка: Отсутствует имя или номер телефона для записи:`, person);
                    return resolve(); // Переходим к следующей записи
                }

                // Преобразуем номер телефона в строку, если он число
                let phoneNumber = person['Phone number'];
                if (typeof phoneNumber === 'number') {
                    phoneNumber = String(phoneNumber);
                }

                // Удаляем все нецифровые символы из номера и добавляем суффикс WhatsApp
                phoneNumber = phoneNumber.replace(/\D/g, '') + '@c.us';


                const message = `Уважаемый(ая) ${person.Name},

Завтра будет проводиться уборка снега с 9:00 до 18:00. Просим вас заранее убрать автомобиль ${person.Car || ' '} с парковки, чтобы работа прошла быстро и качественно. 

Спасибо за понимание!`;

                try {
                    await client.sendMessage(phoneNumber, message);
                    console.log(`Сообщение успешно отправлено на номер ${person['Phone number']}.`);
                } catch (err) {
                    console.error(`Ошибка при отправке сообщения на номер ${person['Phone number']}:`, err);
                }
                resolve();
            }, delay);
        });
    };


    // Персонализированная рассылка сообщений с задержкой
    for (let i = 0; i < data.length; i++) {
        // Задержка 4 секунды между сообщениями (15 сообщений в минуту)
        await sendMessageWithDelay(data[i], i * 4000);
    }

});

// Обработка ошибок
client.on('auth_failure', () => {
    console.error("Ошибка авторизации. Проверьте свои учетные данные.");
});

client.on('disconnected', () => {
    console.log("Клиент WhatsApp был отключен.");
});

// Запуск клиента
client.initialize();