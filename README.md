```markdown
# Генератор SIP-конфигурации / SIP Configuration Generator

Этот скрипт предназначен для генерации конфигурационных файлов SIP-транков. Он принимает параметры через командную строку и создает соответствующие секции для `sip.conf` и `extensions.conf`.

This script is designed to generate configuration files for SIP trunks. It accepts parameters via the command line and creates corresponding sections for `sip.conf` and `extensions.conf`.

---

## Описание / Description

Скрипт генерирует:
- Регистрацию SIP-транка (`register`).
- Параметры SIP-пира.
- Диалплан для исходящих вызовов.
- Диалплан для входящих вызовов.
- Исключения для определенных доменов.

The script generates:
- SIP trunk registration (`register`).
- SIP peer parameters.
- Dialplan for outgoing calls.
- Dialplan for incoming calls.
- Exceptions for specific domains.

---

## Требования / Requirements

- Python 3.x

---

## Установка / Installation

1. Склонируйте репозиторий:
   Clone the repository:
   ```bash
   git clone https://github.com/ваш-логин/ваш-репозиторий.git
   cd ваш-репозиторий
   ```

2. Убедитесь, что Python установлен:
   Ensure Python is installed:
   ```bash
   python3 --version
   ```

---

## Использование / Usage

Запустите скрипт с необходимыми аргументами:
Run the script with the required arguments:

```bash
python3 gen_sip_conf_v1.3.py -n <trunk_name> -d <domain> -u <username> -ps <password> -pn <phone_number> -l <lk_number> -prefix <prefix> [-op <outbound_proxy>] [-exp <exception_domain>] [-v]
```

### Аргументы / Arguments

| Аргумент / Argument     | Описание / Description                                                | Обязательный / Required | Пример / Example      |
|-------------------------|----------------------------------------------------------------------|--------------------------|-----------------------|
| `-n`, `--name`          | Имя транка / Trunk name                                              | Да / Yes                | `my_trunk`           |
| `-d`, `--domain`        | Домен SIP-сервера / SIP server domain                               | Да / Yes                | `sip.example.com`    |
| `-u`, `--username`      | Имя пользователя / Username                                         | Да / Yes                | `user123`            |
| `-ps`, `--password`     | Пароль / Password                                                   | Да / Yes                | `mypassword`         |
| `-pn`, `--phonenumber`  | Номер телефона / Phone number                                       | Да / Yes                | `1234567890`         |
| `-l`, `--lk`            | Идентификатор клиента / Client identifier                          | Да / Yes                | `1001`               |
| `-prefix`, `--prefix`   | Префикс для исходящих вызовов / Prefix for outgoing calls           | Да / Yes                | `9`                  |
| `-op`, `--outboundproxy`| Внешний прокси (по умолчанию `None`) / Outbound proxy (default `None`) | Нет / No               | `proxy.example.com`  |
| `-exp`, `--exception_domain_name` | Исключение для домена (по умолчанию `None`) / Domain exception (default `None`) | Нет / No               | `specialdomain.com`  |
| `-v`, `--verbose`       | Включить режим вывода / Enable verbose mode                         | Нет / No               |                       |

---

### Пример / Example

```bash
python3 gen_sip_conf_v1.3.py -n my_trunk -d sip.example.com -u user123 -ps mypassword -pn 1234567890 -l 1001 -prefix 9 -op proxy.example.com -exp specialdomain.com -v
```

---

## Вывод / Output

Скрипт выведет сгенерированные секции для `sip.conf` и `extensions.conf`, которые можно использовать в Asterisk.

The script will output the generated sections for `sip.conf` and `extensions.conf`, which can be used in Asterisk.

Пример вывода / Example output:
```
--------------------------------------------------
 register => user123:mypassword@sip.example.com/1234567890
--------------------------------------------------
[my_trunk]
host=sip.example.com
username=user123
...
--------------------------------------------------
exten => _9X.,1,Dial(SIP/my_trunk/${EXTEN:1},600)
--------------------------------------------------
exten => _1234567890,1,Dial(SIP/to_twintime/${EXTEN},600)
--------------------------------------------------
```

---

## TODO

- Сделать генератор более универсальным.


- Make the generator more universal.


---

## Лицензия / License

Этот проект распространяется под лицензией MIT. Подробнее см. LICENSE.

This project is licensed under the MIT License. See LICENSE for details.
```

