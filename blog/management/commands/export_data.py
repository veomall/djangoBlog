import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.contrib.auth.models import User
from blog.models import Post, Comment
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
class Command(BaseCommand):
    help = 'Export data to JSON file'

    def handle(self, *args, **options):
        # Получаем все объекты моделей, которые мы хотим экспортировать
        users = User.objects.all()
        posts = Post.objects.all()
        comments = Comment.objects.all()

        # Сериализуем объекты
        serialized_users = serializers.serialize('python', users)
        serialized_posts = serializers.serialize('python', posts)
        serialized_comments = serializers.serialize('python', comments)

        # Объединяем все сериализованные данные
        all_data = serialized_users + serialized_posts + serialized_comments

        # Записываем данные в файл
        with open('data.json', 'w', encoding='utf-8') as out:
            json.dump(all_data, out, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)

        self.stdout.write(self.style.SUCCESS('Successfully exported data'))

