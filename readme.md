# Home Security

> **If You speak English you can help me to translate this page. Thank you!**

**Home Security** позволяет автоматически обнаруживать на видео посторонних людей.

![Imgur](https://i.imgur.com/Wmvv9yV.png)

## Установка и настройка
Список используемых пакетов находится в `req.txt`.

Настройки находятся в папке `Configuration`

* `camera_config.json`
    * `fps` - "скорость" чтения с источника
    * `cameras` - список камер
        * `name` - имя, используемое в логе
        * `source` - источник (порт, путь)
* `notification_config.json` 
    * `password` - рекомендуется создать ключ приложения
    * `bot_key` - API-KEY бота `@alarmer_bot`

## Основные возможности

* В качестве источника видео можно указать: 
    * номер камеры
    * видеофайл
    * URL
* Возможность добавлять доверенные лица в базу данных. С ними позже будут сравниваться обнаруженные на видео лица
* Возможность отключать определенные этапы обработки
* Возможность настройки уведовлений по e-mail (пока только GMail) или Telegram (через `@alarmer_bot`)