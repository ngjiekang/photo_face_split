#!/bin/bash

for i in {1..436}
do
  wget -r -l1 -A.jpg https://www.fotomada.gr/events/view/1545?page=$i
done