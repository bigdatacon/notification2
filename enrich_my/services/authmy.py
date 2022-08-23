import uuid
from core.config import logger

class AuthServiceMy:
    """AuthService."""
    def __init__(self, connection):
        """Initialization.
        :param db:
        """
        self.connection = connection

    def get_by_id(self, user_id: uuid.UUID):
        """Get user info by id.
        :param user_id:
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("select username, first_name, last_name from public.user  WHERE id = (%s);", (user_id,))
            user = cursor.fetchall()
            logger.info(f'Get user: {user}')
            return user

        except Exception:
            logger.exception('Can not found user id in auth database.')
            return None

    def get_all_users_info_from_table(self):
        """Get user info by id.
        :param user_id:
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("select id username, first_name, last_name from public.user")
            user = cursor.fetchall()
            logger.info(f'Get all user: {user}')
            return user

        except Exception:
            logger.exception('Can not found user id in auth database.')
            return None

