from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@localhost:5432/dcdatabase'
db = SQLAlchemy(app)
db.init_app(app)


Base = declarative_base(cls=(JsonSerializableBase,))


class Character(db.Model, Base):

    """
    DC characters with attributes title, hero/villain alias, an image,
    their alignment, and other information
    """

    __tablename__ = 'characters'

    
    title = db.Column(db.String(50), primary_key=True)
    image = db.Column(db.String(250))
    universes = db.Column(ARRAY(db.String(100)))
    gender = db.Column(db.String(50))
    aliases = db.Column(ARRAY(db.String(100)))
    creators = db.Column(ARRAY(db.String(100)))
    identity = db.Column(db.String(50))
    real_name = db.Column(db.String(50))
    debut = db.Column(db.String(50))
    affiliation = db.Column(ARRAY(db.String(100)))
    alignment = db.Column(db.String(50))

    def __init__(self, title, alias, image, alignment, creators, identity, real_name, universe, status, gender, debut, aliases):
        """
        Initialize the character
        """
        self.title = title
        self.aliases = aliases
        self.image = image
        self.alignment = alignment
        self.creators = creators
        self.identity = identity
        self.real_name = real_name
        self.universes = universe
        self.gender = gender
        self.debut = debut


    def to_json(self, list_view = False):
        """
        Return a dictionary of information of this character
        """
        return {
            'title' : self.title,
            'creators' : self.creators,
            'alignment' : self.alignment,
            'identity' : self.identity,
            'real_name' : self.real_name,
            'universes' : self.universes,  
            'image' : self.image,
            'gender' : self.gender,
            'debut' : self.debut,
            'aliases' : self.aliases
            }



class Teams(db.Model):

    """
    DC teams with attributes title, first comic appeared in,
    and other information
    """

    __tablename__ = 'teams'

    title = db.Column(db.String(100), primary_key=True)
    image = db.Column(db.String(250))
    debut = db.Column(db.String(100))
    identity = db.Column(db.String(100))
    status = db.Column(db.String(25))
    creators = db.Column(ARRAY(db.String(100)))
    universes = db.Column(ARRAY(db.String(100)))
    team_leaders = db.Column(ARRAY(db.String(100)))
    enemies = db.Column(ARRAY(db.String(100)))

    def __init__(self, title, image, debut, origin, identity, status, creators, universe, team_leaders, enemies):
        """
        Initialize a team
        """
        self.title = title
        self.image = image
        self.debut = debut
        self.identity = identity
        self.status = status
        self.creators = creators
        self.universes = universe
        self.team_leaders = team_leaders
        self.enemies = enemies


    def to_json(self, list_view = False):
        """
        Return a dictionary of information of this teams
        """
        return {
            'title' : self.title,
            'debut' : self.debut,
            'origin' : self.origin,
            'identity' : self.identity,
            'status' : self.status,
            'creators': self.creators,
            'universe': self.universes,
            'team_leaders' : self.team_leaders,
            'enemies' : self.enemies
        }

class Comics(db.Model):

    """
    DC comics with attributes title, issue number, writer, date
    published, and other information
    """

    __tablename__ = 'comics'

    image = db.Column(db.String(250))
    title = db.Column(db.String(100), primary_key=True)
    release_date = db.Column(db.String(50))
    locations = db.Column(ARRAY(db.String(100)))
    featured_characters = db.Column(ARRAY(db.String(100)))
    creators = db.Column(ARRAY(db.String(100)))

    def __init__(self, image, title, date, locations, featured_characters, creators):
        """
        Initialize a comic
        """
        self.image = image
        self.title = title
        self.release_date = date
        self.locations = locations
        self.featured_characters = featured_characters
        self.creators = creators

    def to_json(self, list_view = False):
        """
        Return a dictionary of information of this comic
        """
        return {
            'title' : self.title,
            'image' : self.image,
            'release_date' : self.date,
            'locations' : self.locations,
            'featured_characters' : self.featured_characters,
            'creators' : self.creators
        }


