import CatalogManager
import Interpreter
import RecordManager
import FileManager
import IndexManager
import time

index_manager = None
catalog_manager = None
start_time = None
parser = None

def init():
    global index_manager, catalog_manager, parser
    index_manager = IndexManager.IndexManager(FileManager.load_index())
    catalog_manager = CatalogManager.CatalogManager()
    catalog_manager.create_table_catalog(FileManager.load_catalog(0))
    catalog_manager.create_index_catalog(FileManager.load_catalog(1))
    parser = Interpreter.command(catalog_manager)
    RecordManager.init(index_manager, catalog_manager)

def sql_exit():
    RecordManager.buf.save_all()
    FileManager.save_index(index_manager.Store())
    FileManager.save_catalog(0, catalog_manager.store_table_catalog())
    FileManager.save_catalog(1, catalog_manager.store_index_catalog())
    print('Bye\n')

def flush():
    global index_manager, catalog_manager, parser
    RecordManager.buf.save_all()
    FileManager.save_index(index_manager.Store())
    FileManager.save_catalog(0, catalog_manager.store_table_catalog())
    FileManager.save_catalog(1, catalog_manager.store_index_catalog())

    index_manager = IndexManager.IndexManager(FileManager.load_index())
    catalog_manager = CatalogManager.CatalogManager()
    catalog_manager.create_table_catalog(FileManager.load_catalog(0))
    catalog_manager.create_index_catalog(FileManager.load_catalog(1))
    parser = Interpreter.command(catalog_manager)
    RecordManager.init(index_manager, catalog_manager)
    print('All commited.')

