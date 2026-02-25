from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Code Snippet Models
class StepSchema(BaseModel):
    title: str
    description: str
    code: str
    language: str = "bash"

class PostInstallationSchema(BaseModel):
    title: str
    content: str

class CodeSnippetCreate(BaseModel):
    title: str
    description: str
    category: str
    os: List[str]
    difficulty: str
    tags: List[str]
    steps: List[StepSchema]
    postInstallation: Optional[PostInstallationSchema] = None

class CodeSnippet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    description: str
    category: str
    os: List[str]
    difficulty: str
    tags: List[str]
    steps: List[StepSchema]
    postInstallation: Optional[PostInstallationSchema] = None
    views: int = 0
    likes: int = 0
    author: str = "Admin"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

# Comment Models
class CommentCreate(BaseModel):
    snippetId: str
    user: str
    text: str

class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    snippetId: str
    user: str
    text: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

# Google Ads Models
class GoogleAdsConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    enabled: bool = True
    headerAdCode: Optional[str] = None
    sidebarAdCode: Optional[str] = None
    betweenSnippetsAdCode: Optional[str] = None
    footerAdCode: Optional[str] = None
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class GoogleAdsConfigUpdate(BaseModel):
    enabled: bool = True
    headerAdCode: Optional[str] = None
    sidebarAdCode: Optional[str] = None
    betweenSnippetsAdCode: Optional[str] = None
    footerAdCode: Optional[str] = None