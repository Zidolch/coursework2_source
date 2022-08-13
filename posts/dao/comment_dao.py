import json
from json import JSONDecodeError

from exceptions.data_exceptions import DataSourceError
from posts.dao.comment import Comment


class CommentDAO:
    """
    Объект доступа к данным комментариев
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
                comment_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return comment_data

    def load_comments(self):
        """
        Возвращает экземпляры класса Comment
        :return: список экземпляров Comment
        """
        comments_data = self.load_data()
        comments_list = [Comment(**comment_data) for comment_data in comments_data]
        return comments_list

    def get_comments_by_post_id(self, post_id):
        """
        Осуществляет поиск комментариев к данному посту
        :param post_id: номер поста
        :return: список комментариев к посту
        """
        comments = self.load_comments()
        post_comments = [comment for comment in comments if comment.post_id == post_id]
        return post_comments
