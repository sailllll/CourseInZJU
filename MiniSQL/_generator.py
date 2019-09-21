f = open('1.txt', 'w')
f.write('drop table test;\ncreate table test(\n	ID int, name char(12) unique, primary key (ID)\n);\n')
for i in range(200000):
    f.write('insert into test values({}, \'{}\');\n'.format(i, 'orz'+str(i)))
f.write('delete from test where ID > 150000 and ID < 160000;\n')
f.close()