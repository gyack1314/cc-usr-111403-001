"""已有接口的核心、边界及错误路径。"""
import unittest,tempfile
from pathlib import Path
from lake.storage import read_source,Objects,digest

class StorageTests(unittest.TestCase):
    def test_source_and_corruption(self):
        value=read_source()
        with tempfile.TemporaryDirectory() as d:
            o=Objects(d);key=o.put(value);self.assertEqual(o.get(key),value)
            self.assertEqual(o.put(value),key)
            Path(d,key).write_bytes(b'bad')
            with self.assertRaises(ValueError):o.get(key)
    def test_bad_object_identity(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):Objects(d).get('../bad')

from lake.proofs import Token,source_tokens
from lake.rows import run,bag

class FeatureTests(unittest.TestCase):
    def test_identity_and_projection_bag(self):
        data={'T':[{'row_id':'a','v':1},{'row_id':'b','v':1}]}
        rows=run({'op':'project','fields':['x.v'],'input':{'op':'scan','table':'T','alias':'x'}},data)
        self.assertEqual(list(bag(rows).values()),[2])
        self.assertEqual(len(set(source_tokens('T','s',data['T']))),2)
        self.assertNotEqual(Token('T','s','a').key(),Token('T','new','a').key())
    def test_duplicate_identity(self):
        with self.assertRaises(ValueError):list(source_tokens('T','s',[{'row_id':'a'},{'row_id':'a'}]))
    def test_join_null(self):
        plan={'op':'join','left':{'op':'scan','table':'L','alias':'l'},'right':{'op':'scan','table':'R','alias':'r'},'on':[['l.v','r.v']]}
        self.assertEqual(run(plan,{'L':[{'v':None}],'R':[{'v':None}]}),[])
