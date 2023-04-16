"""Module that contains the class definitions for the database."""
from config import db, ma


class Win(db.Model):
    __tablename__ = "wins"

    playerName = db.Column(db.String(80), nullable=False, unique=True, primary_key=True)
    wins = db.Column(db.Integer, nullable=False)


    def __repr__(self):  # pragma: no cover
        return 'WinModel(name=%s, wins=%d,)' % (self.playerName, self.wins)

    def json(self):  # pragma: no cover
        return {'player_name': self.playerName, 'wins': self.wins}
    

class WinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Win
        load_instance = True
        sqla_session = db.session


win_schema = WinSchema()
