# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(r'd:\swat-lvpd\index.html')
html = path.read_text(encoding='utf-8')

nav_old = '''          <nav class="manual-nav">
            <a href="#manual-1" class="manual-nav__link active" data-section="manual-1">§1 Общие положения</a>
            <a href="#manual-2" class="manual-nav__link" data-section="manual-2">§2 Дисциплина</a>
            <a href="#manual-3" class="manual-nav__link" data-section="manual-3">§3 Use of Force</a>
            <a href="#manual-4" class="manual-nav__link" data-section="manual-4">§4 Тактика штурма</a>
            <a href="#manual-5" class="manual-nav__link" data-section="manual-5">§5 Коммуникации</a>
            <a href="#manual-6" class="manual-nav__link" data-section="manual-6">§6 Экипировка</a>
          </nav>'''

nav_new = Path(r'd:\swat-lvpd\data\manual-nav.html').read_text(encoding='utf-8')
manual_body = Path(r'd:\swat-lvpd\data\manual-sections.html').read_text(encoding='utf-8')
roleplay = Path(r'd:\swat-lvpd\data\roleplay-section.html').read_text(encoding='utf-8')

html = html.replace(nav_old, nav_new)
html = html.replace(
    '        <h2 class="section__title">Устав и мануал</h2>\n      </div>',
    '        <h2 class="section__title">Устав и мануал</h2>\n        <p class="section__desc">Источник: «Основные положения по работе в отряде SWAT»</p>\n      </div>',
    1,
)

marker_start = '        <div class="manual-content">'
marker_end = '        </div>\n      </div>\n    </div>\n  </section>\n\n  <!-- Academy Form -->'
start = html.index(marker_start) + len(marker_start)
end = html.index(marker_end)
html = html[:start] + '\n' + manual_body + html[end:]

html = html.replace(
    '  <!-- Academy Form -->',
    roleplay + '\n  <!-- Academy Form -->',
    1,
)

path.write_text(html, encoding='utf-8')
print('Patched index.html OK')
