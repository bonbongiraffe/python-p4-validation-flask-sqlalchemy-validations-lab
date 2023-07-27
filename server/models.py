from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String) #, db.CheckConstraint('len(phone_number) == 10'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_email(self, key, new_name):
        if not new_name:
            raise ValueError("Author must have a name.")
        return new_name

    @validates('phone_number')
    def validate_phone_number(self, key, new_phone_number):
        if not len(new_phone_number) == 10:
            raise ValueError("Phone number must have 10 digits.")
        return new_phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String) #, db.CheckConstraint('len(content) <= 250'))
    category = db.Column(db.String) #, db.CheckConstraint('category == "Fiction" or category == "Non-Fiction"'))
    summary = db.Column(db.String) #, db.CheckConstraint('len(summary) >= 250'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, new_title):
        not_allowed_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in not_allowed_words for word in new_title.split()):
            raise ValueError("Post title must be click-baity!")
        return new_title

    @validates('content')
    def validate_content(self, key, new_content):
        if not len(new_content) >= 250:
            raise ValueError("Content must be at least 250 characters long.")
        return new_content

    @validates('summary')
    def validate_summary(self, key, new_summary):
        if not len(new_summary) < 250:
            raise ValueError("Summary cannot be longer thant 250 characters.")
        return new_summary

    @validates('category')
    def validate_category(self, key, new_category):
        if not new_category == "Fiction" and not new_category == "Non-Fiction":
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return new_category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
