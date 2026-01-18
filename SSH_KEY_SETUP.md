# Настройка SSH ключа для хостинга

## Шаг 1: Проверка существующих SSH ключей

Проверьте, есть ли уже SSH ключи:

```powershell
# Проверка RSA ключа
Test-Path "$env:USERPROFILE\.ssh\id_rsa.pub"

# Проверка Ed25519 ключа (рекомендуется)
Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub"
```

Если возвращает `True` - ключ существует. Переходите к Шагу 3.

## Шаг 2: Генерация нового SSH ключа

### Вариант 1: Ed25519 (рекомендуется, более безопасный)

```powershell
ssh-keygen -t ed25519 -C "faraonpupkin@gmail.com"
```

### Вариант 2: RSA (если Ed25519 не поддерживается)

```powershell
ssh-keygen -t rsa -b 4096 -C "faraonpupkin@gmail.com"
```

При запросе:
- **Enter file in which to save the key**: Нажмите Enter (по умолчанию)
- **Enter passphrase**: Введите пароль или оставьте пустым (Enter дважды)

## Шаг 3: Копирование публичного ключа

### Windows PowerShell:

```powershell
# Для Ed25519
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard

# Или для RSA
Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub" | Set-Clipboard
```

### Или просто выведите и скопируйте:

```powershell
cat "$env:USERPROFILE\.ssh\id_ed25519.pub"
```

## Шаг 4: Добавление SSH ключа

### A) Для GitHub:

1. Перейдите на https://github.com/settings/keys
2. Нажмите **"New SSH key"**
3. Заполните:
   - **Title**: `My Computer` или любое имя
   - **Key**: Вставьте скопированный публичный ключ
   - **Key type**: Authentication Key
4. Нажмите **"Add SSH key"**

**Проверка подключения:**
```powershell
ssh -T git@github.com
```

Должно появиться: `Hi Rageapper! You've successfully authenticated...`

### B) Для VPS/хостинга (Linux):

1. Подключитесь к серверу через SSH:
```powershell
ssh user@your-server.com
```

2. Создайте папку .ssh (если её нет):
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

3. Добавьте публичный ключ в authorized_keys:
```bash
nano ~/.ssh/authorized_keys
# Вставьте содержимое вашего публичного ключа
# Сохраните (Ctrl+X, Y, Enter)
chmod 600 ~/.ssh/authorized_keys
```

4. Или одной командой (с вашего локального компьютера):
```powershell
type "$env:USERPROFILE\.ssh\id_ed25519.pub" | ssh user@your-server.com "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Проверка подключения:**
```powershell
ssh user@your-server.com
```

Должно подключиться без пароля (если ключ правильно добавлен).

### C) Для хостинговых панелей (cPanel, Plesk и т.д.):

1. Войдите в панель управления хостингом
2. Найдите раздел "SSH Access" или "SSH Keys"
3. Нажмите "Add SSH Key" или "Import SSH Key"
4. Вставьте содержимое публичного ключа
5. Сохраните

## Шаг 5: Изменение remote на SSH (для GitHub)

После добавления ключа на GitHub можно переключить репозиторий на SSH:

```powershell
git remote set-url origin git@github.com:Rageapper/max-to-tg.git
git remote -v  # Проверка
```

Теперь `git push` будет использовать SSH вместо HTTPS.

## Решение проблем

**Если SSH ключ не работает:**

1. Проверьте, запущен ли SSH агент:
```powershell
Get-Service ssh-agent
```

2. Запустите SSH агент:
```powershell
Start-Service ssh-agent
```

3. Добавьте ключ в агент:
```powershell
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
```

**Проверка прав доступа (на сервере):**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

**Отладка SSH подключения:**
```powershell
ssh -v git@github.com  # Подробный вывод
```
