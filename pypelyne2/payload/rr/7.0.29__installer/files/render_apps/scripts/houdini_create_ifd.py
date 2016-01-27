#python
# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Render script for Houdini
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Version v 7.0.03
# Copyright (c) Holger Schoenberger - Binary Alchemy
# 
######################################################################

import sys
import traceback

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)


try:
    print( "RR - start "  )
    idx = sys.argv.index( "-frames" )
    seqStart = int(sys.argv[ idx + 1 ])
    seqEnd = int(sys.argv[ idx + 2 ])
    seqStep = int(sys.argv[ idx + 3 ])
    
    if "-fileName" not in sys.argv:
        fileName = None
    else:
        idx = sys.argv.index( "-fileName" )
        fileName = sys.argv[ idx + 1 ]

    if "-filePadding" not in sys.argv:
        filePadding = None
    else:
        idx = sys.argv.index( "-filePadding" )
        filePadding = int(sys.argv[ idx + 1 ])

    imgRes = ()
    if "-res" in sys.argv:
        idx = sys.argv.index( "-res" )
        width = int( sys.argv[ idx + 1 ] )
        height = int( sys.argv[ idx + 2 ] )
        imgRes = (width,height)
    
    idx = sys.argv.index( "-driver" )
    driver = sys.argv[ idx + 1 ]
    inputFile = sys.argv[ len(sys.argv) - 1 ]
    try:
        hou.hipFile.load( inputFile, True )
    except hou.LoadWarning, e:
        print( "Error: LoadWarning (probably wrong houdini version)")
        print( e)
    

    rop = hou.node( driver )
    if rop == None:
        print( "Error: Driver node \"" + driver + "\" does not exist" )
    else:
        for fr in range( seqStart, seqEnd + 1 ):
            print( "Rendering Frame #" + str(fr) +" ...")
            rop.render( (fr,fr,seqStep), imgRes )
            print( "Frame Rendered #" + str(fr) )

except hou.OperationFailed, e:
    print( "Error: OperationFailed")
    print( e)
    print( formatExceptionInfo())
            
except:
    print( "Error: Error executing script")
    print( formatExceptionInfo())