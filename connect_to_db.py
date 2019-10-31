#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None

try:
    con = psycopg2.connect("host='192.168.1.102' dbname='lab_db' user='postgres' password='123'")
    cur = con.cursor()
    cur.execute("SELECT * FROM subject")

    while True:
        row = cur.fetchone()

        if row == None:
            break

        print("Subject: " + row[1] + "\t\t\t\thours: " + str(row[2]))

except psycopg2.DatabaseError :
    if con:
        con.rollback()
    
    print("Error " )    
    sys.exit(1)
    
finally:   
    if con:
        con.close()
