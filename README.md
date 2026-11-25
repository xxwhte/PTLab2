# Лабораторная 2 по дисциплине "Технологии программирования"

## Вариант 1. Магазин детских игрушек

Покупатель выбирает игрушку в каталоге и вводит имя, адрес и, по желанию, промокод. `TOY5`, `TOY10` и `TOY15` дают скидку 5%, 10% и 15% соответственно. После оформления магазин показывает итоговую цену и сохраняет заказ в PostgreSQL.

## Локальный запуск

Проект использует Django и PostgreSQL. В базе `django_db` работает пользователь `postgres`. Выполните команды в PowerShell из корня проекта.

```powershell
conda activate tplab2-env
python -m pip install -r requirements.txt
$env:DATABASE_PASSWORD = Read-Host 'Пароль пользователя postgres'
python manage.py migrate
python manage.py loaddata products.yaml
python manage.py runserver
```

Магазин откроется по адресу [localhost:8000](http://localhost:8000/). Загрузка `products.yaml` обновляет три демонстрационные позиции каталога.

## Проверка

```powershell
python manage.py test shop/tests/
```

Все 12 тестов прошли на PostgreSQL 16. Тесты проверяют модели и каталог, форму покупки, три размера скидки, заказ без промокода, обработку регистра и пробелов, ошибку при неизвестном промокоде и выбор товара по адресу страницы

GitHub Actions запускает тесты с PostgreSQL 16 при отправке изменений в `master` и в pull request к этой ветке.
