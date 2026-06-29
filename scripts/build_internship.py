# -*- coding: utf-8 -*-
"""Generate internship section HTML with full spreadsheet columns."""
import csv
from pathlib import Path

CSV_PATH = Path(r"d:\swat-lvpd\data\personnel.csv")
OUT_PATH = Path(r"d:\swat-lvpd\data\internship-section.html")

# Column indices in personnel.csv (0-based)
COL_NUM = 1
COL_NAME = 2
COL_RANK = 3
COL_CALLSIGN = 4
COL_FILE = 5
COL_ROLE = 6
COL_WARN_SQUAD = 7
COL_WARN = 8
COL_PREDS = 9
COL_UP = 10
COL_LAST_PROMO = 11
COL_NEXT_PROMO = 12
COL_CLEARANCE = 13
COL_RECRUIT_DATE = 14
COL_ATTENDANCE = 15
COL_DAY_START = 16
COL_DAY_END = 22
COL_WEEK_SUM = 23
COL_TOTAL = 24
COL_APPOINTMENT = 25
COL_NOTE = 26

DAY_HEADERS = ["29.06", "30.06", "01.07", "02.07", "03.07", "04.07", "05.07"]

EXTRA_HEADERS = {
    COL_WEEK_SUM: "За неделю",
    COL_TOTAL: "Всего",
}


def cell(row, index, default="—"):
    if index >= len(row):
        return default
    value = (row[index] or "").strip()
    return value if value else default


def is_recruit(row):
    role = cell(row, COL_ROLE, "")
    if role == "—":
        return False
    return "recruit" in role.lower() or "стаж" in role.lower()


def header_label(header_row, index):
    if index in EXTRA_HEADERS:
        return EXTRA_HEADERS[index]
    if COL_DAY_START <= index <= COL_DAY_END:
        return DAY_HEADERS[index - COL_DAY_START]
    if index == COL_APPOINTMENT:
        return cell(header_row, 24, "Дата назначения на должность")
    if index == COL_NOTE:
        return cell(header_row, 25, "Примечание")
    label = cell(header_row, index, "")
    if index == COL_NUM and "STAFF" in label.upper():
        return "№"
    return label if label != "—" else ""


def clearance_cell(value):
    lower = value.lower()
    if "не допущен" in lower:
        return f'<td class="internship-clearance internship-clearance--denied">{value}</td>'
    if "усмотрение" in lower:
        return f'<td class="internship-clearance internship-clearance--review">{value}</td>'
    return f"<td>{value}</td>"


def render_row(row):
    if not is_recruit(row):
        return ""

    cells = [
        f"<td>{cell(row, COL_NUM)}</td>",
        f"<td>{cell(row, COL_NAME)}</td>",
        f"<td>{cell(row, COL_RANK)}</td>",
        f"<td>{cell(row, COL_CALLSIGN)}</td>",
        f"<td>{cell(row, COL_FILE)}</td>",
        f"<td>{cell(row, COL_ROLE)}</td>",
        f"<td>{cell(row, COL_WARN_SQUAD)}</td>",
        f"<td>{cell(row, COL_WARN)}</td>",
        f"<td>{cell(row, COL_PREDS)}</td>",
        f"<td>{cell(row, COL_UP)}</td>",
        f"<td>{cell(row, COL_LAST_PROMO)}</td>",
        f"<td>{cell(row, COL_NEXT_PROMO)}</td>",
        clearance_cell(cell(row, COL_CLEARANCE)),
        f"<td>{cell(row, COL_RECRUIT_DATE)}</td>",
        f"<td>{cell(row, COL_ATTENDANCE)}</td>",
    ]

    for index in range(COL_DAY_START, COL_DAY_END + 1):
        cells.append(f"<td>{cell(row, index)}</td>")

    cells.extend(
        [
            f"<td>{cell(row, COL_WEEK_SUM)}</td>",
            f"<td>{cell(row, COL_TOTAL)}</td>",
            f"<td>{cell(row, COL_APPOINTMENT)}</td>",
            f'<td class="internship-note">{cell(row, COL_NOTE)}</td>',
        ]
    )

    return "            <tr>\n              " + "\n              ".join(cells) + "\n            </tr>"


def load_legend(rows):
    items = []
    for row in rows[17:]:
        text = cell(row, 18, "")
        if text == "—" or not any(ch.isalpha() for ch in text):
            continue
        items.append(text)
    return items


