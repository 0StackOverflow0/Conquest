' A Conquest Client in FastBASIC

' N: Unit to use
unit=8

' URL to Conquest Server
register$="N:HTTP://127.0.0.1:8001/register/"
name$="Janus"
register$=+name$

start$="N:HTTP://localhost:8001/start/"
id$=""

gamestart$=""

' QUERY string
query$=""

' QUERY result
DIM result(1024) BYTE
BW = 0

' JSON channel mode
JSON_MODE=1

' PROCEDURES '''''''''''''''''''''''''
PROC nprinterror
 NSTATUS unit
 PRINT "ERROR- "; PEEK($02ED)
ENDPROC

PROC nsetchannelmode mode
 SIO $71, unit, $FC, $00, 0, $1F, 0, 12, JSON_MODE
ENDPROC

PROC nparsejson
 SIO $71, unit, $50, $00, 0, $1f, 0, 12, 0
ENDPROC

PROC njsonquery
 SIO $71, unit, $51, $80, &query$+1, $1f, 256, 12, 0
ENDPROC

PROC getresult
 @njsonquery
 NSTATUS unit
 
 IF PEEK($02ED) > 128
  PRINT "Could not fetch query:"
  PRINT query$
  EXIT
 ENDIF
 
 BW=DPEEK($02EA)
 NGET unit, &result, BW
ENDPROC

PROC getid
 @getresult
 
 POKE &id$, BW
 MOVE &result, &id$+1, BW
 
 PRINT id$
ENDPROC

PROC registeruser
 ' Open connection
 NOPEN unit, 12, 0, register$

 ' If not successful, then exit.
 IF SERR()<>1
  PRINT "Could not open connection."
  @nprinterror
  EXIT
 ENDIF

 ' Change channel mode to JSON
 @nsetchannelmode JSON_MODE

 ' Ask FujiNet to parse JSON
 @nparsejson

 ' If not successful, then exit.
 IF SErr()<>1
  PRINT "Could not parse JSON."
  @nprinterror
  EXIT
 ENDIF

 query$="N:/id"

 @getid

 NCLOSE unit
ENDPROC

PROC startgame
 start$=+id$
 ' Open connection
 NOPEN unit, 12, 0, start$

 ' If not successful, then exit.
 IF SERR()<>1
  PRINT "Could not open connection."
  @nprinterror
  EXIT
 ENDIF

 ' Change channel mode to JSON
 @nsetchannelmode JSON_MODE

 ' Ask FujiNet to parse JSON
 @nparsejson

 ' If not successful, then exit.
 IF SErr()<>1
  PRINT "Could not parse JSON."
  @nprinterror
  EXIT
 ENDIF
 
 query$="N:/start"

 @getresult
 BPUT #0, &result, BW
 
 PRINT BW
ENDPROC

PROC waitforstart
 REPEAT
  @startgame
  
  POKE &gamestart$, BW
  MOVE &result, &gamestart$+1, BW
 UNTIL gamestart$ = "TRUE"
ENDPROC

@registeruser

@waitforstart

