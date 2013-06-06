"""The application's model objects"""
from guessword.model.meta import Session, Base


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

    global AppsData
    class AppsData(Base):
        """Creates SQLAlchemy model for the table AppsDataTable"""
        __tablename__ = 'AppsDataTable'
        __table_args__ = {
            'autoload': True,
            'autoload_with': engine
            }
