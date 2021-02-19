# quik_python_connector
------------------------
Асинхронный адаптер lua api для торгового терминала Quik. Основан на пакете quik-lua-rpc и библиотеке для python3 qlua. 
Состоит из 2-х подмодулей connector и trade. Для корректной работы требуется `python => 3.8`.
 
Для лучшего понимания смотрите: [документация автора quik-lua-rpc](https://github.com/Enfernuz/quik-lua-rpc#quik-lua-rpc).


## connector
Модуль для работы с асинхронной работы с библиотекой qlua напрямую. Для лучшего понимания читайте: [документация для qlua](https://gitlab.com/abrosimov.a.a/qlua/-/wikis/home)

###connection.py
Управляет запросами и ответами в Quik, для пользователя в режиме REQ/REP. Запросы кодируются в Protocol Buffers и отправляются с помощью ZeroMQ 
отправлять по url, указанному в настройках, а именно в `connector/settings.py`

###events.py
Подписывается на события Quik, для пользователя в режиме PUB/SUB. Все возможные события описаны в [API lua для Quik](http://luaq.ru/).
Пример подписки на события:

```python
from connector.events import Dispatcher, EventTypes

def printer(response):
    print(response)

Dispatcher().subscribe(EventTypes.ON_QUOTE, callback=printer)
```

###managers.py
Модуль разбит на 4 основных класса по смыслу, все функции описаны в документации по [API lua для Quik](http://luaq.ru/)

###settings.py
Файл для настроек соединения с quik-lua-rpc. Существует 2 типа соединения REQ и SUB. 
Для каждого отдельно можно создать пользователя или не создавать, как в примере. 
(Для удобства было принято решение сделать username и password такими же как и в Quik) 
Эти настройки *должны быть такими же*, как и в файле `lua/quik-lua-rpc/config.json`.

## trade
Модуль добавляет удобные оболочки для работы с модулем connector. 

### base.py
В этом модуле описаны основные базовые классы, такие как Transaction, Order, StopOrder, Bar и др.

### managers.py
В данном модуле описаны класс-оболочки для базовых классов из `connector/managers.py`

## Логгирование
Данное ПО поддерживает логгирование. В корневом каталоге в файле `settings.py` лежат 
настройки для модуля logger. Все логи лежат в каталоге `/logs`, логи запросов и ответов Quik лежат в `connector.log`, 
все приходящие события лежат в `events.log`, ошибки – в `error.log`


## Установка
1. Установка quik-lua-rpc. Для работы необходимо скачать [quik-lua-rpc](https://github.com/BelovN/quik-lua-rpc), установить его в Quik и запустить.
Для установки необходимо распаковать `built/quik_lua_rpc.tar.xz` в каталог установленного терминала Quik (например, `D:/QUIK/`).


2. Установка quik_python_connector. Скачать текущий репозиторий и настроить виртуальную среду.
Также необходимо установить зависимые библиотеки из файла **requirements.txt**. 

```
python3 -m venv env

pip3 install -r requirements.txt
```

3. Далее необходимо настроить `lua/quik-lua-rpc/config.json` и `connector/settings.py`. 
   Убедитесь, что username и password совпадают. Пример настройки `config.json`:
   
```json
{
  "endpoints": [
    {
      "type": "RPC",
      "serde_protocol": "protobuf",
      "active": true,
      "address": {
        "host": "127.0.0.1",
        "port": 5560
      },
      "auth": {
        "mechanism": "PLAIN",
        "plain": {
          "users": [
            {"username": "U0177818", "password": "07855"}
          ]
        },
        "curve": {
          "server": {
            "public": "rq:rM>}U?@Lns47E1%kR.o@n%FcmmsL/@{H8]yf7",
            "secret": "JTKVSB%%)wK0E.X)V>+}o?pNmC{O&4W4b!Ni{Lh6"
          },
          "clients": ["Yne@$w-vo<fVvi]a<NY6T1ed:M$fCG*[IaLV{hID"]
        }
      }
    },

    {
      "type": "PUB",
      "serde_protocol": "protobuf",
      "active": true,
      "address": {
        "host": "127.0.0.1",
        "port": 5561
      },
      "auth": {
        "mechanism": "PLAIN",
        "plain": {
          "users": [
            {"username": "U0177818", "password": "07855"}
          ]
        },
        "curve": {
          "server": {
            "public": "rq:rM>}U?@Lns47E1%kR.o@n%FcmmsL/@{H8]yf7",
            "secret": "JTKVSB%%)wK0E.X)V>+}o?pNmC{O&4W4b!Ni{Lh6"
          },
          "clients": ["Yne@$w-vo<fVvi]a<NY6T1ed:M$fCG*[IaLV{hID"]
        }
      }
    }
  ]
}

```
Для лучшего понимания читайте [документацию quik-lua-rpc по запуску приложения](https://github.com/Enfernuz/quik-lua-rpc#%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B).

Пример настройки файла `connector/settings.py`:

```python
USERS = {
    'REQ': {
        'username': 'U0177818',
        'password': '07855',
        'url': 'tcp://127.0.0.1:5560'
    },
    'SUB': {
        'username': 'U0177818',
        'password': '07855',
        'url': 'tcp://127.0.0.1:5561'
    }
}
```

4. Теперь необходимо настроить `trade/settings.py`. Пример заполнения настроек:

```python
USER_SETTINGS = {
    'CLIENT_CODE': "10744",
}

# Cчета
ACCOUNTS = {
    'fixed_term': "SPBFUT000yt", # Срочный 
    'stock': "NL0011100043", # Фондовый
    'currency': "MB1000100002", # Валютный
}

FIRM_ID = {
    'fixed_term': "SPBFUT000000", # Срочный
    'stock': "NC0011100000", # Фондовый
    'currency': "MB1000100000", # Валютный
}
```