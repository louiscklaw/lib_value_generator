#!/usr/bin/env bash


_gen_files="gen*.py"
for f in $_gen_files
do
  echo 'generating ' $f '...'
  python3 $f
  echo 'generating ' $f 'done'
done