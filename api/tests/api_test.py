from run import app
import pytest


class TestApi:

    post_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    @pytest.fixture
    def app_instance(self):
        return app.test_client()

    # Тестирование всех постов

    def test_all_posts_types(self, app_instance):
        result = app_instance.get("/api/posts")
        posts = result.get_json()
        assert type(posts) == list, 'Неверный тип данных для списка'
        post = posts[0]
        assert type(post) == dict, 'Неверный тип данных для поста'

    def test_all_posts_keys(self, app_instance):
        result = app_instance.get("/api/posts")
        post = result.get_json()[0]
        post_keys = set(post.keys())
        assert post_keys == self.post_keys, 'Неверные поля'

    # Тестирование одного поста

    def test_single_post_type(self, app_instance):
        result = app_instance.get("/api/posts/1")
        post = result.get_json()
        assert type(post) == dict, 'Неверный тип данных для поста'

    def test_single_post_keys(self, app_instance):
        result = app_instance.get("/api/posts/1")
        post = result.get_json()
        post_keys = set(post.keys())
        assert post_keys == self.post_keys, 'Неверные поля'
