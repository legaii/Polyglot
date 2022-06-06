import sys
import requests
import fileinput

def translate(api_key, lang, text):
  return requests.get(f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang={lang}&text={text}").json()

def main():
  assert len(sys.argv) == 3
  for line in fileinput.input():
    for item_from in translate(sys.argv[1], sys.argv[2], line)["def"]:
      print("; ".join(item_to["text"] for item_to in item_from["tr"]) + f" ({item_from.get('pos', 'unknown')})", item_from["text"], 0, sep=" = ")

if __name__ == "__main__":
  main()

