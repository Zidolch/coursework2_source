import pytest as pytest

from posts.dao.comment import Comment
from posts.dao.comment_dao import CommentDAO

# Проверка полей комментария


def check_fields(comment):
    fields = {"pk", "post_id", "commenter_name", "comment"}
    for field in fields:
        assert hasattr(comment, field), f'Нет поля {field}'


class TestCommentDAO:
    """
    Тестирование объекта доступа к данным комментариев
    """
    @pytest.fixture
    def comment_dao(self):
        comment_dao_instance = CommentDAO('./posts/tests/comment_mock.json')
        return comment_dao_instance

    # Тестирование функции search_for_posts

    def test_get_comments_by_post_id_types(self, comment_dao):
        comments = comment_dao.get_comments_by_post_id(1)
        assert type(comments) == list, 'Неверный тип данных для списка'
        comment = comment_dao.get_comments_by_post_id(1)[0]
        assert type(comment) == Comment, 'Неверный тип данных для комментария'

    def test_get_comments_by_post_id_fields(self, comment_dao):
        comment = comment_dao.get_comments_by_post_id(1)[0]
        check_fields(comment)

    def test_get_comments_by_post_id_not_found(self, comment_dao):
        comments = comment_dao.get_comments_by_post_id(666)
        assert comments == [], 'Найдены комментарии по неверному запросу'

    @pytest.mark.parametrize('post_id, expected_pks', [
        (1, {1}),
        (2, {5}),
        (3, {9})
    ])
    def test_search_for_posts_results(self, comment_dao, post_id, expected_pks):
        comments = comment_dao.get_comments_by_post_id(post_id)
        pks = set([comment.pk for comment in comments])
        assert pks == expected_pks, f'Неверные комментарии для поста {post_id}'
