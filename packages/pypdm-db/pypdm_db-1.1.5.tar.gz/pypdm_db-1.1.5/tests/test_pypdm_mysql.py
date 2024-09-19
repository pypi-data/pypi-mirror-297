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
from src.pypdm.dbc._mysql import MysqlDBC

HOST = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '123456'
DB_NAME = 'test'
M_DBC = MysqlDBC(host = HOST,
            port = PORT,
            username = USERNAME,
            password = PASSWORD,
            dbname = DB_NAME,
            encoding = ENCODING
)
CACHE_ROOT_DIR = 'tmp'


class TestPypdmMysql(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        M_DBC.exec_script('db/mysql/init_db.sql')


    @classmethod
    def tearDownClass(cls) :
        M_DBC.exec_script('db/mysql/rollback_db.sql')
        # if os.path.exists(CACHE_ROOT_DIR) :
        #     shutil.rmtree(CACHE_ROOT_DIR)


    def setUp(self) :
        M_DBC.conn()


    def tearDown(self) :
        M_DBC.close()


    def test_build_pdm(self) :
        from src.pypdm.builder import build
        paths = build(
            dbc = M_DBC,
            pdm_pkg = CACHE_ROOT_DIR + '.pdm.mysql',
            table_whitelist = [ 't_teachers', 't_students' ],
            table_blacklist = [ 't_employers', 't_employees' ],
            to_log = True
        )
        self.assertEqual(len(paths), 4)
        self.assertTrue('tmp/pdm/mysql/bean/t_teachers.py' in paths)
        self.assertTrue('tmp/pdm/mysql/dao/t_teachers.py' in paths)
        self.assertTrue('tmp/pdm/mysql/bean/t_students.py' in paths)
        self.assertTrue('tmp/pdm/mysql/dao/t_students.py' in paths)


    def test_update(self) :
        from tests.tmp.pdm.mysql.bean.t_students import TStudents
        from tests.tmp.pdm.mysql.dao.t_students import TStudentsDao
        table = TStudents()
        dao = TStudentsDao()
        where = { (table.i_id + ' = '): 1 }

        # before
        bean = dao.query_one(M_DBC, where)
        bean.name = 'EXP'
        bean.remark = '289065406@qq.com'
        is_ok = dao.update(M_DBC, bean)
        self.assertTrue(is_ok)

        # after
        bean = dao.query_one(M_DBC, where)
        self.assertEqual(bean.name.decode(CHARSET), 'EXP')
        self.assertEqual(bean.remark.decode(CHARSET), '289065406@qq.com')


    def test_insert(self) :
        from tests.tmp.pdm.mysql.bean.t_students import TStudents
        from tests.tmp.pdm.mysql.dao.t_students import TStudentsDao
        bean = TStudents()
        bean.name = 'exp'
        bean.remark = 'https://github.com/lyy289065406/pypdm'

        dao = TStudentsDao()
        is_ok = dao.insert(M_DBC, bean)
        self.assertTrue(is_ok)


    def test_delete(self) :
        from tests.tmp.pdm.mysql.bean.t_students import TStudents
        from tests.tmp.pdm.mysql.dao.t_students import TStudentsDao
        table = TStudents()
        dao = TStudentsDao()
        where = { (table.i_id + ' = '): 2 }

        before_rownum = dao.count(M_DBC)
        is_ok = dao.delete(M_DBC, where)
        after_rownum = dao.count(M_DBC)
        self.assertTrue(is_ok)
        self.assertEqual(before_rownum - 1, after_rownum)


    def test_query(self) :
        from tests.tmp.pdm.mysql.dao.t_teachers import TTeachersDao
        dao = TTeachersDao()
        beans = dao.query_all(M_DBC)
        self.assertEqual(len(beans), 3)
        # for bean in beans :
        #     print(bean)


    def test_truncate(self) :
        from tests.tmp.pdm.mysql.dao.t_teachers import TTeachersDao
        dao = TTeachersDao()
        rownum = dao.count(M_DBC)
        self.assertEqual(rownum, 3)

        is_ok = dao.truncate(M_DBC)
        rownum = dao.count(M_DBC)
        self.assertTrue(is_ok)
        self.assertEqual(rownum, 0)


if __name__ == '__main__':
    unittest.main()



