#!/usr/bin/python 

def enum(**kwargs):
    return type('Enum', (), kwargs)


