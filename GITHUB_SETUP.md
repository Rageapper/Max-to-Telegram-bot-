# Инструкция по загрузке проекта на GitHub

## Шаг 1: Создайте первый коммит

```bash
git commit -m "Initial commit: MAX to Telegram forwarding bot"
```

## Шаг 2: Создайте репозиторий на GitHub

1. Перейдите на https://github.com
2. Войдите в свой аккаунт
3. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
4. Заполните форму:
   - **Repository name**: `maxtg-bot` (или любое другое имя)
   - **Description**: `Бот для пересылки сообщений из MAX в Telegram`
   - Выберите **Public** или **Private** (рекомендуется Private, так как проект использует токены)
   - НЕ отмечайте "Initialize this repository with a README" (у нас уже есть файлы)
   - Нажмите **"Create repository"**

## Шаг 3: Подключите локальный репозиторий к GitHub

После создания репозитория GitHub покажет инструкции. Выполните команды (замените `YOUR_USERNAME` и `REPOSITORY_NAME` на свои):

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

Или, если вы используете SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## Шаг 4: Проверьте

Перейдите на страницу вашего репозитория на GitHub - все файлы должны быть загружены.

## Важные замечания:

✅ `.gitignore` уже настроен и исключает:
- `.env` файл (с токенами) - НЕ будет загружен
- `venv/` (виртуальное окружение) - НЕ будет загружен
- `__pycache__/` - НЕ будет загружен
- `*.log` файлы - НЕ будут загружены

⚠️ **ВАЖНО**: Убедитесь, что файл `.env` НЕ попал в репозиторий:
```bash
git status
# Убедитесь, что .env не в списке файлов
```

Если `.env` всё же попал в список, удалите его:
```bash
git rm --cached .env
git commit -m "Remove .env from repository"
```

## Дополнительные команды:

**Проверка удаленного репозитория:**
```bash
git remote -v
```

**Добавление изменений в будущем:**
```bash
git add .
git commit -m "Описание изменений"
git push
```

**Просмотр истории коммитов:**
```bash
git log
```
