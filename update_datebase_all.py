import os
import sqlite3
import pandas as pd

from xlrd_extra_info import extra_info,extra_info_maxx


class UpdateAll(object):

	def __init__(self):
		self.basedir = os.path.abspath(os.path.dirname(__file__))
		self.db_path = self.basedir + '\main.db'
		self.conn = sqlite3.Connection(self.db_path)
		self.cur = self.conn.cursor()

	def add_data_VMI(self,SPEC):
	    if len(str(SPEC)) != 4:
	        return 'SPEC LENGTH ERROR, PLEASE CHECK'

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

	    num, = self.cur.execute(sql3).fetchall()[0]

	    res = extra_info(SPEC)
	    res2 = []
	    res2.extend(res)
	    res2.append(SPEC)

	    #print res2
	    if num > 0:
	        print SPEC,'ALREADY EXISTED\n'
	        print 'TRYING TO UPDATE...'
	        self.cur.execute(sql5 % tuple(res2))
	        print 'UPDATED!'
	    else:
	        self.cur.execute(sql4 % tuple(res))

	def add_data_MAXX(self,SPEC):
		    if len(str(SPEC)) != 4:
		        return 'SPEC LENGTH ERROR, PLEASE CHECK'

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

		    num, = self.cur.execute(sql3).fetchall()[0]

		    res = extra_info_maxx(SPEC)
		    res2 = []
		    res2.extend(res)
		    res2.append(SPEC)

		    #print res,len(res)
		    #print res2,len(res2)

		    if num > 1:
		        print SPEC,'ALREADY EXISTED'
		        print 'TRYING TO UPDATE...'
		        self.cur.execute(sql5 % tuple(res2))
		        print 'UPDATED!'
		    else:
		        self.cur.execute(sql4 % tuple(res))

	def db_to_dat(self):
		pd.read_sql('''SELECT * FROM tb1''',self.conn).to_pickle(self.basedir + '\static\data.dat')

	def update_all(self):
		spec = self.cur.execute('''select SPEC,MACHINE_TYPE from tb1''').fetchall()
		for x in spec:
			if x[1] == u'VMI':
				print 'adding VMI spec %s ...' % x[0]
				try:
					self.add_data_VMI(x[0])
					self.conn.commit()
				except Exception, e:
					print 'something wrong with %s' %x[0]
					pass
			if x[1] == u'MAXX':
				print 'adding Maxx spec %s ...' % x[0]
				try:
					self.add_data_MAXX(x[0])
					self.conn.commit()
				except Exception:
					print 'something wrong with %s' %x[0]
					pass

		self.db_to_dat()
		self.conn.close()

if __name__ == '__main__':
	a = UpdateAll()
	# a.update_all()
	# extra_info(6897)
	a.update_all()