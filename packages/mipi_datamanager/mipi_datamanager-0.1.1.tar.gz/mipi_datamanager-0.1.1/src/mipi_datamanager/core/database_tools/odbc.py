import pyodbc
import datetime as dt

class Odbc:
    """Creates an Odbc connection object to be used to specify the connection for mipi querys.
    This class automatically handles setup, tare down, and connection settings.
    """

    def __init__(self, dsn = None, driver = None, server = None, database = None, uid = None, pwd = None, trusted_connection = "yes"):

        #check param integrity
        # self.check_dsn_or_driver(dsn,driver)

        self.dsn = dsn
        self.driver = driver
        self.server = server
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.trusted_connection = trusted_connection



    @property
    def connection_string(self):
        con_str = ""
        params = {self.dsn:"DSN",
                  self.driver:"DRIVER",
                  self.server:"SERVER",
                  self.database:"DATABASE",
                  self.uid:"UID",
                  self.pwd:"PWD",
                  self.trusted_connection:"Trusted_Connection"}
        for param,key in params.items():
            if param:
                con_str += f"{key}={param};"

        return con_str

    def __enter__(self):
        self.con = pyodbc.connect(self.connection_string)
        self.start = dt.datetime.now()
        print(f"\nConnection Established: {self.database} @ {self.start}")
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()
        end = dt.datetime.now()
        print(f"Connection Terminated:  {self.database} @ {end}")
        print(f"Connection Open For:    {end - self.start}")
