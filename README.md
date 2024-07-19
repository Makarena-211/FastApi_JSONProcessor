# FastApi_JSONProcessor
Тестовое задание для компании VK
## Rest приложение разработанное на языке Python на фреймворке FastApi

## Технологии внутри: 
* Pydantic для схемы модели и генерации json-схемы
* Postgresql база данных развернутая в Docker
* Kafka consumer и producer для отслеживания сообщений на сервер развернуты в Docker
* Alembic для миграции баз данных    

## Get ready:
* Установите json схему в формате {name}_schema.json в начальную директорию проекта
* Запустите docker контейнеры с БД и Kafka 
* Запустите сервер через CLI - `fastapi run main.py`


## База Данных 
![](/photoes/db.png)
## Контроллеры:

### Get_all
![](/photoes/get_all.png)
### Post_all
![](/photoes/post_all.png)
### Delete by id
![](/photoes/delete_by_id.png)
### Get state
![](/photoes/get_state.png)
### Update state
![](/photoes/update_state.png)
### Update specialisation
![](/photoes/update_spec.png)
### Update settings
![](/photoes/update_settings.png)