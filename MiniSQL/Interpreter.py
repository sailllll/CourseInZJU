import re
import ElementDef
import copy

class command:
    def __init__(self, catalog_manager):
        self.Catlog = catalog_manager
        self.error_type=""
    def clear(self):
        self.error_type=""

    def save_data(self):
        self.Catlog.store_index_catalog()
        self.Catlog.store_table_catalog()
    def sentence_analyse(self,s):
        try:
            command_dict = {}
            cmd=[]
            sentence=re.split('[ ;(),]',s)
            for i in sentence:
                if i!="":
                    cmd.append(i)
            if cmd[0]=='create' and cmd[1]=='table':#create table
                command_dict = self.create_table(cmd)
            elif cmd[0]=='create' and cmd[1]=='index':#create index
                command_dict =self.create_index(cmd)
            elif cmd[0]=='drop' and cmd[1]=='table':#drop table
                command_dict =self.drop_table(cmd)
            elif cmd[0]=='drop' and cmd[1]=='index':#drop index
                command_dict =self.drop_index(cmd)
            elif cmd[0]=='select':#select
                command_dict =self.select(cmd)
            elif cmd[0]=='insert':#insert
                command_dict =self.insert(cmd)
            elif cmd[0]=='delete':#delete
                command_dict =self.delete(cmd)
            else:#invalid cmd
                self.error_type='ERROR:invalid cmd'
                return
            return command_dict
        except:
            self.error_type = 'ERROR:syntax error'
            return

#done
    def create_table(self,cmd):
        result_dict={}
        table=ElementDef.Table()#the table that will be created
        attribute=[]#attributes in this table
        if cmd[0]!="create" or cmd[1]!="table":
            self.error_type="ERROR:invalid cmd"
            return

        result_dict['command_type']='create_table'
        if len(cmd)>3:#get table name
            if self.Catlog.find_tablename(cmd[2]):#check whether table name exist
                self.error_type = "ERROR:exist table"
                return
            else:
                table.name=cmd[2]
                result_dict['table_name']=cmd[2]
        i=3#get a attribute's name and its type
        temp_attribute=ElementDef.Attribute()
        flag=False
        while i<len(cmd):
            '''
            for j in attribute:
                if j[0]==cmd[i]:
                    self.error_type = "ERROR:existed attribute"
                    return
            '''
            temp_attribute.name=cmd[i]#get attribute name
            i=i+1
            if cmd[i]=='int':#get attribute type
                temp_attribute.type='int'
                temp_attribute.length=4
                table.table_length+=4
                i=i+1
            elif cmd[i]=='char':
                if 2<=int(cmd[i+1])<=255:#check the digit of char
                    temp_attribute.type='char'
                    temp_attribute.length=int(cmd[i+1])
                    table.table_length+=int(cmd[i+1])
                else:
                    self.error_type = 'ERROR:invalid char digit'
                    print(self.error_type)
                    return
                i=i+2
            elif cmd[i]=='float':
                temp_attribute.type='float'
                temp_attribute.length=4
                table.table_length+=4
                i=i+1
            else:
                self.error_type = 'ERROR:unknown attribute type'
                return

            if i<len(cmd):#check where this cmd is end
                if cmd[i]=='primary' and cmd[i+1]=='key':#reach the end
                    temp_attribute.isUnique=False
                    temp_attribute.isPrimary=False
                    flag=True
                    break
                elif cmd[i]=='unique':
                    temp_attribute.isUnique=True
                    temp_attribute.isPrimary=False
                    i=i+1
                else:
                    temp_attribute.isPrimary=False
                    temp_attribute.isUnique=False
            else:
                self.error_type="ERROR:no primary key"
                return
            attribute.append(copy.deepcopy(temp_attribute))
            if flag==False:
                if i>=len(cmd):
                    self.error_type='ERROR:no primary key'
                    return
                if cmd[i]=='primary' and cmd[i+1]=='key':#reach the end after unique
                    break
        primarykey=""
        if  i<len(cmd):#primary key
            if cmd[i]=='primary' and cmd[i+1]=='key':
                i=i+2
                if i>=len(cmd):
                    self.error_type="ERROR:no primary key"
                    return
                primarykey_not_exist=False
                for k in range(len(attribute)):
                    if attribute[k].name==cmd[i]:
                        primarykey_not_exist=True
                        primarykey=cmd[i]
                        attribute[k].isPrimary=True
                        attribute[k].isUnique=True
                if primarykey_not_exist==False:
                    self.error_type="ERROR:primary key not exist"
                    return
                if flag==True:
                    attribute.append(copy.deepcopy(temp_attribute))
        table.attribute=attribute
        table.attributeNum=len(attribute)
        self.Catlog.create_table(table)
        #create primary key index
        primary_index=ElementDef.Index()
        primary_index.table_name=table.name
        primary_index.attribute_name=primarykey
        primary_index.index_name=table.name+'_'+primarykey
        self.Catlog.create_index(primary_index)

        return result_dict
