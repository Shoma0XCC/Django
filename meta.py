import os
import django
from django.db.models import Count, Avg
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ORM.settings')
django.setup()

from method.models import Post, User, Info
from datetime import timedelta




print('\nИзменение title')
a.title = 'Other title'
a.save()
print(f'Title: {a.title}, Content: {a.content}')

print('\nПолучение всех объектов')
b = Post(title='Document', content='Something document')
b.save()
all_posts = Post.objects.all()
print(f'All Object: {all_posts}')

# Create user
u1 = User.objects.create(name="Алиса", email="alice@example.com")
u1.save()
u2 = User.objects.create(name="Боб", email="bob@example.com")
u2.save()
u3 = User.objects.create(name="Чарли", email="charlie@example.com")
u3.save()

# Create post
p1 = Post.objects.create(title="Django ORM", content="Как использовать ORM")
p1.save()
p2 = Post.objects.create(title="Django Views", content="Функции и классы")
p2.save()


#Create Info
i1 = Info.objects.create(
    post=p1,
    headline="Обзор ORM",
    text="Полный обзор всех методов ORM",
    pub_date=timezone.now() - timedelta(days=10),
    mod_date=timezone.now() - timedelta(days=5),
    count_comments=12,
    count_likes=30,
    rating=9
)
i1.user.set([u1, u2])

i2 = Info.objects.create(
    post=p1,
    headline="Фильтрация",
    text="Как работает filter, exclude",
    pub_date=timezone.now() - timedelta(days=3),
    mod_date=timezone.now(),
    count_comments=5,
    count_likes=10,
    rating=7
)
i2.user.set([u1])

i3 = Info.objects.create(
    post=p2,
    headline="CBV vs FBV",
    text="Что выбрать",
    pub_date=timezone.now() - timedelta(days=2),
    mod_date=timezone.now(),
    count_comments=8,
    count_likes=14,
    rating=8
)
i3.user.set([u2, u3])

print('\n Filter')
post_filter = Post.objects.filter(title='Document')
print(f'Filter Object: {post_filter}')

print('\nPost.objects.all().filter(content="Something document")')
post_filter_all = Post.objects.all().filter(content='Something document')
print(f'Filter Object: {post_filter_all}')

print('\nExlude')
post_exclude = Post.objects.exclude(title='Document')
print(f'Exclude Object: {post_exclude}')

print('\nСрез QuerySet')
s = Post.objects.all()[:1]
print(f'Срез постов до 1: {s}')

# TO DO Lookup

print('\nAnnotate QuerySet')
posts = Post.objects.annotate(info_count=Count('info'))

for post in posts:
    print(post.title, post.info_count, '\nДобавляет новое поле в котором можно сделать подсчет')


print('\norder_by')
w = Post.objects.order_by('title')
for item in w:
    print(f' {item}')
print('\nСортировка по одному полю')


print('\nAlias')
c = Info.objects.alias(user_count=Count('user')).order_by('-user_count')

for item in c:
    print(f' {item.headline}')
print('\nНужен для сортировки фильрации по вычислению')

print('\nNormal')
for i in Post.objects.all().order_by('-title'):
    print(f' {i.title}')
print('\nReverse')
post2 = Post.objects.all().order_by('-title').reverse()
for item in post2:
    print(f' {item.title}')



print('\nDistinct')
info2 = Info.objects.order_by('-headline').distinct()
for item in info2:
    print(f' {item.headline}')


print('\nValues 3 последние записи по дате публикации')
info3 = Info.objects.order_by('-pub_date').values('pub_date')
for item in info3:
    print(f'Value: {item}')

print('\nValues user')
user2 = User.objects.values()
for item in user2:
    print(f'{item}')


print('\nValues key ManyToMany')
info4 = Info.objects.values('user')
for item in info4:
    print(f'Value: {item}')

print('\nValues_list user')
user3 = User.objects.values_list()
for item in user3:
    print(f'Value: {item}')


print('\nDateTime')
info5 = Info.objects.datetimes('pub_date', 'day')
for item in info5:
    print(f'Value: {item}')
print('''"year" возвращает список всех различных значений года.
        "month" возвращает список всех различных значений года/месяца.
        "week" возвращает список всех различных значений года/недели. Все даты будут понедельником.
        "day" возвращает список всех различных значений года/месяца/дня.''')

print('\nNone()')
user4 = User.objects.none()
print(f'EmptyQuerySet {user4}')


print('\nUnion')
qs1 = Post.objects.values_list('title')
qs2 = Post.objects.values_list('content')
post3 = qs1.union(qs1, qs2)
print(f'Union QuerySet {post3}')

print('\nIntersection')
qs1 = Post.objects.values_list('title')
qs2 = Post.objects.values_list('title')
post4 = qs1.intersection(qs1, qs2)
print(f'Intersection QuerySet {post4}')

print('\nDifference')
qs1 = Post.objects.values_list('title')
qs2 = Info.objects.values_list('headline')
qs3 = User.objects.values_list('name')
post5 = qs1.difference(qs2, qs3)
print(f'Difference QuerySet {post5}')


print('\nSelect_related OneToOne ForeignKey 1 sql запрос')
e = Info.objects.select_related('post').get(id=28)
print(f'Select_related {e.post}')


print(f'\nPrefetch_related связь с ManyToMany and ForeignKey 2 sql запроса')
p = Info.objects.prefetch_related('user').get(id=29)
for user in p.user.all():
    print(f'Prefetch_related {user}')



print(f'\nDefer отложенный запрос(пока к нему не обратяться)')
post6 = Post.objects.defer('content').filter(info__rating=9)
print(f'Defer QuerySet {post6}')


print('\nOnly противоположность defer')
post7 = Post.objects.only('content').get(id=37)
print(post7)


print('\nLatest')
print(User.objects.latest('id'))

print('\nFirst')
print(User.objects.first())

print('\nLast')
print(Post.objects.order_by('content').last())

print('\nAggregate')
print(Info.objects.aggregate(avg=Avg('count_comments')))

print('\nUpdate')
print(User.objects.get(id=40))
User.objects.filter(id=40).update(name='Sofa')
print(User.objects.get(id=40))


u1.delete()
u2.delete()
u3.delete()
p1.delete()
p2.delete()
i1.delete()
i2.delete()
i3.delete()
a.delete()
b.delete()


