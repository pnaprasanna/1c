import markdown
from bs4 import BeautifulSoup

def md_to_cards(md_file, html_file):
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_table = markdown.markdown(md_content, extensions=["tables"])
    soup = BeautifulSoup(html_table, "html.parser")

    headers = [th.get_text(strip=True) for th in soup.select("thead th")]
    rows = soup.select("tbody tr")

    cards_html = ""

    for row in rows:
        values = [td.get_text(strip=True) for td in row.select("td")]
        row_data = dict(zip(headers, values))
        url = row_data.get("URL", "")

        fields = ""
        for key, value in row_data.items():
            if key.lower() == "url":
                fields += f"""
                <div class="field">
                  <div class="label">{key}</div>
                  <a class="value link" href="{value}" target="_blank" rel="noopener">
                    {value}
                  </a>
                </div>
                """
            else:
                fields += f"""
                <div class="field">
                  <div class="label">{key}</div>
                  <div class="value">{value}</div>
                </div>
                """

        cards_html += f"""
        <div class="card">
          {fields}
          <div class="status" data-url="{url}">⏳</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>URL Dashboard</title>

<style>
:root {{
  --bg: #f7f7f7;
  --card: #ffffff;
  --text: #222222;
  --muted: #6b6b6b;
  --link: #0066cc;
}}

body.dark {{
  --bg: #1b1b1b;
  --card: #262626;
  --text: #e6e6e6;
  --muted: #9e9e9e;
  --link: #4da3ff;
}}

body {{
  margin: 0;
  padding: 16px;
  font-family: Arial, Helvetica, Verdana, sans-serif;
  font-size: 13px;
  background: var(--bg);
  color: var(--text);
  line-height: 1.4;
}}

.header {{
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}}

.toggle {{
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
}}

.timestamp {{
  text-align: center;
  font-size: 11px;
  color: var(--muted);
  margin-bottom: 14px;
}}

.container {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}}

.card {{
  background: var(--card);
  border-radius: 10px;
  padding: 14px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.08);
  position: relative;
}}

.field {{
  margin-bottom: 8px;
}}

.label {{
  font-size: 11px;
  color: var(--muted);
}}

.value {{
  font-weight: 600;
  word-break: break-word;
}}

.link {{
  color: var(--link);
  text-decoration: none;
}}

.link:hover {{
  text-decoration: underline;
}}

.status {{
  position: absolute;
  top: 10px;
  right: 12px;
  font-size: 16px;
}}

.ok {{ color: #2e8b57; }}
.fail {{ color: #cc3333; }}
</style>
</head>

<body>

<div class="header">
  <button class="toggle" id="modeBtn">🌙</button>
</div>

<div class="timestamp" id="updated"></div>

<div class="container">
  {cards_html}
</div>

<script>
// Timestamp
document.getElementById("updated").textContent =
  "Last updated: " + new Date().toLocaleString();

// Dark mode toggle
const body = document.body;
const btn = document.getElementById("modeBtn");

btn.onclick = () => {{
  body.classList.toggle("dark");
  btn.textContent = body.classList.contains("dark") ? "☀️" : "🌙";
}};

// URL status check
document.querySelectorAll(".status").forEach(el => {{
  const url = el.dataset.url;
  if (!url) {{
    el.textContent = "-";
    return;
  }}

  fetch(url, {{ method: "HEAD", mode: "no-cors" }})
    .then(() => {{
      el.textContent = "✔";
      el.classList.add("ok");
    }})
    .catch(() => {{
      el.textContent = "✖";
      el.classList.add("fail");
    }});
}});
</script>

</body>
</html>
"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Responsive index.html generated successfully")


# Usage
md_to_cards("bm.md", "index.html")
