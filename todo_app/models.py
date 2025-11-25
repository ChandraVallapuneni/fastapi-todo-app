from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    # relationship placeholder - # One user → many todos
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    title: Mapped[str] = mapped_column(String, nullable = False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    # Foreign key → each todo belongs to one user
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # Reverse relationship → todo.owner gives the user
    owner = relationship("User", back_populates="todos")

    
