import xlrd2
import psycopg2
from psycopg2 import Error
import datetime
import re


def extract():
    files =["Подкаменная Тунгуска 2008.xlsx",
            "Подкаменная Тунгуска 2009.xlsx",
            "Подкаменная Тунгуска 2010.xlsx"
            ]




    for file in files:

        book = xlrd2.open_workbook("..\\Rivers\\"+file)
        worksheet = book.sheet_by_index(0)

        #настройка!
        Y = re.findall(r'\d+', file)[0]  # не забыть!
        if Y =='2008':
            row = 48 #48 #49
            row_offset_post = 7 #7 #8
            row_offset_river = 5 #5 #6
            offset = 24 #24 # 25
            zero_offset = 4 #4 #5
            offset_row = 1

        else:
            row = 49  # 48 #49
            row_offset_post = 8  # 7 #8
            row_offset_river = 6  # 5 #6
            offset = 25  # 24 # 25
            zero_offset = 5  # 4 #5

        if int(Y) > 2013:
            offset_col = 1
        else:
            offset_col = 0



        date =''
        lavelW='' # уровень воды
        stateW ='' # состояние воды

        try:
            connection = psycopg2.connect(user="postgres", password="123", host="127.0.0.1", port="5432", database="riversV2")

            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()


            for post in range(1, 13):
                try:
                    codePost = worksheet.cell_value(row - row_offset_post, 1+offset_col) #7
                except:
                    continue

                river = worksheet.cell_value(row - row_offset_river, 1+offset_col) #5
                zero_check = str(worksheet.cell_value(row - zero_offset, 1+offset_col))

                for r in range(row, row + 31):
                    for c in range(0, 13):
                        month = c
                        if c > 0:
                            # Формируем дату
                            day = str(int(worksheet.cell_value(r, 0)))
                            if int(day) < 9:
                                day = f'0{day}'
                            if month < 9:
                                month = f'0{str(month)}'
                            date = f'{day}{month}{Y}'
                            try:
                                date =  datetime.datetime.strptime( date , "%d%m%Y").date()
                            except:
                                date = None
                                continue


                            # уровень воды

                                #levelW = str(worksheet.cell_value(r, c)).split()[0]
                            #lavelW = str(re.findall(r'\d+', worksheet.cell_value(r, c+offset_col))[0])
                            coff =0
                            if int(Y)>2013 and c>1:
                                coff = 1
                            str1 = str(worksheet.cell_value(r, c+offset_col+coff))
                            if str1.split()[0] !='-':
                                #str1 = float(str1.split()[0])
                                lavelW = (str1.split()[0])



                            if len(lavelW)<1 or lavelW =='-':
                                lavelW = ''




                            # состояние воды
                            water = str(worksheet.cell_value(r, c)).split()
                            if len(water) > 1:
                                stateW = water[1]
                            else:
                                stateW = ''

                            if not (date is None):
                                #print(f'---- {date}  {levelW}')
                                print(f'{date} {river} {codePost} {lavelW}   {stateW} {zero_check}')
                                insert_query = """INSERT INTO rivers_post (DATE, name,code_post, level_w, state_w,zero) VALUES (%s,%s,%s,%s,%s,%s)"""
                                item_tuple = (date,river,codePost,lavelW,stateW, zero_check)
                                cursor.execute(insert_query,item_tuple)
                                connection.commit()


                            else:
                                print(f'{date} --- {zero_check}')
                                #print(f'{date}  {river}  {codePost} {levelW}   {stateW}') # вывод lfns

                row += 31+offset #24




        except(Exception, Error) as error:
            print(f'{r} - {c}')
            print(f'{date} {codePost} {lavelW}   {stateW} {zero_check}')
            print("Ошибка при работе с PostgreSQL", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")


def convert():
    try:
        connection = psycopg2.connect(user="postgres", password="123", host="127.0.0.1", port="5432", database="riversV2")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        select_query = """ SELECT * FROM rivers_post"""
        cursor.execute( select_query)
        data = cursor.fetchall()

        river=''
        codePost=''
        lavelW=''
        stateW=''
        zero_check=''
        date=''
        for row in range(len(data)):
            river = data[row][0]
            codePost = int(float(data[row][1]))

            if data[row][2] == 'прсх' or data[row][2]=='прмз':
                lavelW = 0
            else:
                lavelW = int(float(data[row][2]))

            stateW = data[row][3]
            date = data[row][4]
            zero_check = float(data[row][5])

            insert_query = """INSERT INTO rivers_post ( name, code_post, level_w, state_w, date, zero) VALUES (%s,%s,%s,%s,%s,%s)"""
            item_tuple = ( river, codePost, lavelW, stateW, date,zero_check)
            cursor.execute(insert_query, item_tuple)
            connection.commit()


    except(Exception, Error) as error:
        #print(f'{r} - {c}')
        #print(f'{date} {codePost} {lavelW}   {stateW} {zero_check}')
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def temp_convert():

    try:
        connection = psycopg2.connect(user="postgres", password="123", host="127.0.0.1", port="5432", database="rivers")
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        with open('data\Температура_осадки\Tttr\Красноярск_29570.dat') as f:
            text = f.read()
            text = text.split('\n')

        for line in text:
            line = line.split()

            vmo_index = int(line[0])
            date = f'{line[1]}-{line[2]}-{line[3]}'
            tflag = int(line[4])
            tmin = float(line[5])
            qtmin = float(line[6])
            tmean = float(line[7])
            qtmean = float(line[8])
            tmax = float(line[9])
            qtmax = float(line[10])
            r= float(line[11])
            cr = int(line[12])
            qr = int(line[13])


            print(f'{vmo_index}  {date} {tflag} {tmin} {qtmin} {tmean} {qtmean} {tmax} {qtmax} {r} {cr} {qr}')

            insert_query = """INSERT INTO temperature_precipitation (vmo_index,  date, tflag, tmin, qtmin, tmean, qtmean, tmax, qtmax, r, cr, qr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            item_tuple = (vmo_index,  date, tflag, tmin, qtmin, tmean, qtmean, tmax, qtmax, r, cr, qr)
            cursor.execute(insert_query, item_tuple)
            connection.commit()

    except(Exception, Error) as error:

        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def snow_convert():

    try:
        connection = psycopg2.connect(user="postgres", password="123", host="127.0.0.1", port="5432", database="rivers")
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        with open('data\Снежный_покров\Snow\Красноярск_29570.dat') as f:
            text = f.read()
            text = text.split('\n')

        for line in text:
            line = line.split()

            vmo_index = int(line[0])
            date = f'{line[1]}-{line[2]}-{line[3]}'
            snow_height = int(line[4])
            degree_coverage = int(line[5])
            additional_info_snow_depth = int(line[6])
            quality_snow_depth = int(line[7])
            additional_info_air_temp = int(line[8])



            print(f'{vmo_index}  {date} {snow_height} {degree_coverage} {additional_info_snow_depth} {quality_snow_depth} {additional_info_air_temp}')

            insert_query = """INSERT INTO snow (vmo_index,  date, snow_height, degree_coverage, additional_info_snow_depth, quality_snow_depth, additional_info_air_temp) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            item_tuple = (vmo_index,  date, snow_height, degree_coverage, additional_info_snow_depth, quality_snow_depth, additional_info_air_temp)
            cursor.execute(insert_query, item_tuple)
            connection.commit()

    except(Exception, Error) as error:

        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

convert()









