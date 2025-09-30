pip install beautifulsoup4

python ./tools/download_words.py ./data/words.txt
python ./tools/words_to_json.py ./data/words.txt ./data/data.json

read -p "Promote new data.json to site usage? (y/n): " choice
case "$choice" in 
    y|Y ) echo "Copying..."; cp ./data/data.json ./kupa/data.json;;
esac
echo "Done."