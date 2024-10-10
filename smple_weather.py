weather = [
    {
        'date':'today',
        'state': 'cloudy',
        'temp': 68.5
    },
    {
        'date':'tomorrow',
        'state': 'sunny',
        'temp': 74.8
    }
]


for forecast in weather:
    print(forecast['date'])
    print(forecast['state'])
    print(forecast['temp'])


for forecast in weather:
    print('The weather for ' + forecast['date'] +
          ' will be ' + forecast['state'] + ' with a temperature of '
          + str(forecast['temp']) + ' degrees.')


for forecast in weather:
    print(f"The weather for {forecast['date']} will be {forecast['state']} "
          f"with a temperature of {forecast['temp']} degrees.")


for forecast in weather:
    print(f"The weather for {forecast['date']} will be {forecast['state']} "
          f"with a temperature of {forecast['temp']} degrees.")