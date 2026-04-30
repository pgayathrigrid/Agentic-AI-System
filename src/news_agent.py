from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

def fetch_news(query):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '%20')}"
    response = requests.get(url)

    root = ET.fromstring(response.content)

    results = []
    for item in root.findall(".//item")[:5]:
        title = item.find("title").text
        link = item.find("link").text

        results.append(f"{title}\nSource: {link}")

    return results


@app.route("/news", methods=["GET"])
def news():
    query = request.args.get("q", "")
    results = fetch_news(query)
    return jsonify({"news": results})


if __name__ == "__main__":
    app.run(port=5001)