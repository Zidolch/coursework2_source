import pytest as pytest

from posts.dao.post import Post
from posts.dao.post_dao import PostDAO

# Проверка полей поста


def check_fields(post):
    fields = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}
    for field in fields:
        assert hasattr(post, field), f'Нет поля {field}'


class TestPostDAO:
    """
    Тестирование объекта доступа к данным постов
    """
    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO('./posts/tests/post_mock.json')
        return post_dao_instance

    # Тестирование функции get_all

    def test_get_all_types(self, post_dao):
        posts = post_dao.get_all()
        assert type(posts) == list, 'Неверный тип данных для списка'
        post = post_dao.get_all()[0]
        assert type(post) == Post, 'Неверный тип данных для поста'

    def test_get_all_fields(self, post_dao):
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_all_ids(self, post_dao):
        posts = post_dao.get_all()
        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, 'Не совпадают полученные id'

    # Тестирование функции get_by_pk

    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, 'Неверный тип данных для поста'

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(1234)
        assert post is None, 'Значение для несуществующего pk не является None'

    @pytest.mark.parametrize('pk', [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f'Неверное значение post.pk для pk = {pk}'

    # Тестирование функции search_for_posts

    def test_search_for_posts_types(self, post_dao):
        posts = post_dao.search_for_posts('тарелка')
        assert type(posts) == list, 'Неверный тип данных для списка'
        post = post_dao.search_for_posts('тарелка')[0]
        assert type(post) == Post, 'Неверный тип данных для поста'

    def test_search_for_posts_fields(self, post_dao):
        post = post_dao.search_for_posts('тарелка')[0]
        check_fields(post)

    def test_search_for_posts_not_found(self, post_dao):
        posts = post_dao.search_for_posts('мама мыла раму')
        assert posts == [], 'Найдены посты по неверному запросу'

    @pytest.mark.parametrize('query, expected_pks', [
        ('тарелка', {1}),
        ('погулять', {2}),
        ('на', {1, 2, 3})
    ])
    def test_search_for_posts_results(self, post_dao, query, expected_pks):
        posts = post_dao.search_for_posts(query)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f'Неверные результаты поиска при запросе {query}'

    # Тестирование функции get_posts_by_user

    def test_get_posts_by_user_types(self, post_dao):
        posts = post_dao.get_posts_by_user('leo')
        assert type(posts) == list, 'Неверный тип данных для списка'
        post = post_dao.get_posts_by_user('leo')[0]
        assert type(post) == Post, 'Неверный тип данных для поста'

    def test_get_posts_by_user_fields(self, post_dao):
        post = post_dao.get_posts_by_user('leo')[0]
        check_fields(post)

    def test_get_posts_by_user_not_found(self, post_dao):
        posts = post_dao.get_posts_by_user('oleg')
        assert posts == [], 'Найдены посты по неверному запросу'

    @pytest.mark.parametrize('user_name, expected_pks', [
        ('leo', {1}),
        ('johnny', {2}),
        ('hank', {3})
    ])
    def test_get_posts_by_user_results(self, post_dao, user_name, expected_pks):
        posts = post_dao.get_posts_by_user(user_name)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f'Неверные результаты поиска при запросе {user_name}'
