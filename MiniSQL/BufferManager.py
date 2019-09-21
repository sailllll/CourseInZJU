import io
import FileManager
import struct

class Block:
    def __init__(self):
        self.data = io.BytesIO()
        self.index = -1
        self.last_used = -1
        self.dirty = False
        self.pinned = False

    def read(self, pos=0, length=4096):
        self.data.seek(pos, 0)
        content = self.data.read(length)
        self.data.seek(0, 0)
        return content

    def write(self, pos, content):
        if pos+len(content) > 4096:
            print('Error: block size out of range')
            return
        self.dirty = True
        self.data.seek(pos, 0)
        self.data.write(content)
        self.data.seek(0, 0)
    
class Buffer:
    def __init__(self, size=4096):
        self.size = size
        self.blocks = tuple(Block() for i in range(size))
        self.counter = 0
        self.table_list = None
        self.deleted = FileManager.load_deleted().copy()

    def first_vacancy(self):
        used = [(self.blocks[i].last_used) for i in range(self.size)]
        least_used = used.index(min(used))
        if self.blocks[least_used].index != -1:
            self.save_block(self.blocks[least_used])
        return self.blocks[least_used]

    def update_table_list(self, lst):
        self.table_list = lst[:]
        for i in self.table_list:
            if i not in self.deleted.keys():
                self.deleted[i] = list()
        tmp = tuple(self.deleted.keys())
        for i in tmp:
            if i not in self.table_list:
                self.deleted.pop(i)

    def load_block(self, block_index):
        block = self.first_vacancy()
        data = FileManager.read_block(self.table_list[block_index>>16], block_index%(1<<16))
        block.index = block_index
        block.last_used = self.counter
        block.write(0, data)
        return block

    def write_back(self, block):
        FileManager.write_block(self.table_list[block.index>>16], block.index%(1<<16), block.read())
        block.dirty = False

    def save_block(self, block):
        if block.pinned == True:
            print('Error: block pinned')
            return
        if block.dirty == True:
            FileManager.write_block(self.table_list[block.index>>16], block.index%(1<<16), block.read())
        block.last_used = -1
        block.index = -1
        block.dirty = False
        block.data = io.BytesIO()

    def fetch_block(self, block_index):
        self.counter += 1
        for i in self.blocks:
            if i.index == block_index:
                i.last_used = self.counter
                if i.dirty == True:
                    self.write_back(i)
                return i
        return self.load_block(block_index)

    def fetch_block_without_loading(self, block_index):
        for i in self.blocks:
            if i.index == block_index:
                self.counter += 1
                i.last_used = self.counter
                return i
        return None

    def append_block(self, table_name):
        self.counter += 1
        block = self.first_vacancy()
        block.index = (self.table_list.index(table_name)<<16)+FileManager.table_size(table_name)
        block.last_used = self.counter
        block.write(4095, b'\x00')
        FileManager.write_block(table_name, block.index%(1<<16), block.read())
        return block

    def save_table(self, table_name):
        table_index = self.table_list.index(table_name)
        for i in self.blocks:
            if i.index>>16 == table_index:
                if i.dirty == True:
                    FileManager.write_block(self.table_list[i.index>>16], i.index%(1<<16), i.read())
                i.dirty = False

    def save_all(self):
        FileManager.save_deleted(self.deleted.copy())
        for i in self.blocks:
            self.save_block(i)
    
    def delete(self, table_name):
        table_index = self.table_list.index(table_name)
        for i in self.blocks:
            if i.index>>16 == table_index:
                i.dirty = False
                self.save_block(i)
        FileManager.delete_table(table_name)

    def insert_position(self, table_name, record_length):
        #deleted list
        if len(self.deleted[table_name]) != 0:
            tmp = self.deleted[table_name][-1]
            self.deleted[table_name].pop(-1)
            return (self.fetch_block(tmp>>11), tmp%(1<<11))
        #last/new block
        block_num = FileManager.table_size(table_name)
        record_num = 4096//record_length
        start = max((0, block_num-1))
        for i in range(start, block_num):
            x = self.fetch_block_without_loading((self.table_list.index(table_name)<<16)+i)
            data = x.read() if x != None else FileManager.read_block(table_name, i)
            for j in range(record_num):
                if struct.unpack('?', data[j*record_length:j*record_length+1])[0] == False:
                    if x != None:
                        return (x, j*record_length)
                    else:
                        return (self.load_block((self.table_list.index(table_name)<<16)+i), j*record_length)
        self.save_table(table_name)
        return (self.append_block(table_name), 0)