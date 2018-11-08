from flask_sqlalchemy import SQLAlchemy

db = SQLAlchmey()

class movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    star = db.Column(db.Float)
    img = db.Column(db.String)
    
    def __initPP(self, title, star, img):
        self.title = title
        self.star = star
        self.img = img
        
    