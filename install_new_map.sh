#!/bin/bash
/usr/bin/screen -p 0 -S minecraft -X stuff "say WOW, FOUND A NEW MAP $1!!! placing it at $3 $4 $5"
/usr/bin/screen -p 0 -S minecraft -X eval 'stuff \\015'

/usr/bin/screen -p 0 -S minecraft -X stuff "replaceitem block $3 $4 $5 container.$6 minecraft:filled_map{map:$2} 1"
/usr/bin/screen -p 0 -S minecraft -X eval 'stuff \\015'
