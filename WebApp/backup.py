import sqlite3
import io
import datetime


def backupDB():
    conn = sqlite3.connect('database.db')  

    string = 'backup/' + str(datetime.datetime.today().strftime('%d-%m-%Y')) 
    # Open() function 
    with io.open(string, 'w') as p: 
            
        # iterdump() function
        for line in conn.iterdump(): 
            
            p.write('%s\n' % line)
        
    print(' Backup performed successfully!')
    print(' Data Saved as backupdatabase_dump.sql')
    
    conn.close()