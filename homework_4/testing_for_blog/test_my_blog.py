from homework_4.my_blog import (
    User,
    Post,
    Tag,
    Session,
    SessionType,
    Base,
    create_user,
    create_post,
    create_tags,
    query_tag_by_text)
from pytest import fixture
import random
from string import ascii_lowercase


@fixture
def session() -> Session:
    """ Экземпляр сессии """
    session: SessionType = Session()
    return session


@fixture
def username_one() -> str:
    """ Имя пользователя один """
    letters = random.choices(ascii_lowercase, k=8)
    username_one = "".join(letters)
    return username_one


@fixture
def username_two() -> str:
    """ Имя пользователя два """
    letters = random.choices(ascii_lowercase, k=8)
    username_two = "".join(letters)
    return username_two


@fixture
def post_one() -> str:
    """ Текст первого поста """
    letters = random.choices(ascii_lowercase, k=30)
    post_one = "".join(letters)
    return post_one


@fixture
def post_two() -> str:
    """ Текст второго поста """
    letters = random.choices(ascii_lowercase, k=30)
    post_two = "".join(letters)
    return post_two


@fixture
def tags() -> list[str]:
    """ Текст первой группы тегов """
    tags_list = []
    for i in range(2):
        letters = random.choices(ascii_lowercase, k=5)
        tag = "".join(letters)
        tags_list.append(tag)
    return tags_list


@fixture
def bd():
    """ Экземпляр базы данных """
    Base.metadata.drop_all()
    bd = Base.metadata.create_all()
    return bd


@fixture
def created_user_one(session, username_one, bd) -> User:
    """ Экземпляр первого пользователя """
    created_user_one = create_user(session, username_one)
    return created_user_one


@fixture
def created_user_two(session, username_two, bd) -> User:
    """ Экземпляр второго пользователя """
    created_user_two= create_user(session, username_two)
    return created_user_two


@fixture
def created_post_one(session, post_one, username_one, bd) -> Post:
    """ Экземпляр поста первого пользователя """
    created_post_one = create_post(session, post_one, username_one)
    return created_post_one


@fixture
def created_post_two(session, post_two, username_two, bd) -> Post:
    """ Экземпляр поста второго пользователя """
    created_post_two = create_post(session, post_two, username_two)
    return created_post_two


@fixture
def created_tags_one(session, tags, created_post_one, bd) -> list[Tag]:
    """ Экземпляр тегов для поста первого пользователя """
    created_tags_one = create_tags(session, tags, created_post_one.id)
    return created_tags_one


@fixture
def created_tags_two(session, tags, created_post_two, bd) -> list[Tag]:
    """ Экземпляр тегов для поста второго пользователя """
    created_tags_two = create_tags(session, tags, created_post_two.id)
    return created_tags_two


def test_query_user(session, username_one, bd, created_user_one):
    """ Тест запроса первого пользователя """
    query_user = session.query(User).filter_by(username=username_one).one_or_none()
    assert query_user


def test_query_user_posts(session, username_one, bd, created_post_one):
    """ Тест запроса постов первого пользователя """
    query_posts = session.query(Post).filter_by(user_username=username_one).all()
    assert query_posts


def test_query_tag_by_text(session, tags, bd, created_tags_one, created_tags_two):
    """ Тест запроса тега по тексту  """
    query_tag = session.query(Tag).filter_by(tag_text=tags[0]).all()
    assert query_tag


def test_query_user_posts_with_tags(session, username_one, tags, bd, created_post_one, created_post_two,
                                    created_tags_one, created_tags_two):
    """ Тест запроса постов пользователя по тегам """
    query_posts = session.query(Post).filter_by(user_username=username_one).all()
    query_posts_with_tags = []
    tags_list = []
    for tag_text in tags:
        query_tag = query_tag_by_text(session, tag_text)
        tags_list += query_tag
    for post in query_posts:
        for tag in tags_list:
            if tag in post.post_tags:
                if post not in query_posts_with_tags:
                    query_posts_with_tags.append(post)
    assert query_posts_with_tags
