#!/bin/bash
sed -i "s/8080/$PORT/g" config.json
./xray run -c config.json
