import wx
import time
import Table
import dbhelper
import t1
class Enroll(wx.Frame):#注册账号
    def __init__(self, parent):
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="注册账号",size=(300,300),style=style)
        self.SetBackgroundColour("#FFFFFF")
        self.HeadLine=wx.StaticText(self,-1,label="账号注册",pos=(80,30))
        self.HeadLine.SetFont(wx.Font(20,wx.DECORATIVE ,wx.NORMAL,wx.BOLD))

        wx.StaticText(self,-1,label="用户名",pos=(50,100))
        wx.StaticText(self,-1,label="密码",pos=(50,135))
        wx.StaticText(self,-1,label="再次输入密码",pos=(50,170))
        wx.StaticText(self,-1,label="注意：账户注册后，需管理员授权后才能借书",pos=(30,220))

        self.account=wx.TextCtrl(self,-1,pos=(125,100),size=(-1,20))
        self.password=wx.TextCtrl(self,-1,pos=(125,135),size=(-1,20),style=wx.TE_PASSWORD)
        self.password_confirm=wx.TextCtrl(self,-1,pos=(125,170),size=(-1,20),style=wx.TE_PASSWORD)

        confirm_button = wx.Button(self,-1,label="确认",pos=(70,200),size=(50,20))
        exit_button = wx.Button(self,-1,label="退出",pos=(160,200),size=(50,20))

        self.Bind(wx.EVT_BUTTON,self.CreateAcount,confirm_button)
        self.Bind(wx.EVT_BUTTON,self.Exit,exit_button)
        self.helper=dbhelper.DBHelper()
        self.Show()
    def Exit(self,evt):
        self.Destroy()
    def CreateAcount(self,evt):
        account = self.account.GetValue()
        password = self.password.GetValue()
        password_confirm=self.password_confirm.GetValue()
        if account=="" or password=="" or password_confirm=="":
            warn=wx.MessageDialog(self,message="所有信息不能为空",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn.ShowModal()
            warn.Destroy()
            return
        elif password_confirm!=password:
            warn1=wx.MessageDialog(self,message="两次输入密码不一致",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn1.ShowModal()
            warn1.Destroy()
            return
        else:
            L=self.helper.getUserAccount(account)
            X=self.helper.getManagerAccount(account)
            if L!=None or X!=None:
                warn2=wx.MessageDialog(self,message="该用户名已被使用",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                warn2.ShowModal()
                warn2.Destroy()
                return
            else:
                User=Table.User(str(account),str(password))
                self.helper.UserInsert(User)
                warn3=wx.MessageDialog(self,message="注册成功",caption="注册结果",style=wx.YES_DEFAULT)
                warn3.ShowModal()
                warn3.Destroy()
        self.Destroy()

class Login(wx.Frame):#登陆账号
    def __init__(self, parent):
        self.User_Account=""
        self.sign=0
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="登陆",size=(300,300),style=style)
        self.user_type="游客"
        self.SetBackgroundColour("#FFFFFF")
        self.HeadLine=wx.StaticText(self,-1,label="登陆账号",pos=(80,30))
        self.HeadLine.SetFont(wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.BOLD))
        wx.StaticText(self,-1,label="用户名",pos=(50,100))
        wx.StaticText(self,-1,label="密码",pos=(50,135))
        self.account=wx.TextCtrl(self,-1,pos=(125,100),size=(-1,20))
        self.password=wx.TextCtrl(self,-1,pos=(125,135),size=(-1,20),style=wx.TE_PASSWORD)

        self.confirm_button = wx.Button(self,-1,label="确认",pos=(70,200),size=(50,20))
        self.exit_button = wx.Button(self,-1,label="退出",pos=(160,200),size=(50,20))
        self.Bind(wx.EVT_BUTTON,self.login,self.confirm_button)
        self.Bind(wx.EVT_BUTTON,self.exit,self.exit_button)
        self.helper=dbhelper.DBHelper()
        self.Show()

    def exit(self,evt):
        self.Destroy()

    def login(self,evt):
        account = self.account.GetValue()
        password = self.password.GetValue()
        if account=="" or password=="":
            warn=wx.MessageDialog(self,message="所有信息不能为空",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn.ShowModal()
            warn.Destroy()
            return
        User_content=self.helper.getUserAccount(account)
        Manager_content = self.helper.getManagerAccount(account)
        if User_content==None and Manager_content == None:
            warn1=wx.MessageDialog(self,message="此用户不存在",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn1.ShowModal()
            warn1.Destroy()
            return
        elif User_content != None:
            if User_content[1]==password:
                self.user_type="用户"
                self.User_Account=account
                t1.ExampleFrame(None,self.user_type,self.User_Account)
            else:
                warn2=wx.MessageDialog(self,message="密码错误",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                warn2.ShowModal()
                warn2.Destroy()
                return
        elif Manager_content !=None:
            if Manager_content[1]==password:
                self.user_type="管理员"
                self.User_Account=account
                t1.ExampleFrame(None,self.user_type,self.User_Account)
            else:
                warn3=wx.MessageDialog(self,message="密码错误",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                warn3.ShowModal()
                warn3.Destroy()
                return
        self.Destroy()


class addAbook(wx.Frame):#添加单册入库
    def __init__(self,parent):
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="单册入库",size=(550,250),style=style)
        self.SetFont(wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL))
        self.SetBackgroundColour("#FFFFFF")
        wx.StaticText(self,label="书名",pos=(10,10))
        wx.StaticText(self,label="作者",pos=(150,10))
        wx.StaticText(self,label="出版社",pos=(300,10))
        wx.StaticText(self,label="数量",pos=(150,75))
        wx.StaticText(self,label="出版时间",pos=(300,75))
        wx.StaticText(self,label="类型",pos=(10,75))

        self.text1=wx.TextCtrl(self,-1,pos=(45,10),size=(100,20))#书名
        self.text2=wx.TextCtrl(self,-1,pos=(185,10),size=(100,20))#作者
        self.text3=wx.TextCtrl(self,-1,pos=(350,10),size=(130,20))#出版社
        self.text4=wx.TextCtrl(self,-1,pos=(185,70),size=(100,25))#数量

        self.YearList=[str(x) for x in range(1970,2019)]
        self.TypeList=["计算机","外语","文学","艺术","经管","人文社科","少儿","生活",
                  "进口原版","科技","考试","离职","学术","古籍","哲学","旅游","法律",
                  "宗教","历史","地理","政治","军事心理学","传记","工具书","建筑","才会","教育",
                  "医学","电子电工","农业","文化","美食","娱乐时尚","青春文学","机械","美术","经济","化工",
                  "汽车与交通运输","健康","冶(yě)金","服饰美容","育儿","通信","管理","摄影","投资理财",
                  "音乐","少儿科普","家庭与办公","儿童文学","图象图形与多媒体","程序设计"]
        self.List1=wx.Choice(self,-1,(370,70),size=(70,25),choices=self.YearList)#出版日期
        self.List3=wx.Choice(self,-1,(45,70),size=(100,25),choices=self.TypeList)#种类

        self.button1=wx.Button(self,-1,label="入库",pos=(100,120))
        self.button2=wx.Button(self,-1,label="重置",pos=(220,120))
        self.Bind(wx.EVT_BUTTON,self.Insert,self.button1)#入库
        self.Bind(wx.EVT_BUTTON,self.clear,self.button2)#清空
        self.helper = dbhelper.DBHelper()
        self.Show()
    def clear(self,evt):
        self.text1.Clear()
        self.text2.Clear()
        self.text3.Clear()
        self.text4.Clear()
        self.List1.SetSelection(wx.NOT_FOUND)
        self.List3.SetSelection(wx.NOT_FOUND)
    def Insert(self,evt):
        L=self.helper.getMaxBookID()
        if L!=None:
            BookID = int(L[0])+1
        else:
            BookID = 10000
        Name=self.text1.GetValue()
        Author=self.text2.GetValue()
        Press=self.text3.GetValue()
        Number=self.text4.GetValue()
        Date=self.YearList[int(self.List1.GetSelection())]
        Type=self.TypeList[int(self.List3.GetSelection())]
        if Name=="" or Author=="" or Press=="" or Number=="" or Date=="" or Type=="":
            warn=wx.MessageDialog(self,message="所有信息均不能为空",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn.ShowModal()
            warn.Destroy()
            return
        Book=Table.Book(BookID,Name,Author,Press,Date,Type,Number)
        self.helper.BookInsert(Book)

class MulInsert(wx.Frame):#批量入库
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,title="批量入库",size=(300,300))
        self.helper=dbhelper.DBHelper()
        Dia=wx.FileDialog(parent,message="Choose a file",defaultDir="C:\\Users\Sail\Desktop\DBLab5",style=1)
        L=self.helper.getMaxBookID()
        if L!=None and L[0]!=None:
            BookID=int(L[0])+1
        else:
            BookID=10000

        if Dia.ShowModal()==wx.ID_OK:
            f=open(Dia.GetPath(),'r')
            num=1
            Book=Table.Book(BookID)
            for line in f:
                line.rstrip('\n')
                line=line.split()
                Book.setID(BookID)
                Book.setName(line[0])
                Book.setAuthor(line[1])
                Book.setPress(line[2])
                Book.setPressDate(line[3])
                Book.setType(line[4])
                Book.setNumber(line[5])
                BookID = BookID + 1
                self.helper.BookInsert(Book)
                num=num+1
                print(line)
            f.close()
            result=wx.MessageDialog(self,message="导入成功",caption="导入结果")
            result.ShowModal()
            result.Destroy()
        Dia.Destroy()
        self.Destroy()
class editAbook(wx.Frame):#编辑书籍
    def __init__(self,parent):
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="单册编辑",size=(550,250),style=style)
        self.SetFont(wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL))
        self.SetBackgroundColour("#FFFFFF")
        wx.StaticText(self,label="书名",pos=(10,10))
        wx.StaticText(self,label="作者",pos=(150,10))
        wx.StaticText(self,label="出版社",pos=(300,10))
        wx.StaticText(self,label="数量",pos=(150,75))
        wx.StaticText(self,label="出版时间",pos=(300,75))
        wx.StaticText(self,label="类型",pos=(10,75))
        wx.StaticText(self,label="输入书籍ID",pos=(10,125))

        self.text1=wx.TextCtrl(self,-1,pos=(45,10),size=(100,20))#书名
        self.text2=wx.TextCtrl(self,-1,pos=(185,10),size=(100,20))#作者
        self.text3=wx.TextCtrl(self,-1,pos=(350,10),size=(130,20))#出版社
        self.text4=wx.TextCtrl(self,-1,pos=(185,70),size=(100,25))#数量
        self.text5=wx.TextCtrl(self,-1,pos=(100,125),size=(100,20))

        self.YearList=[str(x) for x in range(1970,2019)]
        self.TypeList=["计算机","外语","文学","艺术","经管","人文社科","少儿","生活",
                  "进口原版","科技","考试","离职","学术","古籍","哲学","旅游","法律",
                  "宗教","历史","地理","政治","军事心理学","传记","工具书","建筑","才会","教育",
                  "医学","电子电工","农业","文化","美食","娱乐时尚","青春文学","机械","美术","经济","化工",
                  "汽车与交通运输","健康","冶(yě)金","服饰美容","育儿","通信","管理","摄影","投资理财",
                  "音乐","少儿科普","家庭与办公","儿童文学","图象图形与多媒体","程序设计"]
        self.List1=wx.Choice(self,-1,(370,70),size=(70,25),choices=self.YearList)#出版日期
        self.List3=wx.Choice(self,-1,(45,70),size=(100,25),choices=self.TypeList)#种类

        self.button1=wx.Button(self,-1,label="编辑",pos=(200,170))
        self.button2=wx.Button(self,-1,label="重置",pos=(300,170))
        self.button3=wx.Button(self,-1,label="查找",pos=(40,170))
        self.button4=wx.Button(self,-1,label="删除",pos=(400,170))
        self.Bind(wx.EVT_BUTTON,self.edit,self.button1)#入库
        self.Bind(wx.EVT_BUTTON,self.clear,self.button2)#清空
        self.Bind(wx.EVT_BUTTON,self.search,self.button3)#查找
        self.Bind(wx.EVT_BUTTON,self.delete,self.button4)#删除

        self.helper = dbhelper.DBHelper()
        self.Show()
    def delete(self,evt):
        self.ID = self.text5.GetValue()
        self.helper.deleteBook(self.ID)
        self.text1.Clear()
        self.text2.Clear()
        self.text3.Clear()
        self.text4.Clear()
        self.List1.SetSelection(wx.NOT_FOUND)
        self.List3.SetSelection(wx.NOT_FOUND)

    def clear(self,evt):
        self.text1.Clear()
        self.text2.Clear()
        self.text3.Clear()
        self.text4.Clear()
        self.text5.Clear()
        self.List1.SetSelection(wx.NOT_FOUND)
        self.List3.SetSelection(wx.NOT_FOUND)
    def search(self,evt):
        self.ID = self.text5.GetValue()
        if self.ID=="":
            warn0=wx.MessageDialog(self,message="请输入书籍编号",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn0.ShowModal()
            warn0.Destroy()
            return
        Book=Table.Book(self.ID)
        list = self.helper.searchBook(Book)
        for x in list:
            print(x)
        if list!=None and list!= []:
            self.text1.SetLabel(list[0][1])
            self.text2.SetLabel(list[0][2])
            self.text3.SetLabel(list[0][3])
            self.text4.SetLabel(str(list[0][6]))
            self.List1.SetSelection(int(self.YearList.index(list[0][4])))
            self.List3.SetSelection(int(self.TypeList.index(list[0][5])))
        else:
            warn1=wx.MessageDialog(self,message="未找到该书籍",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn1.ShowModal()
            warn1.Destroy()

    def edit(self,evt):
        global BookID
        Name=self.text1.GetValue()
        Author=self.text2.GetValue()
        Press=self.text3.GetValue()
        Number=self.text4.GetValue()
        Date=self.YearList[self.List1.GetSelection()]
        Type=self.TypeList[self.List3.GetSelection()]
        if Name=="" or Author=="" or Press=="" or Number=="" or Date=="" or Type=="":
            warn=wx.MessageDialog(self,message="所有信息均不能为空",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn.ShowModal()
            warn.Destroy()
            return
        Book=Table.Book(self.ID,Name,Author,Press,Date,Type,Number)
        self.helper.updateBook(Book,self.ID)
        warn4=wx.MessageDialog(self,message="修改成功",caption="修改结果",style=wx.YES_DEFAULT)
        warn4.ShowModal()
        warn4.Destroy()
class AccountManage(wx.Frame):#账户管理
    def __init__(self, parent):
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="账户管理",size=(800,600),style=style)
        self.SetBackgroundColour("#FFFFFF")
        self.helper=dbhelper.DBHelper()
        self.list =wx.ListCtrl(self,-1,size=(600,400),style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list.InsertColumn(0,"用户名")
        self.list.InsertColumn(1,"密码")
        self.list.InsertColumn(2,"借书证")
        self.list.InsertColumn(3,"可借本数")
        self.list.InsertColumn(4,"已借本数")

        self.list.SetColumnWidth(0,150)
        self.list.SetColumnWidth(1,100)
        self.list.SetColumnWidth(2,100)
        self.list.SetColumnWidth(3,100)
        self.list.SetColumnWidth(4,120)
        wx.StaticText(self,label="用户名",pos=(10,450))
        wx.StaticText(self,label="可借本数",pos=(180,450))

        self.text1=wx.TextCtrl(self,-1,pos=(60,450),size=(90,20))#用户名
        self.text4=wx.TextCtrl(self,-1,pos=(240,450),size=(50,20))#可借本数
        self.grant_button = wx.Button(self,-1,label="授权/删除账号",pos=(50,500),size=(100,40))
        self.edit_button = wx.Button(self,-1,label="编辑可借本数",pos=(200,500),size=(100,40))
        self.clear_button = wx.Button(self,-1,label="重置",pos=(350,500),size=(100,40))
        self.Bind(wx.EVT_BUTTON,self.grant,self.grant_button)
        self.Bind(wx.EVT_BUTTON,self.clear,self.clear_button)
        self.Bind(wx.EVT_BUTTON,self.edit,self.edit_button)
        self.display()
        self.Show()

    def display(self):
        Alist = self.helper.getAllUser()
        for x in Alist:
            index = self.list.InsertItem(self.list.GetItemCount(),str(x[0]))#用户名
            self.list.SetItem(index,1,x[1])#密码
            self.list.SetItem(index,2,str(x[2]))#借书证
            self.list.SetItem(index,3,str(x[3]))#已借
            self.list.SetItem(index,4,str(x[4]))#可借
    def grant(self,evt):
        Account = self.text1.GetValue()
        L=self.helper.getUserAccount(Account)
        if int(L[2])==0:#无借书证
            self.helper.updateUserLibCard(str(1),str(3),Account)
        else:
            if int(L[4])!=0:
                warn=wx.MessageDialog(self,"该用户有未还的图书，不可删除",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                warn.ShowModal()
                warn.Destroy()
                return
            else:
                self.helper.deleteUserAcount(Account)
                warn4=wx.MessageDialog(self,message="修改成功",caption="修改结果",style=wx.YES_DEFAULT)
                warn4.ShowModal()
                warn4.Destroy()

        self.list.DeleteAllItems()
        self.display()
    def edit(self,evt):
        Account = self.text1.GetValue()
        num = self.text4.GetValue()
        self.helper.updateUserLibCard(str(1),str(num),Account)
        self.list.DeleteAllItems()
        self.display()

    def clear(self,evt):
        self.text1.Clear()
        self.text4.Clear()
class BookRecord(wx.Frame):#借阅记录
    def __init__(self, parent,account):
        self.account=account
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="借阅记录",size=(800,600),style=style)
        self.SetBackgroundColour("#FFFFFF")
        self.helper=dbhelper.DBHelper()
        self.list =wx.ListCtrl(self,-1,size=(600,400),style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list.InsertColumn(0,"借阅编号")
        self.list.InsertColumn(1,"书本编号")
        self.list.InsertColumn(2,"书名")
        self.list.InsertColumn(3,"借阅日期")
        self.list.InsertColumn(4,"最晚归还日期")
        self.list.InsertColumn(5,"归还时间")

        self.list.SetColumnWidth(0,100)
        self.list.SetColumnWidth(1,100)
        self.list.SetColumnWidth(2,100)
        self.list.SetColumnWidth(3,100)
        self.list.SetColumnWidth(4,100)
        self.list.SetColumnWidth(5,100)
        wx.StaticText(self,label="借阅编号",size=(100,-1),pos=(10,450))


        self.text1=wx.TextCtrl(self,-1,pos=(120,450),size=(90,20))#借阅编号
        self.grant_button = wx.Button(self,-1,label="归还书籍",pos=(50,500),size=(100,40))
        self.Bind(wx.EVT_BUTTON,self.returnBook,self.grant_button)
        self.display()
        self.Show()

    def display(self):
        Alist = self.helper.searchByAccount(self.account)
        for x in Alist:
            index = self.list.InsertItem(self.list.GetItemCount(),str(x[0]))#Loan_ID
            self.list.SetItem(index,1,x[1])#Book_ID
            book = Table.Book(str(x[1]))
            name=self.helper.searchBook(book)
            if name!=None and name!= []:
                self.list.SetItem(index,2,str(name[0][1]))#Book_name
            self.list.SetItem(index,3,str(x[3]))#Loan_date
            self.list.SetItem(index,4,str(x[4]))#ddl
            self.list.SetItem(index,5,str(x[5]))#returnDate

    def returnBook(self,evt):
        Code = self.text1.GetValue()
        Date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        L=self.helper.updateReturnLoan(Date,Code)
        self.helper.updateUserBorrow(self.account,"-")
        NL=self.helper.getBookIDByLoanID(str(Code))
        BookID=str(NL[0])
        self.helper.updateNum(BookID,"+")
        warn4=wx.MessageDialog(self,message="归还成功",caption="归还结果",style=wx.YES_DEFAULT)
        warn4.ShowModal()
        warn4.Destroy()
        self.list.DeleteAllItems()
        self.display()
class BorrowBook(wx.Frame):#借阅一本书籍
    def __init__(self, parent,account):
        self.account=account
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="书籍借阅",size=(300,270),style=style)
        self.SetBackgroundColour("#FFFFFF")
        self.HeadLine=wx.StaticText(self,-1,label="书籍借阅",pos=(80,30))
        self.HeadLine.SetFont(wx.Font(20,wx.DECORATIVE ,wx.NORMAL,wx.BOLD))

        wx.StaticText(self,-1,label="书籍编号",pos=(50,100))

        wx.StaticText(self,-1,label="注意：请根据查询结果输入要借阅的书籍编号",pos=(30,180))

        self.ID=wx.TextCtrl(self,-1,pos=(125,100),size=(-1,20))
        confirm_button = wx.Button(self,-1,label="确认",pos=(70,150),size=(50,20))
        exit_button = wx.Button(self,-1,label="退出",pos=(160,150),size=(50,20))

        self.Bind(wx.EVT_BUTTON,self.Borrow,confirm_button)
        self.Bind(wx.EVT_BUTTON,self.Exit,exit_button)
        self.helper=dbhelper.DBHelper()
        self.Show()
    def Exit(self,evt):
        self.Destroy()
    def Borrow(self,evt):
        BookID = self.ID.GetValue()
        if BookID=="":
            warn=wx.MessageDialog(self,message="书籍编号不能为空",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
            warn.ShowModal()
            warn.Destroy()
            return
        else:
            book=Table.Book(BookID)
            L=self.helper.searchBook(book)
            if L==None or L==[]:
                warn1=wx.MessageDialog(self,message="图书库中不存在该书籍",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                warn1.ShowModal()
                warn1.Destroy()
                return
            else:
                for k in L:
                    if int(k[6])<=0:
                        warn2=wx.MessageDialog(self,message="该书暂无库存",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                        warn2.ShowModal()
                        warn2.Destroy()
                        return
                    else:
                        UserInfo=self.helper.getUserAccount(self.account)
                        if int(UserInfo[3])-int(UserInfo[4])<=0 :
                            for x in UserInfo:
                                print(x)
                            warn3=wx.MessageDialog(self,message="当前账户无借书证或借书数已达上限",caption="错误警告",style=wx.YES_DEFAULT|wx.ICON_ERROR)
                            warn3.ShowModal()
                            warn3.Destroy()
                        else:#借书成功
                            L=self.helper.getMaxBorrowID()
                            if L!=None and L[0]!=None:
                                LoanID=int(L[0])+1
                            else :
                                LoanID = 10000
                            BorrowDate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                            DDL=time.strftime('%Y-%m-%d',time.localtime(time.time()+24*3600*60))
                            self.helper.updateNum(BookID,"-")#库存变化 借阅变化 更新借阅记录
                            Loan = Table.Loan(BookID,self.account,LoanID,BorrowDate,DeadLine=DDL)
                            self.helper.LoanInsert(Loan)
                            self.helper.updateUserBorrow(self.account,"+")
                            warn4=wx.MessageDialog(self,message="借阅成功",caption="借阅结果",style=wx.YES_DEFAULT)
                            warn4.ShowModal()
                            warn4.Destroy()
        self.Destroy()

app = wx.App(False)
editAbook(None)
app.MainLoop()

