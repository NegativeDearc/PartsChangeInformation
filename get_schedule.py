# -*- coding:utf-8 -*-

import xlrd
import datetime
import os
import re
import pandas as pd
import pytz
from itertools import chain

def get_schedule():
    '''
    This function purpose on get Schedule Data from file , merge with parts information database
    '''
    #initial
    #row_num from 6 to 151,could change any time
    row_range = range(6,166)
    #machine_name,FSR 4 * 12,DRA 6 * 7,VMI 5 *11, MAXX 5 * 3
    machine = list(chain(*
              [['FSR' + str(x) for x in sorted(4 * range(1,13))],
              ['DRA' + str(y) for y in sorted(6 * range(1,8))]	,
              ['VMI ' + str("%02d" % z) for z in sorted(5 * range(1,12))],
              ['X ' + str(a) + ' MAXX' for a in sorted(5 * range(1,4))]]))

    machine_type = list(chain(*
              [['FSR' for x in sorted(4 * range(1,13))],
              ['DRA' for y in sorted(6 * range(1,8))],
              ['VMI' for z in sorted(5 * range(1,12))],
              ['MAXX'for a in sorted(5 * range(1,4))]]))

    # ru times zone ,slow than china 5 hours
    tz = pytz.timezone('Asia/Shanghai')
    def re_find_file(debug = None):
        '''
        using regular expression to find the right file path this year(if exist)
        when debug = True,program will test itself
        '''
        path = u'/\\ksa008/shared/Production/Schedule_Data/Sharepoint/生管/计划日报表/16年计划日报表汇总/TBM/TBM plan/'
        file_list = os.listdir(path)

        now_date = datetime.datetime.now(tz)
        month_abb = now_date.strftime('%b')

        def this_month_file(month_abb):
            '''
            according to the month find the file named by month.abb.
            Return a list
            '''
            pattern = '^TBM.*' + month_abb + '.*xlsx$'
            f = lambda x:re.findall(pattern,x,flags = re.IGNORECASE)
            lst = map(f,file_list)
            r = list(chain(*lst))
            return r

        result = this_month_file(month_abb = month_abb)

        '''debug to test'''
        DEBUG = debug
        if DEBUG == True:
            result = []

        if len(result) == 0:
            '''if can't find any file match,go back to 28days ago,try it again'''
            delta = datetime.timedelta(days = 28)
            month_abb_28d_ago = (now_date - delta).strftime('%b')
            res = this_month_file(month_abb = month_abb_28d_ago)
            if len(res) == 0:
                return "Can't find any file matched"
            else:
                res = res[0]
        if len(result) >= 1:
            '''if find more than one,choose the last one'''
            res = result[-1]
        return path + res

    #the file path
    path = re_find_file()

    #database
    df3 = pd.read_pickle('c:/users/sxchen/desktop/PartsChangeInformation/static/data.dat')
    df3.columns = ['SPEC',u'MACHINE_TYPE',u'DIM',u'CENTER_DECK',u'PUSHOVER_CAN',u'SIDE_RING',u'BT_ADD',u'TRANSFER_RING',u'BO_PUSH_CAN']
    #dealing today and next day
    today = datetime.datetime.now(tz)
    today_sheet = str(today.month) + '.' + str(today.day)
    next_day = today + datetime.timedelta(days = 1)
    next_day_sheet = str(next_day.month) + '.' + str(next_day.day)

    def data_clean(x):
        '''
        clean data: Make sure all cell values convert to string.
                    If the data type is not a python string,it will get NaN when merge.
        '''
        if isinstance(x,float):
            x = int(x)
            if str(x).startswith('99'):
                return str(x)[2:]
            else:
                return str(x)
        if isinstance(x,str):
            return 0

    #If the file can't be open.
    #Most time spent here when try to open the workbook almost 5 seconds
    try:
        book = xlrd.open_workbook(path,on_demand = True)
    except IOError:
        return 'No such file or directory!'

    try:
        sheet = book.sheet_by_name(today_sheet)
    except Exception:
        return 'No Sheet Name! %s' % sheet
    else:
        #day_spec
        day_spec = map(data_clean,[sheet.cell_value(row,2) for row in row_range])
        day_num = map(data_clean,[sheet.cell_value(row,3) for row in row_range])

        #night_spec
        night_spec = map(data_clean,[sheet.cell_value(row,8) for row in row_range])
        night_num =  map(data_clean,[sheet.cell_value(row,9) for row in row_range])

        #dayshift
        #print len(machine)
        #print len(day_spec)
        #print len(day_num)

        df = pd.DataFrame({
            'Type':['白' for x in range(160)],
            'Machine':machine,
            'SPEC':day_spec,
            'NUM':day_num,
            'MACHINE_TYPE':machine_type
            },columns= ['Type','Machine','SPEC','NUM','MACHINE_TYPE'],dtype = 'O')

        #nightshift
        df1 = pd.DataFrame({
            'Type':['夜' for x in range(160)],
            'Machine':machine,
            'SPEC':night_spec,
            'NUM':night_num,
            'MACHINE_TYPE':machine_type
            },columns= ['Type','Machine','SPEC','NUM','MACHINE_TYPE'],dtype = 'O')

        #drop index contain FSR & DRA 90行以后
        #day
        df2 = df.ix[90:,:][df.SPEC != 0]
        len_df2 = len(df2.index)
        #night
        df4 = df1.ix[90:,:][df1.SPEC != 0]
        len_df4 = len(df4.index)
        #取夜班第一个规格，供白班整合数据
        lst2 = []
        for s,g in df4.groupby(by = 'Machine'):
            lst2.append(g.ix[min(g.index),:]) #---> Series

        today_day_df_first = pd.DataFrame(lst2).sort_index()
        print today_day_df_first
        len_today_day_df_first = len(today_day_df_first.index)


    #try to open the next day sheet
    try:
        sheet2 = book.sheet_by_name(next_day_sheet)
    except Exception:
        #make a fake empty DataFrame to concat
        next_day_df3 = pd.DataFrame({}, columns = ['Type','Machine','SPEC','NUM','MACHINE_TYPE'])
    else:
        #读取第二天的白班第一进度
        next_day_spec = map(data_clean,[sheet2.cell_value(row,2) for row in row_range])
        next_day_num = map(data_clean,[sheet2.cell_value(row,3) for row in row_range])
        
        next_day_df = pd.DataFrame({
            'Type':['白' for x in range(160)],
            'Machine':machine,
            'SPEC':next_day_spec,
            'NUM':next_day_num,
            'MACHINE_TYPE':machine_type
        },columns=['Type','Machine','SPEC','NUM','MACHINE_TYPE'],dtype='O')

        next_day_df2 = next_day_df.ix[90:,:][next_day_df.SPEC != 0]

        lst = []
        for s,g in next_day_df2.groupby(by = 'Machine'):
            lst.append(g.ix[min(g.index),:]) #---> Series

        next_day_df3 = pd.DataFrame(lst).sort_index()
        print next_day_df3
        len_next_day_df3 = len(next_day_df3.index)

    d = pd.merge(pd.concat([df2,today_day_df_first],keys=['day','night_first']),df3,'left',on = ['SPEC','MACHINE_TYPE'])
    n = pd.merge(pd.concat([df4,next_day_df3],keys=['night','next_day_first']),df3,'left',on = ['SPEC','MACHINE_TYPE'])

    #print d
    #print n
    return d,n

if __name__ ==  '__main__':
    a,b = get_schedule()
    print a
    print b
