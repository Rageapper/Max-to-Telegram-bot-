# Как получить SSH ключ с сервера хостинга

## Шаг 1: Подключитесь к серверу через SSH

```bash
ssh user@your-server.com
```

## Шаг 2: Проверьте существующие ключи

```bash
# Проверьте, есть ли ключи
ls -la ~/.ssh/

# Просмотрите публичный ключ Ed25519
cat ~/.ssh/id_ed25519.pub

# Или RSA
cat ~/.ssh/id_rsa.pub
```

## Шаг 3: Если ключа нет, создайте его

```bash
# Создайте Ed25519 ключ (рекомендуется)
ssh-keygen -t ed25519 -C "hosting@server"

# Или RSA (если Ed25519 не поддерживается)
ssh-keygen -t rsa -b 4096 -C "hosting@server"
```

**При запросе:**
- `Enter file in which to save the key`: Нажмите **Enter** (по умолчанию)
- `Enter passphrase`: Нажмите **Enter** дважды (без пароля, так как для деплоя)

## Шаг 4: Скопируйте публичный ключ

```bash
# Показать и скопировать ключ
cat ~/.ssh/id_ed25519.pub
# или
cat ~/.ssh/id_rsa.pub
```

**Весь вывод должен быть одной строкой, например:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMp1TVjiM8+9aTWRRM3D2lG66mCOkbjToqj5/P3R2av3 hosting@server
```

## Шаг 5: Вставьте в GitHub Deploy Keys

1. Перейдите: https://github.com/Rageapper/max-to-tg/settings/keys
2. Нажмите **"Add deployment key"**
3. Вставьте **ВСЮ строку** из шага 4 в поле **"Key"**
4. **Title**: `Hosting Server`
5. **Allow write access**: Отметьте, если нужна запись
6. Нажмите **"Add key"**

## Что НЕ нужно делать:

❌ Не используйте приватный ключ (id_ed25519 или id_rsa БЕЗ .pub)
❌ Не добавляйте переносы строк в ключ
❌ Не используйте ключ с вашего локального компьютера (нужен ключ с сервера)

## Правильный формат:

✅ **Публичный ключ** (.pub файл)
✅ **Одна строка** (без переносов)
✅ **Начинается с** `ssh-ed25519` или `ssh-rsa`
✅ **С сервера хостинга**, не с локального компьютера

## Альтернатива: Если нет SSH доступа к серверу

Используйте **HTTPS с Personal Access Token**:

1. Создайте токен: https://github.com/settings/tokens
2. В панели хостинга используйте:
   - URL: `https://github.com/Rageapper/max-to-tg.git`
   - Username: `x-access-token`
   - Password: ваш токен

Это проще и не требует SSH ключей!
