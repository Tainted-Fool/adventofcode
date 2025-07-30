in="1321131112";

for i in $(seq 1 40); do
  in=$(echo "$in" | fold -w1 | uniq -c | tr '\n' ' ' | tr -d ' ');
  echo $in | tr -d '\n' | wc -c;
done
echo "Part 1: $(echo $in | wc -c)"

in="1321131112";
for i in `seq 50`; do
  in=`fold -w1 <<< "$in" | uniq -c | tr -d '\n '`;
done
wc -c <<< $in
echo "Part 2: $(echo $in | wc -c)"
