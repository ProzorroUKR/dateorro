#!/bin/sh

INFO_FILE='info.md'
DOCSFILE='docs.md'

FILE='README.md'

cat $INFO_FILE $DOCSFILE > $FILE
