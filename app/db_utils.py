# app/db_utils.py

import psycopg2

def conectar_db():
    return psycopg2.connect(
        host="ballast.proxy.rlwy.net",
        port="10605",
        dbname="railway",
        user="postgres",
        password="vFqfjqGKjbzNaSscGyLjvWifXrhaifHy"
    )
