from pathlib import Path

html = Path(r"d:\swat-lvpd\index.html").read_text(encoding="utf-8")
frag = Path(r"d:\swat-lvpd\data\personnel-section.html").read_text(encoding="utf-8")

marker_start = '      <div class="org-chart">'
marker_end = '  </section>\n\n  <!-- Blacklist -->'

start = html.index(marker_start)
end = html.index(marker_end)
html = html[:start] + frag + "\n" + html[end:]
Path(r"d:\swat-lvpd\index.html").write_text(html, encoding="utf-8")
print("patched personnel")