#done
    def create_index(self,cmd):
        result_dict={}
        index=ElementDef.Index()
        if cmd[0]!='create' or cmd[1]!='index':
            self.error_type='ERROR:invalid cmd'
            return
        if len(cmd)<3:#no index name
            self.error_type = 'ERROR:empty index name'
            return

        result_dict['command_type']='create_index'
        index.index_name=cmd[2]
        if self.Catlog.find_indexname(cmd[2]):
            self.error_type='ERROR:index exist'
            return
        if cmd[3]!='on':
            self.error_type='ERROR:index error'
            return

        index.table_name=cmd[4]
        if self.Catlog.find_tablename(cmd[4])==False:#table not exist
            self.error_type='ERROR:table not exist'
            return

        #check whether this attribute has index and create index
        index.attribute_name=cmd[5]
        if self.Catlog.find_attribute_index(cmd[4],cmd[5]):#this attribute have index
            self.error_type='ERROR:index exist'
            return
        if self.Catlog.check_unique(cmd[4],cmd[5])==False:
            self.error_type='ERROR:not unique attribute'
        self.Catlog.create_index(index)
        return result_dict
#done
    def drop_table(self,cmd):
        result_dict={}
        if cmd[0]!='drop' or cmd[1]!='table':
            self.error_type='ERROR:invalid command'
            return
        result_dict['command_type']='drop_table'
        if len(cmd)<3:#empty table name
            self.error_type='ERROR:empty table name'
            return

        if self.Catlog.find_tablename(cmd[2]):
            result_dict['table_name'] = cmd[2]
            self.Catlog.drop_table(cmd[2])
            return result_dict
        else:
            self.error_type='ERROR:table not exists'
            return
#done
    def drop_index(self,cmd):
        result_dict={}
        if cmd[0]!='drop' or cmd[1]!='index':
            self.error_type='ERROR:invalid command'
            return

        result_dict['command_type']='drop_index'
        if len(cmd)<3:#no index name
            self.error_type='ERROR:empty index name'
            return

        if self.Catlog.find_indexname(cmd[2]):
            result_dict['index_name']=cmd[2]
            self.Catlog.drop_index(cmd[2])
            return result_dict
        else:
            self.error_type='ERROR:index not exists'
            return
#done
    def select(self,cmd):
        index_conditions=[]
        other_conditions=[]
        conditions=[]
        attribute=[]
        result_dict={}
        i=1
        if cmd[0]!='select':
            self.error_type='ERROR:invalid command'
            return

        if cmd[1]=='*':#select all attribute
            attribute=['*']
            i=i+1
        else:
            while cmd[i]!='from':#get attribute
                attribute.append(cmd[i])
                i=i+1
        if cmd[i]!='from':
            self.error_type='ERROR:invalid command'
            return
        i=i+1
        result_dict['table_name'] = cmd[i]
        if not self.Catlog.find_tablename(result_dict['table_name']):
            self.error_type = 'ERROR:table not exist'
            return
        if len(attribute) == 0:
            self.error_type = 'ERROR:syntax error'
            return
        if attribute[0]=='*':#select all
            attribute_list=self.Catlog.get_attribute(cmd[i])
            attribute=[i[0] for i in attribute_list]
        else:
            attr_name = [i[0] for i in self.Catlog.get_attribute(result_dict['table_name'])]
            for j in attribute:
                if j not in attr_name:
                    self.error_type = 'ERROR:invalid attribute'
                    return
                

        result_dict['attrs']=attribute
        result_dict['conditions']=[]
        result_dict['index_conditions']=[]
        result_dict['other_conditions']=[]
        index_list=self.Catlog.get_indice(result_dict['table_name'])
        result_dict['command_type']='select'
        i=i+1
        if i>=len(cmd):#no where-clause
            return result_dict
        else:
            if cmd[i]!='where':
                self.error_type='ERROR:invalid command'
            else:
                i=i+1
                attr_type=self.Catlog.get_attribute_type(result_dict['table_name'], cmd[i])
                if attr_type=='int':
                    cmd[i+2]=int(cmd[i+2])
                elif attr_type=='float':
                    cmd[i+2]=float(cmd[i+2])
                elif attr_type == 'char':
                    cmd[i+2]=str(cmd[i+2][1:-1])
                else:
                    self.error_type = 'ERROR:invalid condition'
                    return

                if cmd[i] in index_list:
                    result_dict['command_type']='select_index'
                    conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                    index_conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                else:
                    conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                    other_conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))

                #attribute operator value
                i=i+4
                while(i<len(cmd)):#more condition
                    attr_type=self.Catlog.get_attribute_type(result_dict['table_name'], cmd[i])
                    if attr_type=='int':
                        cmd[i+2]=int(cmd[i+2])
                    elif attr_type=='float':
                        cmd[i+2]=float(cmd[i+2])
                    else:
                        cmd[i+2]=str(cmd[i+2][1:-1])
                    if cmd[i] in index_list:
                        result_dict['command_type']='select_index'
                        conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                        index_conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                    else:
                        conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                        other_conditions.append(ElementDef.Condition(cmd[i],cmd[i+1],cmd[i+2]))
                    i=i+4#and op1 operator op2
        result_dict['index_conditions']=index_conditions
        result_dict['other_conditions']=other_conditions
        result_dict['conditions']=conditions
        return result_dict
