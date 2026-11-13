"""正关系的普通逐行执行路径。"""
from collections import Counter
from .storage import encode

def run(node,tables):
    op=node['op']
    if op=='scan':
        alias=node['alias']
        return [{alias+'.'+k:v for k,v in r.items()} for r in tables[node['table']]]
    if op=='union-all':return run(node['left'],tables)+run(node['right'],tables)
    if op=='join':
        left=run(node['left'],tables);right=run(node['right'],tables);out=[]
        for l in left:
            for r in right:
                if set(l)&set(r):raise ValueError('别名作用域冲突')
                if all(l[a] is not None and r[b] is not None and l[a]==r[b] for a,b in node['on']):out.append(dict(l,**r))
        return out
    if op=='select':
        return [r for r in run(node['input'],tables) if r[node['field']] is not None and r[node['field']]==node['value']]
    if op=='project':return [{k:r[k] for k in node['fields']} for r in run(node['input'],tables)]
    raise ValueError('不支持的正关系节点')

def bag(rows):return Counter(encode(r) for r in rows)
