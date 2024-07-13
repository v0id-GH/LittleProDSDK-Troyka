# LittleProDSDK-Troyka

## 0 - Начало работы с Raspberry Pi (RPI)

### 0.1 - Установка операционной системы

Для начала работы с RPI требуется установить операционную систему Raspberry OS на SD-карту
> [!NOTE]
> Ссылка на установку [RPI-Imager](https://www.raspberrypi.com/software/)

1. Выбираем свою модель RPI
2. Выбираем **RPI OS 64 bit**
3. После того как нажали кнопку `ДАЛЕЕ` во вкладке `ИЗМЕНИТЬ ПАРАМЕТРЫ` устанавливаем логин и пароль,

   а также данные для первичного подключения wi-fi
4. Загружаем систему на SD-карту

### 0.2 - Первое подключение

> [!TIP]
> Для начала следует установить программу Advanced IP Scanner чтобы найти IP-адресс вашего RPI
> 
> Также нужно скачать программу PuTTy, она обязательна для первого подключения

> [!NOTE]
> Ссылка на установку [Advanced IP Scanner](https://www.advanced-ip-scanner.com/ru/)
>
> Cсылка на установку [PuTTy](https://www.putty.org/)

1. Открываем Advanced IP Scanner
2. Нажимаем кнопку `СКАНИРОВАТЬ`
3. Находим IP-адрес вашего RPI
4. Открываем PuTTy
5. Подключаемся по IP-адресу к вашему RPI
6. Заходим в систему под логином и паролем который установили в пункте [0.1](https://github.com/v0id-GH/LittleProDSDK-Troyka/edit/main/README.md#01---%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B)

## 1 - Установка библиотек
Для начала работы требуется установить библиотеки "troykahat" и "dynamixel-sdk"

> [!WARNING]
> На этом этапе у вас может возникнуть проблема, а именно при установке через привычную команду
>
> `pip install`, скорее всего возникнет ошибка `externally-managed-environment`

> [!TIP]
> Для решения данной ошибки требуется ввести следующую команду в терминал rpi:
>
> `sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED`

> [!NOTE]
> Подробности и другие способы решения ошибки [externally-managed-environment](https://stackoverflow-com.translate.goog/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3?_x_tr_sl=en&_x_tr_tl=ru&_x_tr_hl=ru&_x_tr_pto=sc)

## 2 - Установка файла инициализации 

Переместите файл `pipInit.py` в папку с вашим проектом 
