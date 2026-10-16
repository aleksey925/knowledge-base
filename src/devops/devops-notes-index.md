# Заметки о devops

# Оглавление

1. [GitLab CI](#gitlab-ci)
   - [Использование в CI конфиге docker образ из приватного docker-hub](#использование-в-ci-конфиге-docker-образ-из-приватного-docker-hub)

## GitLab CI

### Использование в CI конфиге docker образ из приватного docker-hub

Для того, чтобы иметь возможность использовать свой собственный docker образ из
приватного репозитория docker-hub, необходимо:

- в `.gitlab-ci.yml` указать какой образ вы хотите использовать. В общем виде
  это выглядит так:
  ```
  image: registry.hub.docker.com/<username>/<repo-name>:<tag>
  ```
- после этого необходимо по [инструкции](#настройка-авторизации-в-docker-hub)
  сформировать настроки для docker, которые будут использоваться gitlab runner
  для доступа к приватному docker-hub
- теперь, когда настройки были сформированы, необходимо в gitlab открыть
  `Settings` -> `CI / CD` -> `Variables`, создать переменную
  `DOCKER_AUTH_CONFIG` и поместить в нее настройки, которые были сгенерированны
  на предыдущем шаге (флажки `Protected` и `Masked` активировать не нужно).

#### Настройка авторизации в docker hub

Обычно для подключения к docker hub используется логин и пароль, но так делать
не безопасно, когда речь заходить про настройку доступа к реппозиторию из CI/CD
систем. Для того, чтобы сделать авторизацию более безопасной, docker hub дает
возможность сгенерировать специальный токен, который можно будет использовать
вместо пароля. Для того, чтобы его сненерировать, необходимо перейти по
[ссылке](https://hub.docker.com/settings/security).

После того как токен был сгенерирован, можно приступать к написанию конфига для
docker, где будет описано при помощи каких credentials будет происходить
автризация.

Перед созданием конфига необходимо выполнить команду:

```bash
echo -n "<docker-hub-login>:<docker-hub-pass-or-token>" | base64
```

> `<docker-hub-login>` логин к вашему docker hub аккаунту
> `<docker-hub-pass-or-token>` пароль или токен для доступа к docker hub

И подставить результат в следеющую структуру:

```
{
    "auths": {
        "registry.hub.docker.com": {
            "auth": "<generated-string>"
        }
    }
}
```

В результате получится примерно вот такой конфиг:

```
{
    "auths": {
        "registry.hub.docker.com": {
            "auth": "PGRvY2tlci1odWItbG9naW4+Ojxkb2NrZXItaHViLXBhc3Mtb3ItdG9rZW4+"
        }
    }
}
```

Полезные ссылки:

- [Define an image from a private Container Registry - gitlab doc](https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#define-an-image-from-a-private-container-registry)
- [Can't Access Private MySQL Docker Image From Gitlab CI - stackoverflow](https://stackoverflow.com/questions/51580858/cant-access-private-mysql-docker-image-from-gitlab-ci)
