import logging

from flask import Blueprint, jsonify, abort
from posts.dao.post_dao import PostDAO
from app_config.config import DATA_PATH_POSTS


# Создание блюпринта

bp_api = Blueprint('bp_api', __name__)

# Создание объекта доступа к данным

post_dao = PostDAO(DATA_PATH_POSTS)
api_logger = logging.getLogger("api_logger")


@bp_api.route("/api/posts")
def api_posts_all():
    """
    Страничка всех постов
    """
    all_posts = post_dao.get_all()
    api_logger.debug("Запрос всех постов")
    return jsonify([post.as_dict() for post in all_posts])


@bp_api.route("/api/posts/<int:pk>")
def api_posts_single(pk):
    """
    Страничка одного поста
    """
    post = post_dao.get_by_pk(pk)
    if post is None:
        api_logger.debug(f"Запрос несуществующего поста {pk}")
        abort(404)
    else:
        api_logger.debug(f"Запрос поста {pk}")
    return jsonify(post.as_dict())


@bp_api.errorhandler(404)
def api_error_404(error):
    """
    Обработчик ошибки 404
    """
    api_logger.debug(f"Ошибка {error}")
    return jsonify({'error': str(error)})
