import keras


def load_model(filename, model_type):
    """
    Функция для загрузки модели из файла

    filename: имя файла модели
    model_type: тип модели
    """

    if model_type.lower() == 'lstm':
        model = keras.models.load_model(filename)
    else:
        model = None

    return model


def model_forecast(model_fit, model_type, series=None, steps=5, features=1):
    """
    Прогнозирование временного ряда с использованием модели

    model_fit: обученная модель
    model_type: тип модели
    series: времненной ряд для прогнозирования
    steps: количество шагов для прогноза (у timemixer по умолчанию стоит свой размер горизонта прогнозирования)
    features: количество признаков на временной шаг

    """

    if model_type.lower() == 'lstm':
        input_seq = series.iloc[-steps:].values
        input_seq = input_seq.reshape((1, steps, features))
        forecast = model_fit.predict(input_seq, verbose=0)

    elif model_type.lower() == 'timemixer':
        forecast = model_fit.predict()[:steps]
    else:
        forecast = model_fit.forecast(steps=steps)

    return forecast
