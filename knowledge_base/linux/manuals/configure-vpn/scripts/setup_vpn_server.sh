#!/bin/bash
# Имя пользовыателя, который будет создан на сервере для того, чтобы не
# использовать на постоянной основе учетную запись root
NEW_USER='USER_NAME'
# Название VPN профиля, которое будет записано в конфигах использемых для
# авытоматической настройки подключения
PROFILE_NAME='PROFILE_NAME'
# Подобрать "чистый порт" можно на https://www.speedguide.net/ports.php или
# https://www.adminsub.net/tcp-udp-port-finder/
SSH_PORT=45444

# Данный блок настроек не обязательно менять перез запуском. Если вы вносите в
# них изменения, это должно делаться осознано.
SERVER_IP="$(curl ifconfig.me)"
CA_CERT_NAME="ca"
SERVER_CERT_NAME="debian"
USER_CERT_NAME="me"

IPSEC_CONF="
include /var/lib/strongswan/ipsec.conf.inc

config setup
        uniqueids=never
        charondebug=\"ike 2, knl 2, cfg 2, net 2, esp 2, dmn 2,  mgr 2\"

conn %default
        keyexchange=ikev2
        ike=aes128gcm16-sha2_256-prfsha256-ecp256!
        esp=aes128gcm16-sha2_256-ecp256!
        fragmentation=yes
        rekey=no
        compress=yes
        dpdaction=clear
        left=%any
        leftauth=pubkey
        leftsourceip=${SERVER_IP}
        leftid=${SERVER_IP}
        leftcert=${SERVER_CERT_NAME}.pem
        leftsendcert=always
        leftsubnet=0.0.0.0/0
        right=%any
        rightauth=pubkey
        rightsourceip=10.10.10.0/24
        rightdns=8.8.8.8,8.8.4.4

conn ikev2-pubkey
        auto=add"


SYSCTL_CONF="
# Включаем переадресацию пакетов
net.ipv4.ip_forward = 1

# Позволяет предотвратить MITM-атаки
net.ipv4.conf.all.accept_redirects = 0

# Запрещаеи отправку ICMP-редиректов
net.ipv4.conf.all.send_redirects = 0

# Запрещает поиск PMTU
net.ipv4.ip_no_pmtu_disc = 1"


timestamp() {
  date +%s
}


function checks() {
    if [ ! "$(id -u)" -eq 0 ] ; then
        echo "Скрипт необходимо запускать от имени root"
        return 1
    fi

    if ! [ -d ./.ssh/ ] ; then
        echo "Скрипт небходимо расположить в корне домашней дирректории"
        return 1
    fi

    return 0
}


checks
if [ $? -eq 1 ] ; then
    exit
fi


apt-get update && apt-get -y upgrade && apt-get -y install sudo rsync mc zsh strongswan strongswan-pki iptables-persistent

# Создание пользователя
adduser $NEW_USER

# Добавление пользователя в группу sudo для того, чтобы можно было выполнять команды от имени root
usermod -aG sudo $NEW_USER

# Активация возможности авторизоваться под новым пользователем при помощи ssh
rsync --archive --chown=$NEW_USER:$NEW_USER ./.ssh /home/$NEW_USER


# Настройка ssh
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.`timestamp`_backup
# Меняем порт, запрещаем авторизацию под root, запрещаем авторизацию с пустым паролем и реализуем автоматический разрыв соединения через 360 сек
cat /etc/ssh/sshd_config | sed "s/^#Port 22/Port ${SSH_PORT}/g" |
	sed "s/^PermitRootLogin yes/PermitRootLogin no/g" |
	sed "s/^#PermitEmptyPasswords no/PermitEmptyPasswords no/g" |
	sed "s/^#ClientAliveInterval 0/ClientAliveInterval 360/g" |
	sed "s/^#ClientAliveCountMax 3/ClientAliveCountMax 0/g" > /etc/ssh/new_sshd_config ; mv /etc/ssh/new_sshd_config /etc/ssh/sshd_config

# Генерация сертификатов

# Корневой сертификат, который в дальнейшем используется для выпуска всех остальных сертификатов
ipsec pki --gen --type rsa --size 4096 --outform pem > /etc/ipsec.d/private/$CA_CERT_NAME.pem
ipsec pki --self --ca --lifetime 3650 --in /etc/ipsec.d/private/$CA_CERT_NAME.pem \
 --type rsa --digest sha256 \
 --dn "CN=${SERVER_IP}" \
 --outform pem > /etc/ipsec.d/cacerts/$CA_CERT_NAME.pem