#done
    def insert(self,cmd):
        result_dict={}
        if cmd[0]!='insert' or cmd[1]!='into':
            self.error_type='ERROR:invalid command'
            return

        result_dict['command_type']='insert'

        if len(cmd)<3:
            self.error_type='ERROR:empty table'
            return

        if self.Catlog.find_tablename(cmd[2])==False:#check whether table exist
            self.error_type='ERROR:table not exist'
            return
        else:
            result_dict['table_name']=cmd[2]
            attribute_list=self.Catlog.get_attribute(cmd[2])

        if cmd[3]!='values':
            self.error_type='ERROR:insert'
            return
        values={}
        i=0
        try:
            if len(cmd[4:]) != len(self.Catlog.get_attribute(cmd[2])):
                print('debug', len(cmd[4:]), self.Catlog.get_attribute(cmd[2]))
                0/0
            for v in cmd[4:]:
                type_list=self.Catlog.get_type_length(cmd[2])
                if type_list[i][0]=='int':
                    v=int(v)
                    if v>2147486348 or v<-2147486348:
                        self.error_type="ERROR:int value out of range"
                        return
                elif type_list[i][0]=='float':
                    v=float(v)
                else:#char
                    if v[0] != v[-1]:
                        0/0
                    elif v[0] != '\'' and v[0] != '\"':
                        0/0
                    v=str(v[1:-1])
                    if len(v)>int(type_list[i][1]):
                        self.error_type="ERROR:char length out of range"
                        return

                values[attribute_list[i][0]] = v
                i=i+1
        except:
            self.error_type='ERROR:data type not matched'
            return

        result_dict['values']=values
        return result_dict
#done
    def delete(self,cmd):
        condition=[]
        table=ElementDef.Table()
        result_dict={}
        if cmd[0]!='delete' or cmd[1]!='from':
            self.error_type = 'ERROR:invalid command'
            return
        result_dict['command_type']='delete'

        if len(cmd)<3:
            self.error_type='ERROR:empty table'
            return

        if self.Catlog.find_tablename(cmd[2])==False:#check whether table exist
            self.error_type='ERROR:table not exist'
            return
        else:
            table.name = cmd[2]#store table name
            result_dict['table_name']=cmd[2]

        if len(cmd)==3:#no where-clause
            result_dict['conditions']=[]
            return result_dict
        if cmd[3]!='where':
            self.error_type='ERROR:delete-condition'
            return
        #analyse where-clause
        #if (len(cmd)-4)%3!=0:#valid condition
            #self.error_type='ERROR:delete-condition'
            #return
        tempCondition=ElementDef.Condition()
        #get the first condition
        tempCondition.attribute=cmd[4]
        tempCondition.op=cmd[5]
        tempCondition.value=eval(cmd[6])
        condition.append(tempCondition)#op1  operator op2
        #other condition
        for i in range(2,(len(cmd)-3)//4 + 1):#/4 reason: and op1 operator op2
            condition.append(ElementDef.Condition(cmd[4*i],cmd[4*i+1],eval(cmd[4*i+2])))#op1 operator op2
        result_dict['conditions']=condition
        return result_dict
