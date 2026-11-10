#!/usr/bin/env bash
# Compile et execute les quatre programmes (cours + variante, deux formes chacun).
set -e
cd "$(dirname "$0")"
for d in Cours variantes; do
  mkdir -p "out/$d"
  javac -d "out/$d" $(find "$d/src" -name '*.java')
  for p in factorymethod factoryabstraite; do
    echo "=== $d / $p ==="
    java -cp "out/$d" "$p.Client"
    echo
  done
done
