import pymysql
import Table
__metaclass__=type

class DBHelper:
    def GetConn(self):
        conn = pymysql.connect(host = "localhost",user="root",password="nevermind",port=3306,db="library",charset="utf8")
        return conn

#--------------------------------------------User----------------------------------------
    def UserInsert(self,NewUser):#注册账户
        sql ="insert into User(Account, Password, LibraryCard, CanBorrow, haveBorrowed) values (%s,%s,%s,%s,%s)"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(NewUser.getAccount(),NewUser.getPassword(),NewUser.getLibraryCard(),NewUser.getCanBorrow(),NewUser.getHaveBorrowed()))

        conn.commit()
        cursor.close()
        conn.close()

    def getUserAccount(self,Account):#得到账户信息
        sql = "select * from User where Account = %s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,str(Account))
        content = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return content
    def getAllUser(self):#得到所有用户的信息
        sql = "select * from User"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        content = cursor.fetchall()
        Alist=[(item[0],item[1],item[2],item[3],item[4]) for item in content]
        conn.commit()
        cursor.close()
        conn.close()
        return Alist
    def deleteUserAcount(self,Account):#删除账户
        sql = "delete from User where Account = %s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Account))

        conn.commit()
        cursor.close()
        conn.close()
    def updateUserLibCard(self,card,Num,Account):#更新用户的借书证和可借本书
        sql ="update User set LibraryCard=%s,CanBorrow=%s where Account=%s"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(card,Num,Account))
        conn.commit()
        cursor.close()
        conn.close()

    def updateUser(self,Account,User_Edit):#更新用户信息，如借书登记、授予借书证等
        sql = "update User set Password=%s,LibraryCard=%s,CanBorrow=%s,haveBorrowed=%s where Account=%s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(User_Edit.getPassword(),User_Edit.getLibraryCard(),User_Edit.getCanBorrow(),User_Edit.getHaveBorrowed(),Account))

        conn.commit()
        cursor.close()
        conn.close()
    def updateUserBorrow(self,Account,sign):#更新用户的已借书本数
        if sign=="+":
            sql="update User set haveBorrowed=haveBorrowed+1 where Account = %s"
        else:
            sql="update User set haveBorrowed=haveBorrowed-1 where Account = %s"
        conn = self.GetConn()
        if conn==None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,Account)
        conn.commit()
        cursor.close()
        conn.close()

#-------------------------------------------Manager---------------------------------------------------------------------------
    def ManagerInsert(self,NewManager):#插入一个新管理员
        sql ="insert into Manager(Account, Password) values (%s,%s)"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(NewManager.getAccount(),NewManager.getPassword()))

        conn.commit()
        cursor.close()
        conn.close()
    def getManagerAccount(self,Account):#得到账户信息
        sql = "select * from Manager where Account = %s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Account))
        content = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()
        return content
#------------------------------------------------Book-------------------------------------------------------------------
    def BookInsert(self,NewBook):#书籍入库
        sql ="insert into Book(ID, Name,Author,Press,PressDate,Type,Number) values (%s,%s,%s,%s,%s,%s,%s)"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(NewBook.getID(),NewBook.getName(),NewBook.getAuthor(),\
                            NewBook.getPress(),NewBook.getPressDate(),NewBook.getType(),NewBook.getNumber()))

        conn.commit()
        cursor.close()
        conn.close()
    def getMaxBookID(self):#得到最大书籍的编号  用于生成新ID
        sql = "select max(ID) from Book"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    def updateBook(self,Book_Edit,ID):#更新书籍信息
        sql = "update Book set Name=%s,Author=%s,Press=%s,PressDate=%s,Type=%s,Number=%s where ID=%s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Book_Edit.getName(),Book_Edit.getAuthor(),Book_Edit.getPress(),Book_Edit.getPressDate(),Book_Edit.getType(),Book_Edit.getNumber(),ID))

        conn.commit()
        cursor.close()
        conn.close()
    def updateNum(self,ID,change):#更改书籍的库存量
        if change=="+":
            sql = "update book set number=number+1 where ID=%s"
        elif change=="-":
            sql = "update book set number=number-1 where ID=%s"
        else:
            print("error in updateNum")
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(ID))
        conn.commit()
        cursor.close()
        conn.close()
    def deleteBook(self,ID):#删除书籍
        sql = "delete from Book where ID = %s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(ID))

        conn.commit()
        cursor.close()
        conn.close()
    def searchBook(self,book):#查询书籍
        sql = "select * from Book where"
        sign = 0
        conn = self.GetConn()
        if conn == None:
            return
        if book.getID()!="":
            sql=sql+" ID="+str(book.getID())
        else:
            if book.getName()!="":
                sign=1
                sql=sql+" Name like "+"\""+"%"+str(book.getName())+"%"+"\""

            if book.getAuthor()!="":
                if sign==0:
                    sign=1
                    sql = sql+" Author like \""+"%"+book.getAuthor()+"%"+"\""
                else:
                    sql = sql+" and Author like \""+"%"+book.getAuthor()+"%"+"\""

            if book.getPressDate()!="" and book.getPressDate()!=-1:
                if sign==0:
                    sign=1
                    sql = sql+" PressDate=\""+book.getPressDate()+"\""
                else:
                    sql = sql+" and PressDate=\""+book.getPressDate()+"\""

            if book.getPress()!="":
                if sign==0:
                    sign=1
                    sql = sql+" Press like \""+"%"+book.getPress()+"%"+"\""
                else:
                    sql = sql+" and Press like \""+"%"+book.getPress()+"%"+"\""

            if book.getType()!="" and book.getType()!=-1:
                if sign==0:
                    sign=1
                    sql = sql+" Type=\""+str(book.getType())+"\""
                else:
                    sql = sql+" and Type=\""+str(book.getType())+"\""

            if book.getNumber()>0:
                if sign==0:
                    sql=sql+" Number>0"
                else:
                    sql= sql +" and Number>0"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        content = cursor.fetchall()
        list = [(item[0],item[1],item[2],item[3],item[4],item[5],item[6]) for item in content]
        conn.commit()
        cursor.close()
        conn.close()
        return list

#-----------------------------------------------------------Loan------------------------------------------------------------------------
    def LoanInsert(self,NewLoan):#插入一个新借阅记录
        sql ="insert into Loan(Loan_ID,BookID, Account,Loan_Date,Deadline,Return_Date) values (%s,%s,%s,%s,%s,%s)"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(NewLoan.getLoan_ID(),NewLoan.getBookID(),NewLoan.getAccount(),\
                            NewLoan.getLoan_Date(),NewLoan.getDeadLine(),NewLoan.getReturnDate()))

        conn.commit()
        cursor.close()
        conn.close()
    def getBookIDByLoanID(self,Loan_ID):#根据借阅ID得到书籍ID
        sql ="select BookID from Loan where Loan_ID=%s"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Loan_ID))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    def updateReturnLoan(self,Return_Date,Loan_ID):#更新还书信息
        sql = "update Loan set Return_Date=%s where Loan_ID=%s"

        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Return_Date,Loan_ID))

        conn.commit()
        cursor.close()
        conn.close()

    def searchByAccount(self,Account):#根据账户查询借阅记录
        sql = "select * from Loan where Account = %s"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql,(Account))

        content = cursor.fetchall()
        list = [(item[0],item[1],item[2],item[3],item[4],item[5]) for item in content]

        conn.commit()
        cursor.close()
        conn.close()
        return list
    def getMaxBorrowID(self):#得到最大的借阅ID，用于生成新借阅ID
        sql = "select max(Loan_ID) from Loan"
        conn = self.GetConn()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
