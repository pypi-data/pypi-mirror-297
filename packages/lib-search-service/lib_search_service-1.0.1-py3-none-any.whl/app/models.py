from enum import Enum

from pydantic import BaseModel, Field


class SearchIndex(str, Enum):
    FOLDER = "library.folder"
    COURSE = "library.course"
    MAJOR = "library.major"
    FACULTY = "library.faculty"


class IndexList(BaseModel):
    indices: list = Field(examples=[list(SearchIndex)])


class DetailedCriteria(BaseModel):
    index_list: list = Field(examples=[list(SearchIndex)])
    exact_match: dict
    query: dict = Field(examples=[{"*": "تلخيص سجود حمايل فيزياء"}])


class Criteria(BaseModel):
    index_list: list = Field(examples=[list(SearchIndex)])
    query: str = Field(examples=["تلخيص سجود حمايل فيزياء"])


class SearchInfo(BaseModel):
    id: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    type: SearchIndex = Field(examples=[SearchIndex.FOLDER])


class Folder(SearchInfo):
    name: str = Field(examples=["new folder name"])
    description: str = Field(examples=["This is a description for the new folder"])
    courseNameArabic: str = Field(examples=["إسم المجلد بالعربية"])
    courseNameEnglish: str = Field(examples=["new folder courseNameEnglish"])


class Course(SearchInfo):
    nameEnglish: str = Field(examples=["new course nameEnglish"])
    nameArabic: str = Field(examples=["إسم المساق بالعربية"])
    symbol: str = Field(examples=["COURSE123"])


class Major(SearchInfo):
    nameEnglish: str = Field(examples=["new major nameEnglish"])
    nameArabic: str = Field(examples=["إسم التخصص بالعربية"])
    symbol: str = Field(examples=["MAJOR234"])
    description: str = Field(examples=["This is a description for the new major"])


class Faculty(SearchInfo):
    nameEnglish: str = Field(examples=["new faculty nameEnglish"])
    nameArabic: str = Field(examples=["إسم الكلية بالعربية"])
    symbol: str = Field(examples=["FACULTY345"])
    description: str = Field(examples=["This is a description for the new faculty"])
