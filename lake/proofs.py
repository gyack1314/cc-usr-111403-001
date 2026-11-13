"""物理来源行的稳定叶子身份。"""
from dataclasses import dataclass
from .storage import encode,digest

@dataclass(frozen=True,order=True)
class Token:
    table:str
    snapshot:str
    row_id:str
    def __post_init__(self):
        if not all(isinstance(x,str) and x for x in (self.table,self.snapshot,self.row_id)):raise ValueError('来源身份缺失')
    def key(self):return digest([self.table,self.snapshot,self.row_id])
    def as_dict(self):return {'table':self.table,'snapshot':self.snapshot,'row_id':self.row_id}

def source_tokens(table,snapshot,rows):
    seen=set()
    for row in rows:
        token=Token(table,snapshot,row['row_id'])
        if token in seen:raise ValueError('同快照来源身份重复')
        seen.add(token);yield token
