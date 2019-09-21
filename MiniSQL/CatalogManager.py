
import ElementDef
class CatalogManager:
    def __init__(self, table=[], index=[]):
        self.table = table[:]
        self.index = index[:]
        self.tableNum = int(len(table))
        self.indexNum = len(index)

    def store_table_catalog(self):
        catalog_table_str = str(self.tableNum)+'\n'
        for element in self.table:
            catalog_table_str += element.name+' '
            catalog_table_str += str(element.attributeNum)+' '
            catalog_table_str += str(element.table_length)+'\n'
            for column in element.attribute:
                catalog_table_str += column.name+' '
                catalog_table_str += column.type+' '
                catalog_table_str += str(column.length)+' '
                catalog_table_str += str(int(column.isPrimary))+' '
                catalog_table_str += str(int(column.isUnique))+'\n'
        return catalog_table_str.encode('utf-8')

    def create_table_catalog(self, bytes_data):
        TableLog = bytes_data.decode('utf-8').rstrip().split('\n')
        self.tableNum = TableLog[0]   #get number of table
        if self.tableNum == "" or self.tableNum == None:
            self.tableNum = 0
        else:
            self.tableNum = int(self.tableNum)
        line_pos = 1
        for i in range(int(self.tableNum)): #get a table
            tempTable=ElementDef.Table()
            line = TableLog[line_pos].split()
            line_pos += 1
            tempTable.name=line[0]
            tempTable.attributeNum=int(line[1])
            tempTable.table_length=int(line[2])
            for j in range(tempTable.attributeNum):
                tempAttribute=ElementDef.Attribute()
                line = TableLog[line_pos].split()  #get a new attribute
                line_pos += 1
                tempAttribute.name = line[0]
                tempAttribute.type = line[1]
                tempAttribute.length = int(line[2])
                tempAttribute.isPrimary = bool(int(line[3]))
                tempAttribute.isUnique = bool(int(line[4]))
                tempTable.attribute.append(tempAttribute)
            self.table.append(tempTable)

    def store_index_catalog(self):
        catalog_index_str = str(self.indexNum)+'\n'
        for element in self.index:
            catalog_index_str += element.table_name+' '
            catalog_index_str += element.index_name+' '
            catalog_index_str += element.attribute_name+'\n'
        return catalog_index_str.encode('utf-8')

    def create_index_catalog(self, bytes_data):
        IndexLog = bytes_data.decode('utf-8').rstrip().split('\n')
        self.indexNum=IndexLog[0]
        if self.indexNum == "" or self.indexNum == None:
            self.indexNum=0
        else:
            self.indexNum = int(self.indexNum)
        line_pos = 1
        for i in range(self.indexNum):
            tempIndex = ElementDef.Index()
            line = IndexLog[line_pos].split()
            line_pos += 1
            tempIndex.table_name = line[0]
            tempIndex.index_name = line[1]
            tempIndex.attribute_name = line[2]
            self.index.append(tempIndex)

    def find_tablename(self,name):#check whether table exist
        for i in self.table:
            if name==i.name:
                return True
        return False

    def find_indexname(self,name):#check whether this index exist
        for i in self.index:
            if name==i.index_name:
                return True
        return False

    def find_attribute_index(self,table_name,attribute_name):#find a attribute's index
        for i in self.index:
            if i.table_name==table_name and i.attribute_name==attribute_name:
                return True
        return False


    def create_table(self,table):#create a new table
        self.tableNum+=1
        self.table.append(table)

    def create_index(self,index):#create a new index
        self.indexNum+=1
        self.index.append(index)

    def drop_table(self,table_name):#drop a table
        for i in range(len(self.table)):
            if self.table[i].name==table_name:
                del self.table[i]
                break
        self.tableNum-=1
        for i in self.index:#delete index on it
            if i.table_name==table_name:
                self.index.remove(i)
                self.indexNum-=1

    def drop_index(self,index_name):#drop an index
        for i in self.index:
            if i.index_name==index_name:
                self.index.remove(i)
                self.indexNum-=1

    def get_attribute(self,table_name):#get a table's attribute
        search_table=[i for i in self.table if i.name==table_name]
        result=[]
        for i in search_table[0].attribute:
            result.append([i.name,i.type,i.length])
        return result

    def get_tables(self):#get all tables' name
        result=[i.name for i in self.table]
        return result

    def get_primary(self,table_name):#find the primary key of a table
        for i in self.table:
            if i.name==table_name:#find the table
                for j in i.attribute:
                    if j.isPrimary==True:#find the primary key
                        return j.name

    def get_unique(self,table_name):
        res = []
        for i in self.table:
            if i.name==table_name:
                for j in i.attribute:
                    if j.isUnique==True:
                        res.append(j.name)
        return res
                        
    def get_indice(self,table):#find the attributes of a table that has an index
        result=[i.attribute_name for i in self.index if i.table_name==table]
        return result

    def get_index_info(self,index_name):#get the table and attribute of an index
        for i in self.index:
            if i.index_name==index_name:
                return [i.table_name,i.attribute_name]

    def get_length(self,table_name):
        for i in self.table:
            if i.name==table_name:#find the table
                return i.table_length

    def get_type_length(self,table_name):
        search_table=[i for i in self.table if i.name==table_name]
        result=[]
        for i in search_table[0].attribute:
            result.append([i.type,i.length])
        return result
    def get_attribute_type(self,table_name,attr_name):
        search_table=[i for i in self.table if i.name==table_name]
        for i in search_table[0].attribute:
            if i.name==attr_name:
                return i.type

    def check_unique(self,table_name,attr_name):
        search_table=[i for i in self.table if i.name==table_name]
        for i in search_table[0].attribute:
            if i.name==attr_name:
                return i.isUnique
        return False
