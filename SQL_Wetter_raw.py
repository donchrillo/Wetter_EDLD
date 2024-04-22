import pyodbc
import math
import logging
from datetime import datetime, timezone
import mail as mail



#Verbindung zur SQL Datenbank wird hergestellt
def make_connection():
    SERVER = '<IP-Adresse-hier>'
    PORT = '<Port>'
    DATABASE = '<DB NAME>'
    USERNAME = 'USER'
    PASSWORD = 'PASS'

    #connectioon Sting für Raspi
    connectionString = f'DRIVER={{FreeTDS}};SERVER={SERVER};PORT={PORT};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TDS_Version=4.2'    

    #return wird in der aufrufenden Funktion als "Conn" gespeichert
    return pyodbc.connect(connectionString)
    

def get_data(cursor):

    #Hier wird eine Stored Procedure auf dem SQL Server aufgerufen
    #Hier heißt die get_wetter_raw!
    SQL_QUERY = """
    Execute get_wetter_raw
    """
    cursor.execute(SQL_QUERY)
    #Return wird in der aufrufenden Funktion als "records" gespeichert
    return cursor.fetchall()

def records2dict(records):
    
    windrichtungen = [item[0] for item in records]
   
    # Um den Durschnitt der Windrichtung zu berechnen, wird die trigonomische Mittelung verwendet
    # Die Winkel werden in kartesische Koordinaten konvertiert.
    xy_coordinates = [(math.cos(math.radians(windrichtung)), math.sin(math.radians(windrichtung))) for windrichtung in windrichtungen]

    #Berechne den Durschnitt der Koordinaten
    # _ ist ein Platzhalter für den Teil, der nicht berücksichtigt wird
    avg_x = sum(x for x, _ in xy_coordinates) / len(xy_coordinates)
    avg_y = sum(y for _, y in xy_coordinates) / len(xy_coordinates)    
  
    #Konvertire den Durschnitt der Koordinaten zurück in einen Winkel
    avg_angel = math.degrees(math.atan2(avg_y, avg_x))
    if avg_angel <0:
        avg_angel +=360 # Korrektur für negative Winkel
    


    windspeeds = [item[1] for item in records]
    temeratur = [item[2] for item in records]
    qfe = [item[3] for item in records]
    qnh = [item[4] for item in records]

    min_windrichtung = min(windrichtungen)
    avg_windrichtung = round(avg_angel,0)
    max_windrichtung = max(windrichtungen)        

    min_windspeed = min(windspeeds)
    avg_windspeed = round(sum(windspeeds) / len(windspeeds),1)
    max_windspeed = max(windspeeds)    

    avg_temp = round(sum(temeratur) / len(temeratur),0)
    avg_qfe = round(sum(qfe) / len(qfe),0)
    avg_qnh = round(sum(qnh) / len(qnh),0)

    #Wind noch von KN in KM/h umrechnen und zum Dict hinzufügen
    min_Speed_KMH = round(min_windspeed * 1.852,1)
    avg_Speed_KMH = round(avg_windspeed * 1.852,1)
    max_Speed_KMH = round(max_windspeed * 1.852,1)

    # Aktuelle Zeit einfügen in UTX
    utc_datetime = datetime.now(timezone.utc)
    utc_iso_str = datetime.strftime(utc_datetime, "Letztes Update am %d-%m-%Y um %H:%M:%S UTC")
    time = utc_iso_str

    #Alles als Dictionary speichern
    data = {
        "min_Windrichtung": min_windrichtung,
        "max_Windrichtung": max_windrichtung,
        "avg_Windrichtung": avg_windrichtung,
        "min_Windspeed": min_windspeed,
        "max_Windspeed": max_windspeed,
        "avg_Windspeed": avg_windspeed,
        "min_Speed_KMH": min_Speed_KMH,
        "max_Speed_KMH": max_Speed_KMH,
        "avg_Speed_KMH": avg_Speed_KMH,        
        "Temp": avg_temp,
        "QFE": avg_qfe,
        "QNH": avg_qnh,
        "time": time
    }

    return(data)


def getWetter():

    # Konfiguriere das Logging
    logging.basicConfig(filename='logfile.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

    try:
        #Verbindung zur SQL Datenbank wird geöffnet
        conn = make_connection()
        #Zeiger oder Cursor auf die Datenbank. 
        cursor = conn.cursor()
    
    except Exception as e:
            logging.error(f"Fehler bei der SQL Verbindung: {e}")  
            mail.SendError(f"Fehler bei der SQL Verbindung: {e}")  

    #Im  Try Block wird versucht die Daten aus der Datenvank zu lesen.
    try:
        #Daten aus Datenbank mit SQL Statement holen.
        records = get_data(cursor)
        
        #Daten verarbeiten
        data =records2dict(records)
        #Verbindung zur Datenbank schliessen
        conn.close()
    
    except Exception as e:
        logging.error(f"Fehler beim Ausführen der SQL-Abfrage: {e}")
        mail.SendError(f"Fehler beim Ausführen der SQL-Abfrage: {e}") 
        
        # Aktuelle Zeit einfügen in UTX
        utc_datetime = datetime.now(timezone.utc)
        utc_iso_str = datetime.strftime(utc_datetime, "Letztes Update am %d-%m-%Y um %H:%M:%S UTC")
        time = utc_iso_str
        
        #Überschriften und Rows in ein Dictionary
        data = {
            "min_Windrichtung": "noData",
            "max_Windrichtung": "noData",
            "avg_Windrichtung": "noData",
            "min_Windspeed": "noData",
            "max_Windspeed": "noData",
            "avg_Windspeed": "noData",
            "min_Speed_KMH": "noData",
            "max_Speed_KMH": "noData",
            "avg_Speed_KMH": "noData",        
            "Temp": "noData",
            "QFE": "noData",
            "QNH": "noData",
            "time": time
        }

    return data     
    

if __name__ == '__main__':
    data = getWetter()
    print(data)