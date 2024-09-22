from fastapi import FastAPI, Request, Response, Form
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from uvicorn import run
from authbase import setup_authbase, DEVELOPMENT, PRODUCTION, Base, User
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect, Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import Session, relationship, backref
from pathlib import Path
from re import compile
from sys import argv, path
from os import getcwd
from openai import OpenAI
try:
    path.append(getcwd())
    from config import OPENAI_API_KEY
    path.pop()
except Exception as e:
    print("Error: invalid or missing config.py")
    exit(1)

this_file_directory = Path(__file__).parent
mode = (DEVELOPMENT if (len(argv) == 2 and argv[1] == "dev") else PRODUCTION)

app = FastAPI()
engine = create_engine('sqlite:///taskpath.db')
get_current_user = setup_authbase(app, engine, mode=mode)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    user = relationship('User', backref=backref('projects', cascade="all, delete"))
    tasks = relationship('Task', back_populates='project')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    index = Column(Integer)
    project_id = Column(String, ForeignKey('projects.id'))
    parent_id = Column(String, ForeignKey('tasks.id'), nullable=True)
    description = Column(String)
    completed = Column(Boolean)
    project = relationship('Project', back_populates='tasks')
    parent = relationship('Task', remote_side=[id], backref=backref('subtasks', cascade="all, delete"))

class CreateTask(BaseModel):
    description: str
    completed: bool
    subtasks: List["CreateTask"]

CreateTask.update_forward_refs()

class ReadTask(BaseModel):
    id: str
    index: int
    description: str
    completed: bool
    subtasks: List["ReadTask"]
    class Config:
        from_attributes = True

ReadTask.update_forward_refs()

class ListProject(BaseModel):
    id: str
    title: str
    class Config:
        from_attributes = True

class CreateProject(BaseModel):
    title: str
    description: str

class ReadProject(BaseModel):
    id: str
    title: str
    description: str
    tasks: List[ReadTask]
    class Config:
        from_attributes = True

class UpdateProject(BaseModel):
    title: str
    description: str
    tasks: List[CreateTask]

for Model in [Project, Task]:
    if not inspect(engine).has_table(Model.__tablename__):
        Model.__table__.create(engine)

class ParserTask(BaseModel):
    header_length: Optional[int]
    whitespace_and_bullets_length: int
    number: Optional[str]
    task: Task
    class Config:
        arbitrary_types_allowed = True

def parse_tasks_from_content(content: str, project: Project) -> List[Task]:
    print(content)
    lines = content.strip().split('\n')
    tasks = []
    stack = []
    index_counter = 1

    # First check the level of indentation. If greater than previous line, level += 1
    # Then check if a number or a set of bullet points exists. If different to previous line, level += 1
    # Then check if a header exists. If different to previous line, level -= 1
    header_pattern = compile(r'^(#+\s+)')
    whitespace_and_bullets_pattern = compile(r'^([•\-\*\s]+\s+)')
    number_pattern = compile(r'^([\d\.]+\s+)')

    for line in lines:
        if not line.strip():
            continue

        ignore = True

        header_match = header_pattern.match(line)
        if header_match:
            header_length = len(header_match.group(1))
            line = line[header_length:]
            ignore = False
        else:
            header_length = None

        whitespace_and_bullets_match = whitespace_and_bullets_pattern.match(line)
        if whitespace_and_bullets_match:
            whitespace_and_bullets_length = len(whitespace_and_bullets_match.group(1))
            line = line[whitespace_and_bullets_length:]
            ignore = False
        else:
            whitespace_and_bullets_length = 0

        line = line.replace("**", "").strip()

        number_match = number_pattern.match(line)
        if number_match:
            number = number_match.group(1)
            line = line[len(number):]
            ignore = False
        else:
            number = None

        if ignore:
            continue

        pop = True
        while pop:
            pop = False
            if len(stack) == 0:
                break
            if stack[-1].whitespace_and_bullets_length > whitespace_and_bullets_length:
                pop = True
            elif stack[-1].whitespace_and_bullets_length == whitespace_and_bullets_length:
                # In almost all circumstances where level is equal, we want to pop
                # However, there might be like this:
                # ### Heading
                # 1. First point
                # #### Heading
                #
                # So, we don't want to pop as long as the current header_length
                # is greater than previous header length, or the current
                # header_length is None and the previous one is not.
                if header_length is not None and stack[-1].header_length is not None and header_length > stack[-1].header_length:
                    pass
                elif header_length is None and stack[-1].header_length is not None:
                    pass
                else:
                    pop = True
            if pop:
                stack.pop()

        if len(stack) >= 1:
            parent = stack[-1].task
            task = Task(index=index_counter, parent=parent, description=line, completed=False)
        else:
            task = Task(index=index_counter, project=project, description=line, completed=False)
        index_counter += 1

        stack.append(ParserTask(
            header_length=header_length,
            whitespace_and_bullets_length=whitespace_and_bullets_length,
            number=number,
            task=task,
        ))
        tasks.append(task)
    return tasks


