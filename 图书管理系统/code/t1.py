import wx
import time
import dbhelper
import Table
import page
class ExampleFrame(wx.Frame,):#图书管理系统的主界面
    def __init__(self, parent,User_Type,User_ID=""):
        self.user=User_Type
        self.UserID=User_ID
        style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,title="图书管理系统",size=(810,670),style=style)
        self.helper=dbhelper.DBHelper()
        self.Book=Table.Book("")
        self.SetBackgroundColour("#FFFFFF")
        self.Top=wx.Panel(self,size=(770,90),pos=(10,10))#顶端部分
        self.Display=wx.Panel(self,size=(770,300),pos=(10,110))#顶端部分
        self.Search = wx.Panel(self,size = (500,200),pos=(10,420))
        self.Switch = wx.Panel(self,size=(100,200),pos=(600,420))
        #----------------------Top---------------------------------------------------
        self.Top_text1=wx.StaticText(self.Top,label="图书管理系统",pos=(10,20))
        self.Top_text1.SetFont(wx.Font(30,wx.DECORATIVE,wx.NORMAL,wx.BOLD))

        self.time=wx.StaticText(self.Top,label="当前日期:"+time.strftime('%Y-%m-%d',time.localtime(time.time())),pos=(400,70))
        wx.StaticText(self.Top,label="当前用户:"+self.user,pos=(540,70))
        if self.user=="游客":
            self.enroll=wx.Button(self.Top,-1,label="注册",pos=(630,68),size=(50,20))
            self.login=wx.Button(self.Top,-1,label="登陆",pos=(700,68),size=(50,20))
            self.Bind(wx.EVT_BUTTON,self.Sign,self.enroll)
            self.Bind(wx.EVT_BUTTON,self.log,self.login)
        else:
            wx.StaticText(self.Top,label="用户名:"+User_ID,pos=(650,70))
            self.exit_button=wx.Button(self.Top,-1,label="退出",pos=(680,30),size=(50,20))
            self.Bind(wx.EVT_BUTTON,self.exit,self.exit_button)
        #---------------------------------Display-------------------------------------
        self.list =wx.ListCtrl(self.Display,-1,size=(700,280),style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list.InsertColumn(0,"书籍编号")
        self.list.InsertColumn(1,"书名")
        self.list.InsertColumn(2,"作者")
        self.list.InsertColumn(3,"出版社")
        self.list.InsertColumn(4,"出版时间")
        self.list.InsertColumn(5,"书籍类型")
        self.list.InsertColumn(6,"余量")

        self.list.SetColumnWidth(0,100)
        self.list.SetColumnWidth(1,120)
        self.list.SetColumnWidth(2,100)
        self.list.SetColumnWidth(3,80)
        self.list.SetColumnWidth(4,80)
        self.list.SetColumnWidth(5,80)
        self.list.SetColumnWidth(6,80)





        #------------------------------Search----------------------------------
        self.Search.SetFont(wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL))

        wx.StaticText(self.Search,label="书名",pos=(10,10))
        wx.StaticText(self.Search,label="作者",pos=(150,10))
        wx.StaticText(self.Search,label="出版社",pos=(300,10))
        wx.StaticText(self.Search,label="出版时间",pos=(250,75))
        wx.StaticText(self.Search,label="类型",pos=(10,75))
        wx.StaticText(self.Search,label="--",pos=(390,75))

        self.Search_text1=wx.TextCtrl(self.Search,-1,pos=(45,10),size=(100,20))
        self.Search_text2=wx.TextCtrl(self.Search,-1,pos=(185,10),size=(100,20))
        self.Search_text3=wx.TextCtrl(self.Search,-1,pos=(350,10),size=(130,20))

        self.Search_checkBox1=wx.CheckBox(self.Search,-1,"可租借",pos=(170,75))
        self.YearList=[str(x) for x in range(1970,2019)]
        self.TypeList=["计算机","外语","文学","艺术","经管","人文社科","少儿","生活",
                  "进口原版","科技","考试","离职","学术","古籍","哲学","旅游","法律",
                  "宗教","历史","地理","政治","军事心理学","传记","工具书","建筑","才会","教育",
                  "医学","电子电工","农业","文化","美食","娱乐时尚","青春文学","机械","美术","经济","化工",
                  "汽车与交通运输","健康","冶(yě)金","服饰美容","育儿","通信","管理","摄影","投资理财",
                  "音乐","少儿科普","家庭与办公","儿童文学","图象图形与多媒体","程序设计"]
        self.Search_List1=wx.Choice(self.Search,-1,(320,75),size=(70,20),choices=self.YearList)
        self.Search_List2=wx.Choice(self.Search,-1,(410,75),size=(70,20),choices=self.YearList)
        self.Search_List3=wx.Choice(self.Search,-1,(45,70),size=(100,25),choices=self.TypeList)

        self.Search_button1=wx.Button(self.Search,-1,label="搜索",pos=(100,120))
        self.Search_button2=wx.Button(self.Search,-1,label="重置",pos=(220,120))
        self.Search_button1.Bind(wx.EVT_BUTTON,self.search)
        self.Search_button2.Bind(wx.EVT_BUTTON,self.Search_Clear)

        #---------------------------------------------------------------------------------
        if self.user=="管理员":#管理员按钮
            self.Switch_button1=wx.Button(self.Switch,-1,label="单册入库",pos=(10,10))
            self.Switch_button2=wx.Button(self.Switch,-1,label="批量入库",pos=(10,50))
            self.Switch_button3=wx.Button(self.Switch,-1,label="单册编辑",pos=(10,90))
            self.Switch_button4=wx.Button(self.Switch,-1,label="用户管理",pos=(10,130))
            self.Bind(wx.EVT_BUTTON,self.AddOne,self.Switch_button1)
            self.Bind(wx.EVT_BUTTON,self.AddMul,self.Switch_button2)
            self.Bind(wx.EVT_BUTTON,self.EditOne,self.Switch_button3)
            self.Bind(wx.EVT_BUTTON,self.Manage,self.Switch_button4)
        elif self.user=="用户":#用户按钮
            self.Switch_button5=wx.Button(self.Switch,-1,label="借阅书籍",pos=(10,10))
            self.Switch_button6=wx.Button(self.Switch,-1,label="借阅记录",pos=(10,70))
            self.Bind(wx.EVT_BUTTON,self.BorrowBook,self.Switch_button5)
            self.Bind(wx.EVT_BUTTON,self.BorrowRecord,self.Switch_button6)
        self.Show()
    def Sign(self,evt):
        sign=page.Enroll(self)
        sign.Show()
    def log(self,evt):
        self.Destroy()
        page.Login(None)
    def AddOne(self,evt):#单册入库
        addABook = page.addAbook(self)
        addABook.Show()
    def AddMul(self,evt):#批量入库
        Addmul = page.MulInsert(self)
        Addmul.Show()
    def EditOne(self,evt):#单册编辑
        Editone = page.editAbook(self)
        Editone.Show()
    def Manage(self,evt):#账号管理
        Manage=page.AccountManage(self)
        Manage.Show()
    def BorrowBook(self,evt):#借阅书籍
        Borrow=page.BorrowBook(self,account=self.UserID)
        Borrow.Show()
    def BorrowRecord(self,evt):#借阅记录
        Record=page.BookRecord(self,account=self.UserID)
        Record.Show()
    def Search_Clear(self,evt):#重置按钮
        self.Search_List1.SetSelection(int(-1))
        self.Search_List2.SetSelection(int(-1))
        self.Search_List3.SetSelection(int(-1))
        self.Search_text1.Clear()
        self.Search_text2.Clear()
        self.Search_text3.Clear()
        self.Search.Refresh()
    def exit(self,evt):
        self.Destroy()
        ExampleFrame(None,"游客")

    def search(self,evt):#搜索按钮
        self.search_book()
    def search_book(self):#搜索函数
        self.list.DeleteAllItems()
        self.Book.setName(self.Search_text1.GetValue())
        self.Book.setAuthor(self.Search_text2.GetValue())
        self.Book.setPress(self.Search_text3.GetValue())
        if int(self.Search_List3.GetSelection())!=-1:
            self.Book.setType(self.TypeList[int(self.Search_List3.GetSelection())])
        else:
            self.Book.setType("")

        if self.Search_List1.GetSelection()==-1:
            y1=1970
        else:
            y1=int(self.YearList[int(self.Search_List1.GetSelection())])
        if self.Search_List2.GetSelection()==-1:
            y2=2019
        else:
            y2=int(self.YearList[int(self.Search_List2.GetSelection())])+1
        self.Book.setNumber(self.Search_checkBox1.GetValue())
        for i in range(y1,y2):
            if i!=-1:
                self.Book.setPressDate(str(i))
            list=self.helper.searchBook(self.Book)
            for k in list:
                index = self.list.InsertItem(self.list.GetItemCount(),str(k[0]))
                self.list.SetItem(index,1,k[1])
                self.list.SetItem(index,2,k[2])
                self.list.SetItem(index,3,k[3])
                self.list.SetItem(index,4,k[4])
                self.list.SetItem(index,5,str(k[5]))
                self.list.SetItem(index,6,str(k[6]))

app = wx.App(False)
ExampleFrame(None,"游客")

app.MainLoop()
