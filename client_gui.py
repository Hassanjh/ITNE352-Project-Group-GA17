import sys
import socket 
import PySimpleGUI as sg

#setting the color theme 
sg.theme('DarkGrey1')

#creating client socket
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #connecting the client to the server
    cs.connect(("127.0.0.1", 49999))
except Exception as e:
    print("Error connecting to the server")
    sg.popup_error("Connection error. Please check your connection")
    sys.exit()

#layout for username input window
layout_username = [
    [sg.Text("Enter username: "), sg.Input(key='-USERNAME-')],
    [sg.Button("ENTER")]
]
#creation of username input window 
window_username = sg.Window("Flight data client", layout_username)
#variable to store inputted username
username = '' 

while True:
    try:
        event, name = window_username.read()
        if event == sg.WINDOW_CLOSED:
            sys.exit()
        elif event == 'ENTER':
            #sending inputted username to server
            username = name['-USERNAME-']
            cs.send(username.encode('ascii'))
            break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt...")
        print("\nCtrl+C entered. Exiting...")
        sys.exit()

window_username.close()

while True:
    try:
        #layout for option selection window
        layout_options = [
            [sg.Text('Options:')],
            [sg.Text('1- Arrived flights')],
            [sg.Text('2- Delayed flights')],
            [sg.Text('3- All flights coming from a specific city')],
            [sg.Text('4- Details of a particular flight')],
            [sg.Text('5- Quit')],
            [sg.Input(key='-OPTION-')],
            [sg.Button('ENTER')]
        ]
        #Creation of option selection window
        window_options = sg.Window('Flight data client', layout_options)

        event, options = window_options.read()

        if event == sg.WINDOW_CLOSED:
            sys.exit()

        op = options['-OPTION-']
        #sending the selection option to the server 
        cs.send(op.encode('ascii'))

        #if statements for each of the possible options
        if op == '1':
            arrived = cs.recv(29999).decode('ascii')
            sg.popup_scrolled('Arrived flights', arrived)

        elif op == '2':
            delayed = cs.recv(29999).decode('ascii')
            sg.popup_scrolled('Delayed flights', delayed)

        elif op == '3':
            #layout for departure IATA input window 
            city_layout = [
                [sg.Text('Enter the departure IATA code: '), sg.Input(key='-DEPARTURE-')],
                [sg.Button('ENTER')]
            ]
            #creation of departure IATA input window 
            city_window = sg.Window('airport', city_layout)

            event, city = city_window.read()

            if event == sg.WINDOW_CLOSED:
                break

            dep_iata = city['-DEPARTURE-']
            #sending the departure IATA to the server
            cs.send(dep_iata.encode('ascii'))
            city_airport = cs.recv(29999).decode('ascii')
            sg.popup_scrolled('All flights coming from' ,city_airport)
            #closing the window after entering the input
            city_window.close()

        elif op == '4':
            #layuout for flight IATA input window
            flight_layout = [
                [sg.Text('Enter the flight IATA code: '), sg.Input(key='-FLIGHT-')],
                [sg.Button('ENTER')]
            ]
            #Creation of flight IATA input window 
            flight_window = sg.Window('specific flight', flight_layout)

            event, fnum = flight_window.read()

            if event == sg.WINDOW_CLOSED:
                break
            
            #Sending the flight IATA and receiving the data 
            flight_iata = fnum['-FLIGHT-']
            cs.send(flight_iata.encode('ascii'))
            specific = cs.recv(29999).decode('ascii')
            sg.popup_scrolled('All details about flight number', specific)
            flight_window.close()

        elif op == '5':
            cs.send(f"{username} has disconnected from the server".encode('ascii'))
            cs.close()
            break

        window_options.close()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt...")
        print("\nCtrl+C entered. Exiting...")
        sys.exit()