def get_tasks_from_chat_text(chat_text, project):
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You break down tasks into small, actionable steps.",
            },
            {
                "role": "user",
                "content": chat_text,
            }
        ]
    )
    return parse_tasks_from_content(completion.choices[0].message.content, project)

# List projects.
@app.get("/projects", response_model=List[ListProject])
async def projects(request: Request):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        return user.projects

# Create project.
@app.post("/projects", response_class=HTMLResponse)
async def create_project(
    request: Request,
    project: CreateProject,
):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        project = Project(user=user, **project.dict())
        session.add(project)
        chat_text = f"{project.title}\n\n{project.description}"
        tasks = get_tasks_from_chat_text(chat_text, project)
        for task in tasks:
            session.add(task)
        session.commit()
    return "<p>Project created.</p>"

# Read project.
@app.get("/projects/{project_id}", response_model=ReadProject)
async def read_project(request: Request, project_id: str):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        project = session.get(Project, project_id)
        if project is None or project.user_id != user.id:
            return Response(status_code=HTTP_404_NOT_FOUND)
        def touch(tasks):
            for task in tasks:
                touch(task.subtasks)
        touch(project.tasks)
        return project

# Update project.
@app.patch("/projects/{project_id}")
async def update_project(request: Request, project_id: str, _project: UpdateProject):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        project = session.get(Project, project_id)
        if project is None or project.user_id != user.id:
            return Response(status_code=HTTP_404_NOT_FOUND)
        project.title = _project.title
        project.description = _project.description
        session.query(Task).where(Task.project_id == project.id).delete()
        def set_indexes(task, index):
            task.index = index
            index += 1
            for subtask in task.subtasks:
                index = set_indexes(subtask, index)
            return index
        index = 0
        for task in _project.tasks:
            index = set_indexes(task, index)
        project.tasks = _project.tasks
        session.commit()
    return Response()

# Delete project.
@app.delete("/projects/{project_id}")
async def delete_project(request: Request, project_id: str):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        project = session.get(Project, project_id)
        if project is None or project.user_id != user.id:
            return Response(status_code=HTTP_404_NOT_FOUND)
        session.delete(project)
        session.commit()
    return Response()

# Create task.
@app.post("/projects/{project_id}/tasks", response_class=HTMLResponse)
async def create_task(request: Request, project_id: str, _task: CreateTask):
    with Session(engine) as session:
        user = get_current_user(request, session)
        if user is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        project = session.get(Project, project_id)
        if project is None or project.user_id != user.id:
            return Response(status_code=HTTP_404_NOT_FOUND)
        def get_min_index(task):
            m = task.index
            for subtask in task.subtasks:
                m = min(m, get_min_index(subtask))
            return m
        m = 1e99
        for task in project.tasks:
            m = min(m, get_min_index(task))
        if m == 1e99:
            m = 0
        task = Task(
            project=project,
            index=m,
            description=_task.description,
            completed=_task.completed,
        )
        session.add(task)
        session.commit()
    return "<p>Task created.</p>";

app.mount("/", StaticFiles(directory=str(this_file_directory / "dist"), html=True), name="static")

def main():
    run("taskpath:app", host="127.0.0.1", port=8000, reload=True)
