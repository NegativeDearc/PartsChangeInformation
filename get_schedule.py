# -*- coding:utf-8 -*-

import xlrd
import time
import pandas as pd
from itertools import chain

def get_schedule():
	path = u'P:/Production/Schedule_Data/Sharepoint/生管/计划日报表/16年计划日报表汇总/TBM/TBM plan/TBM Daily Report-2016(Jan).xlsx'
	try:
		book = xlrd.open_workbook(path,on_demand = True)
	except IOError:
		return 'No such file or directory!'
	today_sheet = str(time.localtime()[1]) + '.' + str(time.localtime()[2])
	try:
		sheet = book.sheet_by_name(today_sheet)
	except Exception:
		return 'No Sheet Name!'

	#row_num
	row_range = range(6,151)
	#day_spec
	day_spec = []
	day_num = []

	def data_clean(x):
		if isinstance(x,float):
			x = int(x)
			if str(x).startswith('99'):
				return x[2:]
			else:
				return str(x)
		if isinstance(x,str):
			return 0

	for row in row_range:
		if sheet.cell_value(row,2) == '':
			day_spec.append(0)
		elif str(int(sheet.cell_value(row,2))).startswith('99'):
			#str make sure pd.DataFrame will convert it to Python Object[string] or pd.merge will fail.
			day_spec.append(str(int(sheet.cell_value(row,2)))[2:])
		else:
			day_spec.append(str(int(sheet.cell_value(row,2))))

	for row in row_range:
		if sheet.cell_value(row,3) == '':
			day_num.append(None)
		else:
			day_num.append(sheet.cell_value(row,3))

	#night_spec
	night_spec = map(data_clean,[sheet.cell_value(row,8) for row in row_range])
	night_num =  map(data_clean,[sheet.cell_value(row,9) for row in row_range])

	#machine_name,FSR 4 * 12,DRA 6 * 7,VMI 5 *11
	machine = list(chain(*
			   [['FSR' + str(x) for x in sorted(4 * range(1,13))],
			   ['DRA' + str(y) for y in sorted(6 * range(1,8))]	,
			   ['VMI ' + str(z) for z in sorted(5 * range(1,12))]]))
	#dayshfit
	df = pd.DataFrame({
		'Machine':machine,
	    'SPEC':day_spec,
	    'NUM':day_num
		},columns= ['Machine','SPEC','NUM'],index = machine,dtype = 'O')
	#nightshift
	df1 = pd.DataFrame({
		'Machine':machine,
	    'SPEC':night_spec,
	    'NUM':night_num
		},columns= ['Machine','SPEC','NUM'],index = machine,dtype = 'O')
	#drop index contain FSR & DRA
	df2 = df[df.SPEC != 0].drop(machine[:-55])
	df4 = df1[df1.SPEC != 0].drop(machine[:-55])

	#database
	df3 = pd.read_pickle('c:/users/sxchen/desktop/PartsChangeInformation/static/data.dat')
	df3.columns = ['SPEC',u'DIM',u'CENTER_DECK',u'PUSHOVER_CAN',u'SIDE_RING',u'BT_ADD',u'TRANSFER_RING',u'BO_PUSH_CAN']

	return pd.merge(df2,df3,'left',on = 'SPEC'),pd.merge(df4,df3,'left',on = 'SPEC')

