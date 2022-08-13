from flask import Blueprint, render_template, request, abort
from posts.dao.comment_dao import CommentDAO
from posts.dao.post_dao import PostDAO
from app_config.config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

# Создание блюпринта

bp_posts = Blueprint('bp_posts', __name__, template_folder='templates')

# Создание объектов доступа к данным

post_dao = PostDAO(DATA_PATH_POSTS)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route("/")
def page_posts_index():
    """
    Главная страница, отображающая все посты
    """
    all_posts = post_dao.get_all()
    return render_template("index.html", posts=all_posts)


@bp_posts.route("/posts/<int:pk>")
def page_posts_single(pk):
    """
    Страница одного поста
    """
    post = post_dao.get_by_pk(pk)
    comments = comment_dao.get_comments_by_post_id(pk)

    if post is None:
        abort(404, 'Пост не найден')
    return render_template("post.html",
                           post=post,
                           comments=comments,
                           comments_count=len(comments)
                           )


@bp_posts.route("/users/<user_name>")
def page_posts_by_user(user_name):
    """
    Страница одного пользователя
    """
    user_posts = post_dao.get_posts_by_user(user_name)

    if not user_posts:
        abort(404, 'Пользователь не найден')
    return render_template("user-feed.html",
                           user_name=user_name,
                           posts=user_posts
                           )


@bp_posts.route("/search/")
def page_posts_search():
    """
    Страница поиска постов
    """
    query = request.args.get("s", "")
    if query == "":
        posts = []
    else:
        posts = post_dao.search_for_posts(query)
    return render_template("search.html",
                           posts=posts,
                           query=query,
                           posts_count=len(posts)
                           )
