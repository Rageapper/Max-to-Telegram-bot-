# Настройка репозитория на хостинге

## Проблема: Host key verification failed

Эта ошибка возникает, когда сервер не знает GitHub. Нужно добавить GitHub в known_hosts.

## Решение 1: SSH (рекомендуется)

### Шаг 1: Получите публичный SSH ключ с сервера

На сервере хостинга выполните:
```bash
cat ~/.ssh/id_rsa.pub
# или
cat ~/.ssh/id_ed25519.pub
```

Если ключа нет, создайте:
```bash
ssh-keygen -t ed25519 -C "hosting@server"
# Нажмите Enter для всех вопросов
cat ~/.ssh/id_ed25519.pub
```

### Шаг 2: Добавьте ключ в GitHub Deploy Keys

1. Перейдите: https://github.com/Rageapper/max-to-tg/settings/keys
2. Нажмите **"Add deploy key"**
3. Заполните:
   - **Title**: `Hosting Server`
   - **Key**: Вставьте публичный ключ с сервера
   - **Allow write access**: Отметьте, если нужна запись
4. Нажмите **"Add key"**

### Шаг 3: Добавьте GitHub в known_hosts на сервере

На сервере выполните:
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

Или вручную:
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" >> ~/.ssh/known_hosts
chmod 600 ~/.ssh/known_hosts
```

### Шаг 4: Проверьте подключение

На сервере:
```bash
ssh -T git@github.com
```

Должно появиться: `Hi Rageapper! You've successfully authenticated...`

## Решение 2: HTTPS с токеном (проще)

### Шаг 1: Создайте Personal Access Token на GitHub

1. Перейдите: https://github.com/settings/tokens
2. Нажмите **"Generate new token"** → **"Generate new token (classic)"**
3. Заполните:
   - **Note**: `Hosting Deploy Token`
   - **Expiration**: Выберите срок действия
   - **Scopes**: Отметьте `repo` (полный доступ к репозиториям)
4. Нажмите **"Generate token"**
5. **Скопируйте токен** (он показывается только один раз!)

### Шаг 2: Настройте на хостинге

В панели хостинга:
- **URL репозитория**: `https://github.com/Rageapper/max-to-tg.git`
- **Ветка**: `main`
- **Способ доступа**: `HTTPS`
- **Username**: `x-access-token` (или `oauth2` для GitLab)
- **Пароль/Токен**: Вставьте скопированный Personal Access Token

### Шаг 3: Проверьте доступ

Нажмите **"Проверить доступ"** в панели хостинга.

## Сравнение методов

| Метод | Плюсы | Минусы |
|-------|-------|--------|
| **SSH** | Безопаснее, не нужно обновлять токен | Нужно настраивать ключи |
| **HTTPS** | Проще настроить | Токен нужно обновлять периодически |

## Рекомендация

Для продакшена используйте **HTTPS с токеном**, так как:
- Проще настроить
- Легче обновить при необходимости
- Токен можно отозвать в любой момент

## Дополнительно: Настройка на сервере вручную

Если у вас есть SSH доступ к серверу:

```bash
# Клонирование репозитория
git clone https://github.com/Rageapper/max-to-tg.git
cd max-to-tg

# Или с SSH (после настройки ключей)
git clone git@github.com:Rageapper/max-to-tg.git
cd max-to-tg

# Обновление
git pull origin main
```
