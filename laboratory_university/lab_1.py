import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional
import uuid


# Базовые исключения
class SocialNetworkError(Exception):
    """Базовое исключение для социальной сети"""
    pass


class UserNotFoundError(SocialNetworkError):
    """Пользователь не найден"""
    pass


class PostNotFoundError(SocialNetworkError):
    """Пост не найден"""
    pass


class FriendshipError(SocialNetworkError):
    """Ошибка дружбы"""
    pass


class ValidationError(SocialNetworkError):
    """Ошибка валидации данных"""
    pass


# Классы предметной области
class User:
    def __init__(self, user_id: str, username: str, email: str, first_name: str, last_name: str):
        self._validate_user_data(username, email, first_name, last_name)

        self.user_id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = datetime.now()
        self.friends: List[str] = []  # список ID друзей
        self.posts: List[str] = []  # список ID постов

    def _validate_user_data(self, username: str, email: str, first_name: str, last_name: str):
        """Валидация данных пользователя"""
        if not username or len(username) < 3:
            raise ValidationError("Имя пользователя должно содержать минимум 3 символа")
        if not email or '@' not in email:
            raise ValidationError("Некорректный email")
        if not first_name or not last_name:
            raise ValidationError("Имя и фамилия обязательны")

    def add_friend(self, friend_id: str):
        """Добавить друга"""
        if friend_id == self.user_id:
            raise FriendshipError("Нельзя добавить себя в друзья")
        if friend_id in self.friends:
            raise FriendshipError("Пользователь уже в друзьях")
        self.friends.append(friend_id)

    def remove_friend(self, friend_id: str):
        """Удалить друга"""
        if friend_id not in self.friends:
            raise FriendshipError("Пользователь не найден в друзьях")
        self.friends.remove(friend_id)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'registration_date': self.registration_date.isoformat(),
            'friends': self.friends,
            'posts': self.posts
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Создание объекта из словаря"""
        user = cls(
            data['user_id'],
            data['username'],
            data['email'],
            data['first_name'],
            data['last_name']
        )
        user.registration_date = datetime.fromisoformat(data['registration_date'])
        user.friends = data.get('friends', [])
        user.posts = data.get('posts', [])
        return user

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"


class Post:
    def __init__(self, post_id: str, author_id: str, content: str, post_type: str = "text"):
        self._validate_post_data(content, post_type)

        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.post_type = post_type
        self.created_at = datetime.now()
        self.likes: List[str] = []  # список ID пользователей, поставивших лайк
        self.comments: List['Comment'] = []

    def _validate_post_data(self, content: str, post_type: str):
        """Валидация данных поста"""
        if not content or len(content.strip()) == 0:
            raise ValidationError("Содержание поста не может быть пустым")
        if post_type not in ["text", "image", "video"]:
            raise ValidationError("Некорректный тип поста")

    def add_like(self, user_id: str):
        """Добавить лайк"""
        if user_id in self.likes:
            raise SocialNetworkError("Пользователь уже поставил лайк")
        self.likes.append(user_id)

    def remove_like(self, user_id: str):
        """Удалить лайк"""
        if user_id not in self.likes:
            raise SocialNetworkError("Лайк не найден")
        self.likes.remove(user_id)

    def add_comment(self, comment: 'Comment'):
        """Добавить комментарий"""
        self.comments.append(comment)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'post_id': self.post_id,
            'author_id': self.author_id,
            'content': self.content,
            'post_type': self.post_type,
            'created_at': self.created_at.isoformat(),
            'likes': self.likes,
            'comments': [comment.to_dict() for comment in self.comments]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Post':
        """Создание объекта из словаря"""
        post = cls(
            data['post_id'],
            data['author_id'],
            data['content'],
            data['post_type']
        )
        post.created_at = datetime.fromisoformat(data['created_at'])
        post.likes = data.get('likes', [])
        post.comments = [Comment.from_dict(comment_data) for comment_data in data.get('comments', [])]
        return post

    def __str__(self):
        return f"Пост {self.post_id} от пользователя {self.author_id}"


class Comment:
    def __init__(self, comment_id: str, author_id: str, content: str):
        self._validate_comment_data(content)

        self.comment_id = comment_id
        self.author_id = author_id
        self.content = content
        self.created_at = datetime.now()

    def _validate_comment_data(self, content: str):
        """Валидация данных комментария"""
        if not content or len(content.strip()) == 0:
            raise ValidationError("Содержание комментария не может быть пустым")

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'comment_id': self.comment_id,
            'author_id': self.author_id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Comment':
        """Создание объекта из словаря"""
        comment = cls(
            data['comment_id'],
            data['author_id'],
            data['content']
        )
        comment.created_at = datetime.fromisoformat(data['created_at'])
        return comment


class SocialNetwork:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.posts: Dict[str, Post] = {}

    def add_user(self, username: str, email: str, first_name: str, last_name: str) -> User:
        """Добавить пользователя"""
        try:
            # Проверка уникальности username и email
            for user in self.users.values():
                if user.username == username:
                    raise ValidationError("Имя пользователя уже занято")
                if user.email == email:
                    raise ValidationError("Email уже зарегистрирован")

            user_id = str(uuid.uuid4())
            user = User(user_id, username, email, first_name, last_name)
            self.users[user_id] = user
            return user
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при добавлении пользователя: {str(e)}")

    def get_user(self, user_id: str) -> User:
        """Получить пользователя по ID"""
        if user_id not in self.users:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        return self.users[user_id]

    def create_post(self, author_id: str, content: str, post_type: str = "text") -> Post:
        """Создать пост"""
        try:
            if author_id not in self.users:
                raise UserNotFoundError(f"Автор с ID {author_id} не найден")

            post_id = str(uuid.uuid4())
            post = Post(post_id, author_id, content, post_type)
            self.posts[post_id] = post

            # Добавляем пост к пользователю
            self.users[author_id].posts.append(post_id)

            return post
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при создании поста: {str(e)}")

    def add_friendship(self, user1_id: str, user2_id: str):
        """Добавить дружбу между двумя пользователями"""
        try:
            user1 = self.get_user(user1_id)
            user2 = self.get_user(user2_id)

            user1.add_friend(user2_id)
            user2.add_friend(user1_id)
        except Exception as e:
            raise FriendshipError(f"Ошибка при добавлении дружбы: {str(e)}")

    def like_post(self, user_id: str, post_id: str):
        """Поставить лайк посту"""
        try:
            user = self.get_user(user_id)
            if post_id not in self.posts:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден")

            post = self.posts[post_id]
            post.add_like(user_id)
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при добавлении лайка: {str(e)}")

    def add_comment_to_post(self, post_id: str, author_id: str, content: str):
        """Добавить комментарий к посту"""
        try:
            if post_id not in self.posts:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден")
            if author_id not in self.users:
                raise UserNotFoundError(f"Автор с ID {author_id} не найден")

            comment_id = str(uuid.uuid4())
            comment = Comment(comment_id, author_id, content)

            post = self.posts[post_id]
            post.add_comment(comment)
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при добавлении комментария: {str(e)}")

    def to_dict(self) -> Dict:
        """Преобразование социальной сети в словарь"""
        return {
            'users': {user_id: user.to_dict() for user_id, user in self.users.items()},
            'posts': {post_id: post.to_dict() for post_id, post in self.posts.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SocialNetwork':
        """Создание социальной сети из словаря"""
        social_network = cls()

        # Загрузка пользователей
        for user_id, user_data in data.get('users', {}).items():
            social_network.users[user_id] = User.from_dict(user_data)

        # Загрузка постов
        for post_id, post_data in data.get('posts', {}).items():
            social_network.posts[post_id] = Post.from_dict(post_data)

        return social_network


# Сериализация и десериализация
class SocialNetworkSerializer:
    @staticmethod
    def save_to_json(social_network: SocialNetwork, filename: str):
        """Сохранить социальную сеть в JSON файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(social_network.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при сохранении в JSON: {str(e)}")

    @staticmethod
    def load_from_json(filename: str) -> SocialNetwork:
        """Загрузить социальную сеть из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return SocialNetwork.from_dict(data)
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при загрузке из JSON: {str(e)}")

    @staticmethod
    def save_to_xml(social_network: SocialNetwork, filename: str):
        """Сохранить социальную сеть в XML файл"""
        try:
            root = ET.Element("social_network")

            # Пользователи
            users_elem = ET.SubElement(root, "users")
            for user_id, user in social_network.users.items():
                user_elem = ET.SubElement(users_elem, "user")
                user_elem.set("id", user_id)

                ET.SubElement(user_elem, "username").text = user.username
                ET.SubElement(user_elem, "email").text = user.email
                ET.SubElement(user_elem, "first_name").text = user.first_name
                ET.SubElement(user_elem, "last_name").text = user.last_name
                ET.SubElement(user_elem, "registration_date").text = user.registration_date.isoformat()

                friends_elem = ET.SubElement(user_elem, "friends")
                for friend_id in user.friends:
                    ET.SubElement(friends_elem, "friend").text = friend_id

                posts_elem = ET.SubElement(user_elem, "posts")
                for post_id in user.posts:
                    ET.SubElement(posts_elem, "post").text = post_id

            # Посты
            posts_elem = ET.SubElement(root, "posts")
            for post_id, post in social_network.posts.items():
                post_elem = ET.SubElement(posts_elem, "post")
                post_elem.set("id", post_id)

                ET.SubElement(post_elem, "author_id").text = post.author_id
                ET.SubElement(post_elem, "content").text = post.content
                ET.SubElement(post_elem, "post_type").text = post.post_type
                ET.SubElement(post_elem, "created_at").text = post.created_at.isoformat()

                likes_elem = ET.SubElement(post_elem, "likes")
                for like_user_id in post.likes:
                    ET.SubElement(likes_elem, "like").text = like_user_id

                comments_elem = ET.SubElement(post_elem, "comments")
                for comment in post.comments:
                    comment_elem = ET.SubElement(comments_elem, "comment")
                    comment_elem.set("id", comment.comment_id)
                    ET.SubElement(comment_elem, "author_id").text = comment.author_id
                    ET.SubElement(comment_elem, "content").text = comment.content
                    ET.SubElement(comment_elem, "created_at").text = comment.created_at.isoformat()

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            raise SocialNetworkError(f"Ошибка при сохранении в XML: {str(e)}")


# Демонстрация работы
def demo():
    """Демонстрация работы социальной сети"""
    try:
        # Создание социальной сети
        sn = SocialNetwork()

        # Добавление пользователей
        user1 = sn.add_user("ivan_petrov", "ivan@example.com", "Иван", "Петров")
        user2 = sn.add_user("maria_ivanova", "maria@example.com", "Мария", "Иванова")
        user3 = sn.add_user("alex_smirnov", "alex@example.com", "Алексей", "Смирнов")

        print("Созданы пользователи:")
        for user in [user1, user2, user3]:
            print(f"  - {user}")

        # Добавление дружбы
        sn.add_friendship(user1.user_id, user2.user_id)
        sn.add_friendship(user1.user_id, user3.user_id)
        print(f"\nДрузья {user1.first_name}: {[sn.get_user(friend_id).first_name for friend_id in user1.friends]}")

        # Создание постов
        post1 = sn.create_post(user1.user_id, "Мой первый пост в социальной сети!", "text")
        post2 = sn.create_post(user2.user_id, "Прекрасный день для прогулки в парке 🌳", "text")

        print(f"\nСозданы посты:")
        print(f"  - {post1}")
        print(f"  - {post2}")

        # Лайки и комментарии
        sn.like_post(user2.user_id, post1.post_id)
        sn.like_post(user3.user_id, post1.post_id)
        sn.add_comment_to_post(post1.post_id, user2.user_id, "Отличный пост, Иван!")

        print(f"\nЛайки на первом посте: {len(post1.likes)}")
        print(f"Комментарии на первом посте: {len(post1.comments)}")

        # Сохранение в JSON
        SocialNetworkSerializer.save_to_json(sn, "social_network.json")
        print("\nДанные сохранены в social_network.json")

        # Сохранение в XML
        SocialNetworkSerializer.save_to_xml(sn, "social_network.xml")
        print("Данные сохранены в social_network.xml")

        # Загрузка из JSON
        sn_loaded = SocialNetworkSerializer.load_from_json("social_network.json")
        print(f"\nЗагружено пользователей: {len(sn_loaded.users)}")
        print(f"Загружено постов: {len(sn_loaded.posts)}")

    except SocialNetworkError as e:
        print(f"Ошибка в социальной сети: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    demo()