from typing import List
from pydantic import BaseModel, Field


class Reference(BaseModel):
    file_name: str
    file_link: str
    page_numbers: List[int] = Field(default_factory=list)
    sheet_names: List[str] = Field(default_factory=list)

    def to_md(self) -> str:
        ref_name = self.file_name
        if self.page_numbers:
            pages = ", ".join(map(str, self.page_numbers))
            ref_name += f" - 第 {pages} 頁"
        elif self.sheet_names:
            sheets = ", ".join(self.sheet_names)
            ref_name += f" - 頁籤：{sheets}"
        return f"- [{ref_name}]({self.file_link})"


class References(BaseModel):
    references: List[Reference] = Field(default_factory=list)

    def to_md(self) -> str:
        if len(self.references) == 0:
            return ""
        return f"參考來源：\n" + "\n".join(ref.to_md() for ref in self.references)
