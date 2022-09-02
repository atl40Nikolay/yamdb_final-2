import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from core.utils import (add_category, add_comments, add_genres, add_links,
                        add_review, add_titles, add_user)


class Command(BaseCommand):
    help = 'Заполнение базы из CSV'

    def handle(self, *args, **options):

        user_processing()
        category_processing()
        title_processing()
        review_processing()
        genre_processing()
        comments_processing()
        links_processing()


def user_processing():
    """чтение и добавление пользователей из CSV"""
    with open(settings.CSV_FILES_DICT + '/users.csv',
              newline='') as csvfile:
        users_info = csv.reader(csvfile, delimiter=',')
        for row in users_info:
            if row[0] != 'id':
                user = {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'role': row[3],
                }
                add_user(user)
    print("Users added")


def category_processing():
    """чтение и добавление категорий из CSV"""
    with open(settings.CSV_FILES_DICT + '/category.csv',
              newline='', encoding='utf-8') as csvfile:
        category_info = csv.reader(csvfile, delimiter=',')
        for row in category_info:
            if row[0] != 'id':
                category = {
                    'id': row[0],
                    'name': row[1],
                    'slug': row[2],
                }
                print(category)
                add_category(category)
    print("Categories added")


def title_processing():
    """чтение и добавление тайтлов из CSV"""
    with open(settings.CSV_FILES_DICT + '/titles.csv',
              newline='', encoding='utf-8') as csvfile:
        titles_info = csv.reader(csvfile, delimiter=',')
        for row in titles_info:
            if row[0] != 'id':
                title = {
                    'id': row[0],
                    'name': row[1],
                    'year': row[2],
                    'category': row[3],
                }
                print(title)
                add_titles(title)
    print("Titles added")


def review_processing():
    """чтение и добавление ревью из CSV"""
    with open(settings.CSV_FILES_DICT + '/review.csv',
              newline='', encoding='utf-8') as csvfile:
        review_info = csv.reader(csvfile, delimiter=',')
        for row in review_info:
            if row[0] != 'id':
                review = {
                    'id': row[0],
                    'title_id': row[1],
                    'text': row[2],
                    'author': row[3],
                    'score': row[4],
                    'pub_date': row[3],
                }
                print(review)
                add_review(review)
    print("Reviews added")


def genre_processing():
    """чтение и добавление жанров из CSV"""
    with open(settings.CSV_FILES_DICT + '/genre.csv',
              newline='', encoding='utf-8') as csvfile:
        genres_info = csv.reader(csvfile, delimiter=',')
        for row in genres_info:
            if row[0] != 'id':
                genre = {
                    'id': row[0],
                    'name': row[1],
                    'slug': row[2],
                }
                print(genre)
                add_genres(genre)
    print("Genres added")


def comments_processing():
    """чтение и добавление комментов из CSV"""
    with open(settings.CSV_FILES_DICT + '/comments.csv',
              newline='', encoding='utf-8') as csvfile:
        comments_info = csv.reader(csvfile, delimiter=',')
        for row in comments_info:
            if row[0] != 'id':
                comment = {
                    'id': row[0],
                    'review_id': row[1],
                    'text': row[2],
                    'author': row[3],
                    'pub_date': row[4],
                }
                print(comment)
                add_comments(comment)
    print("Comments added")


def links_processing():
    """чтение и добавление связей из CSV"""
    with open(settings.CSV_FILES_DICT + '/genre_title.csv',
              newline='', encoding='utf-8') as csvfile:
        links_info = csv.reader(csvfile, delimiter=',')
        for row in links_info:
            if row[0] != 'id':
                link = {
                    'id': row[0],
                    'title_id': row[1],
                    'genre_id': row[2],
                }
                print(link)
                add_links(link)
    print("links added")