# Сертификат VPN-сервера
ipsec pki --gen --type rsa --size 4096 --outform pem > /etc/ipsec.d/private/$SERVER_CERT_NAME.pem
ipsec pki --pub --in /etc/ipsec.d/private/$SERVER_CERT_NAME.pem --type rsa |
 ipsec pki --issue --lifetime 3650 --digest sha256 \
 --cacert /etc/ipsec.d/cacerts/$CA_CERT_NAME.pem --cakey /etc/ipsec.d/private/$CA_CERT_NAME.pem \
 --dn "CN=${SERVER_IP}" \
 --san $SERVER_IP \
 --flag serverAuth --outform pem > /etc/ipsec.d/certs/$SERVER_CERT_NAME.pem


# Сертификат используемый устройствами для подключения
ipsec pki --gen --type rsa --size 4096 --outform pem > /etc/ipsec.d/private/$USER_CERT_NAME.pem
ipsec pki --pub --in /etc/ipsec.d/private/$USER_CERT_NAME.pem --type rsa |
 ipsec pki --issue --lifetime 3650 --digest sha256 \
 --cacert /etc/ipsec.d/cacerts/$CA_CERT_NAME.pem --cakey /etc/ipsec.d/private/$CA_CERT_NAME.pem \
 --dn "CN=me" --san me \
 --flag clientAuth \
 --outform pem > /etc/ipsec.d/certs/$USER_CERT_NAME.pem


# ПОСЛЕ ЗАВЕРШЕНИЯ ГЕНЕРАЦИИ ВСЕХ СЕРТИФИКАТОВ, ДЛЯ ПОВЫШЕНИЯ БЕЗОПАСНОСТИ
# ЛУЧШЕ УДАЛИТЬ КОРНЕВОЙ СЕРТИФИКАТ
#rm /etc/ipsec.d/private/ca.pem


# Настройка strongSwan
mv /etc/ipsec.conf /etc/ipsec.conf.`timestamp`_backup
echo "$IPSEC_CONF" > /etc/ipsec.conf

# Указываем сертификат сервера
echo -e "\n: RSA ${SERVER_CERT_NAME}.pem" >> /etc/ipsec.secrets

# Настройка сетевых параметров ядра
echo -e "\n\n${SYSCTL_CONF}" >> /etc/sysctl.conf && sysctl -p


# Очищаем все цепочки
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -F
iptables -Z

# Разрешаем работу ssh
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport $SSH_PORT -j ACCEPT

# Разрешаем соединения на loopback-интерфейсе
iptables -A INPUT -i lo -j ACCEPT

# Разрешим входящие IPSec-соединения на UDP-портах 500 и 4500
iptables -A INPUT -p udp --dport  500 -j ACCEPT
iptables -A INPUT -p udp --dport 4500 -j ACCEPT

# Разрешаем переадресацию ESP-трафика
iptables -A FORWARD --match policy --pol ipsec --dir in  --proto esp -s 10.10.10.0/24 -j ACCEPT
iptables -A FORWARD --match policy --pol ipsec --dir out --proto esp -d 10.10.10.0/24 -j ACCEPT

# Настраиваем маскирование трафика, так как VPN-сервер, по сути, выступает как шлюз между Интернетом и VPN-клиентами
iptables -t nat -A POSTROUTING -s 10.10.10.0/24 -o eth0 -m policy --pol ipsec --dir out -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.10.10.0/24 -o eth0 -j MASQUERADE

# Настраиваем максимальный размер сегмента пакетов
iptables -t mangle -A FORWARD --match policy --pol ipsec --dir in -s 10.10.10.0/24 -o eth0 -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360

# Запрещаем все прочие соединения к серверу
iptables -A INPUT -j DROP
iptables -A FORWARD -j DROP

netfilter-persistent save
netfilter-persistent reload

# Генерируем vpn профили
zsh ./mobileconfig.sh "$CA_CERT_NAME" "$USER_CERT_NAME" "$PROFILE_NAME" > /home/$NEW_USER/apple.mobileconfig
zsh ./strongswan.sh "$CA_CERT_NAME" "$USER_CERT_NAME" "$PROFILE_NAME" > /home/$NEW_USER/android.sswan

# Перезапускаем strongswan и ssh
ipsec restart
systemctl restart ssh



