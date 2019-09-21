import BufferManager
import FileManager
import struct
from functools import reduce

buf = None
i_manager = None
c_manager = None

class Record:
    def __init__(self, attrs):
        self.data = dict()
        self.attrs = attrs[:]

    def read_from_bytes(self, bytes_data):
        self.clear()
        valid = struct.unpack('?', bytes_data[:1])[0]
        self.data['valid'] = valid
        pos = 1
        temp = None
        for i in self.attrs:
            if i[1] == 'int':
                temp = struct.unpack('i', bytes_data[pos:pos+i[2]])[0]
            elif i[1] == 'char':
                temp = struct.unpack(str(i[2])+'s', bytes_data[pos:pos+i[2]])[0].decode('utf-8').rstrip('\x00')
            elif i[1] == 'float':
                temp = round(struct.unpack('f', bytes_data[pos:pos+i[2]])[0], 4)
            else:
                print('Error: attribute type unknown')
                return
            self.data[i[0]] = temp
            pos += i[2]

    def read_from_dict(self, dict_data):
        if set(dict_data.keys()) != set(i[0] for i in self.attrs):
            print('Error: attribute not matched')
            return
        self.data = dict_data.copy()

    def select_data(self, attrs):
        return tuple(self.data[i] for i in attrs)

    def to_bytes(self):
        bytes_data = struct.pack('?', True)
        for i in self.attrs:
            if i[1] == 'int':
                bytes_data += struct.pack('i', self.data[i[0]])
            elif i[1] == 'char':
                bytes_data += struct.pack(str(i[2])+'s', self.data[i[0]].encode('utf-8'))
            elif i[1] == 'float':
                bytes_data += struct.pack('f', self.data[i[0]])
        return bytes_data

    def clear(self):
        self.data.clear()

def init(index_manager, catalog_manager):
    global buf, i_manager, c_manager
    buf = BufferManager.Buffer(4096)
    i_manager = index_manager
    c_manager = catalog_manager
    buf.update_table_list(c_manager.get_tables())

def conditions_judge(record, conditions):
    if record.data['valid'] == False:
        return False
    for i in conditions:
        if i.judge(record.data[i.attribute]) == False:
            return False
    return True

def parse_range(condition):
    left, right = None, None
    left_type, right_type = 0, 0    #0:[], 1:()
    if condition.op == '=':
        left = right = condition.value
        left_type = right_type = 0
    elif condition.op == '!=':
        left = right = condition.value
        left_type = right_type = 1
    elif condition.op == '<':
        right = condition.value
        right_type = 1
    elif condition.op == '<=':
        right = condition.value
        right_type = 0
    elif condition.op == '>':
        left = condition.value
        left_type = 1
    elif condition.op == '>=':
        left = condition.value
        left_type = 0
    return (left, right, left_type, right_type)

def select_index(table_name, attrs, index_conditions, other_conditions):
    possible_res = []    #set of record_index(32bit)
    for i in index_conditions:
        r = parse_range(i)
        if r[0] == r[1] and r[2] == 0:
            possible_res.append({i_manager.SearchOnValue(table_name, i.attribute, i.value)})
        elif r[0] == r[1] and r[2] != 0:
            temp = i_manager.SearchInRange(table_name, i.attribute, None, None)
            possible_res.append(set(j[1] for j in temp if j[0] != i.value))
        else:
            if r[2] == 0 and r[3] == 0:
                temp = i_manager.SearchInRange(table_name, i.attribute, r[0], r[1])
                possible_res.append(set(j[1] for j in temp))
            elif r[2] == 1 and r[3] == 0:
                temp = i_manager.SearchInRange(table_name, i.attribute, r[0], r[1])
                possible_res.append(set(j[1] for j in temp if j[0] != r[0]))
            elif r[2] == 0 and r[3] == 1:
                temp = i_manager.SearchInRange(table_name, i.attribute, r[0], r[1])
                possible_res.append(set(j[1] for j in temp if j[0] != r[1]))
            else:
                possible_res.append(set(j[1] for j in i_manager.SearchInRangeNE(table_name, i.attribute, r[0], r[1])))
    possible_records = reduce(lambda x, y: x.intersection(y), possible_res)
    
    res = set()
    all_attrs = c_manager.get_attribute(table_name)
    record_length = c_manager.get_length(table_name)+1
    record = Record(all_attrs)
    for i in possible_records:
        block_index = i>>11
        block_offset = i%(2**11)
        block = buf.fetch_block(block_index)
        record.read_from_bytes(block.read(block_offset*record_length, record_length))
        if conditions_judge(record, other_conditions) == True:
            res.add(record.select_data(attrs))
        record.clear()
    return res

def select(table_name, attrs, conditions):
    res = set()
    block_num = FileManager.table_size(table_name)
    table_index = buf.table_list.index(table_name)
    record_length = c_manager.get_length(table_name)+1
    all_attrs = c_manager.get_attribute(table_name)
    record = Record(all_attrs)
    for i in range(block_num):
        block = buf.fetch_block((table_index<<16)+i)
        bytes_data = block.read()
        for j in range(4096//record_length):
            record.read_from_bytes(bytes_data[j*record_length:(j+1)*record_length])
            if conditions_judge(record, conditions) == True:
                res.add(record.select_data(attrs))
            record.clear()
    return res

def delete(table_name, conditions):
    res = 0
    block_num = FileManager.table_size(table_name)
    table_index = buf.table_list.index(table_name)
    attrs = c_manager.get_attribute(table_name)
    unique = c_manager.get_unique(table_name)
    record_length = c_manager.get_length(table_name)+1
    record = Record(attrs)
    for i in range(block_num):
        block = buf.fetch_block((table_index<<16)+i)
        bytes_data = block.read()
        for j in range(4096//record_length):
            record.read_from_bytes(bytes_data[j*record_length:(j+1)*record_length])
            if conditions_judge(record, conditions) == True:
                res += 1
                block.write(j*record_length, struct.pack('?', False))
                buf.deleted[table_name].append((block.index<<11)+j)
                for k in unique:
                    i_manager.Delete(table_name, k, record.select_data([k])[0])
            record.clear()
    return res

def insert(table_name, values):
    unique = c_manager.get_unique(table_name)
    for i in values.keys():
        if i in unique:
            if i_manager.SearchOnValue(table_name, i, values[i]) != None:
                print("ERROR: Duplicate entry '{}' for key '{}'".format(values[i], i))
                return False
    attrs = c_manager.get_attribute(table_name)
    record_length = c_manager.get_length(table_name)+1
    record = Record(attrs)
    record.read_from_dict(values)
    block, pos = buf.insert_position(table_name, record_length)
    block.write(pos, record.to_bytes())

    index_value = (block.index<<11) + pos//record_length
    for i in unique:
        if i_manager.Insert(table_name, i, values[i], index_value) == False:
            print('Error: failed to insert index')
    return True