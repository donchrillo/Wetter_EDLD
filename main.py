import SQL_Wetter_raw as wetter
import time
import json
import logging
import sftp_upload as ftp
import mail as mail



def make_json():
    # Konfiguriere das Logging
    logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    logging.info("Programm ordentlich gestartet!")
    while True:
        try:
            data = wetter.getWetter()
        
            with open("daten.json", "w") as outfile:
                json.dump(data, outfile, indent=2)

            # FTP-Upload
            ftp.put_json()
            #PAuse von 2 minuten
            time.sleep(120)
            #no return |  Just safe the file for FTP Upload
        except Exception as e:
            logging.error(f"Fehler beim Ausführen von Main: {e}")   
            mail.SendError(f"Fehler beim Ausführen von Main: {e}")              
            #Pause von 10min
            time.sleep(600)


if __name__ == "__main__":
    make_json()
 