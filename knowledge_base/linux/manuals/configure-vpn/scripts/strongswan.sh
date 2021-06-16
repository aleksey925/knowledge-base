#!/bin/zsh
# Данный скрипт генерирует VPN профиль для программы strongswan android и
# позволяет очень просто настроить подключение к VPN на android.

# Пароль защищающий сертификат, его нужно будет ввести при импорте профиля на
# устройстве
PKCS12PASSWORD=12345

# Данный блок настроек не обязательно менять перез запуском. Если вы вносите в
# них изменения, это должно делаться осознано.
CA_CERT_NAME=$1
USER_CERT_NAME=$2
PROFILE_NAME=$3
SERVER_ADDR="$(curl ifconfig.me)"

cat << EOF
{
    "uuid": "$( cat /proc/sys/kernel/random/uuid )",
    "name": "${PROFILE_NAME}",
    "type": "ikev2-cert",
    "remote": {
        "addr": "${SERVER_ADDR}" 
    },
    "local": {
        "p12": "$( openssl pkcs12 -export -inkey /etc/ipsec.d/private/${USER_CERT_NAME}.pem -in /etc/ipsec.d/certs/${USER_CERT_NAME}.pem -name "${USER_CERT_NAME}" -certfile /etc/ipsec.d/cacerts/${CA_CERT_NAME}.pem -password pass:${PKCS12PASSWORD} | base64 )"
    }
}
EOF
