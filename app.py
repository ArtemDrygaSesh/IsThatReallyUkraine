from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:@localhost:5432/ukraine2"
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

foreign_ukraine = db.Table('foreign_ukraine',
    db.Column('foreign_id', db.Integer, db.ForeignKey('foreign_location.id'), primary_key=True),
    db.Column('ukraine_id', db.Integer, db.ForeignKey('ukraine_location.id'), primary_key=True)
)
class Foreign_Location(db.Model):
    __tablename__ = 'foreign_location'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    ukraine_locations = db.relationship('Ukraine_Location', secondary='foreign_ukraine',
                                        back_populates='foreign_locations')
class Ukraine_Location(db.Model):
    __tablename__ = "ukraine_location"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    width = db.Column(db.String(500), nullable=False)
    longitude = db.Column(db.String(500), nullable=False)
    picture_url = db.Column(db.String(500), nullable=False)
    foreign_locations = db.relationship('Foreign_Location', secondary='foreign_ukraine',
                                        back_populates='ukraine_locations')




@app.route('/', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        place = request.form["search"]
        location = Foreign_Location.query.filter_by(name=place).first()
        foreign_id = location.id
        ukraine_location_id = db.session.query(foreign_ukraine.c.ukraine_id).filter_by(foreign_id=foreign_id).all()
        info = []
        i = 0
        for id in ukraine_location_id:
            info.append(Ukraine_Location.query.filter_by(id=id[i]).all())
            i += 1
        return(render_template('result.html', info=info))
    return render_template('home.html')

if __name__ == "__main__":
    app.run()



