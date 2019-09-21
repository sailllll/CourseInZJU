import os
import pickle
import platform

if os.path.exists('record') == True:
    if os.path.isdir('record') == False:
        print('File Manager: Unable to initialize.')
else:
    os.mkdir('record')
    print('File Manager: Empty record dictory created.')

if os.path.exists('record/deleted_record') == True:
    if os.path.isdir('record/deleted_record') == False:
        print('File Manager: Unable to initialize.')
else:
    os.mkdir('record/deleted_record')

if os.path.exists('meta') == True:
    if os.path.isdir('meta') == False:
        print('File Manager: Unable to initialize.')
else:
    os.mkdir('meta')
    print('File Manager: Empty metadata dictory created.')

def create_table(table_name):
    f = open('record/{}'.format(table_name), 'wb')
    f.close()
    f = open('record/deleted_record/deleted_{}'.format(table_name), 'wb')
    f.close()

def delete_table(table_name):
    if platform.system() == 'Windows':
        os.system('del record\\{}'.format(table_name))
        os.system('del record\\deleted_record\\deleted_{}'.format(table_name))
    else:
        os.system('rm record/{}'.format(table_name))
        os.system('rm record/deleted_record/deleted_{}'.format(table_name))

def read_block(table_name, block_index):
    f = open('record/{}'.format(table_name), 'rb')
    f.seek(4096*block_index, 0)
    block = f.read(4096)
    f.close()
    return block

def write_block(table_name, block_index, block):
    f = open('record/{}'.format(table_name), 'rb+')
    f.seek(4096*block_index, 0)
    f.write(block)
    f.close()

def table_size(table_name):
    file_path = 'record/'+table_name
    size = os.path.getsize(file_path)
    return size//4096

def load_catalog(num):
    f = None
    if num == 0:
        try:
            f = open('meta/catalog_table', 'rb')
        except:
            print('File Manager: Empty catalog file A created.')
            f = open('meta/catalog_table', 'wb')
            f.close()
            f = open('meta/catalog_table', 'rb')
    else:
        try:
            f = open('meta/catalog_index', 'rb')
        except:
            print('File Manager: Empty catalog file B created.')
            f = open('meta/catalog_index', 'wb')
            f.close()
            f = open('meta/catalog_index', 'rb')
    data = f.read()
    f.close()
    return data

def save_catalog(num, data):
    f = None
    if num == 0:
        f = open('meta/catalog_table', 'wb')
    else:
        f = open('meta/catalog_index', 'wb')
    f.write(data)
    f.close()

def load_index():
    try:
        f = open('meta/index', 'rb')
    except:
        print('File Manager: Empty index file created.')
        f = open('meta/index', 'wb')
        f.write(pickle.dumps([[0]],2))
        f.close()
        f = open('meta/index', 'rb')
    data = f.read()
    f.close()
    return data

def save_index(data):
    f = open('meta/index', 'wb')
    f.write(data)
    f.close()

def load_deleted():
    res = dict()
    file_list = os.listdir('record/deleted_record')
    for i in file_list:
        if i.startswith('deleted_'):
            tmp = open('record/deleted_record/'+i, 'r')
            tmp_data = tmp.read().strip()
            if tmp_data == '':
                res[i[8:]] = list()
            else:
                res[i[8:]] = list(map(int, tmp_data.split('\n')))
            tmp.close()
    return res

def save_deleted(dict_data):
    file_list = dict_data.keys()
    for i in file_list:
        tmp = open('record/deleted_record/deleted_'+i, 'w')
        tmp.write('\n'.join(list(map(str, dict_data[i]))))
        tmp.close()
