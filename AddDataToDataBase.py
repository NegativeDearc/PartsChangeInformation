# -*- coding:utf-8 -*-
__author__ = 'SXChen'

import sqlite3
import pandas as pd
from xlrd_extra_info import extra_info

def add_data(SPEC):
    if len(str(SPEC)) != 4:
        return 'SPEC LENGTH ERROR, PLEASE CHECK'

    conn = sqlite3.Connection('c:/users/sxchen/desktop/PartsChangeInformation/main.db')
    cur = conn.cursor()

    #COUNT could find records of database,but the row [SPEC,0,0,0,0,0,0,0,0] also need to handle
    sql = "SELECT * FROM tb1 WHERE SPEC = '%s'" % SPEC
    sql2 = "SELECT COUNT(*) FROM tb1"
    sql3 = "SELECT COUNT(*) FROM tb1 WHERE SPEC = %s" % SPEC

    num, = cur.execute(sql3).fetchall()[0]
    if num > 0:
        print SPEC,'ALREADY EXISTED',cur.execute(sql).fetchall()
        return SPEC,'ALREADY EXISTED'

    lst = []
    res = extra_info(SPEC)
    lst.append(res)

    df = pd.DataFrame(lst,columns = ['SPEC',u'DIM',u'CENTER_DECK',u'PUSHOVER_CAN',u'SIDE_RING',u'BT_ADD',u'TRANSFER_RING',u'BO_PUSH_CAN'])
    df.to_sql('tb1',conn,'sqlite',if_exists = 'append',index = False)

    print cur.execute(sql).fetchall()
    print cur.execute(sql2).fetchall()

    cur.close()
    conn.commit()
    conn.close()

def db_to_dat():
    conn = sqlite3.Connection('c:/users/sxchen/desktop/PartsChangeInformation/main.db')
    pd.read_sql("SELECT * FROM tb1",conn).to_pickle('c:/users/sxchen/desktop/PartsChangeInformation/static/data.dat')

