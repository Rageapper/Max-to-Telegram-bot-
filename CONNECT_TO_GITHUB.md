# Инструкция по подключению к GitHub

## После создания репозитория на GitHub выполните:

### Вариант 1: HTTPS (рекомендуется для начала)

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
git push -u origin main
```

### Вариант 2: SSH (если настроен SSH ключ)

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
git push -u origin main
```

## Проверка подключения:

```bash
git remote -v
```

Должно показать:
```
origin  https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git (fetch)
origin  https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git (push)
```

## Если возникли ошибки:

**Если репозиторий уже существует и нужно заменить remote:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
```

**Если нужно переименовать ветку:**
```bash
git branch -M main
```

## После успешного push:

Перейдите на страницу вашего репозитория на GitHub - все файлы должны быть загружены!

⚠️ **ВАЖНО**: Убедитесь, что файл `.env` НЕ попал в репозиторий. Проверьте:
```bash
git ls-files | Select-String ".env"
```

Если `.env` в списке, удалите его:
```bash
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```
