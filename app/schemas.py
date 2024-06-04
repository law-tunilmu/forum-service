from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class USER_ROLES(str, Enum):
    STUDENT = "STUDENT"
    MENTOR = "MENTOR"

class UserBase(BaseModel):
    username: str
    role: USER_ROLES

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    owner_id: Optional[int] = None

class Question(QuestionBase):
    id: int
    owner_id: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    question_id: int
    owner_id: Optional[int] = None

class Answer(AnswerBase):
    id: int
    question_id: int
    owner_id: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    answer_id: int
    owner_id: Optional[int] = None

class Comment(CommentBase):
    id: int
    answer_id: int
    owner_id: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True
