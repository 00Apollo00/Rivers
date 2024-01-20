import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
# конфигурация
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = '123a'
#USERNAME = 'admin'
#PASSWORD = 'default'