#FileManager, IndexManager, Interpreter->CatalogManager, RecordManager->BufferManager
def create_table(table_name):
    attrs = catalog_manager.get_attribute(table_name)
    unique = catalog_manager.get_unique(table_name)
    FileManager.create_table(table_name)
    RecordManager.buf.update_table_list(catalog_manager.get_tables())
    index_manager.CreateTable(table_name, [(i[0], 4096//i[2]) for i in attrs if i[0] in unique])
    print('Query OK, 0 rows affected ({:.2f} sec)'.format(time.process_time()-start_time))

#RecordManager->BufferManager(FileManager), IndexManager, Interpreter->CatalogManager
def drop_table(table_name):
    RecordManager.buf.delete(table_name)
    RecordManager.buf.update_table_list(catalog_manager.get_tables())
    index_manager.DeleteTable(table_name)
    print('Query OK, 0 rows affected ({:.2f} sec)'.format(time.process_time()-start_time))
    
#Read-only
#RecordManager(CatalogManager, BufferManager(FileManager))
def select(table_name, attrs, conditions):
    all_attrs = catalog_manager.get_attribute(table_name)
    length_list = []
    for i in attrs:
        for j in all_attrs:
            if j[0] == i:
                if j[1] == 'int' or j[1] == 'float':
                    length_list.append((max((len(i), 12)), 0))
                else:
                    length_list.append((max((len(i), j[2])), 1))
                break
    res = RecordManager.select(table_name, attrs, conditions)
    if len(res) == 0:
        print('Empty set ({:.2f} sec)'.format(time.process_time()-start_time))
    else:
        print(format_record(None, length_list))
        print(format_record(attrs, length_list))
        print(format_record(None, length_list))
        for i in res:
            print(format_record(i, length_list))
        print(format_record(None, length_list))
        print('{} rows in set ({:.2f} sec)'.format(len(res), time.process_time()-start_time))

#Read-only
#RecordManager(CatalogManager, IndexManager, BufferManager(FileManager))
def select_index(table_name, attrs, index_conditions, other_conditions):
    all_attrs = catalog_manager.get_attribute(table_name)
    length_list = []
    for i in attrs:
        for j in all_attrs:
            if j[0] == i:
                if j[1] == 'int' or j[1] == 'float':
                    length_list.append((max((len(i), 12)), 0))
                else:
                    length_list.append((max((len(i), j[2])), 1))
                break
    res = RecordManager.select_index(table_name, attrs, index_conditions, other_conditions)
    if len(res) == 0:
        print('Empty set ({:.2f} sec)'.format(time.process_time()-start_time))
    else:
        print(format_record(None, length_list))
        print(format_record(attrs, length_list))
        print(format_record(None, length_list))
        for i in res:
            print(format_record(i, length_list))
        print(format_record(None, length_list))
        print('{} rows in set ({:.2f} sec)'.format(len(res), time.process_time()-start_time))

#RecordManager(CatalogManager, IndexManager, BufferManager(FileManager))
def delete(table_name, conditions):
    res = RecordManager.delete(table_name, conditions)
    print('Query OK, {} rows affected ({:.2f} sec)'.format(res, time.process_time()-start_time))

#RecordManager(CatalogManager, IndexManager, BufferManager(FileManager))
def insert(table_name, values):
    res = RecordManager.insert(table_name, values)
    if res == True:
        print('Query OK, 1 rows affected ({:.2f} sec)'.format(time.process_time()-start_time))

def format_record(record_tuple, length_list):
    if record_tuple == None:
        return '+-'+'-+-'.join([i[0]*'-' for i in length_list])+'-+'
    else:
        res = []
        for i in range(len(record_tuple)):
            if length_list[i][1] == 1:
                res.append(str(record_tuple[i]).ljust(length_list[i][0]))
            else:
                res.append(str(record_tuple[i]).rjust(length_list[i][0]))
        return '| '+' | '.join(res)+' |'

def execute(command_dict):
    global start_time
    start_time = time.process_time()
    if command_dict == None:
        print(parser.error_type)
        return
    if len(command_dict) == 0:
        print('ERROR: invalid command')
        return
    if command_dict['command_type'] == 'create_table':
        create_table(command_dict['table_name'])
    elif command_dict['command_type'] == 'drop_table':
        drop_table(command_dict['table_name'])
    elif command_dict['command_type'] == 'select':
        select(command_dict['table_name'], command_dict['attrs'], command_dict['conditions'])
    elif command_dict['command_type'] == 'select_index':
        select_index(command_dict['table_name'], command_dict['attrs'], command_dict['index_conditions'], command_dict['other_conditions'])
    elif command_dict['command_type'] == 'delete':
        delete(command_dict['table_name'], command_dict['conditions'])
    elif command_dict['command_type'] == 'insert':
        insert(command_dict['table_name'], command_dict['values'])
    elif command_dict['command_type'] == 'drop_index' or command_dict['command_type'] == 'create_index':
        print('Query OK, 0 rows affected ({:.2f} sec)'.format(time.process_time()-start_time))
    else:
        print('Error: unknown command \'{}\''.format(command_dict['command_type']))
    print()

def command_prompt():
    print('Welcome to the MySQL monitor.  Commands end with ;.')
    print('Server version: 1.0.0 MiniSQL Server')
    print('Copyright (c) 2018, 2018, ******. All rights reserved.')
    while True:
        command = input('minisql> ').strip()
        if command.startswith('#'):
            print(eval(command[1:]))
            continue
        while ';' not in command:
            command += ' '+input('       > ').strip()
        command = command[:command.find(';')].strip()
        if command == '':
            continue
        elif command.startswith('exec '):
            filename = command[command.find(' ')+1:]
            script = open(filename, 'r')
            while True:
                tmp = script.readline()
                if tmp == '':
                    break
                print(filename+'> '+tmp.strip())
                script_cmd = tmp.strip()
                while ';' not in script_cmd:
                    tmp = script.readline()
                    if tmp == '':   #incomplete command
                        script_cmd = '#'
                        break
                    print(filename+'> '+tmp.strip())
                    script_cmd += ' '+tmp.strip()
                if script_cmd == '#':   #ignore incomplete command
                    break
                script_cmd = script_cmd[:script_cmd.find(';')].strip()
                if script_cmd == 'exit':
                    sql_exit()
                    return
                elif script_cmd == 'flush':
                    flush()
                elif script_cmd.startswith('exec '):
                    print('Nested script not supported.')
                else:
                    execute(parser.sentence_analyse(script_cmd+';'))
            script.close()
            print('minisql> Script ended.')
            flush()
        elif command == 'exit':
            sql_exit()
            return
        elif command == 'flush':
            flush()
        else:
            execute(parser.sentence_analyse(command+';'))

if __name__ == '__main__':
    init()
    command_prompt()
