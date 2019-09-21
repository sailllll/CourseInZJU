import time
__metaclass__=type
class Manager:#管理员表，包含用户名、密码
    def __init__(self,account="",password=""):
        self.Account = account
        self.Password = password

    def setAccount(self,acount):
        self.Account = acount

    def setPassword(self,password):
        self.Password = password

    def getAccount(self):
        return self.Account

    def getPassword(self):
        return self.Password

class User:#用户表,包含用户名、密码、有无借书证、可借书数、已借书数
    def __init__(self,account="",password="",libraryCard=0,canBorrow=0,haveBorrowed=0):
        self.Account = account
        self.Password = password
        self.LibraryCard = libraryCard
        self.CanBorrow = canBorrow
        self.HaveBorrowed= haveBorrowed

    def setAccount(self,account):
        self.Account = account

    def setPassword(self,password):
        self.Password = password

    def setLibraryCard(self,libraryCard):
        self.LibraryCard = libraryCard

    def setCanBorrow(self,canBorrow):
        self.CanBorrow = canBorrow

    def setHaveBorrowed(self,haveBorrowed):
        self.HaveBorrowed = haveBorrowed

    def getAccount(self):
        return self.Account

    def getPassword(self):
        return self.Password

    def getLibraryCard(self):
        return int(self.LibraryCard)

    def getCanBorrow(self):
        return int(self.CanBorrow)

    def getHaveBorrowed(self):
        return int(self.HaveBorrowed)

class Book:#书的列表
    def __init__(self,ID,Name="",Author="",Press="",PressDate="",Type="",Number=0):
        self.ID = ID
        self.Name = Name
        self.Author = Author
        self.Press = Press
        self.PressDate = PressDate
        self.Type = Type
        self.Number = Number

    def setID(self,ID):
        self.ID = ID

    def setName(self,Name):
        self.Name = Name

    def setAuthor(self,Author):
        self.Author = Author

    def setPress(self,Press):
        self.Press = Press

    def setPressDate(self,PressDate):
        self.PressDate = PressDate

    def setType(self,Type):
        self.Type = Type

    def setNumber(self,Number):
        self.Number = Number

    def getID(self):
        return self.ID

    def getName(self):
        return self.Name
    def getAuthor(self):
        return self.Author
    def getPress(self):
        return self.Press
    def getPressDate(self):
        return self.PressDate
    def getType(self):
        return self.Type
    def getNumber(self):
        return self.Number

class Loan:#借阅关系
    def __init__(self,BookID,Account,Loan_ID,Loan_Date="",DeadLine="",Return_Date=""):
        self.Loan_ID = Loan_ID
        self.BookID = BookID
        self.Account = Account
        self.Loan_Date = Loan_Date
        self.DeadLine=DeadLine
        self.Return_Date=Return_Date

    def setBookID(self,BookID):
        self.BookID = BookID

    def setAccount(self,Account):
        self.Account = Account

    def setLoan_ID(self,Load_ID):
        self.Loan_ID = Load_ID

    def setLoanDate(self,Loan_Date):
        self.Loan_Date = Loan_Date

    def setDeadLine(self,DeadLine):
        self.DeadLine=DeadLine

    def setReturnDate(self,Return_Date):
        self.Return_Date=Return_Date

    def getBookID(self):
        return self.BookID
    def getAccount(self):
        return self.Account
    def getLoan_ID(self):
        return self.Loan_ID
    def getLoan_Date(self):
        return self.Loan_Date
    def getDeadLine(self):
        return self.DeadLine
    def getReturnDate(self):
        return self.Return_Date

