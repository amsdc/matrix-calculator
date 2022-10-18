import unittest
import matrixcalc.controllers
import matrices


class TestSQLAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.database = matrixcalc.controllers.SQLAdapter(":memory:")
    
    def tearDown(self) -> None:
        self.database.connection.close()
    
    def test_varadd(self):
        matar = matrices.Matrix([[3, 4, 2], [5, 7, 9], [1, 1, 1]])
        self.database.variable("dks", matar)
        self.assertTrue(self.database.list_all()[0][3][:] == matar[:])
        self.assertTrue(self.database.list_all()[0][1] == "assignment")
        self.assertTrue(self.database.list_all()[0][2] == "dks")
        
    def test_varrecall(self):
        matar = matrices.Matrix([[3, 4, 2], [5, 7, 9], [1, 1, 1]])
        self.database.variable("dks", matar)
        
        self.assertTrue(self.database.get_variable("dks")[:] == matar[:])
    
    def test_varedit(self):
        kajal = matrices.Matrix([[1, 3, 4]])
        self.database.variable("dks", kajal)
        matar = matrices.Matrix([[3, 4, 2], [5, 7, 9], [1, 1, 1]])
        self.database.variable("dks", matar)
        self.assertTrue(self.database.list_all()[0][3][:] == matar[:])
        self.assertTrue(self.database.list_all()[0][1] == "assignment")
        self.assertTrue(self.database.list_all()[0][2] == "dks")
    
    def test_operation(self):
        matar = matrices.Matrix([[3, 4, 2], [5, 7, 9], [1, 1, 1]])
        self.database.variable("dks", matar)
        deeksha2 = 2*matar
        self.database.operation("2*dks", deeksha2)
        self.assertTrue(self.database.list_all()[1][3][:] == deeksha2[:])
        self.assertTrue(self.database.list_all()[1][1] == "operation")
        self.assertTrue(self.database.list_all()[1][2] == "2*dks")

if __name__ == "__main__":
    unittest.main(verbosity=2)