class Movies(db.Model):

    """
    DC movies with attributes title, director, date released,
    and other information
    """

    __tablename__ = 'movies'

    image = db.Column(db.String(250))
    title = db.Column(db.String(100), primary_key=True)
    release_date = db.Column(db.String(50))
    running_time = db.Column(db.String(50))
    budget = db.Column(db.String(50))
    creators = db.Column(ARRAY(db.String(50)))
    featured_characters = db.Column(ARRAY(db.String(100)))

    def __init__(self, image, title, date, running_time, budget, creators, featured_characters):
        """
        Initialize a movie
        """
        self.image = image
        self.title = title
        self.date = date
        self.running_time = running_time
        self.budget = budget
        self.creators = creators
        self.featured_characters = featured_characters

    def to_json(self, list_view = False):
        """
        Return a dictionary of information of this movie
        """
        return {
            'title' : self.title,
            'image' : self.image,
            'date' : self.date,
            'running_time' : self.running_time,
            'budget' : self.budget,
            'featured_characters' : self.featured_characters,
            'creators' : self.creators
        }

class Shows(db.Model):

    """
    DC shows with attributes title, network aired on, date first
    aired on, and other information
    """

    __tablename__ = 'shows'

    title = db.Column(db.String(100), primary_key=True)
    last_air_date  = db.Column(db.String(250))
    running_time  = db.Column(db.String(250))
    image = db.Column(db.String(250))
    first_air_date = db.Column(db.String(50))
    creators = db.Column(ARRAY(db.String(100)))

    def __init__(self, image, title, network, running_time, first_air, creators, characters, last_air):
        """
        Initialize a show
        """
        self.image = image
        self.title = title
        self.last_air  = last_air
        self.running_time  = running_time
        self.first_air = first_air
        self.creators = creators

    def to_json(self, list_view = False):

        """
        Return a dictionary of information of this movie
        """
        return {
            'title' : self.title,
            'last_air' : self.last_air,
            'running_time' : self.running_time,
            'first_air' : self.first_air,
            'creators' : self.creators,
            'characters' : self.characters,
            'image' : self.image
        }

class Creators(db.Model):

    """
    DC creators with attirubtes title, occupation, birth date, birth place
    first publication made (if applicable), and other information
    """

    __tablename__ = 'creators'

    title = db.Column(db.String(50), primary_key=True)
    image = db.Column(String(50))
    job_titles = db.Column(ARRAY(db.String(50)))
    gender = db.Column(String(50))
    birth_date = db.Column(db.String(50))
    first_publication = db.Column(db.String(100))
    employers = db.Column(ARRAY(db.String(100)))

    def __init__(self, title, occupations, birth_date, first_publication, employers):        
        """
        Initialize a creator
        """
        self.title = title
        self.occupations = occupations
        self.birth_date = birth_date
        self.first_publication = first_publication
        slef.employers = db.Column(ARRAY(db.String(100)))


    def to_json(self, list_view = False):
        """
        Return a dictionary of information of this movie
        """
        return {
            'title' : self.title,
            'birth_date' : self.birth_date,
            'gender' : self.gender,
            'first_publication' : self.first_publication,
            'employers' : self.employers
        }


###SCHEMA###

class CharacterSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    universes = fields.Str()
    gender = fields.Str()
    aliases = fields.Str()
    creators = fields.Str()
    identity = fields.Str()
    real_name = fields.Str()
    debut = fields.Str()
    affiliation = fields.Str()
    alignment = fields.Str()


class TeamsSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    debut = fields.Str()
    identity = fields.Str()
    status = fields.Str()
    creators = fields.Str()
    universes = fields.Str()
    team_leaders = fields.Str()
    enemies = fields.Str()

class ComicsSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    release_date = fields.Str()
    locations = fields.Str()
    featured_characters = fields.Str()
    creators = fields.Str()

class MoviesSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    release_date = fields.Str()
    running_time = fields.Str()
    budget = fields.Str()
    creators = fields.Str()
    featured_characters = fields.Str()

class ShowsSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    last_air_date  = fields.Str()
    running_time  = fields.Str()
    first_air_date = fields.Str()
    creators = fields.Str()

class CreatorsSchema(Schema):
    title = fields.Str(dump_only=True)
    image = fields.Str()
    job_titles = fields.Str()
    gender = fields.Str()
    birth_date = fields.Str()
    first_publication = fields.Str()
    employers = fields.Str()

# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


characters_schema = CharacterSchema(many=True)
teams_schema = TeamsSchema(many=True)
comics_schema = ComicsSchema(many=True)
movies_schema = MoviesSchema(many=True)
shows_schema = ShowsSchema(many=True)
creators_schema = CreatorsSchema(many=True)

character_schema = CharacterSchema()
team_schema = TeamsSchema()
comic_schema = ComicsSchema()
movie_schema = MoviesSchema()
show_schema = ShowsSchema()
creator_schema = CreatorsSchema()


