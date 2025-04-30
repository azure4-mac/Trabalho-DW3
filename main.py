from flask import Flask, request, jsonify
import psycopg
import requests

app = Flask(__name__)

connection_db = psycopg.connect("dbname=mac user=postgres password=3f@db host=164.90.152.205 port=80")
