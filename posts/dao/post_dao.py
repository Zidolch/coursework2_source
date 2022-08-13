import json
from json import JSONDecodeError
from posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """
    Объект доступа к данным постов
    """
    def __init__(self, path):
        self.path = path

    def load_data(self):
        """
        Загружает данные из файла JSON
        :return: список словарей с данными
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data

    def load_posts(self):
        """
        Возвращает экземпляры класса Post
        :return: список экземпляров Post
        """
        posts_data = self.load_data()
        posts_list = [Post(**post_data) for post_data in posts_data]
        return posts_list

    def get_all(self):
        """
        Получает все посты
        :return: список экземпляров класса Post
        """
        posts = self.load_posts()
        return posts

    def get_by_pk(self, pk):
        """
        Получает пост по его PK
        :param pk: PK поста
        :return: экземпляр класса Post
        """
        if type(pk) != int:
            raise TypeError('pk must be an int')

        posts = self.load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_for_posts(self, query):
        """
        Осуществляет поиск постов, содержащих подстроку query
        :param query: искомая подстрока
        :return: список экземпляров класса Post
        """
        substring = str(query).lower()
        posts = self.load_posts()

        search_result = [post for post in posts if substring in post.content.lower()]
        return search_result

    def get_posts_by_user(self, user_name):
        """
        Осуществляет поиск постов, выложенный пользователем user_name
        :param user_name: имя пользователя
        :return: список экземпляров класса Post
        """
        user_name = str(user_name).lower()
        posts = self.load_posts()

        search_result = [post for post in posts if user_name == post.poster_name.lower()]
        return search_result

