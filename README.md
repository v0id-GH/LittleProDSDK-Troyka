+# LittleProDSDK-Troyka

## 0 - Начало работы с Raspberry Pi (RPI)

### 0.1 - Установка операционной системы

Для начала работы с RPI требуется установить операционную систему Raspberry OS на SD-карту
> [!NOTE]
> Ссылка на установку [RPI-Imager](https://www.raspberrypi.com/software/)

1. Выбираем свою модель RPI
2. Выбираем **RPI OS 64 bit**
3. После того как нажали кнопку `ДАЛЕЕ` во вкладке `ИЗМЕНИТЬ ПАРАМЕТРЫ` настраиваем параметры входа и wifi
   
> [!CAUTION]
> Во вкладке `ИЗМЕНИТЬ ПАРАМЕТРЫ` обязательно включить SSH!

4. Загружаем систему на SD-карту

### 0.2 - Первое подключение

> [!TIP]
> Для начала следует установить программу Advanced IP Scanner чтобы найти IP-адресс вашего RPI
> 
> Также нужно скачать программу PuTTy, она обязательна для первого подключения
>
> Для трансляции интерфейса RPI на монитор вашего ПК потребуется скачать Real VNC Viewer

> [!NOTE]
> Ссылка на установку [Advanced IP Scanner](https://www.advanced-ip-scanner.com/ru/)
>
> Cсылка на установку [PuTTy](https://www.putty.org/)
>
> Ссылка на установку [Real VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/?lai_sr=20-24&lai_sl=l)

1. Открываем Advanced IP Scanner
2. Нажимаем кнопку `СКАНИРОВАТЬ`
3. Находим IP-адрес вашего RPI
4. Открываем PuTTy
5. Подключаемся по IP-адресу к вашему RPI
6. Заходим в систему под логином и паролем который установили в пункте ***0.1***

> [!TIP]
> Для использования беспроводного подключения к RPI потребуется включить VNC

7. В терминале который открыл PuTTy прописываем команду: `sudo raspi-config`
8. В открывшемся меню выбираем раздел `Interfacing options`
9. Далее выбираем `VNC` и включаем его
10. Перезапускаем RPI командой: `sudo reboot`
11. Открываем Real VNC Viewer
12. Подключаемся к RPI по его IP-адресу

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

> [!WARNING]
> Для вашего удобства рекомендую открыть этот репозиторий на браузере в RPI и выполнять следующие этапы оттуда

1. Скачайте файл `pipInit.py` с данного репозитория
2. Переместите файл `pipInit.py` в папку с вашим проектом
3. В основном файле вашего проекта напишите строчку `from pipInit import *` дабы импортировать функции и инициализационные данные

## 3 - Базовая работа с ***dynamixel-sdk***

### 3.1 - Адреса и байты

Чаще всего вы будете использовать команды `dxl_comm_result, dxl_error = packetHandler.writeNByteTxRx(portHandler, ....... )` и `dxl_comm_result, dxl_error = packetHandler.readNByteTxRx(portHandler, ...... )` , где N кол-во байт которое вы записываете или читаете, для каждой операции указано число байт необходимых для корректной работы, в свое время у операции имеется свой адрес, который вы прописываете в параметре

> [!NOTE]
> Подробное описание и пример работы всех [операций](https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/)

## 4 - Работа с функциями из файла `pipInit.py`

В данном файле представленно некое число функций, полностью протестированные и рабочие:
1. `testTurn(ID1, ID2, rotation, position, speed)`
2. `testDirect(ID1, ID2, rotation, position, speed)`

Где:
- ID1-2 - id моторов (чаще всего это 1 и 2)
- rotation - желаемое направление ('R', 'L') для `testTurn()` и ('F', 'B') для `testDirect()`
- speed - скорость (предельное значение 1000)

> [!TIP]
> Вас может волновать вопрос как же обнулить инкодеры мотора?
> Обнуление происходит благодоря функции `cleaningEncoder(ID1, ID2)` которую я рекомендую использовать как в начале движения, так и в конце!

## 5 - Базовая работа с ***troykahat***

> [!NOTE]
> Базовая работа с модулем [troyka](https://wiki.amperka.ru/products:raspberry-pi-troyka-hat)