EXAM_PROGRAM = [
    {
        "tag": "10/66",
        "title": "Остановка повышенного риска",
        "time": "Время не ограничено",
        "task": "Проведение процесса по траффик-стопу 10-66 и задержание ООП.",
        "allowed": [
            "Разрешено ознакомиться с информацией (регламент → полезные ссылки → 10-66)",
            "Разрешается консультация от экзаменатора перед сдачей экзамена",
        ],
        "criteria": [
            ("fail", "Запрещается биндерство", "Пересдача (при 2-м использовании биндера — недопуск)"),
            ("review", "Нелогичные или неправильные действия", "Решение комиссии"),
            ("fail", "Если ничего не сделали", "Пересдача"),
        ],
    },
    {
        "tag": "ДС",
        "title": "Координация",
        "time": "Время не ограничено",
        "task": "Преследование экзаменатора на патрульном крузере Dodge (PS3 + ECG).",
        "subsections": [
            {
                "title": "Наземная координация",
                "desc": "Тренер берёт на себя роль преступника, используя транспорт. Экзаменуемый преследует автомобиль нарушителя, координируя действия и сообщая о положении цели.",
                "tasks": [
                    "Координация движения преследуемого Т/C (местонахождение, скорость, направление)",
                    "Уверенное управление автомобилем при манёврах и в условиях ограниченного пространства",
                ],
            },
            {
                "title": "Воздушная координация",
                "desc": "Преследование вражеского вертолёта. Передача данных о положении цели и своём местоположении.",
                "tasks": [
                    "Сохранять контроль над вертолётом",
                    "Координировать действия с учётом направления, высоты и окружающих ориентиров",
                    "Умение точно описывать ситуацию и местоположение",
                ],
            },
        ],
    },
    {
        "tag": "БП",
        "title": "Боевая подготовка",
        "stages": [
            {
                "title": "I этап — Теория",
                "time": "2 минуты на ответ",
                "task": "3 вопроса по тактике владения оружием (из оружейки LVPD).",
                "criteria": [
                    ("pass", "3 правильных ответа", "Сдача"),
                    ("review", "2 правильных ответа", "Решение комиссии"),
                    ("fail", "1 правильный ответ", "Пересдача"),
                ],
            },
            {
                "title": "II этап — Дуэли",
                "time": "Время не ограничено",
                "task": "Дуэль с 2-мя экзаменаторами в секторе B-7 LVPD до 2 побед. Формат 1×2. Экзаменаторы без бронежилетов. Экзаменуемому не допускается надевать маску (нарушение — −1 балл).",
                "criteria": [
                    ("pass", "2 победы", "Сдача"),
                    ("review", "Ничья", "Решение комиссии"),
                    ("fail", "0 побед", "Пересдача"),
                ],
            },
            {
                "title": "III этап",
                "time": "Время не ограничено",
                "task": "Дуэль с экзаменатором в секторе G-11 до 2 побед. Формат 1×1.",
                "criteria": [
                    ("pass", "Победа", "Сдача"),
                    ("review", "Ничья", "Решение комиссии"),
                    ("fail", "Поражение", "Пересдача"),
                ],
            },
        ],
    },
    {
        "tag": "ТЕОР",
        "title": "Теория",
        "time": "1 минута на ответ",
        "task": "Правильно ответить на вопросы по категориям: общие правила полиции, регламент SWAT, процессуальный кодекс.",
        "details": [
            "На каждую категорию — по 2 вопроса",
            "Итоговая оценка зависит от правильности ответов",
            "При неправильном ответе задаётся дополнительный вопрос",
            "Опоздание / неправильный ответ — экзаменатор суммирует",
        ],
    },
    {
        "tag": "ПМП",
        "title": "Первая медицинская помощь",
        "time": "Время не ограничено",
        "task": "Оказать первую медицинскую помощь условно раненому экзаменатору.",
        "allowed": [
            "Разрешено ознакомиться с информацией (регламент → полезные ссылки → ПМП/Разм)",
            "Разрешается консультация от экзаменатора перед сдачей экзамена",
        ],
        "criteria": [
            ("fail", "Запрещается биндерство", "Пересдача"),
            ("review", "Нелогичные или неправильные действия", "Решение комиссии"),
            ("fail", "Если ничего не сделали", "Пересдача"),
        ],
    },
    {
        "tag": "EOD",
        "title": "Разминирование",
        "time": "5 минут",
        "task": "Обезвредить взрывное устройство указанного типа. Тип устройства определяет экзаменатор.",
        "allowed": ["Разрешается консультация от экзаменатора перед сдачей экзамена"],
        "bans": ["Запрещается биндерство"],
        "criteria": [
            ("fail", "Запрещается биндерство", "Пересдача"),
            ("review", "Нелогичные или неправильные действия", "Решение комиссии (на пересдачу)"),
            ("fail", "Если ничего не сделали", "Пересдача"),
        ],
    },
    {
        "tag": "FINAL",
        "title": "Итоговая аттестация",
        "time": "Выезд — 7 мин · Оцепление — 5 мин",
        "task": "Своевременная реакция на вызов диспетчера 9-1-1. Экзаменатор выбирает сценарий (например, ограбление МО). Стажёр должен быстро отреагировать, собрать департамент на месте, оцепить территорию и при необходимости произвести штурм здания.",
        "details": [
            "Время на выезд до точки вызова — 7 минут",
            "Время на оцепление территории — 5 минут",
        ],
    },
]


