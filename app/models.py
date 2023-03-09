from app import db


class User(db.Model):  # type: ignore
    __tablename__ = "user"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    discord_id = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(32),
        nullable=True,
    )

    discriminator = db.Column(
        db.String(4),
        nullable=True,
    )

    avatar = db.Column(
        db.String(32),
        nullable=True,
    )


class Category(db.Model):  # type: ignore
    __tablename__ = "category"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    text = db.Column(
        db.String(100),
        nullable=False
    )

    parent = db.Column(
        db.Integer,
        nullable=True
    )


class Word(db.Model):  # type: ignore
    __tablename__ = "word"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    author = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    category = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=True
    )

    word = db.Column(
        db.String(500),
        nullable=False
    )

    meaning = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=True,
    )
