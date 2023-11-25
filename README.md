Все файлы пользователей хранятся в локальной директории, 
указанной в переменной окружения

```
STORAGE_DIR=user_storage
```

Иерархия файлового хранилища:

* user_storage/
  * < user-id >/
    * < files... >
  * < user-id >/
    * < files... >

## Запуск

Синхронный

```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Асинхронный

```shell
uvicorn async_app.main:app --reload --host 0.0.0.0 --port 8000
```