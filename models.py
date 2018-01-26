import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    # THESE ARE WHAT IS NEEDED TO CREATE THE USER
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    def get_posts(self):
        return Post.select().where(Post.user == self)
    
    def get_stream(self):
        # GENERATE A STREAM FROM THE USERS THIS USER IS FOLLOWING
        return Post.select().where(
            (Post.user << self.following()) |
            (Post.user == self)
        )
    
    def following(self):
        # USERS WE ARE FOLLOWING
        return (
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )
    
    def followers(self):
        # USERS FOLLOWING CURRENT USER
        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )
        
    @classmethod
    # FUNCTION THAT ACTUALLY CREATES THE USER!!! XD
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists.")
            
            
class Post(Model):
    # THIS CREATES A POST!!! HOW COOL???
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        related_name='posts'
    )
    content = TextField()
    
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

        
class Relationship(Model):
    # CREATES A RELATIONSHIP BETWEEN USERS AKA THE FOLLOW/UNFOLLOW FUNCTION
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')
    
    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True)
        )
            

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()