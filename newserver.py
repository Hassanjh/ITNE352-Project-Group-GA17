import json 
import threading
import socket
from pip._vendor import requests

ss= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1',49999))

print (10*'-','The server has started',10*'-')

msg= 'Send the arr icao code: '
ss.send=msg.encode('ascii')

selected_option= ss.recv(1024).decode('ascii')

def flight_data(arr_icao):
    params={
    'access_key':'',
    'arr_icao':arr_icao,
    'limit':100
}
    api_response = requests.get('http://api.aviationstack.com/v1/flights', params)
    data= api_response.json()
    with open ('GA17.json','w') as j:
        json.dump(data,j)
    return data
    
with open ('GA17.json','r') as file: 
    flight_info=json.load(file)

#function to store arrived flights
def all_arrived_flights(flight_info):
    arr_flight=[]
    for flight in flight_info['data']:
        if flight['flight_status'] == 'landed':
            flight_data = {
                'flight_IATA': flight['flight']['iata'],
                'departure_airport': flight['departure']['airport'],
                'arrival_time': flight['arrival']['scheduled'],
                'arrival_terminal': flight['arrival']['terminal'],
                'arrival_gate': flight['arrival']['gate']
            }
            arr_flight.append(flight_data)
    return arr_flight

def delayed_flights(flight_info):
    d_flights = []
    for flight in flight_info['data']:
        if flight['flight_status'] =='landed' and flight['departure']['delay']:
            flight_data = {
                'flight_IATA': flight['flight']['iata'],
                'departure_airport': flight['departure']['airport'],
                'departure_time': flight['departure']['scheduled'],
                'arrival_time_estimate': flight['arrival']['estimated'],
                'arrival_terminal':flight['arrival']['terminal'],
                'arrival_delay': flight['arrival']['terminal'],
                'arrival_gate': flight['arrival']['gate']
            }
            d_flights.append(flight_data)
    return d_flights

def specific_airport(flight_info, city):
    s_flights = []
    for flight in flight_info['data']:
        if flight['departure']['airport']==city:
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
    return s_flights

def all_flight_details(flight_info, flight_IATA):
    specific_flight = {}
    for flight in flight_info['data']:
        if flight ['flight']['iata'] == flight_IATA:
            specific_flight = {
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
            break

    return specific_flight   

clients=[]
names=[]

def connection(conn,addr):
        name=conn.recv(2048).decode('ascii')
        print(f"Got a connection from {addr} with username {name}")
        clients.append(conn)
        names.append(name)
        msg = f"Hi {name}\nenter Airport code: "
        conn.send(msg.encode('ascii'))
        print(names)
        airportCode = conn.recv(2048).decode('ascii')
        print(f"Airport code from {name} is: {airportCode}")
        conn.send(f"your Airport code is {airportCode}".encode('ascii'))
def main():
    while True:
        conn, addr = ss.accept()
        t=threading.Thread(target=connection, args=(conn,addr))
        t.start()
        
if __name__ == '__main__':
    main()


