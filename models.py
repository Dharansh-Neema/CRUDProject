# app/models.py

from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, email, full_name, age, _id=None, created_at=None, updated_at=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.username = username
        self.email = email
        self.full_name = full_name
        self.age = age
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "age": self.age,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            age=data['age'],
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
