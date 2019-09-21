import pickle
import math
class BPT:
    Gap=0.0000000001
    def __init__(self,IndexName,n):
        self.Tree=[[-1]]#初始值，-1表示这个节点不是叶节点，但也没有子节点
        self.N=n
        self.IndexName=IndexName
        self.Half=int(n/2)+1
    def insert(self,T,value,address):
        NodeInfo=T[0]
        SonNum=len(T)-1
        if SonNum==0:#叶子节点，很开心
            LeafInfo=[1,value,address]
            InfoNum=len(NodeInfo)-1
            insertPos=-1
            for i in range(1,InfoNum+1):#找到插入点
                if type(LeafInfo[1])==float:
                   if NodeInfo[i][1]>LeafInfo[1]or math.fabs(NodeInfo[i][1]-LeafInfo[1])<self.Gap:
                        insertPos=i
                        break
                else:
                   if NodeInfo[i][1]>=LeafInfo[1]:
                        insertPos=i
                        break
            if type(LeafInfo[1])==float:
                if InfoNum==0:
                    NodeInfo.append(LeafInfo)
                elif math.fabs(NodeInfo[insertPos][1]-LeafInfo[1])<self.Gap:#曾经插入过
                    NodeInfo[insertPos][0]=1
                    NodeInfo[insertPos][2]=address
                else:
                    if insertPos==-1:
                        NodeInfo.append(LeafInfo)
                    else:
                        NodeInfo.insert(insertPos,LeafInfo)
            else:
                    if InfoNum==0:
                        NodeInfo.append(LeafInfo)
                    elif NodeInfo[insertPos][1]==LeafInfo[1]:#曾经插入过
                        NodeInfo[insertPos][0]=1
                        NodeInfo[insertPos][2]=address
                    else:
                        if insertPos==-1:
                            NodeInfo.append(LeafInfo)
                        else:
                            NodeInfo.insert(insertPos,LeafInfo)
            if InfoNum==self.N:#不行啊满了
                CutPos=int(self.N/2)+1
                NodeMax=NodeInfo[CutPos][1]#假设n=3,则现在有四个点，第2个是最大的
                Apart=NodeInfo[CutPos+1:]
                Apart.insert(0,1)#表明这不是顶层
                Apart=[Apart]#作为叶节点，是整个节点
                del(NodeInfo[CutPos+1:])
                Rtn=[NodeMax,Apart]#返回一个列表，第一位放最大值，第二位放分开后的部分
                if NodeInfo[0]==-1:#这个点是顶层
                    NodeInfo[0]=1#现在已经不是了
                    NewTop=[[-1,NodeMax],T,Apart]
                    self.Tree=NewTop
                    return 1
                else:
                    return Rtn
            else:
                    if NodeInfo[0]==-1:
                        self.Tree=T
                        return 1
                    else:
                        return 1

        else:#非叶子节点寻找位置
            SonPos=-1
            for i in range (1,SonNum):#n个儿子 n-1个标志
                if type(NodeInfo[i])==float:
                    if value<NodeInfo[i] or math.fabs(NodeInfo[i]-value)<self.Gap:
                        SonPos=i
                        break
                else:
                    if value<=NodeInfo[i] :
                        SonPos=i
                        break
            sit=self.insert(T[SonPos],value,address)
            if sit==1:#插入成功无需分裂
                if NodeInfo[0]==-1:
                    self.Tree=T
                    return 1
                else:
                    return 1
            else:#有新的块提上来
                if SonPos==-1:
                    T.append(sit[1])
                    NodeInfo.append(sit[0])
                else:
                    T.insert(SonPos+1,sit[1])
                    NodeInfo.insert(SonPos,sit[0])
                if SonNum==self.N:#最难受的部分，这一层索引已经有了n个
                    CutPos=int(self.N/2)+1
                    IndexMax=NodeInfo[CutPos]#假设n=3,则现在有四个点，第2个是最大的
                    Apart=T[CutPos+1:]
                    ApartIndex=NodeInfo[CutPos+1:]
                    ApartIndex.insert(0,1)#表明新的索引块不是顶层
                    Apart.insert(0,ApartIndex)
                    del(T[CutPos+1:])
                    del(NodeInfo[CutPos:])
                    Rtn=[IndexMax,Apart]#返回一个列表，第一位放索引最大值，第二位放分开后的部分
                    if NodeInfo[0]==-1:
                        NodeInfo[0]=1
                        NewTop=[[-1,IndexMax],T,Apart]
                        self.Tree=NewTop
                        return 1
                    else:
                        return Rtn
                else:
                    if NodeInfo[0]==-1:
                        self.Tree=T
                        return 1
                    else:
                        return 1
    def search(self,T,value):
        NodeInfo=T[0]
        SonNum=len(T)-1
        if SonNum==0:#叶节点
            Add=None
            for i in range(1,len(NodeInfo)):
                if type(value)==float:
                    if math.fabs(NodeInfo[i][1]-value)<self.Gap:
                        if NodeInfo[i][0]==1:
                            Add=NodeInfo[i][2]
                        break
                else:
                    if NodeInfo[i][1]==value:
                        if NodeInfo[i][0]==1:
                            Add=NodeInfo[i][2]
                        break
            return Add
        else:
            NextPos=-1
            for i in range(1,SonNum):
                if type(value)==float:
                    if value<NodeInfo[i] or math.fabs(value-NodeInfo[i])<self.Gap:
                        NextPos=i
                        break
                else:
                    if value<=NodeInfo[i]:
                        NextPos=i
                        break
            return self.search(T[NextPos],value)
    def delete(self,T,value):
        NodeInfo=T[0]
        SonNum=len(T)-1
        if SonNum==0:#叶节点开删！
            InfoNum=len(NodeInfo)
            DelPos=None
            for i in range(1,InfoNum):
                if type(value)==float:
                    if math.fabs(NodeInfo[i][1]-value)<self.Gap:
                        if NodeInfo[i][0]==1:
                            DelPos=i
                        break
                else:
                    if NodeInfo[i][1]==value:
                        if NodeInfo[i][0]==1:
                            DelPos=i
                        break
            if DelPos==None:#没找到
                return None
            else:
                NodeInfo[DelPos][0]=0
                return 1
        
        else:#非叶节点
            NextPos=SonNum
            for i in range(1,SonNum):
                if type(value)==float:
                    if value<NodeInfo[i] or math.fabs(value-NodeInfo[i])<self.Gap:
                        NextPos=i
                        break
                else:
                    if value<=NodeInfo[i]:
                        NextPos=i
                        break
            sit=self.delete(T[NextPos],value)
            if sit==None:
                return None
            else:
                return 1
    def search_in_range(self,T,dlimit,ulimit,result):
        NodeInfo=T[0]
        SonNum=len(T)-1
        if SonNum==0:#叶节点
            if len(NodeInfo)==1:#没得节点
                return
            if NodeInfo[0]==-1:
                if dlimit!=None:
                    if dlimit>NodeInfo[-1][1]:
                        return 
                if ulimit!=None:
                    if ulimit<NodeInfo[1][1]:
                        return
            if dlimit==None:#从头抓取
                dlimit=NodeInfo[1][1]
            if ulimit==None:#到尾截止
                ulimit=NodeInfo[len(NodeInfo)-1][1]
            if (ulimit < dlimit):
                result = list()
                return
            Pos=1
            for i in range(1,len(NodeInfo)):
                if type(dlimit)==float:
                    if NodeInfo[i][1]>dlimit or math.fabs(NodeInfo[i][1]-dlimit)<self.Gap:
                        Pos=i
                        break
                else:
                    if NodeInfo[i][1]>=dlimit:
                        Pos=i
                        break
            while Pos<len(NodeInfo):
                if NodeInfo[Pos][1]>ulimit:#超过上界
                    break
                else:
                    if NodeInfo[Pos][0]==1:
                        Info=[NodeInfo[Pos][1],NodeInfo[Pos][2]]
                        result.append(Info)
                Pos+=1
            return 
        else:#非叶节点
            StartPos=SonNum
            EndPos=SonNum
            if dlimit==None:
                StartPos=1
            else:
                for i in range(1,SonNum):
                    if type(dlimit)==float:
                        if NodeInfo[i]>dlimit or math.fabs(NodeInfo[i]-dlimit)<self.Gap:
                            StartPos=i
                            break
                    else:
                        if NodeInfo[i]>=dlimit:
                            StartPos=i
                            break
            if ulimit!=None:
                for i in range(1,SonNum):     
                    if type(dlimit)==float:
                        if NodeInfo[i]>ulimit or math.fabs(NodeInfo[i]-ulimit)<self.Gap:
                            EndPos=i
                            break
                    else:
                        if NodeInfo[i]>=ulimit:
                            EndPos=i
                            break
            if dlimit==None:
                if ulimit==None:#从头到尾
                    for i in range(StartPos,EndPos+1):
                        self.search_in_range(T[i],None,None,result)
                else:#从头到某个位置
                    for i in range(StartPos,EndPos):
                        self.search_in_range(T[i],None,None,result)
                    self.search_in_range(T[EndPos],None,ulimit,result)
            else:
                if ulimit==None:#从某个位置到尾
                    self.search_in_range(T[StartPos],dlimit,None,result)
                    for i in range(StartPos+1,EndPos+1):
                        self.search_in_range(T[i],None,None,result)
                else:#从某个位置到某个位置
                    if StartPos==EndPos:
                        self.search_in_range(T[StartPos],dlimit,ulimit,result)
                    else:
                        self.search_in_range(T[StartPos],dlimit,None,result)
                        for i in range(StartPos+1,EndPos):
                            self.search_in_range(T[i],None,None,result)
                        self.search_in_range(T[EndPos],None,ulimit,result)
            return
    def search_in_range_NE(self,T,dlimit,ulimit,result):
        self.search_in_range(T,dlimit,ulimit,result)
        if len(result)>=2:
            if type(result[0][0])==float:
                if dlimit!=None and math.fabs(result[0][0]-dlimit)<self.Gap:
                    del result[0]
                if ulimit!=None and math.fabs(result[-1][0]-ulimit)<self.Gap:
                    del result[-1]
                return
            else:
                if dlimit!=None and result[0][0]==dlimit:
                    del result[0]
                if ulimit!=None and result[-1][0]==ulimit:
                    del result[-1]
                return
        elif len(result)==1:
            if type(result[0][0])==float:
                if dlimit!=None and math.fabs(result[0][0]-dlimit)<self.Gap:
                    del result[0]
                elif ulimit!=None and math.fabs(result[0][0]-ulimit)<self.Gap:
                    del result[0]
                return
            else:
                if dlimit!=None and result[0][0]==dlimit:
                    del result[0]
                elif ulimit!=None and result[0][0]==ulimit:
                    del result[0]
                return
    def search_in_range_LNE(self,T,dlimit,ulimit,result):
        self.search_in_range(T,dlimit,ulimit,result)
        if len(result)>=1:
            if type(result[0][0])==float:
                if dlimit!=None and math.fabs(result[0][0]-dlimit)<self.Gap:
                    del result[0]
            else:
                if dlimit!=None and result[0][0]==dlimit:
                    del result[0]
        return
    def search_in_range_RNE(self,T,dlimit,ulimit,result):
        self.search_in_range(T,dlimit,ulimit,result)
        if len(result)>=1:
            if type(result[0][0])==float:
                if ulimit!=None and math.fabs(result[-1][0]-ulimit)<self.Gap:
                    del result[-1]
            else:
                if ulimit!=None and result[-1][0]==ulimit:
                    del result[-1]
        return
    
