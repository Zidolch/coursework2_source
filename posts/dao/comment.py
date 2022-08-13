class Comment:
    """
    Класс комментариев для использования в DAO
    """
    def __init__(self,
                 pk,
                 post_id,
                 commenter_name,
                 comment,
                 ):
        self.pk = pk
        self.post_id = post_id
        self.commenter_name = commenter_name
        self.comment = comment

    def __repr__(self):
        return f"Comment ( " \
               f"{self.pk}, " \
               f"{self.post_id}, " \
               f"{self.commenter_name}, " \
               f"{self.comment}, " \
               f")"
