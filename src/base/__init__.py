#!/usr/bin/python 

###
#GLOBAL FUNCTIONS AND DEFINITIONS
###

def enum(**kwargs):
    """ 
    Returns a type object with class name 'Enum' and members given by the
    kwargs dictionary. Found on StackOverflow.
    Create like this:
        Animals = enum(DOG=0, CAT=1)

    :param      kwargs | key=int pairs
    """
    return type('Enum', (), kwargs)
