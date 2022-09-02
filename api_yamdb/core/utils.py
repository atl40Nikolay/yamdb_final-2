from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreToTitle,
                            Review,
                            Title)
from users.models import CustomUser
from users.role_enums import Roles
from django.conf import settings
from django.core.mail import send_mail


class GetTitleID:
    requires_context = True

    def __init__(self, title):
        self.kwarg_id = title

    def __call__(self, serializer_field):
        return serializer_field.context['request'].parser_context['kwargs'][
            self.kwarg_id
        ]


def add_user(user_dict):
    if not CustomUser.objects.filter(username=user_dict['username']).exists():
        user = CustomUser.objects.create_user(id=user_dict['id'],
                                              username=user_dict['username'],
                                              email=user_dict['email'],
                                              role=user_dict['role'])
        if user_dict['role'] == Roles.ADMIN.name.lower():
            user.is_staff = True
        user.save()


def add_titles(title_dict):
    if not Title.objects.filter(id=title_dict['id']).exists():
        category = Category.objects.get(id=title_dict['category'])
        title = Title.objects.create(id=title_dict['id'],
                                     name=title_dict['name'],
                                     year=title_dict['year'],
                                     category=category)
        title.save()


def add_category(category_dict):
    if not Category.objects.filter(id=category_dict['id']).exists():
        category = Category.objects.create(id=category_dict['id'],
                                           name=category_dict['name'],
                                           slug=category_dict['slug'],
                                           )
        category.save()


def add_review(review_dict):
    if not Review.objects.filter(id=review_dict['id']).exists():
        author = CustomUser.objects.get(id=review_dict['author'])
        title = Title.objects.get(id=review_dict['title_id'])
        review = Review.objects.create(id=review_dict['id'],
                                       text=review_dict['text'],
                                       pub_date=review_dict['pub_date'],
                                       author=author,
                                       title=title,
                                       score=review_dict['score'],
                                       )
        review.save()


def add_genres(genre_dict):
    if not Genre.objects.filter(id=genre_dict['id']).exists():
        genre = Genre.objects.create(id=genre_dict['id'],
                                     name=genre_dict['name'],
                                     slug=genre_dict['slug'],
                                     )
        genre.save()


def add_comments(comment_dict):
    if not Comment.objects.filter(id=comment_dict['id']).exists():
        review = Review.objects.get(id=comment_dict['review_id'])
        author = CustomUser.objects.get(id=comment_dict['author'])
        comment = Comment.objects.create(id=comment_dict['id'],
                                         text=comment_dict['text'],
                                         author=author,
                                         review=review,
                                         pub_date=comment_dict['pub_date'],
                                         )
        comment.save()


def add_links(link_dict):
    if not GenreToTitle.objects.filter(id=link_dict['id']).exists():
        title = Title.objects.get(id=link_dict['title_id'])
        genre = Genre.objects.get(id=link_dict['genre_id'])
        link = GenreToTitle.objects.create(id=link_dict['id'],
                                           title=title,
                                           genre=genre
                                           )
        link.save()


def sendmail(email, code):
    send_mail(recipient_list=[email],
              message=f'confirmation_code: {code}',
              subject='confirmation_code',
              from_email=settings.EMAIL_ADDRESS)
