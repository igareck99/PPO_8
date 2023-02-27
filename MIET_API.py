import requests
import json
from typing import Tuple

def RequestAirHT(sensorId : int) -> Tuple[float, float]:
    """
    Функция посылает запрос типа GET для получения значений температуры и влажности воздуха
    URL для запроса: https://dt.miet.ru/ppo_it/api/temp_hum/<number>
    Вход : (int) номер датчика в диапазоне [1..4]
    Выход: (int, int) значения температуры и влажности воздуха
    """
    ret = requests.get(f'https://dt.miet.ru/ppo_it/api/temp_hum/{sensorId}', headers={'X-Auth-Token' : 'test'})
    print(f'Status: {ret.status_code} Answer: {ret.json()}')
    json_code = ret.json()
    return (float(json_code['temperature']), float(json_code['humidity']))

def RequestGroundH(sensorId : int) -> float:
    """
    Функция посылает запрос типа GETдля получения значения влажности почвы
    URL для запроса: https://dt.miet.ru/ppo_it/api/hum/<number>
    Вход : (int) номер датчика в диапазоне [1..6]
    Выход: (int, int) значения температуры и влажности воздуха
    """
    ret = requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{sensorId}', headers={'X-Auth-Token' : 'test'})
    print(f'Status: {ret.status_code} Answer: {ret.text}')
    json_code = json.loads(ret.text)
    return (float(json_code['humidity']))

def OpenWindows(doOpen : bool) -> None:
    """
    Функция посылает запрос типа PATCH для открытия/закрытия форточки в теплицах
    URL для запроса: https://dt.miet.ru/ppo_it/api/fork_drive/ с параметрами вида { "state" : state_value }
    Вход : (bool) открыть (True) или закрыть (False) форточки
    Выход: None
    """
    ret = requests.patch(f'https://dt.miet.ru/ppo_it/api/fork_drive/', params = {'state' : int(doOpen)}, headers={'X-Auth-Token' : 'test'})
    print(f'Status: {ret.status_code} Answer: {ret.text}')

def OpenWaterForGardenBed(deviceId : int, doOpen : bool) -> None:
    """
    Функция посылает запрос типа PATCH для включения/выключения полива заданной грядки
    URL для запроса: https://dt.miet.ru/ppo_it/api/fork_drive/ с параметрами вида { "id" : device_id, "state" : state_value }
    Вход : (int) номер грядки в диапазоне [1..6]
           (bool) открыть (True) или закрыть (False) поливалку
    Выход: None
    """
    ret = requests.patch(f'https://dt.miet.ru/ppo_it/api/watering/', params = {'id' : deviceId, 'state' : int(doOpen)}, headers={'X-Auth-Token' : 'test'})
    print(f'Status: {ret.status_code} Answer: {ret.text}')

def OpenWatering(deviceId : int, doOpen : bool) -> None:
    """
    Функция посылает запрос типа PATCH для включения/выключения единой системы увлажнения
    URL для запроса: https://dt.miet.ru/ppo_it/api/total_hum с параметром вида { "state" : state_value }
    Вход : (bool) открыть (True) или закрыть (False) поливалку
    Выход: None
    """
    ret = requests.patch(f'https://dt.miet.ru/ppo_it/api/total_hum/', params = {'state' : int(doOpen)}, headers={'X-Auth-Token' : 'test'})
    print(f'Status: {ret.status_code} Answer: {ret.text}')

if __name__ == "__main__":
    print('Этот файл должен быть вызван в качестве модуля!')
