import sys
from typing import List

import requests
from bs4 import BeautifulSoup

POOPLE_HOME = "http://poople.io"
MARKER = "const wordDist"
QUOTE_CHAR = "`"
SPLIT_BY = "\n"


def download_data(path: str = "") -> str:
    response = requests.get(f"{POOPLE_HOME}{path}")
    return response.text


def get_script_urls(contents: str) -> List[str]:
    soup = BeautifulSoup(contents, 'html.parser')
    urls = [s["src"] for s in soup.find_all("script") if "src" in s.attrs]
    return urls


def extract_word_list(contents: str) -> List[str]:
    search_start = contents.index(MARKER)
    list_start = contents.index(QUOTE_CHAR, search_start + len(MARKER))
    list_end = contents.index(QUOTE_CHAR, list_start + 1)
    word_list_str = contents[list_start + 1:list_end]
    return word_list_str.split(SPLIT_BY)


def manual_acceptance() -> bool:
    yn = input("Does this look like correct data? (y/n): ")
    return yn.lower() == "y"


def write_to_file(lines: List[str], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line.split(",")[0] + "\n")


def run(output_path: str):
    print("Downloading main page...")
    html_content = download_data()
    print("Searching for scripts...")
    script_urls = get_script_urls(html_content)
    print(f"Found {len(script_urls)} scripts.")

    for script_url in script_urls:
        if script_url.startswith("http"):
            print(f"Skipping external script ({script_url}).")
            continue
        print(f"Downloading script ({script_url})...")
        script_contents = download_data(script_url)
        print("Checking script...")
        if MARKER not in script_contents:
            print("Not the word list script.")
        else:
            print("  Found word list script. Extracting words...")
            word_list = extract_word_list(script_contents)
            print(f"  Got {len(word_list)} words.")
            print(f"  {word_list[:5]} ... {word_list[-5:]}")
            if not manual_acceptance():
                print("Manually rejected.")
            else:
                write_to_file(word_list, output_path)
                print(f"Wrote word list to {output_path}")
                break
    print("Done.")


if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) != 1:
        print("Usage: python download_words.py <output_text_file>")
        sys.exit(1)
    run(params[0])
