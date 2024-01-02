import json
import threading
import socket
from pip._vendor import requests


# Function for retrieving flight data from an API and saving it in a JSON file
def flight_data(arr_icao):
    #parameters for retrieving the data from the API
    params={
    'access_key':'8f101121b2e162dcc73f1536f835e332',
    'arr_icao':arr_icao,
    'limit':100
    }
    api_response = requests.get('http://api.aviationstack.com/v1/flights', params)
    data= api_response.json()
    try:
        flights = data.get('data', [])
        with open('GA17.json', 'w') as file:
                json.dump(flights, file, indent=4)
        print("Data retrieved successfully.✅")
        
    except Exception as e:
        print(f'Error occurred while opening JSON file for writing: {e}')
    return data

#Function for responding to client requests and providing the proper information
def options(conn):
    
    username = conn.recv(2048).decode('ascii')
    print("\nhi ", username)
    while True:
        op = conn.recv(2048).decode('ascii')
        print(f"\n{username} picked option: {op}")
        if op == '1':
            print ("Request from", username,"\n Request type: All arrived flights \n")
            print("Loading arrived flights please wait ⌛ ")
            flight_info = all_arrived_flights()
            conn.send(flight_info.encode('ascii'))
        elif op == '2':
            print ("Request from", username,"\n Request type: Delayed flights \n")
            print("Loading delayed flights please wait ⌛ ")
            flight_info = delayed_flights()
            conn.send(flight_info.encode('ascii'))

        elif op == '3':
            print ("Request from", username,"\n Request type: All flights from a specific city \n")
            dep_iata = conn.recv(9999).decode('ascii')
            print(f"\nLoading All flights coming from {dep_iata} ⌛ ")
            flight_info = specific_airport(dep_iata)
            conn.send(flight_info.encode('ascii'))
        elif op == '4':
            print ("Request from", username,"\n Request type: Details about a specific flight \n")
            flight_IATA = conn.recv(9999).decode('ascii')
            print(f"\nLoading details of flight number {flight_IATA} please wait ⌛ ")
            flight_info = all_flight_details(flight_IATA)
            conn.sendall(flight_info.encode('ascii'))
        elif op == '5':
            print(12*"*"+" Goodbye 👋 "+"*"*12)
            print(f'\n{username} has disconnected')
            break
    conn.close()

#function to retrieve arrived flights from the JSON file
def all_arrived_flights():
    with open ('GA17.json','r') as file:
        flight_info=json.load(file)
    arr_flight=[]
    for flight in flight_info:
        if flight['flight_status'] == 'landed':
            flight_data = {
            'flight_IATA': flight['flight']['iata'],
            'departure_airport': flight['departure']['airport'],
            'arrival_time': flight['arrival']['scheduled'],
            'arrival_terminal': flight['arrival']['terminal'],
            'arrival_gate': flight['arrival']['gate']
            }
            arr_flight.append(flight_data)
    return json.dumps(arr_flight, indent=2)

#function to retrieve delayed flights from the JSON file
def delayed_flights():
    with open ('GA17.json','r') as file:
        flight_info=json.load(file)
    d_flights = []
    for flight in flight_info:
        if flight['arrival']['delay'] is not None:
            flight_data = {
            'flight_IATA': flight['flight']['iata'],
            'departure_airport': flight['departure']['airport'],
            'departure_time': flight['departure']['actual'],
            'arrival_time_estimate': flight['arrival']['estimated'],
            'arrival_terminal':flight['arrival']['terminal'],
            'arrival_delay': flight['arrival']['delay'],
            'arrival_gate': flight['arrival']['gate']
            }
            d_flights.append(flight_data)
    return json.dumps(d_flights, indent=2)

#Function for retrieving flights from a specific airport from the JSON file 
def specific_airport(dep_iata):
    with open ('GA17.json','r') as file:
        flight_info=json.load(file)
    s_flights = []
    for flight in flight_info:
       if flight['departure']['iata']==dep_iata:
            flight_data = {
            'flight_IATA': flight['flight']['iata'],
            'departure_airport': flight['departure']['airport'],
            'departure_time': flight['departure']['scheduled'],
            'arrival_time_estimate': flight['arrival']['estimated'],
            'departure_gate': flight['departure']['gate'],
            'arrival_gate': flight['arrival']['gate'],
            'flight_status': flight['flight_status']
            }
            s_flights.append(flight_data)
    return json.dumps(s_flights, indent=2)

#Flight for retrieving details of a specific flight from the JSON file 
def all_flight_details(flight_IATA):
    with open ('GA17.json','r') as file:
        flight_info=json.load(file)
    specific_flight = []
    for flight in flight_info:
        if flight ['flight']['iata'] == flight_IATA:
            flight_data= {
            'flight_IATA': flight['flight']['iata'],
            'departure_airport': flight['departure']['airport'],
            'departure_gate': flight['departure']['gate'],
            'departure_terminal': flight['departure']['terminal'],
            'arrival_airport': flight['arrival']['airport'],
            'arrival_gate': flight['arrival']['gate'],
            'arrival_terminal':flight['arrival']['terminal'],
            'flight_status': flight['flight_status'],
            'scheduled_departure_time': flight['departure']['scheduled'],
            'scheduled_arrival_time': flight['arrival']['scheduled']
            }
            specific_flight.append(flight_data)
            
    return json.dumps(specific_flight, indent=2)

#Setting up the socket
ss= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1',49999))

print(10*"="+" Server started "+"="*10)

arr_icao = input("please enter the arrival icao code: ")
flight_data(arr_icao)

ss.listen(5)

#|Function for accepting and handling several clients
def main():
    try:
        while True:
            conn, addr = ss.accept()
            t=threading.Thread(target=options, args=(conn,))
            t.start()
    except KeyboardInterrupt:
            print("Ctrl+c was received. Server terminating")
        
if __name__ == '__main__':
    main()
