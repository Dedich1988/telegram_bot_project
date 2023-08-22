from rivescript.sessions import SessionManager
from peewee import DoesNotExist
from database import UserSession  # Импортируйте вашу модель UserSession

class PostgresSessionManager(SessionManager):
    def __init__(self):
        super().__init__()

    def load(self, username):
        try:
            session = UserSession.get(UserSession.user_id == username)
            return session.context
        except DoesNotExist:
            return None

    def save(self, username, data):
        session, created = UserSession.get_or_create(user_id=username)
        session.context = data
        session.save()

    def delete(self, username):
        try:
            session = UserSession.get(UserSession.user_id == username)
            session.delete_instance()
        except DoesNotExist:
            pass
