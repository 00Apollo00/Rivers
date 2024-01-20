from flask import Flask, url_for,request,flash
from flask import render_template
from catboost import CatBoostRegressor
import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e23edde'

def covert_int_list(arr):
    arr =  arr.split(" ")
    arr = list(map(float, arr))
    return arr

def model_init():
    model = CatBoostRegressor(depth=13, l2_leaf_reg=7, min_child_samples=55,
                              early_stopping_rounds=100,
                              eval_metric='MAPE', grow_policy='Lossguide')
    # load model
    model.load_model("models/catboost.pkl")
    return model


def level_forecast(date, tmean, pas_level1, pasday, w_forecast, forecast_degree_coverage, forecast_snow_height):
    columns_name = ['snow_height', 'degree_coverage', 'tmean',
                    'pasday1', 'pasday2', 'pasday3', 'pasday4', 'pasday5', 'pasday6', 'pasday7',
                    'pasday8', 'pasday9', 'pasday10', 'pasday11', 'pasday12', 'pasday13', 'pasday14',
                    'pas_level1', 'pas_level2', 'pas_level3', 'pas_level4', 'pas_level5', 'pas_level6', 'pas_level7',
                    'day_of_year', 'w_forecast_d1'
                    ]
    # Конвертируем дату(строки) в дату (datetime64)
    # date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    day_of_year = int(date.strftime("%j"))
    # data = np.insert(data, -1, day_of_year )  #временно закаментирую день гда в общем массиве

    # =============================1 проход ===============================
    # global pas_level

    # разбиваем данные на группы
    snow_height = forecast_snow_height[0]  # 1 высота снежного покрова
    degree_coverage = forecast_degree_coverage[0]  # 2 покрытие  снега

    pas_level = pas_level1  # data[0,17:24]#18-24 уровень воды за прошлые 7 днй
    w_forecast_d1 = w_forecast[0]  # data[0,24] #25 прогноз погоды на 1 день

    # формируем массив с фичами
    future = np.array([snow_height, degree_coverage, tmean])
    future = np.append(future, pasday)
    future = np.append(future, pas_level)
    future = np.append(future, [day_of_year, w_forecast_d1])

    # переводим данные в DataFrame
    future = pd.DataFrame(data=[future], columns=columns_name)

    model = model_init()
    # предсказание
    predic_day = model.predict(future)
    global prd
    # global day_number
    prd = []
    day_number = []
    prd = np.append(prd, predic_day)
    #day_number = np.append(day_number, day_of_year)
    day_number = np.append(day_number, str(date + datetime.timedelta(days= 0)))

    # ========================================================================

    for i in range(13):
        day_of_year += 1
        # разбиваем данные на группы
        snow_height = forecast_snow_height[i + 1]  # 1 высота снежного покрова

        degree_coverage = forecast_degree_coverage[i + 1]  # 2 покрытие  снега

        pasday = np.roll(pasday, 1)  # сдвигаем массив вперед
        pasday[0] = tmean  # заменяем первый элемент массива вчерашней темпреатурой

        tmean = w_forecast[i]  # текущая ср.температура

        pas_level = np.roll(pas_level, 1)

        pas_level[0] = prd[i]

        # w_forecast_d1 = data[0,24] #25 прогноз погоды на 1 день
        w_forecast_d1 = w_forecast[i + 1]

        # формируем массив с фичами
        future = np.array([snow_height, degree_coverage, tmean])
        future = np.append(future, pasday)
        future = np.append(future, pas_level)
        future = np.append(future, [day_of_year, w_forecast_d1])

        # переводим данные в DataFrame
        future = pd.DataFrame(data=[future], columns=columns_name)

        # предсказание
        predic_day = model.predict(future)

        prd = np.append(prd, predic_day)
        #day_number = np.append(day_number, day_of_year)
        day_number = np.append(day_number, str(date + datetime.timedelta(days=i+1)))
        # print(prd)

        # prd =  np.linspace (prd.min(), prd.max(), len(prd) )
        # print(prd)
        #temp_date = date + datetime.timedelta(days=i)
        predict = zip(day_number, prd)

    return predict#{'predict': prd, 'day_number': day_number}
@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':

        date = request.form['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        degree_coverage = covert_int_list(request.form['degree_coverage'])
        snow_height  = covert_int_list(request.form['snow_height'])
        tmean = float(request.form['tmean'])
        pasday = covert_int_list(request.form['pasday'])
        w_forecast = covert_int_list(request.form['w_forecast'])
        pas_level = covert_int_list(request.form['pas_level'])

        if len(pasday) != 14:
            flash('Ошибка в данных `Температура за предыдущие 14 дней ` !', category='error')
        elif len(w_forecast) != 14:
            flash('Ошибка в данных `Прогноз температуры на 14 дней` !', category='error')
        elif len(pas_level) != 7:
            flash('Ошибка в данных `Уровень воды за предыдущии 7 дей` !', category='error')
        elif len(degree_coverage) != 14:
            flash('Покрытие  снега на 14 дней` !', category='error')
        elif len(snow_height) != 14:
            flash('Высота снежного покрова на 14 дней` !', category='error')


        #print((date,degree_coverage,snow_height,tmean,pasday, w_forecast, pas_level ))
        predict = level_forecast(date,tmean,pas_level,pasday,w_forecast, degree_coverage,snow_height)
       # day,level = zip(*predict)
        #print(predict)
        return render_template('predict.html', predict = predict)

    else:
        return render_template('index1.html')

    return render_template('index1.html')



@app.route('/charts')
def charts():
    return render_template('charts.html')

if __name__ == '__main__':

    app.run(debug = True)