class Table:
    def __init__(self,name="",attNum=0,attribute=[]):
        self.name=name
        self.attributeNum=attNum
        self.attribute=attribute[:]
        self.table_length=0
    def clear(self):
        self.name=""
        self.attributeNum=0
        self.attribute=list()
        self.table_length=0
    def __repr__(self):
        return self.name

class Attribute:
    def __init__(self,name='',type='',length=0,isPrimary=False,isUnique=False):
        self.name=name
        self.type=type
        self.isPrimary=isPrimary
        self.isUnique=isUnique
        self.length=int(length)
    def clear(self):
        self.name=''
        self.type=''
        self.isPrimary=False
        self.isUnique=False
        self.length=0
    def __repr__(self):
        return self.name+'\t'+self.type

class Index:
    def __init__(self,table_name="",index_name="",attribute_name=""):
        self.table_name=table_name
        self.index_name=index_name
        self.attribute_name=attribute_name
    def clear(self):
        self.index_name=''
        self.table_name=''
        self.attribute_name=''
    def __repr__(self):
        return self.index_name+'\t'+self.table_name+'\t'+self.attribute_name

class Condition:
    def __init__(self,attribute="",op="",value=0):
        self.attribute = attribute
        self.op = op
        self.value = value
        
    def clear(self):
        self.op=""
        self.attribute=""
        self.value=0

    def judge(self,value):
        if type(value)==type(1.0):#float
            if self.op=='<':
                return value<self.value
            elif self.op=='<=':
                return (value<self.value) or abs(self.value-value)<0.0001
            elif self.op=='>':
                return value>self.value
            elif self.op=='>=':
                return (value>self.value) or abs(self.value-value)<0.0001
            elif self.op=='=':
                return abs(self.value-value)<0.0001
            elif self.op=='!=':
                return not abs(self.value-value)<0.0001
            else:
                return False
        else:
            if self.op=='<':
                return value<self.value
            elif self.op=='<=':
                return value<=self.value
            elif self.op=='>':
                return value>self.value
            elif self.op=='>=':
                return value>=self.value
            elif self.op=='=':
                return self.value==value
            elif self.op=='!=':
                return not self.value==value
            else:
                return False
    
    def __repr__(self):
        return self.op+str(self.value)