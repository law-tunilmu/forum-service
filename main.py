import supabase
from typing import List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from supabase.client import AsyncClient
from app import schemas
from app.dependencies import supa, supa_async

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.add_exception_handler(
#     RequestValidationError,
#     handler=invalid_request_handler
# )

QUESTION_TABLE_NAME = 'questions'
ANSWER_TABLE_NAME = 'answers'
COMMENT_TABLE_NAME = 'comments'
SELECT_COLUMNS_QUESTION = ", ".join(schemas.Question.model_fields.keys())
SELECT_COLUMNS_ANSWER = ", ".join(schemas.Answer.model_fields.keys())
SELECT_COLUMNS_COMMENT = ", ".join(schemas.Comment.model_fields.keys())

@app.post("/questions/", response_model=schemas.Question)
async def create_question(question: schemas.QuestionCreate, supa_client: AsyncClient = Depends(supa_async)):
    try:
        db_question = question.model_dump()
        result = await supa_client.table(QUESTION_TABLE_NAME).insert(db_question).execute()
        return result.data[0]
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/questions/", response_model=Dict[str, Any])
async def get_questions(skip: int = 0, limit: int = Query(default=10, alias="page_size"), supa_client: AsyncClient = Depends(supa_async)):
    try:
        # Query for the data
        result = await supa_client.table(QUESTION_TABLE_NAME).select(SELECT_COLUMNS_QUESTION).order("created_at", desc=True).range(skip, skip + limit - 1).execute()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        
        # Query for the total count
        total_count_result = await supa_client.table(QUESTION_TABLE_NAME).select("id", count="exact").execute()
        total_count = total_count_result.count if total_count_result else 0
        
        return {"data": result.data, "total": total_count}
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/questions/{question_id}", response_model=schemas.Question)
async def get_question(question_id: int, supa_client: AsyncClient = Depends(supa_async)):
    try:
        result = await supa_client.table(QUESTION_TABLE_NAME).select(SELECT_COLUMNS_QUESTION).eq("id", question_id).maybe_single().execute()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return result.data
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/answers/", response_model=schemas.Answer)
async def create_answer(answer: schemas.AnswerCreate, supa_client: AsyncClient = Depends(supa_async)):
    try:
        # Check if the question exists
        question_exists = await supa_client.table(QUESTION_TABLE_NAME).select("id").eq("id", answer.question_id).execute()
        if not question_exists.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        
        db_answer = answer.model_dump()
        result = await supa_client.table(ANSWER_TABLE_NAME).insert(db_answer).execute()
        return result.data[0]
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/answers/", response_model=Dict[str, Any])
async def get_answers(question_id: int, skip: int = 0, limit: int = Query(default=10, alias="page_size"), supa_client: AsyncClient = Depends(supa_async)):
    try:
        # Query for the data
        result = await supa_client.table(ANSWER_TABLE_NAME).select(SELECT_COLUMNS_ANSWER).eq("question_id", question_id).order("created_at", desc=False).range(skip, skip + limit - 1).execute()
        
        # Query for the total count
        total_count_result = await supa_client.table(ANSWER_TABLE_NAME).select("id", count="exact").eq("question_id", question_id).execute()
        total_count = total_count_result.count if total_count_result else 0
        
        return {"data": result.data, "total": total_count}
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/comments/", response_model=schemas.Comment)
async def create_comment(comment: schemas.CommentCreate, supa_client: AsyncClient = Depends(supa_async)):
    try:
        # Check if the answer exists
        answer_exists = await supa_client.table(ANSWER_TABLE_NAME).select("id").eq("id", comment.answer_id).execute()
        if not answer_exists.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
        
        db_comment = comment.model_dump()
        result = await supa_client.table(COMMENT_TABLE_NAME).insert(db_comment).execute()
        return result.data[0]
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/comments/", response_model=Dict[str, Any])
async def get_comments(answer_id: int, skip: int = 0, limit: int = Query(default=10, alias="page_size"), supa_client: AsyncClient = Depends(supa_async)):
    try:
        # Query for the data
        result = await supa_client.table(COMMENT_TABLE_NAME).select(SELECT_COLUMNS_COMMENT).eq("answer_id", answer_id).order("created_at", desc=False).range(skip, skip + limit - 1).execute()
        
        # Query for the total count
        total_count_result = await supa_client.table(COMMENT_TABLE_NAME).select("id", count="exact").eq("answer_id", answer_id).execute()
        total_count = total_count_result.count if total_count_result else 0
        
        return {"data": result.data, "total": total_count}
    except supabase.PostgrestAPIError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

