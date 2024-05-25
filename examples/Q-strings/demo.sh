#!/usr/bin/bash

# create pup alias
. <(cat pup.sh | tail -1)

cmd="pup fetch ducks-pandas duckdb pandas"
echo "🎇 $cmd"
eval $cmd

cmd="pup kernel ducks-pandas ducks-pandas-3.12"
echo "$cmd"
eval $cmd

cmd="pup play -k ducks-pandas-3.12 -n play_test.ipynb \
-c \"md|### 🐶 woof! I made this notebook!;and added some code!\" \
-c \"%%bash;pwd\" \
-N"
echo "🎇 $cmd"
eval $cmd

# sleep 3
cmd="pup play -k ducks-pandas-3.12 -n play_test.ipynb \
-c \"md|### 🐶 woof! I made this notebook!;and added some code!;;and ran it!\" \
-c \"%%bash;pwd;ls -l;ls -l ..\" \
-N -E"
echo "🎇 $cmd"
eval $cmd
cat notebooks/play_test.ipynb

# sleep 5
PY_URL=https://raw.githubusercontent.com/liquidcarbon/puppy/main/examples/Q-strings/Q.py
cmd="pup play -k ducks-pandas-3.12 -n play_test.ipynb \
-c \"md|### 🐶 I can fetch external scripts into this notebook!;and run them\" \
-c \"\`curl -s $PY_URL\`\" \
-c \"Q('../examples/Q-strings/query1.sql', file=True, x=42).run()\" \
-N -E"
echo "🎇 $cmd"
eval $cmd

cmd="cat notebooks/play_test.ipynb"
echo "🎇 $cmd"
eval $cmd


# sleep 3
# PY_URL=https://raw.githubusercontent.com/liquidcarbon/puppy/main/examples/Q-strings/Q.py
# cmd="pup play -k ducks-pandas-3.12 -n q/qtest.ipynb \
# -c \"md|### 🐶 I can fetch external scripts into this notebook!;and fetch the notebook for you\" \
# -c \"\`curl -s $PY_URL\`\" \
# -c \"Q('../../examples/Q-strings/query1.sql', file=True, x=42).run()\" \
# -E -S"
# echo "$cmd"
# eval $cmd
