from abc import ABC, abstractmethod
import sqlite3
import pickle



class BaseAdapter(ABC):
    """This is ab Abstract Base Class for Matrix Storage Adapters.

    Inherit this class to create your own Storage Adapter."""

    @abstractmethod
    def variable(self, variable_name, matrix):
        """Add/Overwrite a matrix object to memory.

        Args:
            variable_name (str): The variable name to use for the matrix
            matrix (Matrix): The Matrix object to serialise and store

        Raises:
            
        """
        pass

    @abstractmethod
    def del_variable(self, variable_name):
        """Delete a matrix object to memory.

        Args:
            variable_name (str): The variable name to delete            
        """
        pass
    
    @abstractmethod
    def operation(self, expr, result):
        """Store an operation into the database.

        Args:
            expr (str): The expression evaluated
            result: The result
        """
        pass
    
    @abstractmethod
    def get_variable(self, variable_name):
        """Get the variable 

        Args:
            variable_name (str): Variable name
        """
        pass

    @abstractmethod
    def list_all(self):
        """List all the data in the file.

        Returns:
            list: This returns a list with 3-pair tuples containing the
            Operation Type, Key and Value.
        """
        pass


class SQLAdapter(BaseAdapter):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)

        cur = self.connection.cursor()
        # Type can be one of the two:
        # ass - Assignment actions
        # opr - Operations
        cur.execute("CREATE TABLE IF NOT EXISTS `operations` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `type` CHAR(3) DEFAULT \"ass\", `key` VARCHAR(100), `value` BLOB)")
        self.connection.commit()


    def variable(self, variable_name, matrix):
        pikld = pickle.dumps(matrix)
        
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM operations WHERE `type` = \"ass\" AND key = ? LIMIT 1", (variable_name,))
        res = cur.fetchone()
        if res:
            cur.execute("UPDATE operations SET value = ? WHERE id = ?", (pikld, res[0]))
        else:
            cur.execute("INSERT INTO operations (`type`, key, value) VALUES (\"ass\", ?, ?)", (variable_name, pikld))
        self.connection.commit()
        cur.close()

    def del_variable(self, variable_name, matrix):
        raise NotImplemented
    
    def get_variable(self, variable_name):
        cur = self.connection.cursor()
        cur.execute("SELECT value FROM operations WHERE `type` = \"ass\" AND key = ? LIMIT 1", (variable_name,))
        pikld = pickle.loads(cur.fetchone()[0])
        return pikld

    def operation(self, expr, result):
        pikld = pickle.dumps(result)
        
        cur = self.connection.cursor()
        cur.execute("INSERT INTO operations (`type`, key, value) VALUES (\"opr\", ?, ?)", (expr, pikld))
        self.connection.commit()
        cur.close()

    def list_all(self):
        cur = self.connection.cursor()
        cur.execute("SELECT id, `type`, key, value FROM operations")
        res = []
        for ie, ty, ke, va in cur.fetchall():
            if ty == "ass":
                ty = "assignment"
            elif ty == "opr":
                ty = "operation"
            va = pickle.loads(va)
            res.append((ie, ty, ke, va))
        cur.close()
        return res

Adapter = SQLAdapter