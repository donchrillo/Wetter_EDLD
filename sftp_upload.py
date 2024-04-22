import paramiko
import logging
import mail as mail

def put_json():
    # Konfiguriere das Logging
    logging.basicConfig(filename='logfile.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

    try:
        # create ssh client 
        ssh_client = paramiko.SSHClient()

        # remote server credentials
        host = "<HOSTNAME>"
        username = "<USERNAME>"
        password = "<PORT>"
        port = 22

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host,port=port,username=username,password=password)

        ftp = ssh_client.open_sftp()
        files = ftp.put("daten.json", "wp-content/uploads/wetter/daten.json")

        # close the connection
        ftp.close()
        ssh_client.close()
    except Exception as e:
        logging.error(f"Fehler beim FTP Upload: {e}")   
        mail.SendError(f"Fehler beim FTP Upload: {e}")  

if __name__ == '__main__':
    
    put_json()