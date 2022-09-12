#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:36:07 2022

@author: abdul
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"