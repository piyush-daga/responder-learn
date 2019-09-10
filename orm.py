from tortoise.models import Model
from tortoise import fields


class Person(Model):
    id = fields.IntField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()
    age = fields.IntField()

    def __str__(self):
        return self.id
