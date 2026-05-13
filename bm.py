import os
import hashlib
import markdown
from bs4 import BeautifulSoup

def md_to_cards(md_file, html_file):
    password = os.environ.get("DASH_PASSWORD")
    if not password:
        raise RuntimeError("DASH_PASSWORD environment variable not set")

    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_table = markdown.markdown(md_content, extensions=["tables"])
    soup = BeautifulSoup(html_table, "html.parser")

    headers = [th.get_text(strip=True) for th in soup.select("thead th")]
    rows = soup.select("tbody tr")

    cards_html = ""

    for row in rows:
        values = [td.get_text(strip=True) for td in row.select("td")]
        data = dict(zip(headers, values))
        url = data.get("URL", "").strip()

        if not url:
            continue

        fields_html = ""

        for k, v in data.items():
            if k.lower() == "url":
                continue
            fields_html += f"""
            <div class="field">
              <div class="label">{k}</div>
              <div class="value">{v}</div>
            </div>
            """

        # ✅ URL with inline status
        fields_html += f"""
        <div class="field">
          <div class="label">URL</div>
          <div class="value url-line">
            <span>{url}</span>
            <span class="status status-inline">⏳</span>
          </div>
        </div>
        """

        cards_html += f"""
<a class="card" href="{url}" target="_blank" data-url="{url}">
  {fields_html}
</a>
"""

    html_template = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Service Dashboard</title>

<style>
:root {
  --bg: #121212;
  --card: #1e1e1e;
  --text: #e0e0e0;
  --muted: #9e9e9e;
  --border: #2a2a2a;
  --ok: #3cb371;
  --fail: #e05555;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, Verdana, sans-serif;
  background: var(--bg);
  color: var(--text);
}

/* ✅ LAYOUT FIX */
#layout {
  display: flex;
  min-height: 100vh;
}

/* ✅ SIDEBAR */
.sidebar {
  width: 0;
  overflow: hidden;
  background: var(--card);
  border-right: 1px solid var(--border);
  transition: width 0.3s ease;
}

.sidebar.active {
  width: 220px;
  padding: 16px;
}

.sidebar a {
  display: block;
  margin: 12px 0;
  color: var(--text);
  text-decoration: none;
}

/* ✅ MAIN CONTENT */
#main {
  flex: 1;
  padding: 14px;
}

/* ✅ MENU BUTTON */
.menu-btn {
  cursor: pointer;
  font-size: 18px;
}

/* existing UI */
.topbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.search {
  flex: 1;
  max-width: 420px;
  padding: 8px;
}

.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

/* ✅ CARD (UNCHANGED STYLE) */
.card {
  background: var(--card);
  border-radius: 12px;
  padding: 14px;
  text-decoration: none;
  color: var(--text);
  border: 1px solid var(--border);
  transition: 0.2s;
}

/* ✅ Neon pulse preserved */
@keyframes neonPulse {
  0%,100% {
    box-shadow: 0 0 10px rgba(0,255,200,0.2);
  }
  50% {
    box-shadow: 0 0 30px rgba(0,255,200,0.4);
  }
}

.card:hover {
  transform: translateY(-4px);
  border-color: rgba(0,255,200,0.6);
  animation: neonPulse 1.5s infinite;
}

.field { margin-bottom: 8px; }
.label { font-size: 11px; color: var(--muted); }
.value { font-weight: 600; }

/* ✅ URL + STATUS */
.url-line {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-inline {
  font-size: 14px;
}

.ok {
  color: #3b82f6;
}

.fail {
  color: var(--fail);
}

/* ✅ Mobile fix */
@media (max-width: 768px) {
  .sidebar.active {
    width: 180px;
  }
}
</style>
</head>

<body>

<div id="layout">

  <!-- ✅ SIDEBAR -->
  <div id="sidebar" class="sidebar">
    <a href="#">🏠 Home</a>
    <a href="#">📊 Dashboard</a>
    <a href="#">📁 Projects</a>
    <a href="#">⚙ Settings</a>
  </div>

  <!-- ✅ MAIN -->
  <div id="main">

    <div class="topbar">
      <span class="menu-btn" onclick="toggleMenu()">☰</span>
      <input type="text" class="search" placeholder="Search..." id="searchBox">
    </div>

    <div class="container">
    __CARDS__
    </div>

  </div>

</div>

<script>
function toggleMenu() {
  document.getElementById("sidebar").classList.toggle("active");
}

/* search */
document.getElementById("searchBox").addEventListener("keyup", e => {
  const q = e.target.value.toLowerCase();
  document.querySelectorAll(".card").forEach(card => {
    card.style.display = card.innerText.toLowerCase().includes(q) ? "" : "none";
  });
});

/* status */
function checkStatuses() {
  document.querySelectorAll(".card").forEach(card => {
    const status = card.querySelector(".status-inline");
    const url = card.dataset.url;

    fetch(url, { method: "HEAD", mode: "no-cors" })
      .then(() => {
        status.textContent = "✔";
        status.classList.add("ok");
      })
      .catch(() => {
        status.textContent = "✖";
        status.classList.add("fail");
      });
  });
}

checkStatuses();
</script>

</body>
</html>
"""

    html_final = (
        html_template
        .replace("__CARDS__", cards_html)
        .replace("__PASSWORD_HASH__", password_hash)
    )

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_final)

    print("✅ index.html generated successfully")


md_to_cards("bm.md", "index.html")
