# -*- coding: utf-8 -*-

import xlrd
import os

def extra_info(vmi_spec):
	vmi_spec = str(vmi_spec)

	product_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/'
	test_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/试制准备/'
	project_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/试制准备/项目基准/'

	product_spec_lst = os.listdir(product_spec_path)
	test_spec_lst = os.listdir(test_spec_path)
	project_spec_lst = os.listdir(project_spec_path)

	spec_path = [product_spec_path + x for x in product_spec_lst if x.endswith('.xls') and vmi_spec in x]
	if len(spec_path) == 0:
		spec_path = [test_spec_path + x for x in test_spec_lst if x.endswith('.xls') and vmi_spec in x]
		if len(spec_path) == 0:
			spec_path = [project_spec_path + x for x in project_spec_lst if x.endswith('.xls') and vmi_spec in x]

	if len(spec_path) > 0:
		book = xlrd.open_workbook(spec_path[0],on_demand = True)
		sheet_names = book.sheet_names()
		#print sheet_names

		for x in sheet_names:
			a = x.split(' ')[0]
			if 'CURRENT' == a.upper():
				sheet = book.sheet_by_name(x)
				break
			else:
				sheet = None

		#if didn't have 'current' sheet,find the last? the 'base'?
		#use regexp to find the newest(the lagerest number)?
		if not isinstance(sheet,xlrd.sheet.Sheet):
			sheet_names.sort(key = unicode.upper)
			sheet = book.sheet_by_name(sheet_names[-1])

		p = [[],[]]
		for x in range(55)[1:]:
			cell_obj_19 = sheet.cell(x,19)
			cell_obj_20 = sheet.cell(x,20)
			p[0].append(cell_obj_19.value)
			p[1].append(cell_obj_20.value)

		if 'MAXX' in p[1]:
			dim = p[1][16]
			p[1] = []
			for x in range(55)[1:]:
				cell_obj_21 = sheet.cell(x,21)
				p[1].append(cell_obj_21.value)
			p[1][16] = dim

		res = [vmi_spec]
		for x in p[0]:
			if x.__class__ == unicode:
				u = x.upper()
				#trasfer rin,some people type transfer ring ,so 'SFER RING' is OK
				for y in ['DRUM DIA','CENTER DECK','PUSHOVER','SIDE RING','BT DRUM ADD','SFER RING','ALTERNATIVE PO CAN']:
					if y in u:
						_index = p[0].index(x)
						res.append(p[1][_index])
		res.insert(1,'VMI')
		return res
	else:
		return [vmi_spec,'VMI',0,0,0,0,0,0,0]

def extra_info_maxx(vmi_spec):
	vmi_spec = str(vmi_spec)

	product_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/'
	test_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/试制准备/'
	project_spec_path = u'/\\ksa008/shared/Technical/Building_Specs/CKT_green_tire_spec/Green_tire_specs/试制准备/项目基准/'

	product_spec_lst = os.listdir(product_spec_path)
	test_spec_lst = os.listdir(test_spec_path)
	project_spec_lst = os.listdir(project_spec_path)

	spec_path = [product_spec_path + x for x in product_spec_lst if x.endswith('.xls') and vmi_spec in x]
	if len(spec_path) == 0:
		spec_path = [test_spec_path + x for x in test_spec_lst if x.endswith('.xls') and vmi_spec in x]
		if len(spec_path) == 0:
			spec_path = [project_spec_path + x for x in project_spec_lst if x.endswith('.xls') and vmi_spec in x]

	if len(spec_path) > 0:
		book = xlrd.open_workbook(spec_path[0],on_demand = True)
		sheet_names = book.sheet_names()
		#print sheet_names

		for x in sheet_names:
			a = x.split(' ')[0]
			if 'CURRENT' == a.upper():
				sheet = book.sheet_by_name(x)
				break
			else:
				sheet = None

		#if didn't have 'current' sheet,find the last? the 'base'?
		#use regexp to find the newest(the lagerest number)?
		if not isinstance(sheet,xlrd.sheet.Sheet):
			sheet_names.sort(key = unicode.upper)
			sheet = book.sheet_by_name(sheet_names[-1])

		p = [[],[]]
		for x in range(55)[1:]:
			cell_obj_19 = sheet.cell(x,19)
			cell_obj_20 = sheet.cell(x,20)
			p[0].append(cell_obj_19.value)
			p[1].append(cell_obj_20.value)

		if 'MAXX' not in p[1]:
			return [vmi_spec,'MAXX',0,0,0,0,0,0,0]

		res = [vmi_spec]
		for x in p[0]:
			if x.__class__ == unicode:
				u = x.upper()
				#trasfer rin,some people type transfer ring ,so 'SFER RING' is OK
				for y in ['DRUM DIA','CENTER DECK','PUSHOVER','SIDE RING','BT DRUM ADD','SFER RING','ALTERNATIVE PO CAN']:
					if y in u:
						_index = p[0].index(x)
						res.append(p[1][_index])
		res.insert(1,'MAXX')
		return res
	else:
		return [vmi_spec,'MAXX',0,0,0,0,0,0,0]

if __name__ == '__main__':
	x=extra_info(1126)
	print x