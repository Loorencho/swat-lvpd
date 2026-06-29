from pathlib import Path

html = Path(r"d:\swat-lvpd\index.html").read_text(encoding="utf-8")
frag = Path(r"d:\swat-lvpd\data\internship-section.html").read_text(encoding="utf-8")

start_marker = '      <div class="internship-content">'
end_marker = '  <!-- Arsenal -->'

start = html.index(start_marker)
end = html.index(end_marker)
html = html[:start] + frag + "\n    </div>\n  </section>\n\n  " + html[end:]
Path(r"d:\swat-lvpd\index.html").write_text(html, encoding="utf-8")
print("patched internship")
