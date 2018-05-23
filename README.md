# raspberry-pi-growbox

Код для системы автоматического контроля микроклимата на raspberry pi

Необходимые библиотеки:

* python-smbus
* i2c-tools

### Установка библиотек 
`
sudo apt-get update
sudo apt-get install -y python-smbus i2c-tools
`
### Установка и автозапуск

`
cd 
git clone https://github.com/PepMeister/raspberry-pi-growbox.git 
sudo echo "sudo python3 /home/pi/raspberry-pi-growbox/main.py" >> /etc/profile 
reboot
`

### Внешние модули

* FC-28, Модуль датчика влажности почвы
* 8-разрядный модуль АЦП наикросхеме PCF8591
* Модуль реле 2 канала 5В

Внешний АЦП необходим для подключения аналогового выхода c  модуля влажности почвы; 
встроенный АЦП в raspberry pi отсуствует 
С помощью реле производится управление освещением и подачей воды для полива растения

