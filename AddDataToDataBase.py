# -*- coding:utf-8 -*-
__author__ = 'SXChen'

import sqlite3
import pandas as pd
from xlrd_extra_info import extra_info,extra_info_maxx

def add_data_VMI(SPEC):
    if len(str(SPEC)) != 4:
        return 'SPEC LENGTH ERROR, PLEASE CHECK'

    conn = sqlite3.Connection('c:/users/sxchen/desktop/PartsChangeInformation/main.db')
    conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    cur = conn.cursor()

    #COUNT could find records of database,but the row [SPEC,0,0,0,0,0,0,0,0] also need to handle
    sql = "SELECT * FROM tb1 WHERE SPEC = '%s'" % SPEC
    sql2 = "SELECT COUNT(*) FROM tb1"
    sql3 = "SELECT COUNT(*) FROM tb1 WHERE SPEC = %s" % SPEC
    sql4 = '''INSERT INTO tb1 (SPEC,MACHINE_TYPE,DIM,CENTER_DECK,PUSHOVER_CAN,SIDE_RING,BT_ADD,TRANSFER_RING,BO_PUSH_CAN)
              VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');'''
    sql5 = '''UPDATE tb1
              SET SPEC='%s',
                  MACHINE_TYPE='%s',
                  DIM='%s',
                  CENTER_DECK='%s',
                  PUSHOVER_CAN='%s',
                  SIDE_RING='%s',
                  BT_ADD='%s',
                  TRANSFER_RING='%s',
                  BO_PUSH_CAN='%s'
              WHERE (MACHINE_TYPE='VMI'
              AND SPEC='%s');'''

    num, = cur.execute(sql3).fetchall()[0]

    res = extra_info(SPEC)
    res2 = []
    res2.extend(res)
    res2.append(SPEC)

    #print res2
    if num > 0:
        print SPEC,'ALREADY EXISTED\n'
        print 'TRYING TO UPDATE...'
        cur.execute(sql5 % tuple(res2))
        print 'UPDATED!'
    else:
        cur.execute(sql4 % tuple(res))

    #cur.close()
    conn.commit()
    #conn.close()

def add_data_MAXX(SPEC):
    if len(str(SPEC)) != 4:
        return 'SPEC LENGTH ERROR, PLEASE CHECK'

    conn = sqlite3.Connection('c:/users/sxchen/desktop/PartsChangeInformation/main.db')
    conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    cur = conn.cursor()

    #COUNT could find records of database,but the row [SPEC,0,0,0,0,0,0,0,0] also need to handle
    sql3 = "SELECT COUNT(*) FROM tb1 WHERE SPEC = %s" % SPEC
    sql4 = '''INSERT INTO tb1 (SPEC,MACHINE_TYPE,DIM,CENTER_DECK,PUSHOVER_CAN,SIDE_RING,BT_ADD,TRANSFER_RING,BO_PUSH_CAN)
              VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');'''
    sql5 = '''UPDATE tb1
              SET SPEC='%s',
                  MACHINE_TYPE='%s',
                  DIM='%s',
                  CENTER_DECK='%s',
                  PUSHOVER_CAN='%s',
                  SIDE_RING='%s',
                  BT_ADD='%s',
                  TRANSFER_RING='%s',
                  BO_PUSH_CAN='%s'
              WHERE MACHINE_TYPE="MAXX"
              AND SPEC='%s';'''

    num, = cur.execute(sql3).fetchall()[0]

    res = extra_info_maxx(SPEC)
    res2 = []
    res2.extend(res)
    res2.append(SPEC)

    #print res,len(res)
    #print res2,len(res2)

    if num > 1:
        print SPEC,'ALREADY EXISTED'
        print 'TRYING TO UPDATE...'
        cur.execute(sql5 % tuple(res2))
        print 'UPDATED!'
    else:
        cur.execute(sql4 % tuple(res))

    #cur.close()
    conn.commit()
    #conn.close()

def db_to_dat():
    conn = sqlite3.Connection('c:/users/sxchen/desktop/PartsChangeInformation/main.db')
    pd.read_sql("SELECT * FROM tb1",conn).to_pickle('c:/users/sxchen/desktop/PartsChangeInformation/static/data.dat')

if __name__ == '__main__':
    add_data_VMI(1544)
    add_data_MAXX(1544)
    db_to_dat()