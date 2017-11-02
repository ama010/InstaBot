import peewee
# from main import get_user_id

database = peewee.SqliteDatabase('user_info.db')


class User(peewee.Model):
    user_id = peewee.CharField(unique=True)
    username = peewee.CharField()
    full_name = peewee.CharField()
    follows_count = peewee.IntegerField()
    followed_by_count = peewee.IntegerField()

    class Meta:
        database = database


class Media(peewee.Model):
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    media_id = peewee.CharField(unique=True)
    media_type = peewee.CharField()
    media_link = peewee.CharField()

    class Meta:
        database = database


class Comment(peewee.Model):
    comment_id = peewee.CharField(unique=True)
    media_id = peewee.ForeignKeyField(Media, to_field="media_id")
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    comment_text = peewee.CharField()

    class Meta:
        database = database


def initialize_db():
    database.create_tables([User, Media, Comment], safe=True)


# initialize_db()


    # get_user_details("bansaldivam")
    # print(response)


initialize_db()

# Xuser = User(user_id='10', username='amarjeet',
#              full_name='kashyap', follows_count=204, followed_by_count=1207)
# Xuser.save()
#
# print Xuser.username
# print Xuser.id

# query = User.select().where(User.user_id == 1)
# print query[0].username
# print query[0].full_name
# print query[0].follows_count
# print query[0].followed_by_count
# print user.select()


new_user = User(user_id='10', username='acadview',
                full_name='Acadview', follows_count=200, followed_by_count=1200)

new_user.save()

print new_user.username
print new_user.id
print new_user.user_id
print new_user.full_name
print new_user.follows_count
print new_user.followed_by_count


query = User.select()
for q in query:
    print q.username
    print q.full_name
    print q.follows_count
    print q.followed_by_count
    print"...........Next User.........."
