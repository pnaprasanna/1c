import markdown
import re

def md_to_cards(md_file, html_file):
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extract URLs
    urls = list(set(re.findall(r"https?://[^\s|)]+", md_content)))

    cards_html = ""
    for url in urls:
        cards_html += f"""
        <div class="card">
          <div class="url">{url}</div>
          <div class="status" data-url="{url}">Checking…</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>URL Status Monitor</title>

<style>
  body {{
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 16px;
    background: #f4f6f8;
  }}

  h2 {{
    text-align: center;
    margin-bottom: 16px;
  }}

  .container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
  }}

  .card {{
    background: white;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
  }}

  .card:hover {{
    transform: translateY(-4px);
  }}

  .url {{
    word-break: break-all;
    font-weight: bold;
    margin-bottom: 12px;
    color: #333;
  }}

  .status {{
    font-size: 18px;
    font-weight: bold;
  }}

  .ok {{
    color: green;
  }}

  .fail {{
    color: red;
  }}

  .checking {{
    color: #999;
  }}

  @media (max-width: 600px) {{
    body {{
      padding: 10px;
    }}
  }}
</style>
</head>

<body>

<h2>URL Availability Dashboard</h2>

<div class="container">
  {cards_html}
</div>

<script>
function checkURL(el, url) {{
  fetch(url, {{ method: "HEAD", mode: "no-cors" }})
    .then(() => {{
      el.textContent = "✔ Live";
      el.className = "status ok";
    }})
    .catch(() => {{
      el.textContent = "✖ Failed";
      el.className = "status fail";
    }});
}}

document.querySelectorAll(".status").forEach(el => {{
  const url = el.dataset.url;
  el.classList.add("checking");
  checkURL(el, url);
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