def render_criteria(criteria):
    if not criteria:
        return ""
    items = "".join(
        f'              <li class="exam-criteria__item exam-criteria__item--{kind}">'
        f"<span>{label}</span><strong>{result}</strong></li>\n"
        for kind, label, result in criteria
    )
    return f"""            <ul class="exam-criteria">
{items}            </ul>"""


def render_list(items, css_class="exam-list"):
    if not items:
        return ""
    lines = "".join(f"              <li>{item}</li>\n" for item in items)
    return f"""            <ul class="{css_class}">
{lines}            </ul>"""


def render_subsections(subsections):
    blocks = []
    for sub in subsections:
        tasks = render_list(sub.get("tasks", []))
        blocks.append(
            f"""          <div class="exam-sub">
            <h5 class="exam-sub__title">{sub["title"]}</h5>
            <p class="exam-sub__desc">{sub["desc"]}</p>
{tasks}          </div>"""
        )
    return "\n".join(blocks)


def render_stages(stages):
    blocks = []
    for stage in stages:
        criteria = render_criteria(stage.get("criteria"))
        blocks.append(
            f"""          <div class="exam-stage">
            <h5 class="exam-stage__title">{stage["title"]}</h5>
            <p class="exam-stage__time">{stage.get("time", "")}</p>
            <p class="exam-block__task">{stage["task"]}</p>
{criteria}          </div>"""
        )
    return "\n".join(blocks)


def render_exam(exam, index):
    tag = exam.get("tag", f"{index:02d}")
    time_html = f'<p class="exam-block__time">{exam["time"]}</p>' if exam.get("time") else ""
    task_html = (
        f'<p class="exam-block__task"><strong>Задача:</strong> {exam["task"]}</p>'
        if exam.get("task")
        else ""
    )
    allowed = render_list(exam.get("allowed", []), "exam-list exam-list--allowed")
    details = render_list(exam.get("details", []))
    bans = render_list(exam.get("bans", []), "exam-list exam-list--ban")
    criteria = render_criteria(exam.get("criteria"))
    subsections = render_subsections(exam.get("subsections", []))
    stages = render_stages(exam.get("stages", []))

    extra = "\n".join(filter(None, [subsections, stages, allowed, details, bans, criteria]))

    return f"""        <article class="exam-block">
          <header class="exam-block__header">
            <span class="exam-block__tag">{tag}</span>
            <h4 class="exam-block__title">{exam["title"]}</h4>
          </header>
          {time_html}
          {task_html}
{extra}        </article>"""


def render_exam_program():
    blocks = [render_exam(exam, i + 1) for i, exam in enumerate(EXAM_PROGRAM)]
    return f"""        <div class="internship-program">
          <h3 class="internship-program__title">Программа экзаменов и аттестации</h3>
          <p class="internship-program__desc">Требования к сдаче стажировки SWAT LVPD</p>
{chr(10).join(blocks)}
          <div class="internship-program__note">
            <strong>Примечание:</strong> окончательный результат суммируется с учётом решения комиссии.
          </div>
        </div>"""


def main():
    rows = list(csv.reader(CSV_PATH.open(encoding="utf-8")))
    header_row = rows[0]

    columns = list(range(COL_NUM, COL_NOTE + 1))
    header_cells = "".join(
        f"<th>{header_label(header_row, index)}</th>" for index in columns
    )

    body_rows = []
    for row in rows[2:]:
        rendered = render_row(row)
        if rendered:
            body_rows.append(rendered)
    legend_items = load_legend(rows)
    legend_html = "".join(f"<li>{item}</li>" for item in legend_items)
    program_html = render_exam_program()

    html = f"""      <div class="internship-content">
        <p class="internship-source">Источник: таблица личного состава SWAT — строки со статусом <strong>Recruit of SWAT</strong></p>
        <div class="table-wrap">
          <table class="data-table data-table--internship">
            <thead>
              <tr>
                {header_cells}
              </tr>
            </thead>
            <tbody>
{chr(10).join(body_rows)}
            </tbody>
          </table>
        </div>
        <div class="internship-legend">
          <h3 class="internship-legend__title">Обозначения посещаемости</h3>
          <ul class="internship-legend__list">
            {legend_html}
          </ul>
        </div>
{program_html}
      </div>"""

    OUT_PATH.write_text(html, encoding="utf-8")
    print("OK rows:", len(body_rows), "cols:", len(columns))


if __name__ == "__main__":
    main()