class IndexManager:
    def __init__(self,f):
        self.Index=pickle.loads(f)
        if type(self.Index)!=list:
            Index=[[0]]
    def __findIndex(self,TableName,IndexName):
        TablePos=None
        TableInfo=self.Index[0]
        for i in range(1,len(TableInfo)):
            if TableInfo[i]==TableName:
                TablePos=i
                break
        T=None
        TableIndex=self.Index[TablePos]
        for i in range(len(TableIndex)):
            if TableIndex[i].IndexName==IndexName:
                T=TableIndex[i]
                break
        return T
    def CreateTable(self,TableName,IndexList):#indexlist每个元素第一位表示索引名字，第二位表示叉树
        self.Index[0][0]+=1
        self.Index[0].append(TableName)
        TableIndex=[]
        for i in range(len(IndexList)):
            T=BPT(IndexList[i][0],IndexList[i][1])
            TableIndex.append(T)
        self.Index.append(TableIndex)
    def DeleteTable(self,TableName):
        TablePos=None
        for i in range(1,len(self.Index[0])):
            if self.Index[0][i]==TableName:
                TablePos=i
                break
        del self.Index[0][TablePos]
        del self.Index[TablePos]
        self.Index[0][0]-=1
    def CreateIndex(self,TableName,IndexName,n):
        TablePos=None
        for i in range(1,len(self.Index[0])):
            if self.Index[0][i]==TableName:
                TablePos=i
                break
        T=BPT(IndexName,n)
        self.Index[TablePos].append(T)
    def DeleteIndex(self,TableName,IndexName):
        TablePos=None
        for i in range(1,len(self.Index[0])):
            if self.Index[0][i]==TableName:
                TablePos=i
                break
        TableIndex=self.Index[TablePos]
        for i in range(len(TableIndex)):
            if TableIndex[i].IndexName==IndexName:
                del TableIndex[i]
                return
    def Insert(self,TableName,IndexName,value,address):
        T=self.__findIndex(TableName,IndexName)
        T.insert(T.Tree,value,address)
    def Delete(self,tableName,IndexName,value):
        T=self.__findIndex(tableName,IndexName)
        T.delete(T.Tree,value)
    def SearchOnValue(self,TableName,IndexName,value):
        T=self.__findIndex(TableName,IndexName)
        return T.search(T.Tree,value)
    def SearchInRange(self,TableName,IndexName,dlimit,ulimit):#返回列表
        T=self.__findIndex(TableName,IndexName)
        result=[]
        T.search_in_range(T.Tree,dlimit,ulimit,result)
        return result
    def SearchInRangeNE(self,TableName,IndexName,dlimit,ulimit):#返回列表
        T=self.__findIndex(TableName,IndexName)
        result=[]
        T.search_in_range_NE(T.Tree,dlimit,ulimit,result)
        return result
    def SearchInRangeLNE(self,TableName,IndexName,dlimit,ulimit):
        T=self.__findIndex(TableName,IndexName)
        result=[]
        T.search_in_range_LNE(T.Tree,dlimit,ulimit,result)
        return result
    def SearchInRangeRNE(self,TableName,IndexName,dlimit,ulimit):
        T=self.__findIndex(TableName,IndexName)
        result=[]
        T.search_in_range_RNE(T.Tree,dlimit,ulimit,result)
        return result    
    def Store(self):
        return pickle.dumps(self.Index,2)
