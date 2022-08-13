from flask import Flask

from api.views import bp_api
from app_config import config_logging
from exceptions.data_exceptions import DataSourceError
from posts.views import bp_posts


app = Flask(__name__)

# Регистрация блюпринтов и логгера
app.register_blueprint(bp_posts)
app.register_blueprint(bp_api)
config_logging.config()

# Обработчики ошибок


@app.errorhandler(404)
def page_error_404(error):
    return f'Страница не найдена {error}', 404


@app.errorhandler(500)
def page_error_500(error):
    return f'Ошибка сервера {error}', 500


@app.errorhandler(DataSourceError)
def page_error_data_source_error(error):
    return f'Ошибка данных {error}', 500


if __name__ == '__main__':
    app.run()
