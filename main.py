import PySimpleGUI as sg
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from databasemanager import *
from helpFunc import *


def GeneratePlots(airTable, groundTable):
    fig, axis = plt.subplots(1, 3)
    x = np.arange(len(column(airTable, 0)))
    # Air temperature
    for i in range(4):
        axis[0].plot(x, column(airTable, i))
    axis[0].set_title('Air temperature')
    axis[0].legend(['T1', 'T2', 'T3', 'T4'], loc=2)
    # Air humidity
    for i in range(4, 8):
        axis[1].plot(x, column(airTable, i))
    axis[1].set_title('Air humidity')
    axis[1].legend(['H1', 'H2', 'H3', 'H4'], loc=2)
    # Ground humidity
    for i in range(6):
        axis[2].plot(x, column(groundTable, i))
    axis[2].set_title('Ground humidity')
    axis[2].legend(['H1', 'H2', 'H3', 'H4', 'H5', 'H6'], loc=2)
    plt.figure(figsize=(10, 6))
    return fig


def main():
    sg.theme('SystemDefaultForReal')
    createDatabase()
    firstUpdate()
    airTableData, airTableHeadings, groundTableData, groundTableHeadings, connection, cursor = firstUpdate()
    layoutAirAndGround = [
        [sg.Text('Air')],
        [sg.HSeparator()],
        [sg.Table(values=airTableData, headings=airTableHeadings, auto_size_columns=True, display_row_numbers=False,
                  key='-TABLE-AIR-')],
        [
            sg.Checkbox('Open windows', default=False, key='-AIR-OPEN-WIN-', enable_events=True),
            sg.Checkbox('Enable humidifier', default=False, key='-AIR-OPEN-HUM-', enable_events=True)
        ],
        [sg.Text('Ground')],
        [sg.HSeparator()],
        [sg.Table(values=groundTableData, headings=groundTableHeadings, auto_size_columns=True,
                  display_row_numbers=False, key='-TABLE-GND-')],
        [
            sg.Text('Gates:'),
            sg.Checkbox('1', default=False, key='-WATERING-1-'),
            sg.Checkbox('2', default=False, key='-WATERING-2-'),
            sg.Checkbox('3', default=False, key='-WATERING-3-'),
            sg.Checkbox('4', default=False, key='-WATERING-4-'),
            sg.Checkbox('5', default=False, key='-WATERING-5-'),
            sg.Checkbox('6', default=False, key='-WATERING-6-'),
        ],
    ]

    windowLayout = [
        [
            sg.Column(layoutAirAndGround),
            sg.VSeparator(),
            sg.Canvas(size=(800, 200), key='-CANVAS-', pad=(0, 0)),
        ]
    ]

    window = sg.Window('MIET HotHouse Reader', windowLayout, resizable=False, margins=(0, 0), size=(1000, 510),
                       finalize=True)

    time2call = time.time() + 10

    AH1, AT1 = RequestAirHT(1)
    AH2, AT2 = RequestAirHT(2)
    AH3, AT3 = RequestAirHT(3)
    AH4, AT4 = RequestAirHT(4)
    airTableData.append([AT1, AT2, AT3, AT4, AH1, AH2, AH3, AH4])
    window['-TABLE-AIR-'].update(airTableData)
    GH1 = RequestGroundH(1)
    GH2 = RequestGroundH(2)
    GH3 = RequestGroundH(3)
    GH4 = RequestGroundH(4)
    GH5 = RequestGroundH(5)
    GH6 = RequestGroundH(6)
    groundTableData.append([GH1, GH2, GH3, GH4, GH5, GH6])

    request = f'INSERT INTO data (datetime, airt1, airt2, airt3, airt4, airh1, airh2, airh3, airh4, gndh1, gndh2, gndh3, gndh4, gndh5, gndh6) VALUES ("{datetime.datetime.now()}", {AT1}, {AT2}, {AT3}, {AT4}, {AH1}, {AH2}, {AH3}, {AH4}, {GH1}, {GH2}, {GH3}, {GH4}, {GH5}, {GH6})'
    cursor.execute(request)
    connection.commit()

    window['-TABLE-GND-'].update(groundTableData)

    figure = GeneratePlots(airTableData, groundTableData)
    canvas = window['-CANVAS-'].TKCanvas
    plotArea = FigureCanvasTkAgg(figure, canvas)
    plotArea.draw()
    plotArea.get_tk_widget().pack(side='left', fill='both', expand=1)

    while True:
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            break
        elif time.time() > time2call:
            AH1, AT1 = RequestAirHT(1)
            AH2, AT2 = RequestAirHT(2)
            AH3, AT3 = RequestAirHT(3)
            AH4, AT4 = RequestAirHT(4)
            airTableData.append([AT1, AT2, AT3, AT4, AH1, AH2, AH3, AH4])
            window['-TABLE-AIR-'].update(airTableData)
            GH1 = RequestGroundH(1)
            GH2 = RequestGroundH(2)
            GH3 = RequestGroundH(3)
            GH4 = RequestGroundH(4)
            GH5 = RequestGroundH(5)
            GH6 = RequestGroundH(6)
            groundTableData.append([GH1, GH2, GH3, GH4, GH5, GH6])
            window['-TABLE-GND-'].update(groundTableData)

            request = f'INSERT INTO data (datetime, airt1, airt2, airt3, airt4, airh1, airh2, airh3, airh4, gndh1, gndh2, gndh3, gndh4, gndh5, gndh6) VALUES ("{datetime.datetime.now()}", {AT1}, {AT2}, {AT3}, {AT4}, {AH1}, {AH2}, {AH3}, {AH4}, {GH1}, {GH2}, {GH3}, {GH4}, {GH5}, {GH6})'
            cursor.execute(request)
            connection.commit()

            if plotArea is not None:
                plotArea.get_tk_widget().forget()
                plt.close('all')
            figure = GeneratePlots(airTableData, groundTableData)
            canvas = window['-CANVAS-'].TKCanvas
            plotArea = FigureCanvasTkAgg(figure, canvas)
            plotArea.draw()
            plotArea.get_tk_widget().pack(side='left', fill='both', expand=1)

            time2call = time.time() + 10
        elif values['-AIR-OPEN-WIN-']:
            print('.')

    window.close()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
