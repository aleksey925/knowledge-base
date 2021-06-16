#!/bin/bash
# Скрипт для установки и настроки proxy сервера dante.

#########################
# Общие настройки
#########################
# Указыет есть ли необходимость выполнять базовую настройку сервера (создавать
# пользователя с ограниченными правами, изменять настройки ssh  и т д)
IS_CLEAN_INSTALL=false
# Имя пользовыателя, который будет создан на сервере для того, чтобы не
# использовать на постоянной основе учетную запись root
NEW_USER='USER_NAME'
# Указывает создавать или нет правила IPTABLES
USE_IPTABLES=true
# Подобрать "чистый порт" можно на https://www.speedguide.net/ports.php или
# https://www.adminsub.net/tcp-udp-port-finder/
SSH_PORT=45444


#########################
# Настройки dante
#########################
# Название сетевого интерфейса через который сервер осуществляет доступ к сети
# и на котором будет запущен сервер dante.
# Посмотреть список доступных можно командой ifconfig.
NET_INTERFACE_NAME="eth0"
# Порт на котором будет запущен proxy сервер
DANTE_PORT=45111


timestamp() {
  date +%s
}


function setup_dante() {
    # Выполняет установку и настройка proxy сервера dante
    interface_name=${1-"eth0"}
    port=${2-"1080"}

    dante_config="# Путь к файлу с логами
logoutput: /var/log/danted.log

internal: ${interface_name} port = ${port}
external: ${interface_name}

# Настройки авторизации
clientmethod: none
socksmethod: none

user.privileged: root
user.notprivileged: danted

client pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: error connect disconnect
}
client block {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: connect error
}
socks pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: error connect disconnect
}
socks block {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: connect error
}"

    apt-get -y install dante-server
    adduser --system --no-create-home --disabled-login --group danted

    # Даем доступ Danted демону
    chmod +x /etc/init.d/danted
    update-rc.d danted defaults

    # Активируаем авториматический запуск danted после перезагрузки
    systemctl enable danted

    mv /etc/danted.conf /etc/danted.conf.bak
    echo "$dante_config" > /etc/danted.conf

    touch /var/log/danted.log
    chown root:danted /var/log/danted.log
    chmod 664 /var/log/danted.log

    systemctl restart danted
}


function setup_ssh() {
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config."$(timestamp)"_backup
    cat /etc/ssh/sshd_config | sed "s/^#Port 22/Port ${SSH_PORT}/g" |
    sed "s/^PermitRootLogin yes/PermitRootLogin no/g" |
    sed "s/^#PermitEmptyPasswords no/PermitEmptyPasswords no/g" |
    sed "s/^#ClientAliveInterval 0/ClientAliveInterval 360/g" |
    sed "s/^#ClientAliveCountMax 3/ClientAliveCountMax 0/g" > /etc/ssh/new_sshd_config ; mv /etc/ssh/new_sshd_config /etc/ssh/sshd_config
}


function setup_linux_core() {
    SYSCTL_CONF="
# Включаем переадресацию пакетов
net.ipv4.ip_forward = 1

# Позволяет предотвратить MITM-атаки
net.ipv4.conf.all.accept_redirects = 0

# Запрещаеи отправку ICMP-редиректов
net.ipv4.conf.all.send_redirects = 0

# Запрещаем поиск PMTU
net.ipv4.ip_no_pmtu_disc = 1"

    # Настройка сетевых параметров ядра
    echo -e "\n\n${SYSCTL_CONF}" >> /etc/sysctl.conf && sysctl -p
}


function setup_server() {
    # Выполняет настройку Debian сервера
    apt-get update && apt-get -y upgrade && apt-get -y install sudo rsync mc iptables-persistent

    if [ $IS_CLEAN_INSTALL == false ] ; then
        return 0
    fi

    # Создание пользователя
    adduser $NEW_USER

    # Добавление пользователя в группу sudo для того, чтобы можно было
    # выполнять команды от имени root
    usermod -aG sudo $NEW_USER

    # Активация возможности авторизоваться под новым пользователем при помощи ssh
    rsync --archive --chown=$NEW_USER:$NEW_USER ./.ssh /home/$NEW_USER

    setup_ssh
    setup_linux_core
}


function setup_iptables() {
    if $IS_CLEAN_INSTALL ; then
        if $USE_IPTABLES ; then
            # Очищаем все цепочки
            iptables -P INPUT ACCEPT
            iptables -P FORWARD ACCEPT
            iptables -F
            iptables -Z

            # Разрешаем соединения на loopback-интерфейсе
            iptables -A INPUT -i lo -j ACCEPT

            # Разрешаем работу ssh
            iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
            iptables -A INPUT -p tcp --dport $SSH_PORT -j ACCEPT
        fi
    fi

    if $USE_IPTABLES ; then
        iptables -I INPUT -p tcp -m tcp --dport $port -j ACCEPT -m comment --comment "Open port for work dante-server"
    fi

    if $IS_CLEAN_INSTALL ; then
        if $USE_IPTABLES ; then
            # Запрещаем все прочие соединения к серверу
            iptables -A INPUT -j DROP
            iptables -A FORWARD -j DROP
        fi
    fi

    if $USE_IPTABLES ; then
        netfilter-persistent save
        netfilter-persistent reload
    fi
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


setup_server
setup_dante $NET_INTERFACE_NAME $DANTE_PORT
setup_iptables

if $IS_CLEAN_INSTALL ; then
    systemctl restart ssh
fi

