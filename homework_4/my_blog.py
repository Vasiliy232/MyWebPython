from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    scoped_session,
    sessionmaker,
    relationship,
    Session as SessionType
)

DB_URL = "sqlite:///music-blog.bd"
DB_ECHO = False
engine = create_engine(url=DB_URL, echo=DB_ECHO)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    """ Модель пользователя """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    is_staff = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"username={self.username!r}, "
            f"is_staff={self.is_staff}, "
            f"created_at={self.created_at})"
        )

    def __repr__(self):
        return str(self)


class Post(Base):
    """ Модель поста """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    post_text = Column(Text)
    user_username = Column(Integer, ForeignKey("users.username"))   # Отношение один-ко-много пользоватлей к постам по имени пользователя
    user = relationship("User", backref="user_posts")

    def __str__(self):
        return (f"Username: {self.user_username}\n"
                f"{__class__.__name__}: {self.post_text}\n"
                "Tags: " + ", ".join(map(str, self.post_tags)) + "\n"
                "------------")

    def __repr__(self):
        return str(self)


class Tag(Base):
    """ Модель тега """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag_text = Column(String(30))
    post_id = Column(Integer, ForeignKey("posts.id"))   # Отношение один-ко-много постов к тегам по номеру поста
    post = relationship("Post", backref="post_tags")

    def __str__(self):
        return f"{self.tag_text}"

    def __repr__(self):
        return str(self)


def create_user(session: SessionType, username: str) -> User:
    """ Создание пользователя в базе данных """
    user = User(username=username)
    session.add(user)
    session.commit()
    return user


def create_post(session: SessionType, post_text: str, user_username: str) -> Post:
    """ Создание постов конкретного пользователя в базе данных """
    post = Post(post_text=post_text, user_username=user_username)
    session.add(post)
    session.commit()
    return post


def create_tag(session: SessionType, tag_text: str, post_id: int) -> Tag:
    """ Создание тега для конкретного поста в базе данных """
    tag = Tag(tag_text=tag_text, post_id=post_id)
    session.add(tag)
    session.commit()
    return tag


def create_tags(session: SessionType, tags_text: list[str], post_id: int) -> list[Tag]:
    """ Создание нескольких тегов для поста в базе данных """
    tags_list = []
    for tag_text in tags_text:
        tag = Tag(tag_text=tag_text, post_id=post_id)
        tags_list.append(tag)
    session.add_all(tags_list)
    session.commit()
    return tags_list


def query_user(session: SessionType, username: str) -> User:
    """ Запрос конкретного пользователя из базы данных """
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


def query_user_posts(session: SessionType, username: str) -> list[Post]:
    """ Запрос постов конкретного пользователя из базы данных """
    posts = session.query(Post).filter_by(user_username=username).all()
    print("\n".join(map(str, posts)))
    return posts


def query_tag_by_text(session: SessionType, tag_text: str) -> list[Tag]:
    """ Запрос тегов из базы данных по тексту тегов """
    tags = session.query(Tag).filter_by(tag_text=tag_text).all()
    return tags


def query_user_posts_with_tags(session: SessionType, username: str, tags: list[str]) -> list[Post]:
    """ Запрос постов конкретного пользователя по хотя бы одному из тегов """
    posts = session.query(Post).filter_by(user_username=username).all()
    posts_with_tags = []
    tags_list = []
    for tag_text in tags:   # Запрашиваем теги по тексту тегов
        tag = query_tag_by_text(session, tag_text)
        tags_list += tag
    for post in posts:  # Проверям посты на наличие тегов
        for tag in tags_list:
            if tag in post.post_tags:
                if post not in posts_with_tags:
                    posts_with_tags.append(post)
    for post in posts_with_tags:
        print(post)
    return posts_with_tags


def main():
    Base.metadata.drop_all()    # Удалем таблицы перед повторными запросами
    Base.metadata.create_all()  # Создаём таблицы в базе данных
    session: SessionType = Session()
    create_user(session, "Vasiliy")
    post_one = create_post(session, "In rock we trust, it,s rock or bust", "Vasiliy")
    create_tags(session, ["#music", "#rock"], post_one.id)
    # create_tag(session, "#music", post_one.id)
    # create_tag(session, "#rock", post_one.id)
    post_two = create_post(session, "I play guitar and drums everywhere I want", "Vasiliy")
    create_tags(session, ["#music", "#drums", "#guitar"], post_two.id)
    create_user(session, "Tom")
    tom_post_one = create_post(session, "Today is my first performance as part of a new band", "Tom")
    tom_post_two = create_post(session, "Music is what everyone has", "Tom")
    create_tags(session, ["#rock", "#group"], tom_post_one.id)
    create_tags(session, ["#music", "#foreveryone"], tom_post_two.id)
    query_user_posts_with_tags(session, "Vasiliy", ["#music", "#rock"])   # Запрос постов пользователя Vasiliy по тегам
    query_user_posts(session, "Tom")    # Запрос всех постов пользователя Tom


if __name__ == '__main__':
    main()
