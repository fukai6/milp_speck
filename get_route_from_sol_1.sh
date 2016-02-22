#! /bin/bash

read -p "The sol filename is : " filename
read -p "The blocksize is : "    blocksize
read -p "The round is : "        round
read -p "Differential or linear(input d or l> :" choose

if [ "$choose" = 'd' ]
then
diff="differential"
pron="probability"
mask="differences"
else
diff="linear"
pron="correlation"
mask="linear mask"
fi


printf "The best $diff $pron of $round round of SPECK$blocksize is 2^{-"
head -n 1 $filename | tr "\n\r" "\n" | head -n 1| cut -d" " -f5 | tr "\n" "}"
printf "\n\n"

printf "The $diff path is below:\n\n"

printf "The input $mask of plaintext is:\n"

grep '^p[0-9]* ' $filename | sed 's/p//g' | sort -nk1 | cut -d" " -f2 | tr "\n\r" "\n"| xargs -n 4 | sed 's/ //g' | xargs

for((i=1; i<=$round; i++))
do

printf "The input $mask of the round $i is :\n"
grep "^p[0-9]*Rd$i " $filename | sed -e 's/p//g' -e 's/Rd/ /g' | sort -nk1 | cut -d " " -f3 | tr "\n\r" "\n"| xargs -n 4 | sed 's/ //g' | xargs

done

exit 0



