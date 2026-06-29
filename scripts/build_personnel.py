# -*- coding: utf-8 -*-
"""Generate personnel org sections with photo profile cards (FBI-evolve layout)."""
from pathlib import Path

STATUS_CLASS = {
    "active": "card__status--active",
    "denied": "card__status--leave",
    "inactive": "card__status--leave",
}

ORG_BLOCKS = [
    {
        "tag": "OSO",
        "title": "Управление OSO",
        "layout": "stack",
        "roles": [
            {
                "title": "Директор OSO",
                "people": [
                    {
                        "name": "Danil Schwartz",
                        "rank": "Майор",
                        "callsign": "Укроп",
                        "role": "Директор OSO",
                        "status": "active",
                        "status_label": "Активен",
                        "note": "",
                    }
                ],
            }
        ],
    },
    {
        "tag": "CMD",
        "title": "Командование SWAT",
        "layout": "grid",
        "roles": [
            {
                "title": "Командир SWAT",
                "people": [
                    {
                        "name": "Martini Branos",
                        "rank": "Прапорщик",
                        "callsign": "Бритва",
                        "role": "Командир SWAT",
                        "status": "active",
                        "status_label": "Активен",
                        "note": "Следит за составом, осуществляет вербовку членов отряда.",
                    }
                ],
            },
            {
                "title": "Зам. командира SWAT",
                "people": [
                    {
                        "name": "Culkin Schwartz",
                        "rank": "Мл.Лейтенант",
                        "callsign": "Калкин",
                        "role": "Зам. командира SWAT",
                        "status": "active",
                        "status_label": "Активен",
                        "note": "Тренировки отдела, работа по ордерам, дисциплина.",
                    },
                    {"vacant": True, "role": "Зам. командира SWAT"},
                ],
            },
            {
                "title": "Инструктор SWAT",
                "people": [
                    {
                        "name": "Sergey Karat",
                        "rank": "Ст.Лейтенант",
                        "callsign": "Восток",
                        "role": "Инструктор SWAT",
                        "status": "active",
                        "status_label": "Активен",
                        "note": "",
                    }
                ],
            },
        ],
    },
    {
        "tag": "OPS",
        "title": "Оперативный состав",
        "layout": "grid",
        "roles": [
            {
                "title": "Оперативник SWAT",
                "people": [
                    {"name": "Alonso Montez", "rank": "Ст.Лейтенант", "callsign": "Малой", "role": "Оперативник SWAT", "status": "active", "status_label": "Активен", "note": ""},
                    {"name": "Denis MacTavish", "rank": "Ст.Лейтенант", "callsign": "Сармат", "role": "Оперативник SWAT", "status": "active", "status_label": "Активен", "note": ""},
                    {"name": "Akylbek Mamura", "rank": "Мл.Лейтенант", "callsign": "Вацок", "role": "Оперативник SWAT", "status": "active", "status_label": "Активен", "note": ""},
                    {"name": "Salvestro Suarrez", "rank": "Ст.Прапорщик", "callsign": "Один", "role": "Оперативник SWAT", "status": "denied", "status_label": "Не допущен", "note": ""},
                    {"name": "Miden Heydrich", "rank": "Мл.Лейтенант", "callsign": "Метла", "role": "Оперативник SWAT", "status": "active", "status_label": "Активен", "note": ""},
                ],
            }
        ],
    },
    {
        "tag": "RSV",
        "title": "Резерв SWAT",
        "layout": "grid",
        "roles": [
            {
                "title": "Оперативник SWAT (резерв)",
                "people": [
                    {"name": "Maksim Shom", "rank": "Капитан", "callsign": "Войз", "role": "Оперативник SWAT", "status": "inactive", "status_label": "Неактив", "note": "Неактив 23.04–24.05. Резерв SWAT."},
                    {"name": "Rauf Falk", "rank": "Ст.Лейтенант", "callsign": "?", "role": "Оперативник SWAT", "status": "inactive", "status_label": "Неактив", "note": "Неактив 23.04–24.05. Резерв SWAT."},
                ],
            }
        ],
    },
]


def flatten_people(block):
    people = []
    for role in block["roles"]:
        for person in role["people"]:
            if person.get("vacant"):
                people.append(person)
            else:
                entry = dict(person)
                if not entry.get("role"):
                    entry["role"] = role["title"]
                people.append(entry)
    return people


def render_card(person, img):
    if person.get("vacant"):
        return f'''            <article class="card card--personnel card--profile card--personnel-vacant">
              <div class="card__image card__image--{img}"></div>
              <div class="card__body card__body--profile">
                <h3 class="card__name">—</h3>
                <p class="card__role">{person["role"]}</p>
                <span class="card__status card__status--leave">Вакантно</span>
              </div>
            </article>'''

    st_class = STATUS_CLASS.get(person["status"], "card__status--active")
    note_html = f'\n                <p class="card__note">{person["note"]}</p>' if person.get("note") else ""
    photo_attr = f' data-photo="{person["photo"]}" style="background-image:url(\'{person["photo"]}\')"' if person.get("photo") else ""

    return f'''            <article class="card card--personnel card--profile card--accordion">
              <button type="button" class="card__toggle" aria-expanded="false">
                <div class="card__image card__image--{img}"{photo_attr}></div>
                <div class="card__body card__body--profile">
                  <h3 class="card__name">{person["callsign"]}</h3>
                  <p class="card__role">{person["role"]}</p>
                  <span class="card__expand-hint">Подробнее</span>
                </div>
              </button>
              <div class="card__details" hidden>
                <dl class="card__meta">
                  <dt>Имя, фамилия</dt>
                  <dd>{person["name"]}</dd>
                  <dt>Позывной</dt>
                  <dd>{person["callsign"]}</dd>
                  <dt>Звание</dt>
                  <dd>{person["rank"]}</dd>
                  <dt>Должность</dt>
                  <dd>{person["role"]}</dd>
                  <dt>Статус</dt>
                  <dd><span class="card__status {st_class}">{person["status_label"]}</span></dd>
                </dl>{note_html}
              </div>
            </article>'''


def render_block(block, img_start=0):
    layout = block.get("layout", "grid")
    layout_class = "org-block--stack" if layout == "stack" else "org-block--grid"
    people = flatten_people(block)
    cards = []
    for i, person in enumerate(people):
        cards.append(render_card(person, (img_start + i) % 4 + 1))

    cards_html = "\n".join(cards)
    return f'''        <section class="org-block {layout_class}">
          <header class="org-block__header">
            <div class="org-block__title-box">
              <h3 class="org-block__title">{block["title"]}</h3>
            </div>
          </header>
          <div class="org-block__cards">
{cards_html}
          </div>
        </section>'''


lines = ['      <div class="org-chart">']
img_counter = 0
for block in ORG_BLOCKS:
    people_count = len(flatten_people(block))
    lines.append(render_block(block, img_counter))
    img_counter += people_count
lines.append("      </div>")

Path(r"d:\swat-lvpd\data\personnel-section.html").write_text("\n".join(lines), encoding="utf-8")
print("OK blocks:", len(ORG_BLOCKS))
