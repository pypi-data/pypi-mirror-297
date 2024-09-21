# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
# ----------------------------------------------------------------------
# 把父级目录（项目根目录）添加到工作路径，以便在终端也可以执行单元测试
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import unittest
from src.pypdm.assist.cfg import *
from src.pypdm.dbc._sqlite import SqliteDBC

DB_PATH =  'db/sqlite/data/test.db'
S_DBC = SqliteDBC(DB_PATH)
CACHE_ROOT_DIR = 'tmp'


class TestPypdmSqlite(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        S_DBC.exec_script('db/sqlite/init_db.sql')


    @classmethod
    def tearDownClass(cls) :
        S_DBC.exec_script('db/sqlite/rollback_db.sql')
        # if os.path.exists(CACHE_ROOT_DIR) :
        #     shutil.rmtree(CACHE_ROOT_DIR)


    def setUp(self) :
        S_DBC.conn()


    def tearDown(self) :
        S_DBC.close()


    def test_build_pdm(self) :
        from src.pypdm.builder import build
        paths = build(
            dbc = S_DBC,
            pdm_pkg = CACHE_ROOT_DIR + '.pdm.sqlite',
            table_whitelist = [ 't_teachers', 't_students' ],
            table_blacklist = [ 't_employers', 't_employees' ],
            to_log = True
        )
        self.assertEqual(len(paths), 4)
        self.assertTrue('tmp/pdm/sqlite/bean/t_teachers.py' in paths)
        self.assertTrue('tmp/pdm/sqlite/dao/t_teachers.py' in paths)
        self.assertTrue('tmp/pdm/sqlite/bean/t_students.py' in paths)
        self.assertTrue('tmp/pdm/sqlite/dao/t_students.py' in paths)


    def test_update(self) :
        from tests.tmp.pdm.sqlite.bean.t_students import TStudents
        from tests.tmp.pdm.sqlite.dao.t_students import TStudentsDao
        table = TStudents()
        dao = TStudentsDao()
        where = { (table.i_id + ' = '): 1 }

        # before
        bean = dao.query_one(S_DBC, where)
        bean.name = 'EXP'
        bean.remark = '289065406@qq.com'
        is_ok = dao.update(S_DBC, bean)
        self.assertTrue(is_ok)

        # after
        bean = dao.query_one(S_DBC, where)
        self.assertEqual(bean.name.decode(CHARSET), 'EXP')
        self.assertEqual(bean.remark.decode(CHARSET), '289065406@qq.com')


    def test_insert(self) :
        from tests.tmp.pdm.sqlite.bean.t_students import TStudents
        from tests.tmp.pdm.sqlite.dao.t_students import TStudentsDao
        bean = TStudents()
        bean.name = 'exp'
        bean.remark = 'https://github.com/lyy289065406/pypdm'

        dao = TStudentsDao()
        is_ok = dao.insert(S_DBC, bean)
        self.assertTrue(is_ok)


    def test_delete(self) :
        from tests.tmp.pdm.sqlite.bean.t_students import TStudents
        from tests.tmp.pdm.sqlite.dao.t_students import TStudentsDao
        table = TStudents()
        dao = TStudentsDao()
        where = { (table.i_id + ' = '): 2 }

        before_rownum = dao.count(S_DBC)
        is_ok = dao.delete(S_DBC, where)
        after_rownum = dao.count(S_DBC)
        self.assertTrue(is_ok)
        self.assertEqual(before_rownum - 1, after_rownum)


    def test_query(self) :
        from tests.tmp.pdm.sqlite.dao.t_teachers import TTeachersDao
        dao = TTeachersDao()
        beans = dao.query_all(S_DBC)
        self.assertEqual(len(beans), 3)
        # for bean in beans :
        #     print(bean)


    def test_truncate(self) :
        from tests.tmp.pdm.sqlite.dao.t_teachers import TTeachersDao
        dao = TTeachersDao()
        rownum = dao.count(S_DBC)
        self.assertEqual(rownum, 3)

        is_ok = dao.truncate(S_DBC)
        rownum = dao.count(S_DBC)
        self.assertTrue(is_ok)
        self.assertEqual(rownum, 0)


if __name__ == '__main__':
    unittest.main()



