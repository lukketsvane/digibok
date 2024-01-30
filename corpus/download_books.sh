
while read -r book_id; do
    python3 nbno.py --id "$book_id" --title --pdf
    sleep 2
done < book_ids.txt
