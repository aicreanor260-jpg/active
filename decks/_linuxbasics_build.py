# -*- coding: utf-8 -*-
# Сборка decks/linux-basics.html — «Linux: дистрибутивы и работа в терминале»
# Один самодостаточный HTML: без сборщиков, CDN, внешних шрифтов и картинок.
import json, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "linux-basics.html"
TODO = "<!-- TODO: текст из методички -->"

# ---------------------------------------------------------------- разметка
def head(lbl, w, o, sub=""):
    return (f'<header class="sh"><div class="lbl">{lbl}</div>'
            f'<h2>{w} <span class="o">{o}</span></h2>'
            + (f'<p class="sub">{sub}</p>' if sub else "") + '</header>')

def st(n):
    return f' data-step="{n}"' if n else ""

def card(title, body, num="", tag="", logo="", cls="", step=None, big=False):
    h = ""
    if logo or num or title:
        h = '<div class="chead">'
        if logo:
            h += f'<span class="logo">{logo}</span>'
        if num:
            h += f'<span class="{"nbig" if big else "nbox"}">{num}</span>'
        if title:
            h += f'<span class="t">{title}</span>'
        h += '</div>'
    return (f'<article class="card {cls}"{st(step)}>{h}'
            f'<div class="cbody">{body}</div>{tag}</article>')

def tag(icon, text):
    return f'<span class="tag">{ICON[icon]}<span>{text}</span></span>'

def info(text, cls="", step=None, mark="i"):
    ic = '<span class="ic q">&laquo;</span>' if mark == "q" else '<span class="ic">i</span>'
    return f'<div class="info {cls}"{st(step)}>{ic}<p>{text}</p></div>'

def syn(rows, step=None):
    body = "".join(f'<div class="row"><span class="k">{k}</span><span class="v mono">{v}</span></div>'
                   for k, v in rows)
    return f'<div class="syn"{st(step)}>{body}</div>'

def steps(items, step=None):
    li = "".join(f'<li><span class="circ">{i + 1}</span><div>{t}</div></li>' for i, t in enumerate(items))
    return f'<ul class="steps"{st(step)}>{li}</ul>'

def cmd_html(cmd):
    """Имя команды — основным оранжевым, флаги и аргументы — второй ступенью."""
    parts = cmd.split(" ", 1)
    out = f'<span class="c1">{parts[0]}</span>'
    if len(parts) > 1:
        out += f' <span class="c2">{parts[1]}</span>'
    return out

def T(cmd, out=None, path="~"):
    return {"cmd": cmd, "out": out, "path": path}

def term(items, name="kali@kali: ~", cls="", step=None):
    body = ""
    for it in items:
        body += ('<div class="tline" data-cmd="1"><span class="pmt">kali@kali<span class="tdim">:</span>'
                 f'<span class="pp">{it["path"]}</span><span class="tdim">$</span></span> '
                 f'<span class="tcmd">{cmd_html(it["cmd"])}</span><span class="cur off"></span></div>')
        if it["out"] is not None:
            body += f'<div class="tout" hidden>{it["out"]}</div>'
    return (f'<div class="term" data-term{st(step)}>'
            f'<div class="tbar"><i class="r"></i><i class="y"></i><i class="g"></i>'
            f'<span class="tname">{name}</span></div>'
            f'<div class="tbody">{body}</div></div>')

def lsc(items, rows=2):
    """Вывод ls колонками: (имя, каталог?, доп.класс)"""
    cells = ""
    for it in items:
        n, d = it[0], it[1]
        extra = it[2] if len(it) > 2 else ""
        attrs = it[3] if len(it) > 3 else ""
        cls = " ".join(x for x in (("dir" if d else ""), extra) if x)
        tag_attr = ' class="' + cls + '"' if cls else ""
        if attrs:
            tag_attr += " " + attrs
        cells += "<span" + tag_attr + ">" + n + "</span>"
    return f'<span class="lsc" style="--rows:{rows}">{cells}</span>'

# ---------------------------------------------------------------- иконки и знаки
def _svg(body, vb="0 0 24 24"):
    return f'<svg viewBox="{vb}" aria-hidden="true">{body}</svg>'

ICON = {
    "user": _svg('<circle cx="12" cy="8" r="3.4"/><path d="M5 20c0-3.6 3.1-5.6 7-5.6s7 2 7 5.6"/>'),
    "server": _svg('<rect x="3.5" y="4.5" width="17" height="6" rx="2"/><rect x="3.5" y="13.5" width="17" height="6" rx="2"/>'
                   '<path d="M7 7.5h.01M7 16.5h.01"/>'),
    "chip": _svg('<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3.5v3M14 3.5v3M10 17.5v3M14 17.5v3'
                 'M3.5 10h3M3.5 14h3M17.5 10h3M17.5 14h3"/>'),
    "shield": _svg('<path d="M12 3.5l7 2.6v5.4c0 4.2-2.9 7.6-7 9-4.1-1.4-7-4.8-7-9V6.1z"/>'),
    "rocket": _svg('<path d="M12 3.5c3.2 2 5 5.4 5 9l-2.4 2.4H9.4L7 12.5c0-3.6 1.8-7 5-9z"/>'
                   '<path d="M9.4 15l-2.2 4 3-1.2M14.6 15l2.2 4-3-1.2"/>'),
    "desk": _svg('<rect x="3.5" y="5" width="17" height="11" rx="2"/><path d="M9 20h6M12 16v4"/>'),
    "code": _svg('<path d="M9 8l-4.5 4L9 16M15 8l4.5 4L15 16"/>'),
    "book": _svg('<path d="M4.5 5.5h6a2.5 2.5 0 0 1 2.5 2.5v11a2 2 0 0 0-2-2h-6.5z"/>'
                 '<path d="M19.5 5.5h-6A2.5 2.5 0 0 0 11 8v11a2 2 0 0 1 2-2h6.5z"/>'),
}

# Условные знаки вместо логотипов дистрибутивов.
# TODO: заменить на логотипы из методички, когда будут переданы исходники.
MARK = {
    "ubuntu": _svg('<circle cx="12" cy="12" r="8.2"/><circle cx="12" cy="4.6" r="1.6"/>'
                   '<circle cx="5.6" cy="15.8" r="1.6"/><circle cx="18.4" cy="15.8" r="1.6"/>'),
    "debian": _svg('<path d="M15.6 5.2a8 8 0 1 0 3.1 7.6"/><circle cx="12" cy="12" r="3.6"/>'),
    "kali": _svg('<path d="M4.5 4.5l7 7.5-7 7.5"/><path d="M12.5 19.5h7"/>'),
    "mx": _svg('<path d="M4.5 19V7l4.3 6 4.3-6v12"/><path d="M15.5 9l4 6M19.5 9l-4 6"/>'),
    "manjaro": _svg('<path d="M4.5 19.5V5l5 5v9.5"/><path d="M12 19.5V5l7.5 6v8.5"/>'),
    "mint": _svg('<rect x="4.5" y="6.5" width="15" height="11" rx="2.5"/>'
                 '<path d="M8.5 14.5v-4l2 2.4 2-2.4 2 2.4 2-2.4v4"/>'),
    "solus": _svg('<circle cx="12" cy="12" r="4.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>'),
    "fedora": _svg('<circle cx="12" cy="12" r="8.2"/><path d="M15 8.5h-2.6A2.4 2.4 0 0 0 10 11v5.5"/><path d="M8 12.6h4"/>'),
    "suse": _svg('<path d="M3.5 12.5c3-3.5 6.5-5 9.5-5s6 1.5 7.5 5c-2 3-4.5 4.5-7.5 4.5s-6.5-1.5-9.5-4.5z"/>'
                 '<circle cx="15.5" cy="12" r="1.3"/>'),
    "deepin": _svg('<circle cx="12" cy="12" r="8.2"/><path d="M12 6.2A5.8 5.8 0 0 1 12 17.8"/>'),
}

_RC = [0]

def raccoon(cls="mascot"):
    """Енот — талисман лекции. Рисуется вектором, внешних файлов не требует."""
    _RC[0] += 1
    cid = f"rtail{_RC[0]}"
    return (
        f'<svg class="{cls}" viewBox="0 0 200 250" aria-hidden="true">'
        f'<defs><clipPath id="{cid}">'
        '<path d="M138 206C180 202 196 156 184 122c-8-24-36-30-44-10-7 18 12 28 16 46 4 20-10 34-26 36z"/>'
        '</clipPath></defs>'
        # хвост
        '<path d="M138 206C180 202 196 156 184 122c-8-24-36-30-44-10-7 18 12 28 16 46 4 20-10 34-26 36z"'
        ' fill="#8c8279"/>'
        f'<g clip-path="url(#{cid})" fill="#2e2a27">'
        '<rect x="118" y="104" width="96" height="15" transform="rotate(-16 166 112)"/>'
        '<rect x="118" y="136" width="96" height="15" transform="rotate(-10 166 144)"/>'
        '<rect x="112" y="170" width="96" height="15" transform="rotate(-2 160 178)"/>'
        '</g>'
        # тело
        '<ellipse cx="100" cy="180" rx="54" ry="52" fill="#8c8279"/>'
        '<ellipse cx="100" cy="188" rx="35" ry="38" fill="#cfc7bd"/>'
        # лапы
        '<ellipse cx="72" cy="222" rx="17" ry="11" fill="#2e2a27"/>'
        '<ellipse cx="128" cy="222" rx="17" ry="11" fill="#2e2a27"/>'
        '<ellipse cx="56" cy="180" rx="13" ry="20" fill="#6f665e" transform="rotate(14 56 180)"/>'
        '<ellipse cx="144" cy="180" rx="13" ry="20" fill="#6f665e" transform="rotate(-14 144 180)"/>'
        # уши
        '<path d="M48 56 40 14 80 34z" fill="#8c8279"/><path d="M52 52 47 25 72 37z" fill="#c9713a"/>'
        '<path d="M152 56 160 14 120 34z" fill="#8c8279"/><path d="M148 52 153 25 128 37z" fill="#c9713a"/>'
        # голова
        '<ellipse cx="100" cy="86" rx="58" ry="50" fill="#968c83"/>'
        # светлая полоса на лбу
        '<path d="M100 38c9 17 9 35 0 56-9-21-9-39 0-56z" fill="#efe9e1"/>'
        # маска
        '<path d="M62 70c16-9 34-1 30 18-4 17-26 19-34 7-6-10-4-21 4-25z" fill="#2e2a27"/>'
        '<path d="M138 70c-16-9-34-1-30 18 4 17 26 19 34 7 6-10 4-21-4-25z" fill="#2e2a27"/>'
        # глаза
        '<ellipse cx="77" cy="84" rx="10" ry="11" fill="#efe9e1"/>'
        '<ellipse cx="123" cy="84" rx="10" ry="11" fill="#efe9e1"/>'
        '<circle cx="79" cy="85" r="5.5" fill="#1a1715"/><circle cx="121" cy="85" r="5.5" fill="#1a1715"/>'
        '<circle cx="81" cy="82.5" r="1.8" fill="#fff"/><circle cx="123" cy="82.5" r="1.8" fill="#fff"/>'
        # морда
        '<ellipse cx="100" cy="110" rx="27" ry="21" fill="#efe9e1"/>'
        '<path d="M100 100c7 0 11 4 11 8s-5 7-11 7-11-3-11-7 4-8 11-8z" fill="#2e2a27"/>'
        '<path d="M100 115v7" stroke="#2e2a27" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M100 122c-4 5-11 4-13-1M100 122c4 5 11 4 13-1" fill="none" stroke="#2e2a27"'
        ' stroke-width="2.4" stroke-linecap="round"/>'
        '</svg>')

_RC = [0]

def raccoon(cls="mascot"):
    """Енот — талисман лекции. Рисуется вектором, внешних файлов не требует."""
    _RC[0] += 1
    cid = f"rtail{_RC[0]}"
    return (
        f'<svg class="{cls}" viewBox="0 0 200 250" aria-hidden="true">'
        f'<defs><clipPath id="{cid}">'
        '<path d="M138 206C180 202 196 156 184 122c-8-24-36-30-44-10-7 18 12 28 16 46 4 20-10 34-26 36z"/>'
        '</clipPath></defs>'
        '<path d="M138 206C180 202 196 156 184 122c-8-24-36-30-44-10-7 18 12 28 16 46 4 20-10 34-26 36z"'
        ' fill="#8c8279"/>'
        f'<g clip-path="url(#{cid})" fill="#2e2a27">'
        '<rect x="118" y="104" width="96" height="15" transform="rotate(-16 166 112)"/>'
        '<rect x="118" y="136" width="96" height="15" transform="rotate(-10 166 144)"/>'
        '<rect x="112" y="170" width="96" height="15" transform="rotate(-2 160 178)"/>'
        '</g>'
        '<ellipse cx="100" cy="180" rx="54" ry="52" fill="#8c8279"/>'
        '<ellipse cx="100" cy="188" rx="35" ry="38" fill="#cfc7bd"/>'
        '<ellipse cx="72" cy="222" rx="17" ry="11" fill="#2e2a27"/>'
        '<ellipse cx="128" cy="222" rx="17" ry="11" fill="#2e2a27"/>'
        '<ellipse cx="56" cy="180" rx="13" ry="20" fill="#6f665e" transform="rotate(14 56 180)"/>'
        '<ellipse cx="144" cy="180" rx="13" ry="20" fill="#6f665e" transform="rotate(-14 144 180)"/>'
        '<path d="M48 56 40 14 80 34z" fill="#8c8279"/><path d="M52 52 47 25 72 37z" fill="#c9713a"/>'
        '<path d="M152 56 160 14 120 34z" fill="#8c8279"/><path d="M148 52 153 25 128 37z" fill="#c9713a"/>'
        '<ellipse cx="100" cy="86" rx="58" ry="50" fill="#968c83"/>'
        '<path d="M100 38c9 17 9 35 0 56-9-21-9-39 0-56z" fill="#efe9e1"/>'
        '<path d="M62 70c16-9 34-1 30 18-4 17-26 19-34 7-6-10-4-21 4-25z" fill="#2e2a27"/>'
        '<path d="M138 70c-16-9-34-1-30 18 4 17 26 19 34 7 6-10 4-21-4-25z" fill="#2e2a27"/>'
        '<ellipse cx="77" cy="84" rx="10" ry="11" fill="#efe9e1"/>'
        '<ellipse cx="123" cy="84" rx="10" ry="11" fill="#efe9e1"/>'
        '<circle cx="79" cy="85" r="5.5" fill="#1a1715"/><circle cx="121" cy="85" r="5.5" fill="#1a1715"/>'
        '<circle cx="81" cy="82.5" r="1.8" fill="#fff"/><circle cx="123" cy="82.5" r="1.8" fill="#fff"/>'
        '<ellipse cx="100" cy="110" rx="27" ry="21" fill="#efe9e1"/>'
        '<path d="M100 100c7 0 11 4 11 8s-5 7-11 7-11-3-11-7 4-8 11-8z" fill="#2e2a27"/>'
        '<path d="M100 115v7" stroke="#2e2a27" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M100 122c-4 5-11 4-13-1M100 122c4 5 11 4 13-1" fill="none" stroke="#2e2a27"'
        ' stroke-width="2.4" stroke-linecap="round"/>'
        '</svg>')

# ---------------------------------------------------------------- слайды
S = []

def slide(label, body, cls=""):
    S.append((label, body, cls))


# ---------------------------------------------------------------- доп. помощники

def table(rows, head, mono=0, start=1):
    """Таблица; каждая строка открывается отдельным шагом."""
    r = ""
    for i, row in enumerate(rows):
        cells = ""
        for k, c in enumerate(row):
            if k == 0:
                cells += f'<th>{c}</th>'
            else:
                cells += f'<td class="{"mono o" if k == mono else ""}">{c}</td>'
        step = f' data-step="{start + i}"' if start else ""
        r += f'<tr{step}>{cells}</tr>'
    h = "".join(f'<th>{c}</th>' for c in head)
    return f'<div class="tbw card flat"><table class="tbl"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
def numrow(items, start=1, cols="g3"):
    """Ряд карточек с крупным номером и заголовком-командой."""
    out = ""
    for i, (num, title, body) in enumerate(items):
        out += card(title, body, num=num, step=start + i, big=True)
    return f'<div class="{cols}">{out}</div>'

def dirtable(rows, start=1):
    r = ""
    for i, (path, name, desc) in enumerate(rows):
        r += (f'<tr data-step="{start + i}"><th class="mono o">{path}</th>'
              f'<td><b>{name}</b></td><td>{desc}</td></tr>')
    return ('<div class="tbw card flat"><table class="tbl dirs"><thead><tr><th>Каталог</th>'
            f'<th>Назначение</th><th>Что внутри</th></tr></thead><tbody>{r}</tbody></table></div>')

def steplist(items, start=1):
    """Нумерованные шаги в кружках, как на референсе: заголовок + пояснение."""
    li = ""
    for i, (t, d) in enumerate(items):
        li += (f'<li data-step="{start + i}"><span class="circ">{i + 1}</span>'
               f'<div><b>{t}</b><br>{d}</div></li>')
    return f'<ul class="steps">{li}</ul>'

# ---- 01 --------------------------------------------------------------------
slide("Титул", """
<div class="tslide">
  <div class="lbl">Linux</div>
  <h1>Дистрибутивы <span class="o">Linux</span></h1>
  <p class="tsub">Одна идея — разные возможности</p>
  <div class="card" style="margin-top:1.8rem;max-width:52rem">
    <div class="cbody">
      <b>Дистрибутив Linux</b> — это полноценная операционная система, созданная на основе ядра Linux,
      а также системных инструментов, библиотек и приложений. Разные дистрибутивы предназначены
      для разных задач: от обычной работы на компьютере до серверов, кибербезопасности и разработки.
    </div>
  </div>
  <div class="tmeta">
    <span class="tchip">10 дистрибутивов</span>
    <span class="tchip">файловая система</span>
    <span class="tchip">команды терминала</span>
    <span class="tchip">права доступа</span>
  </div>
</div>""" + raccoon(), "tslide")

# ---- 02 --------------------------------------------------------------------
slide("Применение Linux",
      head("Linux", "Применение", "Linux", "Одна система — множество возможностей")
      + f"""
<p class="p dim" style="margin-bottom:1.2rem">Операционная система Linux широко используется в различных сферах
благодаря своей гибкости, высокому уровню безопасности и открытому исходному коду.</p>
<div class="g4">
  {card("Серверы и хостинг", "Обеспечивает высокую стабильность и безопасность веб-серверов, "
        "облачных платформ и центров обработки данных.", num="01", step=1)}
  {card("Разработка", "Предоставляет полезные инструменты и среды для написания кода, "
        "тестирования и отладки приложений.", num="02", step=2)}
  {card("Настольные компьютеры", "Предлагает безопасные и настраиваемые среды "
        "для повседневных вычислительных задач.", num="03", step=3)}
  {card("Кибербезопасность", "Широко используется для этичного хакинга, тестирования "
        "на проникновение и анализа безопасности.", num="04", step=4)}
  {card("Встраиваемые системы", "Эффективно работает на устройствах Интернета вещей, "
        "маршрутизаторах и других системах с ограниченными ресурсами.", num="05", step=5)}
  {card("Суперкомпьютеры", "Используются в большинстве суперкомпьютеров для научных вычислений "
        "и крупномасштабного моделирования.", num="06", step=6)}
  {card("Образование", "Помогает студентам изучать программирование, сетевые технологии "
        "и системное администрирование с минимальными затратами.", num="07", step=7)}
  {info("Открытый исходный код — больше возможностей: систему можно изучать, "
        "изменять и распространять свободно.", step=8)}
</div>""")

# ---- 03 --------------------------------------------------------------------
D1 = [
    ("01", "ubuntu", "Ubuntu", "Удобный для новичков дистрибутив. Подходит для настольных компьютеров, "
                               "серверов и облачных вычислений.", "user", "Для новичков"),
    ("02", "debian", "Debian", "Стабильный и надёжный дистрибутив. Широко используется для серверов.",
     "server", "Для серверов"),
    ("03", "kali", "Kali Linux", "Ориентирован на кибербезопасность. Используется для этичного взлома "
                                 "и тестирования на проникновение.", "shield", "Для безопасности"),
    ("04", "mx", "MX Linux", "Легковесный дистрибутив. Подходит для старого оборудования.",
     "chip", "Для слабых ПК"),
    ("05", "manjaro", "Manjaro", "Удобный дистрибутив на основе Arch с непрерывными обновлениями.",
     "rocket", "Для продвинутых пользователей"),
]
D2 = [
    ("06", "mint", "Linux Mint", "Простой и удобный дистрибутив для тех, кто переходит с Windows.",
     "user", "Для начинающих"),
    ("07", "solus", "Solus", "Современный дистрибутив, ориентированный на производительность "
                             "и простоту работы на настольных компьютерах.", "desk", "Для повседневного использования"),
    ("08", "fedora", "Fedora", "Ориентирован на разработчиков. Использует новейшие технологии.",
     "code", "Для разработчиков"),
    ("09", "suse", "openSUSE", "Мощный дистрибутив. Используется для разработки и корпоративных сред.",
     "server", "Для бизнеса и серверов"),
    ("10", "deepin", "Deepin", "Визуально привлекательный дистрибутив с простым в использовании интерфейсом.",
     "desk", "Красивый и удобный"),
]

def distro_grid(rows, start=1):
    out = ""
    for i, (num, mark, name, desc, ic, tg) in enumerate(rows):
        out += card(name, desc, num=num, logo=MARK[mark], tag=tag(ic, tg), step=start + i)
    return f'<div class="g5">{out}</div>'

slide("Дистрибутивы 01–05",
      head("Linux", "Дистрибутивы", "Linux", "Один Linux — много возможностей. Первая пятёрка: 01—05")
      + distro_grid(D1))

# ---- 04 --------------------------------------------------------------------
slide("Дистрибутивы 06–10",
      head("Linux", "Дистрибутивы", "Linux", "Продолжение списка: 06—10")
      + distro_grid(D2))

# ---- 05 --------------------------------------------------------------------
PICK = [(n, m, t) for (_, m, n, _, _, t) in D1 + D2]
PICK_TAGS = {
    "Ubuntu": "new mid home server mod",
    "Debian": "mid pro server home mod old",
    "Kali Linux": "pro sec mod",
    "MX Linux": "new mid home old mod",
    "Manjaro": "mid pro home mod",
    "Linux Mint": "new mid home old mod",
    "Solus": "new mid home mod",
    "Fedora": "mid pro home server mod",
    "openSUSE": "mid pro server home mod",
    "Deepin": "new home mod",
}

def opts(q, items):
    return "".join(f'<button class="opt" type="button" data-q="{q}" data-v="{v}" aria-pressed="false">{t}</button>'
                   for v, t in items)

slide("Как выбрать дистрибутив",
      head("Linux", "Как выбрать", "дистрибутив", "Ответьте на три вопроса — подходящие варианты останутся яркими")
      + f"""
<div data-hook="pick">
  <div class="card flat" data-step="1">
    <div class="qrow"><span class="qt">Насколько вы знакомы с Linux</span>{opts("exp", [("new", "Впервые вижу"), ("mid", "Уверенный пользователь"), ("pro", "Хочу разобраться глубже")])}</div>
    <div class="qrow"><span class="qt">Для чего нужна система</span>{opts("use", [("home", "Учёба и дом"), ("server", "Сервер"), ("sec", "Кибербезопасность")])}</div>
    <div class="qrow"><span class="qt">Какое оборудование</span>{opts("hw", [("old", "Старый ноутбук"), ("mod", "Современный компьютер")])}</div>
    <div class="hstack" style="margin-top:.4rem;align-items:center">
      <button class="btn preset" type="button">Сбросить ответы</button>
      <span class="presult mono" style="color:var(--orange);font-size:.92rem"></span>
    </div>
  </div>
  <div class="g5" style="margin-top:1rem" data-step="2">
    """ + "".join(
        f'<article class="card mini pick" data-name="{n}" data-tags="{PICK_TAGS[n]}">'
        f'<div class="chead"><span class="logo">{MARK[m]}</span><span class="t">{n}</span></div>'
        f'<div class="cbody">{t}</div></article>' for n, m, t in PICK) + """
  </div>
</div>""")

# ---- 06 --------------------------------------------------------------------
ARCH = [
    ("01", "Приложения (пользователь)", "Это программы, с которыми вы работаете: веб-браузеры, редакторы, IDE и другие. "
                                        "Они используют возможности системы через библиотеки и утилиты."),
    ("02", "Системные утилиты", "Встроенные инструменты для управления, настройки и обслуживания системы. "
                                "Примеры: systemctl, apt, top, ls, grep."),
    ("03", "Оболочка (Shell)", "Интерфейс командной строки, который интерпретирует и выполняет ваши команды. "
                               "Примеры: bash, zsh, sh."),
    ("04", "Системные библиотеки", "Предоставляют стандартные функции, которые помогают приложениям "
                                   "взаимодействовать с ядром. Примеры: glibc, libm, libpthread."),
    ("05", "Ядро Linux", "Основной компонент: управляет аппаратными ресурсами, процессами, памятью, "
                         "устройствами и системными операциями."),
    ("06", "Аппаратный уровень", "Физические компоненты: процессор, оперативная память, хранилище, "
                                 "сетевые и периферийные устройства."),
]

def arch_stack():
    rows = [("Приложения", "браузер, редактор, IDE", "l1"),
            ("Системные утилиты", "systemctl, apt, top, ls, grep", "l2"),
            ("Оболочка (Shell)", "bash, zsh, sh", "l3"),
            ("Системные библиотеки", "glibc, libm, libpthread", "l4"),
            ("Ядро Linux", "процессы, память, устройства, системные вызовы", "l5"),
            ("Аппаратный уровень", "ЦПУ, ОЗУ, хранилище, ввод-вывод", "l6")]
    out = ""
    for i, (n, sub, eid) in enumerate(rows):
        out += (f'<div class="lyr" data-step="{i + 1}"><span class="lyn mono">0{i + 1}</span>'
                f'<span class="lyt">{n}</span><span class="lys mono">{sub}</span></div>')
    return f'<div class="stack">{out}</div>'

slide("Архитектура Linux",
      head("Linux", "Архитектура", "Linux", "Взаимодействие компонентов, которые делают систему стабильной, гибкой и мощной")
      + f"""
<div class="two w">
  {arch_stack()}
  <div class="vstack">
    """ + "".join(card(t, d, num=n, step=i + 1) for i, (n, t, d) in enumerate(ARCH[:3])) + f"""
    {info("Все уровни работают вместе, чтобы обеспечить стабильную и эффективную работу системы. "
          "Запрос программы спускается сверху вниз и возвращается обратно с результатом.", step=4, mark="q")}
  </div>
</div>""")

# ---- 07 --------------------------------------------------------------------
slide("Ядро и библиотеки",
      head("Linux", "Нижние", "уровни", "Библиотеки, ядро и оборудование: что происходит под оболочкой")
      + f"""
<div class="g3">
  """ + "".join(card(t, d, num=n, step=i + 1) for i, (n, t, d) in enumerate(ARCH[3:])) + f"""
</div>
<div class="two w" style="margin-top:1.2rem">
  {term([T("uname", "Linux"),
         T("uname -r", "5.15.0-91-generic"),
         T("uname -m", "x86_64"),
         T("uname -a", "Linux kali 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux")], step=4)}
  <div class="vstack">
    {card("Команда uname", "Команда <b>uname</b> в Linux используется для отображения системной информации. "
          "Показывает сведения об операционной системе и помогает идентифицировать систему.", step=5)}
    {syn([("Синтаксис:", '<span class="cmd">uname</span> <span class="opt">[OPTIONS]</span>'),
          ("Пример:", '<span class="cmd">uname</span> <span class="opt">-a</span>')], step=6)}
  </div>
</div>""")

# ---- 08 --------------------------------------------------------------------
FS3 = [
    ("01", "Логическая файловая система",
     "Выступает в качестве интерфейса между приложениями и файловой системой. Выполняет ключевые операции: "
     "открытие, чтение, запись и закрытие. Обеспечивает проверку безопасности, в том числе разрешений "
     "и контроля доступа к файлам."),
    ("02", "Виртуальная файловая система (VFS)",
     "Предоставляет общий интерфейс для различных файловых систем (ext4, XFS, FAT32, NTFS). Позволяет Linux "
     "использовать несколько типов файловых систем одновременно и скрывает внутренние сложности каждой из них."),
    ("03", "Физическая файловая система",
     "Непосредственно взаимодействует с аппаратным обеспечением и дисковым хранилищем. Управляет блоками данных, "
     "узлами и распределением физической памяти. Отвечает за запись данных на диск и их извлечение."),
]

slide("Файловая система: три уровня",
      head("Linux", "Файловая система", "Linux", "Три уровня, которые обеспечивают работу с файлами: от приложений до диска")
      + f"""
<div class="two w">
  <div class="stack">
    <div class="lyr" data-step="1"><span class="lyn mono">01</span><span class="lyt">Пользовательские приложения</span>
      <span class="lys mono">открыть | читать | записать | закрыть</span></div>
    <div class="lyr" data-step="2"><span class="lyn mono">02</span><span class="lyt">VFS — виртуальная файловая система</span>
      <span class="lys mono">общий интерфейс</span></div>
    <div class="lyr" data-step="3"><span class="lyn mono">03</span><span class="lyt">Конкретные файловые системы</span>
      <span class="lys mono">ext4, XFS, Btrfs, FAT32, NTFS</span></div>
    <div class="lyr" data-step="4"><span class="lyn mono">04</span><span class="lyt">Дисковое хранилище</span>
      <span class="lys mono">блоки, узлы, физическая память</span></div>
  </div>
  <div class="vstack">
    """ + "".join(card(t, d, num=n, step=i + 1) for i, (n, t, d) in enumerate(FS3)) + f"""
    {info("Всё — это файл. Linux делает работу с файлами простой, универсальной и надёжной.", step=4, mark="q")}
  </div>
</div>""", "tight")

# ---- 09 --------------------------------------------------------------------
slide("Характеристики файловой системы",
      head("Linux", "Характеристики", "файловой системы",
           "Файловая система определяет структуру, правила и методы организации, хранения и доступа к данным")
      + f"""
<div class="g3">
  {card("Управление пространством", "Управляет распределением блоков, отслеживанием свободного пространства "
        "и контролем фрагментации для оптимизации эффективности хранения.", num="01", step=1)}
  {card("Имя файла", "Обеспечивает соблюдение правил именования: наборы символов, ограничения по длине "
        "и чувствительность к регистру.", num="02", step=2)}
  {card("Каталог", "Реализует иерархические структуры индексирования для эффективной организации "
        "и поиска файлов.", num="03", step=3)}
  {card("Метаданные", "Хранят атрибуты файлов: владельца, разрешения, временные метки, размер и тип файла.",
        num="04", step=4)}
  {card("Утилиты", "Обеспечивают операции системного уровня для создания, удаления, резервного копирования "
        "и восстановления файлов.", num="05", step=5)}
  {card("Архитектура", "Определяет ограничения и механизмы, которые влияют на масштабируемость, надёжность "
        "и производительность файловой системы.", num="06", step=6)}
</div>
{info("Файловая система — это порядок в мире данных.", step=7, mark="q")}""")

# ---- 10 --------------------------------------------------------------------
FHS = [
    ("/", "Корневой каталог", "Начало всей файловой системы, вершина единого дерева."),
    ("/bin", "Основные пользовательские команды", "Важные исполняемые файлы, необходимые для работы системы: ls, cp, mv."),
    ("/boot", "Файлы загрузчика", "Статические файлы, необходимые для загрузки Linux: ядро, initramfs."),
    ("/dev", "Файлы устройств", "Представляют устройства в виде файлов: диски, USB, терминалы."),
    ("/etc", "Конфигурационные файлы", "Настройки системы и установленных служб."),
    ("/home", "Домашние каталоги пользователей", "Личные файлы и настройки пользователей."),
    ("/lib", "Общие библиотеки", "Файлы библиотек, необходимые для работы программ из /bin и /sbin."),
    ("/media", "Съёмные носители", "Точки монтирования для автоматически подключаемых устройств: USB, CD/DVD."),
    ("/mnt", "Временные точки монтирования", "Используются для ручного монтирования файловых систем."),
    ("/opt", "Дополнительное ПО", "Сторонние приложения, установленные вручную."),
    ("/proc", "Информация о процессах", "Виртуальная файловая система с данными о процессах и состоянии системы."),
    ("/sbin", "Системные команды", "Важные системные утилиты для администрирования: fsck, reboot."),
    ("/srv", "Данные служб", "Файлы, предоставляемые различными службами: веб-сервер, FTP."),
    ("/tmp", "Временные файлы", "Хранение временных данных, обычно очищается при перезагрузке."),
    ("/usr", "Пользовательские утилиты и приложения", "Программы, библиотеки и файлы для работы пользователей."),
    ("/var", "Изменяемые данные", "Журналы, очереди и кеш: например, /var/log с файлами журналов."),
]

slide("Структура файловой системы",
      head("Linux", "Структура", "файловой системы", "Единое дерево каталогов, где каждый раздел имеет своё назначение")
      + dirtable(FHS)
      + info("Понимание структуры файловой системы — ключ к уверенной работе в Linux.", step=17, mark="q"))

# ---- 11 --------------------------------------------------------------------
slide("Каталог /etc",
      head("Linux", "Файлы", "конфигурации", "Каталог /etc определяет поведение системы, доступ пользователей и работу служб")
      + f"""
<div class="g4">
  {card("/etc/passwd", "Содержит информацию об учётных записях пользователей: имена и идентификаторы. "
        "Пароли хранятся в файле shadow.", num="01", step=1)}
  {card("/etc/group", "Хранит информацию о системных группах и членстве в группах.", num="02", step=2)}
  {card("/etc/hosts", "Сопоставляет IP-адреса с соответствующими именами хостов.", num="03", step=3)}
  {card("/etc/fstab", "Содержит сведения о дисководах и их точках монтирования.", num="04", step=4)}
  {card("/etc/crontab", "Планирование автоматического запуска команд или сценариев "
        "через заранее определённые промежутки времени.", num="05", step=5)}
  {card("/etc/resolv.conf", "Хранит конфигурацию DNS, используемую системой.", num="06", step=6)}
  {card("/etc/bashrc, /etc/profile", "Общесистемные настройки и псевдонимы для оболочки Bash, "
        "настройки среды при входе.", num="07", step=7)}
  {card("/etc/init.d", "Содержит сценарии запуска и завершения работы служб.", num="08", step=8)}
</div>
{info("Конфигурационные файлы — это «мозг» вашей системы: небольшие файлы, большие возможности.", step=9, mark="q")}""")

# ---- 12 --------------------------------------------------------------------
PROC_OUT = ('processor\t: 0\n'
            'model name\t: Intel(R) Core(TM)\n'
            'cpu MHz\t\t: 3696.000')
MEM_OUT = ('MemTotal:       16384256 kB\n'
           'MemFree:         2487236 kB\n'
           'Buffers:          430812 kB\n'
           'Cached:          5234120 kB')

DEV_OUT = ("brw-rw---- 1 root disk 8, 0 Oct 10 12:30 /dev/sda\n"
           "crw-rw-rw- 1 root root 1, 3 Oct 10 12:30 /dev/null")
DEV_DEMO = term([T("ls -l /dev/sda /dev/null", DEV_OUT)], step=5)

slide("Каталоги /proc и /dev",
      head("Linux", "Процессы", "и устройства", "Виртуальные файлы, которые ядро создаёт на лету")
      + f"""
<div class="two w">
  <div class="vstack">
    {card("/proc", "Файлы /proc содержат информацию о системе и процессах в реальном времени, "
          "динамически генерируемую ядром Linux.", step=1)}
    {term([T("cat /proc/cpuinfo", PROC_OUT), T("cat /proc/meminfo", MEM_OUT)], step=2)}
    <div class="g2" data-step="3">
      {card("/proc/version", "Содержит информацию о версии Linux.", num="01")}
      {card("/proc/mounts", "Отображает информацию обо всех смонтированных файловых системах.", num="02")}
      {card("/proc/modules", "Список модулей ядра, загруженных в систему.", num="03")}
      {card("/proc/swaps", "Информация об используемом пространстве подкачки.", num="04")}
    </div>
  </div>
  <div class="vstack">
    {card("/dev", "В каталоге /dev представлены файлы устройств, которые позволяют системе "
          "взаимодействовать с аппаратным обеспечением и виртуальными устройствами.", step=4)}
    {DEV_DEMO}
    <div class="g2" data-step="6">
      {card("/dev/sda", "Первый жёсткий диск SATA или IDE.", num="01")}
      {card("/dev/null", "Специальное устройство «пустота»: отбрасывает все данные.", num="02")}
    </div>
    {info("Файлы в /dev не содержат данных, а служат точками доступа к устройствам "
          "и драйверам ядра. Всё в Linux — это файл, даже устройства.", step=7)}
  </div>
</div>""")

# ---- 13 --------------------------------------------------------------------
LAST_OUT = ('user1   pts/0   192.168.1.15   Tue Oct 22 10:15   still logged in\n'
            'user2   pts/1   192.168.1.22   Mon Oct 21 08:42 - 10:10  (01:28)\n'
            'root    pts/0   192.168.1.10   Sun Oct 20 14:33 - 16:45  (02:12)')
MSG_OUT = ('Oct 26 10:15:01 linux systemd[1]: Started Network Manager.\n'
           'Oct 26 10:15:23 linux sshd[1234]: Accepted password for user1\n'
           'Oct 26 10:16:10 linux kernel: usb 1-1: new high-speed USB device\n'
           'Oct 26 10:17:42 linux CRON[5678]: (root) CMD (/usr/bin/apt update)')

slide("Каталоги /usr и журналы",
      head("Linux", "Общие данные", "и журналы", "Каталог /usr для всех пользователей и /var/log с историей системы")
      + f"""
<div class="two w">
  <div class="vstack">
    {card("/usr", "Каталог верхнего уровня, содержащий пользовательские программы, библиотеки, документацию "
          "и общие данные. Предназначен для совместного использования несколькими пользователями системы.", step=1)}
    <div class="g2" data-step="2">
      {card("/usr/bin", "Большинство исполняемых программ и команд пользовательского уровня: ls, cp, grep, vim, python.", num="01")}
      {card("/usr/sbin", "Административные команды суперпользователя: useradd, userdel, shutdown, reboot.", num="02")}
      {card("/usr/lib", "Объектные файлы и разделяемые библиотеки для программ из /usr/bin: libc.so, libm.so.", num="03")}
      {card("/usr/share", "Данные, не зависящие от архитектуры: документация, локали, файлы приложений.", num="04")}
    </div>
  </div>
  <div class="vstack">
    {card("Файлы журналов", "В этих файлах фиксируются важные системные события, логины и история активности "
          "для мониторинга и устранения неполадок.", step=3)}
    {term([T("tail -5 /var/log/messages", MSG_OUT), T("last", LAST_OUT)], step=4)}
    <div class="g2" data-step="5">
      {card("/var/log/messages", "Общая активность системы и глобальные сообщения журнала.", num="01")}
      {card("/var/log/wtmp", "История входов и выходов пользователей, её показывает команда last.", num="02")}
      {card("/var/log/lastlog", "Информация о последнем входе в систему каждого пользователя.", num="03")}
    </div>
    {info("Журналы — память системы, которая помогает делать её стабильнее.", step=6, mark="q")}
  </div>
</div>""", "tight")

# ---- 14 --------------------------------------------------------------------
slide("Терминал",
      head("Terminal", "Зачем нужен", "терминал", "Одна строка вместо десятка щелчков мышью")
      + f"""
<div class="two n">
  <div class="vstack">
    {card("", "Терминал — окно, в котором работает <b>командная оболочка</b>. Она интерпретирует и выполняет "
              "ваши команды, а затем показывает результат. Примеры оболочек: bash, zsh, sh.", step=1)}
    {card("Приглашение командной строки",
          '<div class="mono" style="font-size:1.15rem;margin-bottom:.6rem">'
          '<span style="color:var(--ink)">kali@kali</span><span class="tdim">:</span>'
          '<span class="o">~</span><span class="tdim">$</span></div>'
          '<b>kali</b> — имя пользователя, после <b>@</b> — имя компьютера, '
          'после двоеточия — <b>текущий каталог</b> (<span class="mono o">~</span> означает домашний), '
          'символ <b>$</b> — обычный пользователь, <b>#</b> — суперпользователь root.', step=2)}
  </div>
  <div class="vstack">
    {syn([("Структура:", '<span class="cmd">команда</span> <span class="opt">-флаги</span> <span class="arg">аргументы</span>'),
          ("Пример:", '<span class="cmd">ls</span> <span class="opt">-l</span> <span class="arg">/etc</span>')], step=3)}
    {term([T("whoami", "kali"),
           T("pwd", "/home/kali"),
           T("ls -l /etc/hosts", "-rw-r--r-- 1 root root 221 Oct 10 12:30 hosts")], step=4)}
    {info("Команда — что выполнить, флаги — как именно, аргументы — над чем работать. "
          "Короткие флаги объединяются: <b>-l -h</b> и <b>-lh</b> — одно и то же.", step=5)}
  </div>
</div>""")

# ---- 15 --------------------------------------------------------------------
LS_HOME = lsc([("Desktop", 1), ("Documents", 1), ("Downloads", 1), ("Music", 1),
               ("Pictures", 1), ("Templates", 1), ("Videos", 1), ("bin", 1)], rows=3)
LS_DL = lsc([("archive.zip", 0), ("docs", 1), ("file1.txt", 0),
             ("image.png", 0), ("notes.md", 0), ("project", 1)], rows=2)

slide("pwd, ls, cd",
      head("Terminal", "Основные", "команды", "Работа с файлами и каталогами в Linux")
      + numrow([
          ("01", "pwd", "<b>(вывести рабочий каталог)</b><br>Команда pwd показывает текущее местоположение "
                        "в системе. Она сообщает, в какой папке вы находитесь."),
          ("02", "ls", "<b>(вывести список файлов и каталогов)</b><br>Команда ls используется для вывода списка "
                       "файлов и каталогов в текущем каталоге. Она позволяет получить общее представление "
                       "о содержимом папки."),
          ("03", "cd", "<b>(смена каталога)</b><br>Команда cd используется для перемещения между папками. "
                       "Вы можете указать, в какую именно папку хотите перейти, или использовать ярлыки "
                       "для навигации."),
      ])
      + f"""
<div class="two w" style="margin-top:1.2rem">
  <div class="vstack">
    {term([T("pwd", "/home/kali/Templates"), T("ls", LS_HOME)], step=4)}
    {info("Текущий каталог — <b>/home/kali/Templates</b>. Командой ls отображаются все файлы и папки, "
          "находящиеся в текущей папке.", step=5)}
  </div>
  <div class="vstack">
    {term([T("cd Downloads", None),
           T("pwd", "/home/kali/Downloads", path="~/Downloads"),
           T("ls", LS_DL, path="~/Downloads")], step=6)}
    {steplist([("Перемещение в соседнюю папку",
                "Если вы хотите переместиться в папку, которая находится внутри той, в которой вы уже "
                "находитесь, просто используйте её название."),
               ("Проверка текущего каталога",
                "Используйте команду pwd, чтобы убедиться, что вы находитесь в нужной папке."),
               ("Просмотр обновлённого каталога",
                "Выведите список файлов и каталогов, чтобы увидеть содержимое новой папки.")], start=7)}
  </div>
</div>""")

# ---- 16 --------------------------------------------------------------------
def ndn(name, path, d=True, cls=""):
    return f'<span class="nd {"d" if d else "f"} {cls}" data-p="{path}" tabindex="0">{name}</span>'

slide("Навигация по каталогам",
      head("Terminal", "Навигация", "по каталогам", "Вы можете указать полный путь к папке, как полный адрес")
      + f"""
<div class="two w" data-hook="cwd" data-cwd="/home/kali|/home/kali|/home/kali/Documents|/home/kali/Documents|/home/kali/Documents">
  <div class="vstack">
    {term([T("cd ~", None),
           T("pwd", "/home/kali"),
           T("cd Documents", None, path="~"),
           T("pwd", "/home/kali/Documents", path="~/Documents"),
           T("cd /home/kali/Documents", None, path="~/Documents")], step=1)}
    <div class="card tree" data-step="1">
      <div>{ndn("home", "/home")}</div>
      <div class="lv">
        <div>{ndn("kali", "/home/kali", cls="cwd")}<span class="tdim">  /home/kali</span></div>
        <div class="lv">
          <div>{ndn("Desktop", "/home/kali/Desktop")}<span class="tdim">  /home/kali/Desktop</span></div>
          <div>{ndn("Documents", "/home/kali/Documents")}<span class="tdim">  /home/kali/Documents</span></div>
          <div>{ndn("Downloads", "/home/kali/Downloads")}<span class="tdim">  /home/kali/Downloads</span></div>
        </div>
      </div>
    </div>
  </div>
  <div class="vstack">
    {steplist([("Переход в домашний каталог", "Вернитесь в свой домашний каталог командой cd ~."),
               ("Переход в папку «Документы»", "Перейдите в папку внутри текущего каталога, указав её название."),
               ("Текущий каталог изменён", "Теперь вы находитесь в папке «Документы» — это подтверждает pwd."),
               ("Переход по полному пути", "Вы также можете указать полный путь к папке, как полный адрес.")], start=2)}
    {info("Рамкой в дереве отмечен текущий каталог: он меняется вместе с командой <b>cd</b>. "
          "Абсолютный путь начинается с косой черты и работает откуда угодно, относительный "
          "отсчитывается от текущего каталога.", step=6)}
  </div>
</div>""")

# ---- 17 --------------------------------------------------------------------
COLS = [
    ("-", "Тип файла", "Первый символ указывает тип: «-» обычный файл, «d» каталог."),
    ("rw-r--r--", "Права доступа", "Девять символов показывают права: r — чтение, w — запись, x — выполнение, «-» — нет права."),
    ("1", "Количество ссылок", "Указывает количество жёстких ссылок на файл."),
    ("user", "Владелец файла", "Пользователь, которому принадлежит файл."),
    ("group", "Группа", "Группа, которой принадлежит файл: может иметь особые права доступа."),
    ("46", "Размер файла", "Размер файла в байтах."),
    ("Apr 14 16:37", "Дата и время изменения", "Дата и время последнего изменения файла."),
    ("Narx.txt", "Имя файла", "Имя файла или каталога."),
]

def cols_line():
    out = ""
    for i, (v, _, _) in enumerate(COLS):
        out += f'<span data-col="{i + 3}">{v}</span>' + (" " if i < len(COLS) - 1 else "")
    return out

slide("Команда ls -l",
      head("Terminal", "Команда", "ls -l", "Просмотр подробной информации о файле")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">ls</span> <span class="opt">-l</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">ls</span> <span class="opt">-l</span> <span class="arg">Narx.txt</span>')], step=1)}
    {term([T("ls -l Narx.txt", "-rw-r--r-- 1 user group 46 Apr 14 16:37 Narx.txt")], step=2)}
    <div class="g2" data-step="2">
      {card("ls -l", "Подробная информация о файлах.", num="01")}
      {card("ls -lh", "Размер в удобочитаемом виде: KB, MB, GB.", num="02")}
      {card("ls -la", "Показать скрытые файлы.", num="03")}
      {card("ls -R", "Рекурсивный просмотр каталогов.", num="04")}
    </div>
  </div>
  <div class="card" data-hook="cols">
    <h3 class="mono">Разбор вывода команды</h3>
    <div class="cols">{cols_line()}</div>
    <div class="exps">
      """ + "".join(
        f'<div class="exp" data-exp="{i + 3}" data-step="{i + 3}">'
        f'<span class="n">{i + 1}</span><b>{name}</b> — {d}</div>'
        for i, (v, name, d) in enumerate(COLS)) + """
    </div>
  </div>
</div>""")

# ---- 18 --------------------------------------------------------------------
TOUCH_LS1 = lsc([("Documents", 1), ("Downloads", 1), ("report.txt", 0)], rows=1)
TOUCH_LS2 = lsc([("Documents", 1), ("Downloads", 1), ("report.txt", 0),
                 ("test.txt", 0, "fade nw", 'data-after="2"')], rows=1)
TOUCH_LSL = ('-rw-r--r-- 1 kali kali 0 '
             '<span class="fade nw" data-after="4">Oct 10 12:30</span> test.txt')
TOUCH_DEMO = term([T("ls", TOUCH_LS1),
                   T("touch test.txt", None),
                   T("ls", TOUCH_LS2),
                   T("touch -t 202410101230 test.txt", None),
                   T("ls -l test.txt", TOUCH_LSL)], step=2)

slide("Команда touch",
      head("Terminal", "Команда", "touch", "Создание файлов и обновление временных меток")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">touch</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">touch</span> <span class="arg">test.txt</span>')], step=1)}
    {TOUCH_DEMO}
    {info("Команда touch не изменяет содержимое файла, она только создаёт файл "
          "или обновляет его временные метки.", step=3)}
    {info("Иногда достаточно одного прикосновения.", step=4, mark="q")}
  </div>
  <div class="g2">
    {card("touch test.txt", "<b>Создание нового файла.</b> Создаёт пустой файл: "
          "файл test.txt успешно создан.", num="01", step=5, big=True)}
    {card("touch file1.txt file2.txt", "<b>Создание нескольких файлов.</b> Можно создать сразу несколько "
          "файлов одной командой.", num="02", step=6, big=True)}
    {card("touch test.txt", "<b>Обновление временных меток.</b> Для существующего файла обновляет дату "
          "и время последнего изменения.", num="03", step=7, big=True)}
    {card("touch -t 202410101230 f", "<b>Установка конкретной даты.</b> Можно задать произвольную дату "
          "и время в формате ГГГГММДДччмм.", num="04", step=8, big=True)}
  </div>
</div>""")

# ---- 19 --------------------------------------------------------------------
MK_LS2 = lsc([("Desktop", 1), ("Documents", 1), ("Downloads", 1),
              ("GeeksForGeeks", 1, "vanish", 'data-gone="4"')], rows=1)
MK_DEMO = term([T("ls", lsc([("Desktop", 1), ("Documents", 1), ("Downloads", 1)], rows=1)),
                T("mkdir GeeksForGeeks", None),
                T("ls", MK_LS2),
                T("cd GeeksForGeeks", None),
                T("rmdir GeeksForGeeks", None, path="~")], step=2)

slide("mkdir и rmdir",
      head("Terminal", "Каталоги:", "mkdir и rmdir", "Создание и удаление каталогов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">mkdir</span> <span class="arg">[directory_name]</span>'),
          ("Пример:", '<span class="cmd">mkdir</span> <span class="arg">GeeksForGeeks</span>')], step=1)}
    {MK_DEMO}
    {info("Команда <b>rmdir</b> удаляет только пустые каталоги. Если в каталоге есть файлы, "
          "сначала удалите их.", step=3)}
  </div>
  <div class="vstack">
    {card("mkdir", "Сокращение от «make directory». Позволяет создавать новые папки в существующей файловой "
          "системе. Это обеспечивает структурированный способ категоризации и хранения файлов.",
          num="01", step=4, big=True)}
    {steplist([("Создание каталога", "Пользователь создал новую папку с названием GeeksForGeeks."),
               ("Переход в новый каталог", "Измените каталог на только что созданный с помощью команды cd."),
               ("Проверка текущего каталога", "Убедитесь, что активный каталог обновился: pwd покажет "
                                              "/home/kali/GeeksForGeeks.")], start=5)}
    {card("rmdir", "Сокращение от «remove directory». Позволяет удалять пустые каталоги. Это полезно "
          "для очистки неиспользуемых папок и поддержания упорядоченной файловой системы.",
          num="02", step=8, big=True)}
  </div>
</div>""")

# ---- 20 --------------------------------------------------------------------
CP_DEMO = term([T("cp ~/Downloads/image.jpg ~/Pictures", None),
                T("cd ~/Pictures", None),
                T("pwd", "/home/kali/Pictures", path="~/Pictures"),
                T("ls", lsc([("image.jpg", 0, "fade nw", 'data-after="3"'),
                             ("photo.png", 0), ("wallpaper.jpg", 0)], rows=1), path="~/Pictures")], step=2)

slide("Команда cp",
      head("Terminal", "Команда", "cp", "Копирование файлов и каталогов с сохранением оригинала")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">cp</span> <span class="arg">[source_file] [location]</span>'),
          ("Пример:", '<span class="cmd">cp</span> <span class="arg">~/Downloads/image.jpg ~/Pictures</span>')], step=1)}
    {CP_DEMO}
    {info("Команда <b>cp</b> копирует файлы и каталоги, оставляя оригинал без изменений. "
          "Для копирования каталога со всем содержимым нужен флаг <b>-r</b>.", step=3)}
  </div>
  <div class="vstack">
    {card("", "Команда cp в Linux используется для копирования файлов и каталогов из одного места в другое, "
              "сохраняя оригинал. Это удобный способ создавать резервные копии и дублировать файлы.", step=4)}
    {steplist([("Копирование файла", "Выполнение команды копирования: файл копируется в новое место, "
                                     "оригинал сохраняется."),
               ("Переход в каталог", "Измените текущий каталог для проверки результата."),
               ("Проверка результата", "С помощью команды ls мы видим, что файл image.jpg был скопирован "
                                       "в папку «Изображения».")], start=5)}
  </div>
</div>""")

# ---- 21 --------------------------------------------------------------------
MV_DEMO = term([T("mv ~/Downloads/image.jpg ~/Documents", None),
                T("cd ~/Documents", None),
                T("pwd", "/home/kali/Documents", path="~/Documents"),
                T("ls", lsc([("image.jpg", 0, "fade nw", 'data-after="3"'),
                             ("notes.txt", 0), ("report.pdf", 0)], rows=1), path="~/Documents")], step=2)

slide("Команда mv",
      head("Terminal", "Команда", "mv", "Перемещение и переименование файлов и каталогов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">mv</span> <span class="arg">[source_file] [location]</span>'),
          ("Пример:", '<span class="cmd">mv</span> <span class="arg">~/Downloads/image.jpg ~/Documents</span>')], step=1)}
    {MV_DEMO}
    {info("Команда <b>mv</b> перемещает файл в новое место. После перемещения оригинал "
          "в исходной папке больше не существует.", step=3)}
  </div>
  <div class="vstack">
    {card("", "Команда mv в Linux используется для перемещения или переименования файлов и каталогов "
              "из одного места в другое.", step=4)}
    {steplist([("Перемещение файла", "Выполнение команды mv: файл image.jpg перемещён из папки «Загрузки» "
                                     "в папку «Документы»."),
               ("Переход в каталог", "Измените текущий каталог для проверки."),
               ("Проверка результата", "Файл image.jpg теперь находится в папке «Документы». "
                                       "В папке «Загрузки» его больше нет.")], start=5)}
    {card("Переименование", "Если указать вместо каталога новое имя, файл будет переименован: "
          "<span class='mono o'>mv notes.txt plan.md</span>. Отдельной команды переименования в Linux нет.",
          num="04", step=8, big=True)}
  </div>
</div>""")

# ---- 22 --------------------------------------------------------------------
RM_LS = lsc([("demo.txt", 0, "vanish", 'data-gone="1"'), ("notes.txt", 0), ("image.jpg", 0)], rows=1)
RM_DEMO = term([T("ls", RM_LS),
                T("rm demo.txt", None),
                T("ls", lsc([("notes.txt", 0), ("image.jpg", 0)], rows=1))], step=2)
RM_DEMO2 = term([T("ls", lsc([("file1.txt", 0, "vanish", 'data-gone="1"'),
                              ("file2.txt", 0, "vanish", 'data-gone="1"'), ("file3.txt", 0)], rows=1)),
                 T("rm file1.txt file2.txt", None),
                 T("ls", lsc([("file3.txt", 0)], rows=1))], step=5)

slide("Команда rm",
      head("Terminal", "Команда", "rm", "Безвозвратное удаление файлов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">rm</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">rm</span> <span class="arg">demo.txt</span>')], step=1)}
    {RM_DEMO}
    <div class="card warn" data-step="3">
      <div class="chead"><span class="nbox red">!</span><span class="t">Будьте внимательны</span></div>
      <div class="cbody">Удалённые файлы <b class="red">невозможно восстановить</b> — они не помещаются
      в корзину. Убедитесь, что вы удаляете нужные данные. Для удаления каталогов используйте
      <span class="mono red">rm -r</span>.</div>
    </div>
  </div>
  <div class="vstack">
    {steplist([("Удаление файла", "Удалим файл demo.txt — команда завершится без вывода."),
               ("Проверка результата", "Снова выведем список файлов: файла demo.txt больше нет в каталоге.")],
              start=4)}
    {RM_DEMO2}
    {card("Удаление нескольких файлов", "Можно удалить сразу несколько файлов, перечислив их через пробел: "
          "файлы file1.txt и file2.txt удалены.", num="03", step=6, big=True)}
  </div>
</div>""")

# ---- 23 --------------------------------------------------------------------
CAT_TXT = 'Привет, Linux!\nЭто пример файла.\nУдачной работы!'
CAT_DEMO = term([T("cat test.txt", CAT_TXT),
                 T("cat -n test.txt", '     1\tПривет, Linux!\n     2\tЭто пример файла.\n     3\tУдачной работы!'),
                 T("cat file1.txt file2.txt", '=== file1.txt ===\nПервый файл.\n=== file2.txt ===\nВторой файл.')], step=2)

slide("Команда cat",
      head("Terminal", "Команда", "cat", "Просмотр содержимого файла и объединение файлов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">cat</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">cat</span> <span class="arg">test.txt</span>')], step=1)}
    {CAT_DEMO}
    {info("Команда <b>cat</b> не изменяет файл, она только отображает его содержимое в терминале.", step=3)}
  </div>
  <div class="g2">
    {card("cat test.txt", "<b>Просмотр содержимого.</b> Отображает содержимое файла в терминале.",
          num="01", step=4, big=True)}
    {card("cat file1.txt file2.txt", "<b>Просмотр нескольких файлов.</b> Выводит содержимое "
          "нескольких файлов подряд.", num="02", step=5, big=True)}
    {card("cat -n test.txt", "<b>Нумерация строк.</b> Опция -n выводит содержимое файла с номерами строк.",
          num="03", step=6, big=True)}
    {card("cat > notes.txt", "<b>Создание нового файла.</b> Можно создать файл и сразу добавить в него текст, "
          "завершив ввод сочетанием Ctrl+D.", num="04", step=7, big=True)}
    {card("cat f1 f2 > all.txt", "<b>Объединение файлов.</b> Несколько файлов объединяются в один новый.",
          num="05", step=8, big=True)}
    {card("cat -E test.txt", "<b>Конец строк.</b> Опция -E показывает символ конца строки ($).",
          num="06", step=9, big=True)}
  </div>
</div>""")

# ---- 24 --------------------------------------------------------------------
GREP_DEMO = term([T('grep "Python" notes.txt', 'I love Python programming\nPython is powerful\nLearn Python every day'),
                  T('grep -i "python" notes.txt', 'Python is great\nPYTHON for beginners\nLearn python today'),
                  T('grep -n "main" app.py', '12:def main():\n45:    main()\n78:# call main function'),
                  T('grep -c "TODO" task.txt', '5')], step=2)

slide("Команда grep",
      head("Terminal", "Команда", "grep", "Поиск текстовых шаблонов в файлах")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">grep</span> <span class="arg">"text" file_name</span>'),
          ("Пример:", '<span class="cmd">grep</span> <span class="arg">"Python" notes.txt</span>')], step=1)}
    {GREP_DEMO}
    {info("Команда <b>grep</b> учитывает регистр. Для поиска без учёта регистра используйте опцию <b>-i</b>.", step=3)}
    {info("Найти нужную информацию — это уже половина решения.", step=4, mark="q")}
  </div>
  <div class="vstack">
    {card("", "Команда grep в Linux используется для поиска текстовых шаблонов в файлах. Находит нужные строки, "
              "фильтрует вывод и помогает быстро анализировать данные.", step=5)}
    <div class="g2" data-step="6">
      {card("grep &quot;error&quot; log.txt", "Находит все строки, содержащие заданный текст.", num="01")}
      {card("grep -i &quot;python&quot; f", "Опция -i игнорирует регистр символов.", num="02")}
      {card("grep -n &quot;main&quot; app.py", "Опция -n показывает номер строки.", num="03")}
      {card("grep -c &quot;TODO&quot; task.txt", "Опция -c выводит только количество строк.", num="04")}
      {card("grep &quot;function&quot; *.py", "Поиск сразу в нескольких файлах по шаблону имени.", num="05")}
    </div>
    {info("Маленькая команда — большие возможности. Используйте <b>man grep</b> "
          "для просмотра всех доступных опций.", step=7)}
  </div>
</div>""", "tight")

# ---- 25 --------------------------------------------------------------------
SORT_DEMO = term([T("sort test.txt", 'apple\nbanana\ncherry\ndate\nfig'),
                  T("sort -n numbers.txt", '10\n25\n42\n100\n256'),
                  T("sort -r test.txt", 'fig\ndate\ncherry\nbanana\napple')], step=2)
WC_DEMO = term([T("wc test.txt", '10 47 312 test.txt'),
                T("wc -l test.txt", '10 test.txt'),
                T("wc -w test.txt", '47 test.txt'),
                T("wc -m test.txt", '299 test.txt')], step=5)

slide("sort и wc",
      head("Terminal", "Команды", "sort и wc", "Сортировка строк и подсчёт строк, слов и байтов")
      + f"""
<div class="two w">
  <div class="vstack">
    {card("Команда sort", "Команда sort используется для сортировки строк в файлах или входных данных. "
          "Она упорядочивает строки по алфавиту, числовому значению или другим критериям.", num="01", step=1)}
    {SORT_DEMO}
    <div class="g3" data-step="3">
      {card("sort", "Базовая сортировка строк по алфавиту.", num="01")}
      {card("sort -n", "Сортировка числовых значений.", num="02")}
      {card("sort -r", "Сортировка в обратном порядке.", num="03")}
    </div>
    {info("Файлы говорят больше, чем кажется.", step=4, mark="q")}
  </div>
  <div class="vstack">
    {card("Команда wc", "Команда wc используется для отображения количества строк, слов, байтов "
          "и символов в файле. Это полезно для быстрого анализа текстовых данных.", num="02", step=5)}
    {WC_DEMO}
    <div class="g2" data-step="6">
      {card("wc file", "Показывает строки, слова и байты.", num="01")}
      {card("wc -l", "Опция -l считает строки.", num="02")}
      {card("wc -w", "Опция -w считает слова.", num="03")}
      {card("wc -m", "Опция -m считает символы.", num="04")}
    </div>
    {info("Команды <b>sort</b> и <b>wc</b> часто используются вместе для анализа "
          "и обработки текстовых файлов в Linux.", step=7)}
  </div>
</div>""", "tight")

# ---- 26 --------------------------------------------------------------------
LN_DEMO = term([T("ln -s file1.txt link1.txt", None),
                T("ls -l link1.txt", 'lrwxrwxrwx 1 kali kali 9 Oct 10 12:30 link1.txt <span class="tdim">-&gt;</span> file1.txt'),
                T("ln file1.txt hardlink.txt", None),
                T("ls -l file1.txt hardlink.txt",
                  '-rw-r--r-- 2 kali kali 1024 Oct 10 12:30 file1.txt\n'
                  '-rw-r--r-- 2 kali kali 1024 Oct 10 12:30 hardlink.txt')], step=2)

slide("Команда ln",
      head("Terminal", "Команда", "ln", "Создание жёстких и символических ссылок на файлы")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Мягкая ссылка:", '<span class="cmd">ln</span> <span class="opt">-s</span> <span class="arg">source link_name</span>'),
          ("Жёсткая ссылка:", '<span class="cmd">ln</span> <span class="arg">source link_name</span>')], step=1)}
    {LN_DEMO}
    {info("Жёсткая ссылка указывает на те же данные (inode). Символическая ссылка — это отдельный файл, "
          "содержащий путь к исходному файлу. Используйте <b>ls -l</b>, чтобы увидеть, "
          "какой тип ссылки создан.", step=3)}
  </div>
  <div class="vstack">
    {card("", "Команда ln в Linux используется для создания ссылок между файлами. Поддерживает жёсткие "
              "и символические (мягкие) ссылки. Ссылки позволяют получать доступ к одному и тому же файлу "
              "по разным именам.", step=4)}
    <div class="g2" data-step="5">
      {card("ln -s file link", "Создание символической ссылки на файл.", num="01")}
      {card("ln file hardlink", "Создание жёсткой ссылки: ещё одно имя для того же файла.", num="02")}
      {card("ln -s /home/kali/docs d", "Создание символической ссылки на каталог.", num="03")}
      {card("ln -s ../file1.txt link", "В ссылке можно использовать относительный путь.", num="04")}
    </div>
    {info("Одна цель — много имён. Это и есть сила ссылок в Linux.", step=6, mark="q")}
  </div>
</div>""")

# ---- 27 --------------------------------------------------------------------
LOC_DEMO = term([T("locate demo.txt", '/home/user/demo.txt\n/usr/share/doc/demo.txt'),
                 T("locate demo", '/home/user/demo.txt\n/usr/bin/demontool'),
                 T("locate *.conf", '/etc/ssh/ssh_config\n/etc/xdg/demo.conf'),
                 T("sudo updatedb", None)], step=2)

slide("Команда locate",
      head("Terminal", "Команда", "locate", "Быстрый поиск файлов по базе данных")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">locate</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">locate</span> <span class="arg">demo.txt</span>')], step=1)}
    {LOC_DEMO}
    {info("Команда <b>locate</b> работает с локальной базой данных файлов. Если файл не найден, "
          "выполните обновление базы командой <b>sudo updatedb</b>.", step=3)}
  </div>
  <div class="vstack">
    {card("", "Команда locate в Linux используется для поиска файлов по базе данных. Позволяет быстро найти "
              "нужные файлы по их названию или части имени.", step=4)}
    <div class="g2" data-step="5">
      {card("locate demo.txt", "Ищет все файлы с заданным именем.", num="01")}
      {card("locate demo", "Находит файлы, содержащие указанную часть имени.", num="02")}
      {card("locate *.conf", "Поиск файлов по типу — по расширению.", num="03")}
      {card("sudo updatedb", "Обновление базы данных, если файл не найден.", num="04")}
    </div>
    {card("man и --help", "Полное руководство по любой команде открывает <b>man команда</b>, "
          "короткую справку — <b>команда --help</b>. В man листают стрелками, ищут по <b>/слово</b>, "
          "выходят клавишей <b>q</b>.", num="05", step=6, big=True)}
  </div>
</div>""")

# ---- 28 --------------------------------------------------------------------
slide("Права доступа",
      head("Linux", "Права доступа", "к файлам", "Кто и какие действия может выполнять с файлами и каталогами в системе")
      + f"""
<div class="two w">
  <div class="vstack">
    <h3>Три основных типа разрешений</h3>
    {card("Чтение (r)", "Просмотр содержимого файла или списка файлов в каталоге. <b>r = read</b>",
          num="01", step=1)}
    {card("Запись (w)", "Изменение содержимого файла или управление файлами в каталоге: создание, "
          "удаление, переименование. <b>w = write</b>", num="02", step=2)}
    {card("Выполнение (x)", "Запуск файла как программы или вход в каталог. <b>x = execute</b>",
          num="03", step=3)}
  </div>
  <div class="vstack">
    <h3>Группы владельцев и разрешений</h3>
    {card("Пользователь (владелец)", "Пользователь, который создал файл. Обозначается <b>u</b> — user.",
          num="01", step=4)}
    {card("Группа", "Пользователи, входящие в общую группу, например «developers». Обозначается <b>g</b> — group.",
          num="02", step=5)}
    {card("Остальные", "Все остальные пользователи системы. Обозначаются <b>o</b> — others. "
          "Это группа, за которой нужно следить в первую очередь.", num="03", step=6)}
    {info("Правильные права доступа — основа безопасности системы. "
          "Контролируй доступ — защищай данные.", step=7, mark="q")}
  </div>
</div>""")

# ---- 29 --------------------------------------------------------------------
PERM9 = ('<div class="perm9">'
         '<div class="pgrp"><div class="pch mono">r w x</div><div class="plb">Пользователь (владелец)</div></div>'
         '<div class="pgrp"><div class="pch mono">r w x</div><div class="plb">Группа</div></div>'
         '<div class="pgrp"><div class="pch mono">r w x</div><div class="plb">Остальные</div></div>'
         '</div>')

slide("Девять символов",
      head("Linux", "Структура", "прав доступа", "Разрешения представлены девятью символами")
      + f"""
<div class="card flat" data-step="1">{PERM9}</div>
<div class="two w" style="margin-top:1.2rem">
  <div class="vstack">
    {card("Всего девять символов", "Три символа для владельца (u), три для группы (g) и три для остальных (o). "
          "Каждый из трёх символов «rwx» обозначает отдельную операцию, которую можно выполнить "
          "с файлом или каталогом.", step=2)}
    """ + table([
      ("r — чтение", "Для файлов: чтение содержимого. Для каталогов: просмотр списка файлов."),
      ("w — запись", "Для файлов: изменение содержимого. Для каталогов: создание, удаление, переименование."),
      ("x — выполнение", "Для файлов: выполнение программы. Для каталогов: переход в каталог командой cd."),
    ], ("Символ", "Что он разрешает"), mono=0, start=3) + f"""
  </div>
  <div class="vstack">
    {card("Пример: -rwxr-xr-- file.txt",
          '<div class="mono o" style="font-size:1.3rem;margin-bottom:.6rem">- rwx r-x r--</div>'
          'Первый символ — тип объекта. Далее <b>u = rwx</b> — владелец может читать, изменять и запускать; '
          '<b>g = r-x</b> — группа читает и запускает; <b>o = r--</b> — остальные только читают.', step=6)}
    """ + table([
      ("u", "user (пользователь)", "Права распространяются только на владельца файла или каталога."),
      ("g", "group (группа)", "Права применяются к группе, назначенной для файла или каталога."),
      ("o", "others (остальные)", "Права распространяются на всех остальных пользователей системы."),
      ("a", "all (все три)", "Владелец, группа и остальные одновременно."),
    ], ("Символ", "Класс", "Описание"), mono=0, start=7) + f"""
    {info("Зная, что означает каждый символ, вы можете легко определить, какие действия разрешены "
          "для файла или каталога.", step=11)}
  </div>
</div>""", "tight")

# ---- 30 --------------------------------------------------------------------
CHMOD_DEMO = term([T("ls -l xyz.txt", '-rw-r--r-- 1 user group 46 Apr 14 16:37 xyz.txt'),
                   T("chmod o+x xyz.txt", None),
                   T("ls -l xyz.txt", '-rw-r--r-<span class="nw">x</span> 1 user group 46 Apr 14 16:37 xyz.txt'),
                   T("chmod ugo-rwx xyz.txt", None),
                   T("ls -l xyz.txt", '<span class="nw">----------</span> 1 user group 46 Apr 14 16:37 xyz.txt')], step=2)

slide("Команда chmod",
      head("Terminal", "Команда", "chmod", "Изменение прав доступа к файлу")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">chmod</span> <span class="opt">[OPTIONS]</span> <span class="arg">file_name</span>'),
          ("Пример:", '<span class="cmd">chmod</span> <span class="opt">o+x</span> <span class="arg">xyz.txt</span>')], step=1)}
    {CHMOD_DEMO}
    {info("Команда <b>chmod</b> используется для изменения прав доступа к файлам и каталогам. "
          "Она позволяет определить, кто может читать, изменять и выполнять файл.", step=3)}
  </div>
  <div class="vstack">
    {steplist([("Проверим текущие права доступа",
                "Файл доступен для чтения и записи владельцу, только для чтения группе и остальным."),
               ("Добавим право выполнения для всех",
                "Команда chmod o+x xyz.txt добавляет право на выполнение для остальных пользователей."),
               ("Проверим результат",
                "Теперь у остальных пользователей появилось право на выполнение (x)."),
               ("Изменим сразу несколько прав",
                "Команда chmod ugo-rwx xyz.txt убирает все права на чтение, запись и выполнение для всех."),
               ("Проверим результат",
                "Файл больше не доступен ни для кого.")], start=4)}
    <div class="g3" data-step="9">
      {card("Оператор +", "Добавить разрешения.", num="01")}
      {card("Оператор -", "Удалить разрешения.", num="02")}
      {card("Оператор =", "Установить указанные разрешения.", num="03")}
    </div>
  </div>
</div>""")

# ---- 31 --------------------------------------------------------------------
OCT = [
    ("0", "000", "---", "Нет прав"),
    ("1", "001", "--x", "Только выполнение"),
    ("2", "010", "-w-", "Только запись"),
    ("3", "011", "-wx", "Запись и выполнение"),
    ("4", "100", "r--", "Только чтение"),
    ("5", "101", "r-x", "Чтение и выполнение"),
    ("6", "110", "rw-", "Чтение и запись"),
    ("7", "111", "rwx", "Чтение, запись и выполнение"),
]

def octtable():
    r = "".join(f'<tr data-step="{i + 1}"><th class="mono o">{v}</th><td class="mono">{b}</td>'
                f'<td class="mono">{p}</td><td>{d}</td></tr>' for i, (v, b, p, d) in enumerate(OCT))
    return ('<div class="tbw card flat"><table class="tbl"><thead><tr><th>Восьмеричное</th>'
            '<th>Двоичное</th><th>Права (rwx)</th><th>Описание</th></tr></thead>'
            f'<tbody>{r}</tbody></table></div>')

def bgrp(title, r, w, x):
    def b(letter, weight, on):
        return (f'<button class="bb" type="button" data-w="{weight}" data-l="{letter}" '
                f'aria-pressed="{"true" if on else "false"}">{letter}</button>')
    return (f'<div class="bgrp"><h4>{title}</h4><div class="bbtns">'
            + b("r", 4, r) + b("w", 2, w) + b("x", 1, x)
            + '</div><div class="bval">0</div></div>')

slide("Восьмеричные обозначения",
      head("Linux", "Восьмеричные", "обозначения", "Каждое число от 0 до 7 соответствует определённому набору прав")
      + f"""
<div class="two w">
  {octtable()}
  <div class="vstack">
    {card("Как это работает", "Каждая из трёх цифр восьмеричного кода соответствует правам для определённой "
          "категории: <b>первая цифра</b> — права владельца (u), <b>вторая</b> — права группы (g), "
          "<b>третья</b> — права остальных (o).", step=9)}
    <div class="card" data-hook="bits" data-step="10">
      <div class="bits">
        {bgrp("Владелец", 1, 1, 0)}
        {bgrp("Группа", 1, 0, 0)}
        {bgrp("Остальные", 1, 0, 0)}
      </div>
      <div class="hstack" style="margin-top:.9rem;align-items:baseline;gap:1.2rem">
        <span class="octl">Число для chmod</span>
        <span class="octal">644</span>
        <span class="mono symb" style="color:var(--dim)">-rw-r--r--</span>
      </div>
    </div>
    {info("Нажимайте буквы: <b>r</b> даёт 4, <b>w</b> — 2, <b>x</b> — 1. Внутри тройки веса складываются. "
          "Пример: установить права rw-r--r-- (644) для файла — <b>chmod 644 file.txt</b>.", step=11)}
    {info("Числовой код — это удобная и компактная альтернатива символьной записи.", step=12, mark="q")}
  </div>
</div>""")

# ---- 32 --------------------------------------------------------------------
slide("Примеры chmod",
      head("Terminal", "Примеры", "управления правами", "Команда chmod указывает, какие разрешения добавить, удалить или установить")
      + f"""
<div class="two w">
  <div class="vstack">
    {card("Добавление и удаление разрешений",
          '<div class="mono o" style="font-size:1.2rem;margin:.2rem 0 .7rem">$ chmod ug+rw,o-x abc.mp4</div>'
          'Команда добавляет разрешения на чтение (r) и запись (w) как для пользователя (u), так и для группы (g), '
          'а также отменяет разрешение на выполнение (x) для других пользователей (o) для файла abc.mp4.',
          num="01", step=1)}
    """ + table([
      ("Пользователь (u)", "+rw", "добавить чтение (r) и запись (w)"),
      ("Группа (g)", "+rw", "добавить чтение (r) и запись (w)"),
      ("Другие (o)", "-x", "отменить выполнение (x)"),
    ], ("Категория", "Операция", "Результат"), mono=1, start=2) + f"""
  </div>
  <div class="vstack">
    {card("Установка и добавление разрешений",
          '<div class="mono o" style="font-size:1.2rem;margin:.2rem 0 .7rem">$ chmod ug=rx,o+r abc.c</div>'
          'Предоставляет права на чтение (r) и выполнение (x) как пользователю (u), так и группе (g), '
          'а также добавляет право на чтение для других пользователей для файла abc.c.',
          num="02", step=5)}
    """ + table([
      ("Пользователь (u)", "=rx", "установить чтение (r) и выполнение (x)"),
      ("Группа (g)", "=rx", "установить чтение (r) и выполнение (x)"),
      ("Другие (o)", "+r", "добавить чтение (r)"),
    ], ("Категория", "Операция", "Результат"), mono=1, start=6) + f"""
    {info("Правильные права доступа защищают ваши данные и обеспечивают стабильность системы. "
          "Минимально необходимые права — залог безопасности.", step=9, mark="q")}
  </div>
</div>""", "tight")

# ---- 33 --------------------------------------------------------------------
slide("VirtualBox",
      head("Virtualization", "Oracle VM", "VirtualBox", "Бесплатная виртуализация — больше возможностей")
      + f"""
<p class="p dim" style="margin-bottom:1.1rem">Oracle VM VirtualBox — это бесплатное программное обеспечение
для виртуализации, которое позволяет запускать различные операционные системы в виртуальных машинах
на одном компьютере. Удобный инструмент для обучения, тестирования и безопасной работы с разными ОС.</p>
<div class="g4">
  {card("Скачивание", "Скачайте установочный файл VirtualBox с официального сайта проекта.", num="01", step=1)}
  {card("Установка", "Запустите установочный файл и следуйте инструкциям мастера установки.", num="02", step=2)}
  {card("Создание виртуальной машины", "Задайте имя, тип и версию операционной системы. Выделите объём "
        "оперативной памяти и создайте виртуальный жёсткий диск.", num="03", step=3)}
  {card("Установка системы", "Выберите ISO-образ нужной ОС и запустите виртуальную машину. "
        "Следуйте стандартной процедуре установки.", num="04", step=4)}
  {card("Использование", "Запускайте, останавливайте и управляйте виртуальными машинами "
        "через интерфейс VirtualBox.", num="05", step=5)}
  {card("Зачем использовать", "Обучение и тестирование разных ОС, безопасный запуск подозрительного ПО, "
        "разработка и отладка, изолированные рабочие среды.", num="06", step=6)}
  {card("Минимальные требования", "Windows, macOS или Linux; не менее 2 ГБ ОЗУ; свободное место на диске; "
        "аппаратная виртуализация, включённая в BIOS или UEFI.", num="07", step=7)}
  {info("Больше чем одна ОС на одном компьютере: Linux, Windows, macOS и другие системы "
        "работают одновременно и не мешают друг другу.", step=8)}
</div>""")

# ---- 34 --------------------------------------------------------------------
slide("Тренажёр",
      head("Terminal", "Живой", "терминал", "Учебная оболочка: файловая система в памяти, всё как в настоящей")
      + """
<div class="trainer" data-hook="shell">
  <div class="tw">
    <div class="tbar"><i class="r"></i><i class="y"></i><i class="g"></i>
      <span class="tname">kali@kali: учебная оболочка</span></div>
    <div class="tscroll"></div>
    <div class="tin"><span class="pmt"></span><input type="text" autocomplete="off" autocorrect="off"
      autocapitalize="off" spellcheck="false" aria-label="Строка ввода команд"></div>
  </div>
  <div class="vstack">
    <div class="card flat">
      <div class="taskhead">""" + raccoon("rmini") + """<h3>Задания</h3></div>
      <div class="tasks"></div>
      <button class="btn sreset" type="button" style="margin-top:.9rem">Сбросить</button>
    </div>
    <div class="info"><span class="ic">i</span><p>Поддерживаются <b>pwd</b>, <b>ls</b>, <b>cd</b>,
      <b>touch</b>, <b>mkdir</b>, <b>rm</b>, <b>cp</b>, <b>mv</b>, <b>cat</b>, <b>clear</b>, <b>help</b>.
      Клавиша <b>Tab</b> дополняет имена файлов, стрелки вверх и вниз листают историю команд.
      Задание засчитывается по состоянию файловой системы — способ решения выбираете сами.</p></div>
  </div>
</div>""")

# ---- 35 --------------------------------------------------------------------
QUIZ = [
    {"q": "Что такое дистрибутив Linux?", "a": 2,
     "o": ["Другое название ядра Linux",
           "Программа для запуска Linux внутри Windows",
           "Полноценная операционная система на основе ядра Linux вместе с системными инструментами, библиотеками и приложениями",
           "Набор драйверов для оборудования"],
     "e": "Разные дистрибутивы предназначены для разных задач: от работы на компьютере до серверов, кибербезопасности и разработки."},
    {"q": "Какой дистрибутив ориентирован на кибербезопасность и тестирование на проникновение?", "a": 1,
     "o": ["Linux Mint", "Kali Linux", "openSUSE", "Deepin"],
     "e": "Kali Linux используется для этичного взлома и тестирования на проникновение. Для слабых ПК подойдёт MX Linux, для новичков — Ubuntu и Mint."},
    {"q": "Что выведет команда pwd?", "a": 1,
     "o": ["Список файлов текущего каталога", "Путь к текущему каталогу",
           "Имя текущего пользователя", "Размер текущего каталога"],
     "e": "Команда pwd показывает текущее местоположение в системе: например /home/kali/Templates."},
    {"q": "В каком каталоге хранятся конфигурационные файлы системы?", "a": 2,
     "o": ["/dev", "/proc", "/etc", "/boot"],
     "e": "/etc содержит настройки системы и установленных служб: passwd, hosts, fstab, crontab. В /dev — файлы устройств, в /proc — данные о процессах, в /boot — файлы загрузчика."},
    {"q": "Что означает третье поле в выводе ls -l: -rw-r--r-- 1 user group 46 Apr 14 16:37 Narx.txt?", "a": 0,
     "o": ["Количество жёстких ссылок на файл", "Размер файла в байтах",
           "Номер владельца", "Количество файлов в каталоге"],
     "e": "Порядок полей: тип, права доступа, количество ссылок, владелец, группа, размер, дата и время изменения, имя файла."},
    {"q": "Что произойдёт, если выполнить touch для уже существующего файла?", "a": 3,
     "o": ["Файл будет очищен", "Команда завершится ошибкой", "Будет создана копия файла",
           "Обновятся временные метки, содержимое останется прежним"],
     "e": "Команда touch не изменяет содержимое файла, она только создаёт файл или обновляет его временные метки."},
    {"q": "Чем команда mv отличается от cp?", "a": 0,
     "o": ["mv перемещает файл: в исходной папке его больше нет, cp оставляет оригинал",
           "mv работает только с каталогами", "cp умеет переименовывать, а mv нет",
           "Разницы нет, это синонимы"],
     "e": "Именно поэтому mv используют и для переименования: файл «перемещается» в тот же каталог под новым именем."},
    {"q": "Какая команда удалит каталог вместе со всем содержимым?", "a": 1,
     "o": ["rmdir каталог", "rm -r каталог", "rm каталог", "mv каталог /dev/null"],
     "e": "rmdir удаляет только пустые каталоги. Удалённые командой rm файлы не помещаются в корзину и не восстанавливаются."},
    {"q": "Что делает команда grep -i «python» notes.txt?", "a": 2,
     "o": ["Заменяет слово python в файле", "Считает количество строк со словом python",
           "Ищет строки со словом python без учёта регистра", "Сортирует строки файла"],
     "e": "Опция -i игнорирует регистр символов. Опция -n покажет номера строк, -c — только количество совпадений."},
    {"q": "Каким числом задаются права rwxr-xr-x?", "a": 1,
     "o": ["644", "755", "777", "700"],
     "e": "rwx = 4+2+1 = 7, r-x = 4+1 = 5, r-x = 5. Получается chmod 755."},
    {"q": "Что сделает команда chmod ug+rw,o-x abc.mp4?", "a": 0,
     "o": ["Добавит чтение и запись владельцу и группе, снимет выполнение у остальных",
           "Установит права 660 для всех категорий",
           "Удалит все права у владельца и группы",
           "Сделает файл исполняемым для всех"],
     "e": "Оператор + добавляет разрешения, - удаляет, = устанавливает указанные разрешения."},
    {"q": "Для чего нужен каталог /proc?", "a": 3,
     "o": ["Для хранения программ пользователя", "Для временных файлов",
           "Для файлов загрузчика",
           "Это виртуальная файловая система с информацией о процессах и состоянии системы в реальном времени"],
     "e": "Файлы /proc динамически генерируются ядром: /proc/cpuinfo, /proc/meminfo, /proc/version."},
]

slide("Проверь себя",
      head("Linux", "Проверь", "себя", "Двенадцать вопросов по материалу лекции")
      + """
<div class="quiz" data-hook="quiz">
  <div class="qtop"><span class="qn mono"></span><span class="qs mono"></span></div>
  <div class="qq"></div>
  <div class="opts"></div>
  <div class="qexp"></div>
  <div class="hstack" style="margin-top:.4rem">
    <button class="btn qprev" type="button">Назад</button>
    <button class="btn pri qnext" type="button">Следующий вопрос</button>
  </div>
</div>""")

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{
  --bg:#0a0a0c;
  --panel:#121316;
  --panel-2:#17181c;
  --edge:rgba(255,138,20,.28);
  --edge-hot:rgba(255,138,20,.75);
  --orange:#ff8a14;
  --orange-2:#ffb35c;
  --ember:#e2560f;
  --ink:#f4f1ec;
  --dim:#b3aea8;
  --term-bg:#0d0f12;
  --term-blue:#5aa9e6;
  --term-green:#7fd66f;
  --red:#ff5f57;
  --f:"Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --ez:cubic-bezier(.22,.7,.3,1);
  --r:12px;
  color-scheme:dark;
}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(14px,min(1vw,1.8vh),22px)}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--f)}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
b{font-weight:700}
/* ------------------------------------------------ фон */
#bg{position:fixed;inset:0;z-index:0;overflow:hidden;background:var(--bg)}
#bg .glow{position:absolute;border-radius:50%;filter:blur(70px)}
#bg .g1{left:-12%;top:-18%;width:52vw;height:52vw;background:radial-gradient(circle,var(--ember),transparent 66%);opacity:.32}
#bg .g2{right:-16%;top:6%;width:46vw;height:46vw;background:radial-gradient(circle,#ff8a14,transparent 68%);opacity:.18}
#bg .g3{left:28%;bottom:-30%;width:64vw;height:48vw;background:radial-gradient(circle,var(--ember),transparent 70%);opacity:.28}
#bg .grid{position:absolute;left:-60%;right:-60%;bottom:-4%;height:58%;opacity:.12;
  background-image:repeating-linear-gradient(90deg,var(--orange) 0 1px,transparent 1px 92px),
                   repeating-linear-gradient(0deg,var(--orange) 0 1px,transparent 1px 64px);
  transform:perspective(340px) rotateX(70deg);transform-origin:50% 100%;
  -webkit-mask-image:linear-gradient(to top,#000 10%,transparent 92%);mask-image:linear-gradient(to top,#000 10%,transparent 92%)}
#bg .spark{position:absolute;width:2px;height:2px;border-radius:50%;background:var(--orange-2);box-shadow:0 0 7px 2px rgba(255,138,20,.55)}
#bg .horizon{position:absolute;left:0;right:0;bottom:38%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,138,20,.45),transparent);opacity:.5}
/* ------------------------------------------------ каркас слайда */
#prog{position:fixed;left:0;top:0;height:2px;width:100%;z-index:30;background:rgba(255,255,255,.07)}
#prog i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--ember),var(--orange));transition:width .3s var(--ez)}
.slide{position:fixed;inset:0;z-index:1;display:none}
.slide.on{display:block}
.sc{height:100%;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;
  padding:clamp(20px,5vh,54px) clamp(16px,5vw,92px) calc(4.6rem + 14px);
  scrollbar-width:thin;scrollbar-color:rgba(255,138,20,.35) transparent}
.sc::-webkit-scrollbar{width:8px}
.sc::-webkit-scrollbar-thumb{background:rgba(255,138,20,.35);border-radius:4px}
.wrap{margin:auto;width:100%;max-width:96rem}
/* ------------------------------------------------ заголовки */
.lbl{display:inline-block;border:1px solid var(--edge);border-radius:6px;padding:.28em .7em;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);margin-bottom:.9rem}
h1,h2{font-weight:900;letter-spacing:-.02em;text-transform:uppercase;line-height:1.02}
h2{font-size:clamp(26px,3.1vw,54px)}
h1{font-size:clamp(34px,6vw,96px)}
.o{color:var(--orange)}
.sub{margin-top:.6rem;color:var(--dim);font-size:clamp(14px,1.15vw,20px);line-height:1.5;max-width:64ch;text-transform:none;letter-spacing:0;font-weight:400}
.sh{margin-bottom:1.5rem}
h3{font-size:1.05rem;font-weight:800;letter-spacing:-.01em;margin-bottom:.45rem}
p{font-size:1rem;line-height:1.55}
.p{font-size:1.02rem;line-height:1.6;color:var(--ink);max-width:66ch}
.p.dim{color:var(--dim)}
.p+.p{margin-top:.7rem}
/* ------------------------------------------------ сетки */
.g2,.g3,.g4,.g5{display:grid;gap:clamp(12px,1.2vw,20px);grid-template-columns:minmax(0,1fr)}
.two{display:grid;gap:clamp(16px,2vw,34px);grid-template-columns:minmax(0,1fr);align-items:start}
.vstack{display:flex;flex-direction:column;gap:clamp(12px,1.4vw,20px)}
.hstack{display:flex;flex-wrap:wrap;gap:.8rem}
/* ------------------------------------------------ карточки */
.card{position:relative;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--edge);border-radius:var(--r);padding:1.1rem 1.2rem;overflow:hidden}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(255,138,20,.75),transparent);opacity:.7}
.card::after{content:"";position:absolute;left:12%;right:12%;top:-42px;height:84px;border-radius:50%;
  background:radial-gradient(ellipse at center,rgba(255,138,20,.22),transparent 68%);pointer-events:none}
.card.flat::after{display:none}
.card.hot{border-color:var(--edge-hot)}
.card.sub2{background:var(--panel-2)}
.nbox{display:inline-grid;place-items:center;width:2.3em;height:2.3em;border:1px solid var(--edge);border-radius:8px;
  font-family:var(--mono);font-weight:800;color:var(--orange);font-size:.92rem}
.nbig{font-family:var(--mono);font-weight:900;color:var(--orange);font-size:clamp(28px,2.7vw,46px);line-height:1;letter-spacing:-.04em}
.chead{display:flex;align-items:center;gap:.8rem;margin-bottom:.7rem}
.chead .t{font-size:1.15rem;font-weight:800}
.cbody{color:#dcd7d1;font-size:1rem;line-height:1.6}
.cbody b{color:var(--ink);font-weight:600}
.tag{display:inline-flex;align-self:flex-start;align-items:center;gap:.5em;border:1px solid var(--edge);border-radius:8px;
  padding:.4em .7em;font-size:.82rem;color:var(--orange-2);margin-top:auto;margin-block-start:.9rem}
.tag svg{width:1.05em;height:1.05em;fill:none;stroke:var(--orange);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.logo{width:2.6rem;height:2.6rem;flex:none}
.logo svg{width:100%;height:100%;fill:none;stroke:var(--orange);stroke-width:1.4;stroke-linejoin:round}
.circ{display:inline-grid;place-items:center;width:2em;height:2em;flex:none;border:1px solid var(--orange);border-radius:50%;
  background:transparent;color:var(--orange);font-family:var(--mono);font-weight:700;font-size:.9rem}
.steps{display:flex;flex-direction:column;gap:.9rem}
.steps li{display:flex;gap:.9rem;align-items:flex-start;list-style:none;font-size:1rem;line-height:1.6;color:#dcd7d1}
.steps li b{color:var(--ink)}
.steprow{display:grid;gap:clamp(12px,1.2vw,18px);grid-template-columns:minmax(0,1fr)}
/* ------------------------------------------------ терминал */
.term{background:var(--term-bg);border:1px solid rgba(255,255,255,.08);border-radius:8px;overflow:hidden;cursor:pointer}
.tbar{display:flex;align-items:center;gap:7px;padding:.55em .8em;border-bottom:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.02)}
.tbar i{width:11px;height:11px;border-radius:50%;flex:none}
.tbar .r{background:#ff5f57}.tbar .y{background:#febc2e}.tbar .g{background:#28c840}
.tname{margin-left:.7em;font-family:var(--mono);font-size:12px;color:var(--dim)}
.tbody{padding:.85em 1em 1em;font-family:var(--mono);font-size:14px;line-height:1.55;overflow-x:auto}
.tline{white-space:pre;color:var(--ink)}
.pmt{color:#cfcac4}
.pmt .pp{color:var(--orange)}
.c1{color:var(--orange);font-weight:600}
.c2{color:var(--orange-2)}
.cur{display:inline-block;width:.6em;height:1.05em;vertical-align:-.18em;background:var(--orange);margin-left:1px;opacity:.6}
.cur.blink{opacity:1}
.cur.blink{animation:cb 1s steps(1,end) infinite}
.cur.off{display:none}
@keyframes cb{0%,49%{opacity:1}50%,100%{opacity:0}}
.tout{white-space:pre;color:var(--ink);padding-bottom:.15em}
.tout[hidden]{display:none}
.dir{color:var(--term-blue)}
.grn{color:var(--term-green)}
.red{color:var(--red)}
.tdim{color:var(--dim)}
.lsc{display:grid;grid-auto-flow:column;grid-template-rows:repeat(var(--rows,3),auto);gap:0 2.4em;justify-content:start;min-width:max-content}
.lsl{display:grid;grid-template-columns:max-content max-content max-content max-content max-content max-content max-content;gap:0 1.2em;min-width:max-content}
.lsl span{white-space:pre}
/* ------------------------------------------------ плашка-пояснение */
.info{display:flex;gap:.8rem;align-items:flex-start;border:1px solid var(--edge);border-radius:var(--r);background:var(--panel-2);padding:.85rem 1rem}
.info .ic{flex:none;display:grid;place-items:center;width:1.7rem;height:1.7rem;border-radius:50%;background:var(--orange);color:#0a0a0c;
  font-weight:900;font-size:.95rem;font-family:var(--f)}
.info .ic.q{font-family:Georgia,"Times New Roman",serif;font-size:1.25rem;line-height:1;padding-top:.28em}
.info p{color:#dcd7d1;font-size:1rem;line-height:1.6}
.info p b,.info p .mono{color:var(--orange)}
.info.quote p{color:var(--ink);font-style:italic}
/* ------------------------------------------------ синтаксис */
.syn{border:1px solid var(--edge);border-radius:var(--r);background:var(--panel-2);overflow:hidden}
.syn .row{display:flex;flex-wrap:wrap;gap:.2rem .9rem;align-items:baseline;padding:.75rem 1rem}
.syn .row+.row{border-top:1px solid var(--edge)}
.syn .k{color:var(--dim);font-size:.88rem;min-width:5.4em}
.syn .v{font-family:var(--mono);font-size:1rem}
.syn .v .cmd{color:var(--orange);font-weight:600}
.syn .v .arg{color:var(--ink)}
.syn .v .opt{color:var(--orange-2)}
/* ------------------------------------------------ дерево каталогов */
.tree{font-family:var(--mono);font-size:.95rem;line-height:1.75}
.tree .nd{display:inline-flex;align-items:center;gap:.45em;padding:.05em .45em;border-radius:6px;cursor:default;transition:background .15s,color .15s}
.tree .nd.d{color:var(--term-blue)}
.tree .nd.f{color:var(--ink)}
.tree .nd:hover,.tree .nd.path{background:rgba(255,138,20,.14);color:var(--orange-2)}
.tree .lv{padding-left:1.6em;border-left:1px solid rgba(255,138,20,.18);margin-left:.7em}
.tree .cwd{outline:1px solid var(--edge-hot);background:rgba(255,138,20,.12)}
.pathbar{font-family:var(--mono);font-size:.95rem;color:var(--dim);margin-top:.9rem}
.pathbar b{color:var(--orange)}
/* ------------------------------------------------ разбор ls -l */
.cols{font-family:var(--mono);font-size:clamp(13px,1.15vw,19px);white-space:pre;overflow-x:auto;padding:.9rem 1rem;background:var(--term-bg);border-radius:8px;border:1px solid rgba(255,255,255,.08)}
.cols span{padding:.12em .18em;border-radius:4px;transition:background .25s var(--ez),color .25s var(--ez)}
.cols span.hot{background:rgba(255,138,20,.25);color:var(--orange-2)}
.exps{margin-top:.9rem;min-height:4.2rem;font-size:1rem;line-height:1.55}
.exp{display:none}
.exp.on{display:block}
.exp .n{color:var(--orange);font-family:var(--mono);font-weight:700;margin-right:.5em}
/* ------------------------------------------------ биты прав */
.bits{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem}
.bgrp{border:1px solid var(--edge);border-radius:var(--r);background:var(--panel-2);padding:.8rem}
.bgrp h4{font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:.6rem;font-weight:700}
.bbtns{display:flex;gap:.4rem}
.bb{font:700 1rem/1 var(--mono);width:2.4em;height:2.4em;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--dim);cursor:pointer;transition:.15s}
.bb[aria-pressed="true"]{border-color:var(--edge-hot);background:rgba(255,138,20,.18);color:var(--orange)}
.bval{margin-top:.6rem;font-family:var(--mono);font-size:1.6rem;font-weight:800;color:var(--orange);text-align:center}
.octal{font-family:var(--mono);font-size:clamp(28px,3.4vw,56px);font-weight:900;color:var(--orange);letter-spacing:.06em}
.octl{color:var(--dim);font-size:.88rem;letter-spacing:.1em;text-transform:uppercase}
/* ------------------------------------------------ подбор дистрибутива */
.qrow{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-bottom:.7rem}
.qrow .qt{color:var(--dim);font-size:.95rem;flex:1 1 14rem}
.opt{font:inherit;font-size:.92rem;padding:.45em .85em;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink);cursor:pointer;transition:.15s}
.opt:hover{border-color:var(--edge-hot);color:var(--orange-2)}
.opt[aria-pressed="true"]{background:rgba(255,138,20,.2);border-color:var(--edge-hot);color:var(--orange)}
.pick{transition:opacity .4s var(--ez),filter .4s var(--ez)}
.pick.off{opacity:.3;filter:grayscale(.7)}
.mini{padding:.75rem .85rem}
.mini .t{font-size:.98rem;font-weight:800}
.mini .cbody{font-size:.9rem}
/* ------------------------------------------------ тренажёр */
.trainer{display:grid;gap:clamp(12px,1.4vw,20px);grid-template-columns:minmax(0,1fr)}
.tw{background:var(--term-bg);border:1px solid rgba(255,255,255,.08);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;min-height:26rem}
.tscroll{flex:1;overflow-y:auto;overflow-x:auto;padding:.85em 1em;font-family:var(--mono);font-size:14px;line-height:1.55}
.tin{display:flex;align-items:baseline;gap:.4em;padding:.6em 1em .8em;font-family:var(--mono);font-size:14px;white-space:pre}
.tin input{flex:1;min-width:4em;font:inherit;background:transparent;border:0;color:var(--ink);outline:none;caret-color:var(--orange)}
.tin input:focus-visible{outline:none}
.tw:focus-within{border-color:var(--edge-hot)}
.tasks{display:flex;flex-direction:column;gap:.7rem}
.task{display:flex;gap:.7rem;align-items:flex-start;border:1px solid var(--edge);border-radius:10px;padding:.7rem .85rem;background:var(--panel);transition:.25s}
.task .mk{flex:none;width:1.4rem;height:1.4rem;border:1px solid var(--edge);border-radius:50%;display:grid;place-items:center;font-size:.8rem;color:var(--dim);font-family:var(--mono)}
.task p{font-size:.96rem;line-height:1.55;color:#dcd7d1}
.task .mono{color:var(--orange-2)}
.task.done{border-color:var(--edge-hot)}
.task.done .mk{background:var(--orange);border-color:var(--orange);color:#0a0a0c}
.task.done p{color:var(--ink)}
/* ------------------------------------------------ проверь себя */
.quiz{border:1px solid var(--edge);border-radius:var(--r);background:var(--panel);padding:1.1rem 1.2rem}
.qtop{display:flex;justify-content:space-between;color:var(--dim);font-family:var(--mono);font-size:.85rem;margin-bottom:.7rem}
.qq{font-size:1.12rem;line-height:1.45;margin-bottom:.9rem;font-weight:600}
.opts{display:grid;gap:.5rem;grid-template-columns:minmax(0,1fr)}
.opts .opt{text-align:left;padding:.65em .9em;font-size:.96rem}
.opts .opt.ok{border-color:var(--edge-hot);background:rgba(255,138,20,.2);color:var(--orange)}
.opts .opt.no{border-color:rgba(255,95,87,.6);background:rgba(255,95,87,.14);color:#ffb3ad}
.qexp{min-height:3.2rem;margin-top:.8rem;color:#dcd7d1;font-size:1rem;line-height:1.6}
.qexp b{color:var(--orange)}
.btn{font:inherit;font-size:.9rem;font-weight:600;padding:.5em .95em;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink);cursor:pointer;transition:.15s}
.btn:hover{border-color:var(--edge-hot);color:var(--orange-2)}
.btn.pri{background:var(--orange);border-color:var(--orange);color:#0a0a0c}
.btn.pri:hover{background:var(--orange-2);border-color:var(--orange-2);color:#0a0a0c}
.btn:disabled{opacity:.4;cursor:default}
/* ------------------------------------------------ шаги показа */
[data-step]{opacity:0;transform:translateY(10px);transition:opacity .28s var(--ez),transform .28s var(--ez)}
[data-step].in{opacity:1;transform:none}
.slide.ni *{transition:none!important}
/* ------------------------------------------------ навигация */
#nav{position:fixed;z-index:40;left:50%;bottom:14px;transform:translateX(-50%);display:flex;align-items:center;gap:.25rem;
  background:rgba(18,19,22,.9);border:1px solid var(--edge);border-radius:10px;padding:.3rem .45rem;
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);max-width:calc(100vw - 20px)}
#nav button{font:600 12px/1 var(--f);border:1px solid transparent;background:transparent;color:var(--ink);border-radius:7px;
  padding:.45em .6em;cursor:pointer;display:inline-flex;align-items:center;gap:.35em}
#nav button:hover{background:rgba(255,138,20,.16);color:var(--orange-2)}
#nav svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
#ind{font-family:var(--mono);font-size:12px;color:var(--dim);padding:0 .5em;white-space:nowrap}
#ind b{color:var(--ink);font-weight:600}
#ind .st{color:var(--orange)}
.nsep{width:1px;height:18px;background:var(--edge);margin:0 .25rem}
:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
/* ------------------------------------------------ содержание */
#ov{position:fixed;inset:0;z-index:60;background:rgba(10,10,12,.96);overflow:auto;padding:clamp(18px,5vh,56px) clamp(16px,6vw,96px)}
#ov[hidden]{display:none}
#ov h2{margin-bottom:1.2rem;font-size:clamp(22px,2.4vw,38px)}
.ovg{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.7rem}
.ovi{font:inherit;text-align:left;display:flex;gap:.7rem;align-items:baseline;padding:.75rem .9rem;background:var(--panel);
  border:1px solid var(--edge);border-radius:10px;cursor:pointer;color:var(--ink);font-size:.95rem}
.ovi:hover{border-color:var(--edge-hot);color:var(--orange-2)}
.ovi.cur{border-color:var(--edge-hot);background:rgba(255,138,20,.12)}
.ovi .mono{color:var(--orange);font-weight:700;width:1.8rem;flex:none}
/* ------------------------------------------------ титул */
.tslide .wrap{max-width:82rem}
.tsub{margin-top:1.1rem;color:var(--dim);font-size:clamp(15px,1.4vw,24px);line-height:1.5;max-width:52ch}
.tmeta{margin-top:2.4rem;display:flex;flex-wrap:wrap;gap:.6rem}
.tchip{border:1px solid var(--edge);border-radius:8px;padding:.45em .8em;font-family:var(--mono);font-size:.88rem;color:var(--orange-2)}
/* ------------------------------------------------ адаптив */
@media (min-width:768px){
  .g2{grid-template-columns:repeat(2,minmax(0,1fr))}
  .g3{grid-template-columns:repeat(2,minmax(0,1fr))}
  .g4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .g5{grid-template-columns:repeat(3,minmax(0,1fr))}
  .steprow{grid-template-columns:repeat(3,minmax(0,1fr))}
  .two{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .opts{grid-template-columns:repeat(2,minmax(0,1fr))}
  .trainer{grid-template-columns:minmax(0,1.55fr) minmax(0,1fr)}
}
@media (min-width:1280px){
  .g3{grid-template-columns:repeat(3,minmax(0,1fr))}
  .g4{grid-template-columns:repeat(4,minmax(0,1fr))}
  .g5{grid-template-columns:repeat(5,minmax(0,1fr))}
  .two.w{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)}
  .two.n{grid-template-columns:minmax(0,1fr) minmax(0,1.3fr)}
}
@media (max-width:767px){
  html{font-size:15px}
  h2{font-size:min(30px,7.4vw)}
  h1{font-size:min(30px,8.6vw)}
  .sc{padding-bottom:8.5rem}
  .bits{grid-template-columns:minmax(0,1fr)}
  .tbody,.tscroll,.cols{font-size:12.5px}
  .tw{min-height:20rem}
  #nav{bottom:8px;width:calc(100vw - 16px);justify-content:center;flex-wrap:wrap}
  #nav .lb{display:none}
  .lsc{grid-auto-flow:row;grid-template-rows:none}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition:none!important;animation:none!important}
}
@media print{
  html,body{overflow:visible;height:auto;background:#fff;color:#000}
  #bg,#nav,#prog,#ov{display:none}
  .slide{display:block;position:relative;height:auto;page-break-after:always}
  [data-step]{opacity:1;transform:none}
}
/* ------------------------------------------------ появление и исчезновение */
.fade{opacity:0;transition:opacity .4s var(--ez)}
.fade.on{opacity:1}
.nw{color:var(--orange-2)}
.vanish{transition:opacity .45s var(--ez),transform .45s var(--ez)}
.vanish.gone{opacity:0;transform:translateY(-4px)}
.card.warn{border-color:rgba(255,95,87,.5)}
.card.warn::before{background:linear-gradient(90deg,transparent,rgba(255,95,87,.7),transparent)}
.card.warn::after{background:radial-gradient(ellipse at center,rgba(255,95,87,.18),transparent 68%)}
.nbox.red{color:var(--red);border-color:rgba(255,95,87,.5)}
.cbody b.red,.cbody .red{color:#ff8f88}
/* ------------------------------------------------ столбик уровней */
.stack{display:flex;flex-direction:column;gap:.55rem;align-self:start}
.lyr{position:relative;display:grid;grid-template-columns:auto 1fr;grid-template-areas:"n t" "n s";
  gap:0 .9rem;align-items:center;background:var(--panel);border:1px solid var(--edge);border-radius:var(--r);
  padding:.75rem 1rem;overflow:hidden}
.lyr::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:linear-gradient(180deg,var(--orange),var(--ember))}
.lyn{grid-area:n;font-size:1.25rem;font-weight:900;color:var(--orange);letter-spacing:-.04em}
.lyt{grid-area:t;font-weight:700;font-size:1rem}
.lys{grid-area:s;color:var(--dim);font-size:.82rem}
/* ------------------------------------------------ таблица каталогов */
.tbl.dirs th:first-child{white-space:nowrap;font-weight:700}
.tbl.dirs td:first-of-type{white-space:nowrap}
.tbl tbody th{color:var(--ink);font-weight:600;text-align:left}
.tbl th,.tbl td{text-align:left;padding:.5rem .9rem;border-bottom:1px solid rgba(255,138,20,.14);vertical-align:top}
.tbl{width:100%;border-collapse:collapse;font-size:.97rem;line-height:1.5}
.tbl thead th{background:rgba(255,138,20,.1);color:var(--orange);font-size:.82rem;letter-spacing:.06em;
  text-transform:uppercase;font-weight:700;position:sticky;top:0}
.tbw{overflow:auto;max-height:64vh;align-self:start}
.tbw.card{padding:0;display:block;align-self:start}
/* ------------------------------------------------ девять символов */
.perm9{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;text-align:center}
.pgrp{border:1px solid var(--edge);border-radius:var(--r);padding:1rem .8rem;background:var(--panel-2)}
.pch{font-size:clamp(24px,3vw,44px);font-weight:900;color:var(--orange);letter-spacing:.14em}
.plb{margin-top:.45rem;color:#dcd7d1;font-size:.88rem}
.steps li b{color:var(--ink)}
@media (max-width:767px){.perm9{grid-template-columns:1fr;gap:.6rem}.tbw{max-height:none}}
/* ------------------------------------------------ плотные слайды */
.tight .sc{padding-top:clamp(16px,3.4vh,34px)}
.tight .sh{margin-bottom:1rem}
.tight .card{padding:.85rem 1rem}
.tight .vstack{gap:.7rem}
.tight .cbody,.tight .steps li{font-size:.95rem;line-height:1.52}
.tight .tbl{font-size:.92rem}
.tight .tbl th,.tight .tbl td{padding:.38rem .8rem}
.tight .pgrp{padding:.7rem .6rem}
.tight .pch{font-size:clamp(20px,2.3vw,34px)}
.tight .tbody{font-size:13px}
.tight h3{font-size:.98rem;margin-bottom:.3rem}
.tight .plb{font-size:.8rem;margin-top:.3rem}
.tight .pgrp{padding:.55rem .6rem}
/* ------------------------------------------------ талисман */
.mascot{position:absolute;right:clamp(14px,4vw,86px);bottom:clamp(88px,11vh,132px);
  width:clamp(104px,13vw,232px);height:auto;pointer-events:none;z-index:3;
  filter:drop-shadow(0 16px 32px rgba(0,0,0,.55))}
.rmini{width:2.3rem;height:auto;flex:none}
.taskhead{display:flex;align-items:center;gap:.6rem;margin-bottom:.6rem}
.taskhead h3{margin:0}
@media (max-width:767px){.mascot{width:96px;right:8px;bottom:9.5rem;opacity:.85}}
.tight .perm9{gap:.7rem}
.tight .pch{font-size:clamp(18px,2vw,30px);letter-spacing:.1em}
.tight .info p{font-size:.92rem;line-height:1.5}
"""

# ---------------------------------------------------------------- JS
JS = r"""
(function(){
'use strict';
function $(s,r){return (r||document).querySelector(s);}
function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
var RM=window.matchMedia('(prefers-reduced-motion: reduce)');
var slides=$$('.slide'), N=slides.length, cur=0, step=0;

/* ============================================================ печать в терминале */
function prep(el){
  if(el._atoms) return;
  var atoms=[];
  [].forEach.call(el.childNodes,function(n){
    var cls=(n.nodeType===1?n.className:'')||'';
    var txt=n.textContent||'';
    for(var i=0;i<txt.length;i++) atoms.push([cls,txt.charAt(i)]);
  });
  el._atoms=atoms;
}
function draw(el,n){
  var out='',cls=null,buf='',i,a;
  for(i=0;i<n;i++){
    a=el._atoms[i];
    if(a[0]!==cls){ if(buf) out+=(cls?'<span class="'+cls+'">'+esc(buf)+'</span>':esc(buf)); cls=a[0]; buf=''; }
    buf+=a[1];
  }
  if(buf) out+=(cls?'<span class="'+cls+'">'+esc(buf)+'</span>':esc(buf));
  el.innerHTML=out;
}
function termLines(t){ return $$('.tline[data-cmd]',t); }
function termReset(t){
  clearTimeout(t._tm); t._tm=null; t._run=false; t._done=false;
  termLines(t).forEach(function(l){
    var c=$('.tcmd',l); prep(c); draw(c,0);
    var cu=$('.cur',l); if(cu){ cu.className='cur off'; }
  });
  $$('.tout',t).forEach(function(o){ o.hidden=true; });
  $$('[data-after]',t.parentNode||t).forEach(function(e){ e.classList.remove('on'); });
  $$('[data-gone]',t.parentNode||t).forEach(function(e){ e.classList.remove('gone'); });
}
function termAll(t){
  clearTimeout(t._tm);
  termLines(t).forEach(function(l){ var c=$('.tcmd',l); prep(c); draw(c,c._atoms.length); var cu=$('.cur',l); if(cu) cu.className='cur off'; });
  $$('.tout',t).forEach(function(o){ o.hidden=false; });
  var ls=termLines(t), last=ls[ls.length-1];
  if(last){ var cu=$('.cur',last); if(cu) cu.className='cur'; }
  t._done=true; t._run=false;
  var i; for(i=0;i<ls.length;i++) fire(t,i);
}
function fire(t,i){
  var slide=t.closest('.slide');
  var ev;
  try{ ev=new CustomEvent('tstep',{detail:{i:i,term:t}}); }
  catch(e){ ev=document.createEvent('CustomEvent'); ev.initCustomEvent('tstep',false,false,{i:i,term:t}); }
  t.dispatchEvent(ev); if(slide) slide.dispatchEvent(ev);
  var sc=t.parentNode;
  $$('[data-after="'+i+'"]',sc).forEach(function(e){ e.classList.add('on'); });
  $$('[data-gone="'+i+'"]',sc).forEach(function(e){ e.classList.add('gone'); });
}
function termRun(t){
  termReset(t);
  if(RM.matches){ termAll(t); return; }
  t._run=true;
  var lines=termLines(t), li=0, ci=0;
  function nextLine(){
    if(li>=lines.length){
      var last=lines[lines.length-1];
      if(last){ var cu=$('.cur',last); if(cu) cu.className='cur'; }
      t._run=false; t._done=true; return;
    }
    var l=lines[li], c=$('.tcmd',l), cu=$('.cur',l);
    prep(c); ci=0;
    if(cu) cu.className='cur blink';
    (function type(){
      if(!t._run) return;
      if(ci<=c._atoms.length){ draw(c,ci); ci++; t._tm=setTimeout(type,28); return; }
      if(cu) cu.className='cur off';
      t._tm=setTimeout(function(){
        var out=l.nextElementSibling;
        if(out&&out.classList.contains('tout')) out.hidden=false;
        fire(t,li);
        li++; t._tm=setTimeout(nextLine,260);
      },320);
    })();
  }
  nextLine();
}
function termStart(t){ if(!t._run&&!t._done) termRun(t); }
$$('.term[data-term]').forEach(function(t){
  termReset(t);
  t.addEventListener('click',function(){ termRun(t); });
});

/* ============================================================ шаги и слайды */
slides.forEach(function(s){
  var els=$$('[data-step]',s), mx=0;
  els.forEach(function(e){ var v=+e.getAttribute('data-step')||0; if(v>mx) mx=v; });
  s._els=els; s._max=mx;
});
function startVisibleTerms(s){
  $$('.term[data-term]',s).forEach(function(t){
    var host=t.closest('[data-step]');
    if(!host||host.classList.contains('in')) termStart(t);
  });
}
function setStep(k,instant){
  var s=slides[cur];
  step=Math.max(0,Math.min(s._max,k));
  if(instant) s.classList.add('ni');
  s._els.forEach(function(e){ e.classList.toggle('in',(+e.getAttribute('data-step'))<=step); });
  if(instant){ void s.offsetWidth; s.classList.remove('ni'); }
  if(!instant&&step>0){
    var cu=null;
    s._els.forEach(function(e){ if((+e.getAttribute('data-step'))===step&&!cu) cu=e; });
    if(cu&&cu.scrollIntoView){ try{ cu.scrollIntoView({block:'nearest',inline:'nearest'}); }catch(err){} }
  }
  var ev;
  try{ ev=new CustomEvent('stepchange',{detail:step}); }
  catch(e){ ev=document.createEvent('CustomEvent'); ev.initCustomEvent('stepchange',false,false,step); }
  s.dispatchEvent(ev);
  startVisibleTerms(s);
  ui();
}
function go(i,atEnd){
  i=Math.max(0,Math.min(N-1,i));
  var prevS=slides[cur];
  $$('.term[data-term]',prevS).forEach(function(t){ clearTimeout(t._tm); t._run=false; });
  slides.forEach(function(s){ s.classList.remove('on'); });
  cur=i; slides[cur].classList.add('on');
  var sc=$('.sc',slides[cur]); if(sc) sc.scrollTop=0;
  $$('.term[data-term]',slides[cur]).forEach(termReset);
  setStep(atEnd?slides[cur]._max:0,true);
  try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
}
function nextStep(){ if(step<slides[cur]._max) setStep(step+1); else if(cur<N-1) go(cur+1); }
function prevStep(){ if(step>0) setStep(step-1); else if(cur>0) go(cur-1,true); }
function nextSlide(){ if(cur<N-1) go(cur+1); }
function prevSlide(){ if(cur>0) go(cur-1); }
var ind=$('#ind');
function ui(){
  var mx=slides[cur]._max;
  ind.innerHTML='<b>'+(cur+1)+'</b> / '+N+(mx?' <span class="st">&middot; '+step+'/'+mx+'</span>':'');
  $('#prog i').style.width=((cur+1)/N*100)+'%';
}
$('#b-prev').onclick=prevStep;
$('#b-next').onclick=nextStep;
$('#b-rep').onclick=function(){ replay(); };
function replay(){
  var s=slides[cur], ts=$$('.term[data-term]',s);
  if(ts.length){ ts.forEach(function(t){ var h=t.closest('[data-step]'); if(!h||h.classList.contains('in')) termRun(t); }); }
  else setStep(0,true);
}
/* ---- содержание ---- */
var ov=$('#ov'), ovg=$('.ovg',ov);
slides.forEach(function(s,k){
  var b=document.createElement('button');
  b.className='ovi'; b.type='button';
  b.innerHTML='<span class="mono">'+(k+1<10?'0':'')+(k+1)+'</span><span></span>';
  b.lastChild.textContent=s.getAttribute('data-label')||('Слайд '+(k+1));
  b.onclick=function(){ closeOv(); go(k); };
  ovg.appendChild(b);
});
function openOv(){ ov.hidden=false; $$('.ovi',ov).forEach(function(b,k){ b.classList.toggle('cur',k===cur); }); var c=$('.ovi.cur',ov); if(c) c.focus(); }
function closeOv(){ ov.hidden=true; }
$('#b-ov').onclick=openOv;
/* ---- клавиатура ---- */
var dbuf='', dtm=null;
document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  var t=e.target, tag=t.tagName;
  var inField=(tag==='INPUT'||tag==='TEXTAREA');
  if(e.key==='Escape'){
    if(inField){ t.blur(); return; }
    e.preventDefault(); ov.hidden?openOv():closeOv(); return;
  }
  if(inField) return;              /* поле терминала управляет собой само */
  if(!ov.hidden) return;
  switch(e.key){
    case 'ArrowRight': e.preventDefault(); nextStep(); return;
    case 'ArrowLeft': e.preventDefault(); prevStep(); return;
    case ' ': if(tag==='BUTTON') return; e.preventDefault(); nextStep(); return;
    case 'ArrowDown': case 'PageDown': e.preventDefault(); nextSlide(); return;
    case 'ArrowUp': case 'PageUp': e.preventDefault(); prevSlide(); return;
    case 'Home': e.preventDefault(); go(0); return;
    case 'End': e.preventDefault(); go(N-1); return;
  }
  var k=e.key.toLowerCase();
  if(k==='r'||k==='к'){ e.preventDefault(); replay(); return; }
  if(/^[0-9]$/.test(e.key)){
    dbuf+=e.key; clearTimeout(dtm);
    dtm=setTimeout(function(){ var n=parseInt(dbuf,10); dbuf=''; if(n>=1&&n<=N) go(n-1); },550);
  }
});
/* ---- колесо и касания ---- */
var lastWheel=0;
window.addEventListener('wheel',function(e){
  if(!ov.hidden) return;
  if(e.target.closest&&e.target.closest('.tscroll,.tbody,.cols,.sc.x')) return;
  var sc=$('.sc',slides[cur]); if(!sc) return;
  var dy=e.deltaY; if(Math.abs(dy)<4) return;
  if(dy>0&&sc.scrollTop+sc.clientHeight<sc.scrollHeight-2) return;
  if(dy<0&&sc.scrollTop>0) return;
  var now=Date.now(); if(now-lastWheel<420) return; lastWheel=now;
  dy>0?nextSlide():prevSlide();
},{passive:true});
var tx=0,ty=0,tt=0;
window.addEventListener('touchstart',function(e){ var p=e.changedTouches[0]; tx=p.clientX; ty=p.clientY; tt=Date.now(); },{passive:true});
window.addEventListener('touchend',function(e){
  var p=e.changedTouches[0], dx=p.clientX-tx, dy=p.clientY-ty;
  if(Date.now()-tt>700||Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy)*1.4) return;
  if(e.target.closest&&e.target.closest('input,.tw,.tbody,.cols')) return;
  dx<0?nextStep():prevStep();
},{passive:true});

/* ============================================================ разбор вывода ls -l */
$$('[data-hook="cols"]').forEach(function(box){
  var s=box.closest('.slide');
  s.addEventListener('stepchange',function(ev){
    var k=ev.detail;
    $$('[data-col]',box).forEach(function(c){ c.classList.toggle('hot',(+c.getAttribute('data-col'))===k); });
    $$('.exp',box).forEach(function(x){ x.classList.toggle('on',(+x.getAttribute('data-exp'))===k); });
  });
});

/* ============================================================ дерево каталогов */
$$('[data-hook="tree"]').forEach(function(box){
  var nodes=$$('.nd',box), bar=$('.pathbar b',box);
  function mark(p){
    nodes.forEach(function(n){
      var np=n.getAttribute('data-p');
      n.classList.toggle('path',!!p&&(p===np||p.indexOf(np==='/'?'/':(np+'/'))===0));
    });
    if(bar) bar.textContent=p||'/';
  }
  nodes.forEach(function(n){
    n.addEventListener('mouseenter',function(){ mark(n.getAttribute('data-p')); });
    n.addEventListener('focus',function(){ mark(n.getAttribute('data-p')); });
  });
  box.addEventListener('mouseleave',function(){ mark(box.getAttribute('data-home')||''); });
  mark(box.getAttribute('data-home')||'');
});

/* ============================================================ маркер текущего каталога */
$$('[data-hook="cwd"]').forEach(function(box){
  var t=$('.term[data-term]',box), list=(box.getAttribute('data-cwd')||'').split('|');
  function set(p){ $$('.nd',box).forEach(function(n){ n.classList.toggle('cwd',n.getAttribute('data-p')===p); }); }
  set(list[0]||'');
  if(t){
    t.addEventListener('tstep',function(ev){ var p=list[ev.detail.i+1]; if(p) set(p); });
    t.addEventListener('click',function(){ setTimeout(function(){ set(list[0]||''); },0); });
  }
});

/* ============================================================ биты прав доступа */
$$('[data-hook="bits"]').forEach(function(box){
  var groups=$$('.bgrp',box), oct=$('.octal',box), sym=$('.symb',box);
  function upd(){
    var digits='', s='';
    groups.forEach(function(g){
      var v=0, str='';
      $$('.bb',g).forEach(function(b){
        var on=b.getAttribute('aria-pressed')==='true';
        if(on) v+=+b.getAttribute('data-w');
        str+= on?b.getAttribute('data-l'):'-';
      });
      $('.bval',g).textContent=v;
      digits+=v; s+=str;
    });
    if(oct) oct.textContent=digits;
    if(sym) sym.textContent='-'+s;
  }
  $$('.bb',box).forEach(function(b){
    b.addEventListener('click',function(){
      b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true'); upd();
    });
  });
  upd();
});

/* ============================================================ подбор дистрибутива */
$$('[data-hook="pick"]').forEach(function(box){
  var cards=$$('.pick',box), chosen={};
  $$('.opt',box).forEach(function(b){
    b.addEventListener('click',function(){
      var q=b.getAttribute('data-q');
      $$('.opt[data-q="'+q+'"]',box).forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); });
      chosen[q]=b.getAttribute('data-v');
      apply();
    });
  });
  var rs=$('.presult',box);
  function apply(){
    var keys=Object.keys(chosen), fit=[];
    cards.forEach(function(c){
      var tags=(c.getAttribute('data-tags')||'').split(' ');
      var ok=keys.every(function(k){ return tags.indexOf(chosen[k])>=0; });
      c.classList.toggle('off',!ok);
      if(ok) fit.push(c.getAttribute('data-name'));
    });
    if(rs) rs.textContent=keys.length?(fit.length?('Подходит: '+fit.join(', ')):'Под такой набор в списке ничего нет — ослабьте одно из условий'):'';
  }
  var rb=$('.preset',box);
  if(rb) rb.addEventListener('click',function(){
    chosen={}; $$('.opt',box).forEach(function(x){ x.setAttribute('aria-pressed','false'); }); apply();
  });
  apply();
});

/* ============================================================ тренажёр «живой терминал» */
(function(){
  var box=$('[data-hook="shell"]'); if(!box) return;
  var scr=$('.tscroll',box), inp=$('.tin input',box), pmt=$('.tin .pmt',box);
  var HOME=['home','kali'];
  var FS0={t:'d',c:{
    home:{t:'d',c:{kali:{t:'d',c:{
      Desktop:{t:'d',c:{}},
      Documents:{t:'d',c:{'notes.txt':{t:'f',s:842},'plan.md':{t:'f',s:310}}},
      Downloads:{t:'d',c:{'archive.tar.gz':{t:'f',s:20480}}},
      Pictures:{t:'d',c:{}},
      Templates:{t:'d',c:{}},
      '.bashrc':{t:'f',s:3771},
      'report.txt':{t:'f',s:1204}
    }}}},
    etc:{t:'d',c:{'hosts':{t:'f',s:221},'passwd':{t:'f',s:2914}}},
    var:{t:'d',c:{log:{t:'d',c:{'syslog':{t:'f',s:65536}}}}},
    usr:{t:'d',c:{bin:{t:'d',c:{}},share:{t:'d',c:{}}}}
  }};
  var fs, cwd, hist=[], hi=-1, lsLong=false;
  function clone(o){ return JSON.parse(JSON.stringify(o)); }
  function node(parts){
    var n=fs,i;
    for(i=0;i<parts.length;i++){ if(!n.c||!n.c[parts[i]]) return null; n=n.c[parts[i]]; }
    return n;
  }
  function pstr(parts){
    var h=HOME.join('/'), p=parts.join('/');
    if(p===h) return '~';
    if(p.indexOf(h+'/')===0) return '~/'+p.slice(h.length+1);
    return '/'+p;
  }
  function resolve(arg){
    var parts;
    if(arg==='~'||arg.indexOf('~/')===0) parts=HOME.concat(arg.slice(2)?arg.slice(2).split('/'):[]);
    else if(arg.charAt(0)==='/') parts=arg.split('/').filter(Boolean);
    else parts=cwd.concat(arg.split('/').filter(Boolean));
    var out=[],i;
    for(i=0;i<parts.length;i++){
      if(parts[i]==='.') continue;
      if(parts[i]==='..'){ out.pop(); continue; }
      out.push(parts[i]);
    }
    return out;
  }
  function prompt(){ return 'kali@kali:'+pstr(cwd)+'$'; }
  function setPrompt(){ pmt.innerHTML='kali@kali<span class="tdim">:</span><span class="pp">'+esc(pstr(cwd))+'</span><span class="tdim">$</span>'; }
  function out(html,cls){
    var d=document.createElement('div');
    if(cls) d.className=cls;
    d.innerHTML=html; scr.appendChild(d); scr.scrollTop=scr.scrollHeight;
  }
  function echo(cmd){
    out('<span class="pmt">kali@kali<span class="tdim">:</span><span class="pp">'+esc(pstr(cwd))+'</span><span class="tdim">$</span></span> '+esc(cmd),'tline');
  }
  function names(n,all){
    return Object.keys(n.c||{}).filter(function(k){ return all||k.charAt(0)!=='.'; }).sort();
  }
  function lsHtml(n,flags){
    var all=flags.indexOf('a')>=0, list=names(n,all);
    if(all) list=['.','..'].concat(list);
    if(!list.length) return '';
    if(flags.indexOf('l')>=0){
      var rows=list.map(function(k){
        var it=(k==='.'?n:(k==='..'?n:n.c[k]))||{t:'d'};
        var d=it.t==='d';
        return (d?'drwxr-xr-x':'-rw-r--r--')+' 1 kali kali '+String(d?4096:(it.s||0))+' Oct 10 12:30 '+
               (d?'<span class="dir">'+esc(k)+'</span>':esc(k));
      });
      return 'итого '+list.length+'\n'+rows.join('\n');
    }
    return '<span class="lsc" style="--rows:'+Math.max(1,Math.ceil(list.length/4))+'">'+list.map(function(k){
      var it=n.c&&n.c[k];
      var d=(k==='.'||k==='..'||(it&&it.t==='d'));
      return '<span'+(d?' class="dir"':'')+'>'+esc(k)+'</span>';
    }).join('')+'</span>';
  }
  function parse(line){
    var toks=line.trim().split(/\s+/).filter(Boolean);
    var cmd=toks.shift()||'', flags='', args=[];
    toks.forEach(function(t){
      if(t.charAt(0)==='-'&&t.length>1) flags+=t.replace(/-/g,'');
      else args.push(t);
    });
    return {cmd:cmd,flags:flags,args:args};
  }
  function run(line){
    var p=parse(line), n, tgt, name, dst, i;
    switch(p.cmd){
      case '': return;
      case 'help':
        out('Доступные команды: pwd, ls, cd, touch, mkdir, rm, cp, mv, cat, clear, help\n'+
            'Флаги: ls -l, ls -a, mkdir -p, rm -r'); return;
      case 'clear': scr.innerHTML=''; return;
      case 'pwd': out(esc('/'+cwd.join('/'))); return;
      case 'ls':
        tgt=p.args.length?resolve(p.args[0]):cwd;
        n=node(tgt);
        if(!n){ out('ls: невозможно получить доступ к \''+esc(p.args[0])+'\': Нет такого файла или каталога','red'); return; }
        if(n.t==='f'){ out(esc(p.args[0])); return; }
        if(p.flags.indexOf('l')>=0&&tgt.join('/')===cwd.join('/')) lsLong=true;
        var h=lsHtml(n,p.flags); if(h) out(h);
        return;
      case 'cd':
        tgt=p.args.length?resolve(p.args[0]):HOME.slice();
        n=node(tgt);
        if(!n){ out('bash: cd: '+esc(p.args[0])+': Нет такого файла или каталога','red'); return; }
        if(n.t!=='d'){ out('bash: cd: '+esc(p.args[0])+': Не каталог','red'); return; }
        cwd=tgt; setPrompt(); return;
      case 'touch':
        if(!p.args.length){ out('touch: пропущен операнд','red'); return; }
        for(i=0;i<p.args.length;i++){
          tgt=resolve(p.args[i]); name=tgt.pop(); n=node(tgt);
          if(!n||n.t!=='d'){ out('touch: невозможно выполнить touch для \''+esc(p.args[i])+'\': Нет такого файла или каталога','red'); continue; }
          if(!n.c[name]) n.c[name]={t:'f',s:0};
        }
        return;
      case 'mkdir':
        if(!p.args.length){ out('mkdir: пропущен операнд','red'); return; }
        for(i=0;i<p.args.length;i++){
          tgt=resolve(p.args[i]);
          if(p.flags.indexOf('p')>=0){
            n=fs;
            tgt.forEach(function(seg){ if(!n.c[seg]) n.c[seg]={t:'d',c:{}}; n=n.c[seg]; });
          }else{
            name=tgt.pop(); n=node(tgt);
            if(!n||n.t!=='d'){ out('mkdir: невозможно создать каталог \''+esc(p.args[i])+'\': Нет такого файла или каталога','red'); continue; }
            if(n.c[name]){ out('mkdir: невозможно создать каталог \''+esc(p.args[i])+'\': Файл существует','red'); continue; }
            n.c[name]={t:'d',c:{}};
          }
        }
        return;
      case 'rmdir':
        for(i=0;i<p.args.length;i++){
          tgt=resolve(p.args[i]); name=tgt.pop(); n=node(tgt);
          if(!n||!n.c[name]){ out('rmdir: не удалось удалить \''+esc(p.args[i])+'\': Нет такого файла или каталога','red'); continue; }
          if(Object.keys(n.c[name].c||{}).length){ out('rmdir: не удалось удалить \''+esc(p.args[i])+'\': Каталог не пуст','red'); continue; }
          delete n.c[name];
        }
        return;
      case 'rm':
        if(!p.args.length){ out('rm: пропущен операнд','red'); return; }
        for(i=0;i<p.args.length;i++){
          tgt=resolve(p.args[i]); name=tgt.pop(); n=node(tgt);
          if(!n||!n.c[name]){ out('rm: невозможно удалить \''+esc(p.args[i])+'\': Нет такого файла или каталога','red'); continue; }
          if(n.c[name].t==='d'&&p.flags.indexOf('r')<0){ out('rm: невозможно удалить \''+esc(p.args[i])+'\': Это каталог','red'); continue; }
          delete n.c[name];
        }
        return;
      case 'cp':
      case 'mv':
        if(p.args.length<2){ out(p.cmd+': пропущен операнд назначения','red'); return; }
        tgt=resolve(p.args[0]); name=tgt.pop(); n=node(tgt);
        if(!n||!n.c[name]){ out(p.cmd+': невозможно выполнить stat для \''+esc(p.args[0])+'\': Нет такого файла или каталога','red'); return; }
        var src=n.c[name];
        if(src.t==='d'&&p.cmd==='cp'&&p.flags.indexOf('r')<0){ out('cp: -r не задан; пропускается каталог \''+esc(p.args[0])+'\'','red'); return; }
        dst=resolve(p.args[1]);
        var dn=node(dst), dname;
        if(dn&&dn.t==='d'){ dname=name; }
        else{ dname=dst.pop(); dn=node(dst); }
        if(!dn||dn.t!=='d'){ out(p.cmd+': невозможно создать \''+esc(p.args[1])+'\': Нет такого файла или каталога','red'); return; }
        dn.c[dname]=clone(src);
        if(p.cmd==='mv'){ var pn=node(resolve(p.args[0]).slice(0,-1)); delete pn.c[name]; }
        return;
      case 'cat':
        if(!p.args.length){ out('cat: пропущен операнд','red'); return; }
        tgt=resolve(p.args[0]); n=node(tgt);
        if(!n){ out('cat: '+esc(p.args[0])+': Нет такого файла или каталога','red'); return; }
        if(n.t==='d'){ out('cat: '+esc(p.args[0])+': Это каталог','red'); return; }
        out(n.s?('<span class="tdim">'+esc(p.args[0])+': '+n.s+' байт содержимого</span>'):'<span class="tdim">(пустой файл)</span>');
        return;
      default:
        out('bash: '+esc(p.cmd)+': command not found','red');
    }
  }
  /* --- задания --- */
  var TASKS=[
    {t:'Создайте каталог <span class="mono">lab1</span> в домашнем каталоге и перейдите в него',
     ok:function(){ var n=node(HOME.concat('lab1')); return !!n&&n.t==='d'&&cwd.join('/')===HOME.concat('lab1').join('/'); }},
    {t:'Создайте в нём три файла',
     ok:function(){ var n=node(HOME.concat('lab1')); if(!n||!n.c) return false;
       return Object.keys(n.c).filter(function(k){ return n.c[k].t==='f'; }).length>=3; }},
    {t:'Выведите содержимое каталога с флагом <span class="mono">-l</span>',
     ok:function(){ return lsLong&&cwd.join('/')===HOME.concat('lab1').join('/'); }}
  ];
  var tbox=$('.tasks',box);
  TASKS.forEach(function(t,i){
    var d=document.createElement('div');
    d.className='task'; d.innerHTML='<span class="mk">'+(i+1)+'</span><p>'+t.t+'</p>';
    tbox.appendChild(d); t.el=d;
  });
  function check(){ TASKS.forEach(function(t){ if(t.ok()) t.el.classList.add('done'); }); }
  function reset(){
    fs=clone(FS0); cwd=HOME.slice(); hist=[]; hi=-1; lsLong=false;
    scr.innerHTML=''; setPrompt();
    out('<span class="tdim">Учебная оболочка. Команда <span class="c1">help</span> выведет список поддерживаемых команд.</span>');
    TASKS.forEach(function(t){ t.el.classList.remove('done'); });
  }
  inp.addEventListener('keydown',function(e){
    if(e.key==='Enter'){
      var line=inp.value; inp.value='';
      echo(line);
      if(line.trim()){ hist.push(line); }
      hi=hist.length;
      run(line); check();
      scr.scrollTop=scr.scrollHeight;
      e.preventDefault(); return;
    }
    if(e.key==='ArrowUp'){ e.preventDefault(); e.stopPropagation(); if(hi>0){ hi--; inp.value=hist[hi]||''; } return; }
    if(e.key==='ArrowDown'){ e.preventDefault(); e.stopPropagation(); if(hi<hist.length-1){ hi++; inp.value=hist[hi]||''; } else { hi=hist.length; inp.value=''; } return; }
    if(e.key==='Tab'){
      e.preventDefault();
      var v=inp.value, m=v.match(/(\S*)$/)[1], n=node(cwd);
      if(!n||!n.c) return;
      var cand=Object.keys(n.c).filter(function(k){ return k.indexOf(m)===0&&m; });
      if(cand.length===1) inp.value=v.slice(0,v.length-m.length)+cand[0]+(n.c[cand[0]].t==='d'?'/':' ');
      else if(cand.length>1){ echo(v); out(cand.map(esc).join('  ')); }
      return;
    }
    if(e.key==='l'&&e.ctrlKey){ e.preventDefault(); scr.innerHTML=''; }
  });
  $('.tw',box).addEventListener('click',function(e){ if(!e.target.closest('button')) inp.focus(); });
  var rb=$('.sreset',box); if(rb) rb.addEventListener('click',function(){ reset(); inp.focus(); });
  reset();
})();

/* ============================================================ проверь себя */
(function(){
  var box=$('[data-hook="quiz"]'); if(!box) return;
  var Q=window.__QUIZ__||[], i=0, got=Q.map(function(){ return -1; });
  var qn=$('.qn',box), qs=$('.qs',box), qq=$('.qq',box), qo=$('.opts',box), qe=$('.qexp',box);
  function score(){ return got.filter(function(g,k){ return g===Q[k].a; }).length; }
  function show(){
    var q=Q[i], bs=$$('.opt',qo);
    bs[q.a].classList.add('ok');
    if(got[i]!==q.a&&got[i]>=0) bs[got[i]].classList.add('no');
    qe.innerHTML=(got[i]===q.a?'<b>Верно.</b> ':'<b>Неверно.</b> ')+q.e;
    qs.textContent='верно: '+score()+' из '+Q.length;
  }
  function render(){
    var q=Q[i];
    qn.textContent='Вопрос '+(i+1)+' из '+Q.length;
    qq.textContent=q.q; qo.innerHTML=''; qe.innerHTML='';
    q.o.forEach(function(t,k){
      var b=document.createElement('button');
      b.type='button'; b.className='opt'; b.textContent=t;
      b.onclick=function(){ if(got[i]<0){ got[i]=k; show(); } };
      qo.appendChild(b);
    });
    if(got[i]>=0) show(); else qs.textContent='верно: '+score()+' из '+Q.length;
    $('.qprev',box).disabled=(i===0);
    $('.qnext',box).textContent=(i===Q.length-1?'Начать заново':'Следующий вопрос');
  }
  $('.qnext',box).onclick=function(){
    if(i===Q.length-1){ got=Q.map(function(){ return -1; }); i=0; } else i++;
    render();
  };
  $('.qprev',box).onclick=function(){ if(i>0){ i--; render(); } };
  render();
})();

/* ============================================================ старт */
var h=parseInt((location.hash||'').slice(1),10);
go(h>=1&&h<=N?h-1:0);
if(RM.addEventListener) RM.addEventListener('change',function(){ go(cur); });
})();
"""

# ---------------------------------------------------------------- сборка
ICON_L = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
ICON_R = '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
ICON_REP = '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.5-5.8M4 4v5h5"/></svg>'
ICON_GRID = '<svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg>'

SPARKS = [(12, 22), (28, 61), (44, 17), (57, 44), (68, 72), (79, 31), (88, 58), (35, 84), (94, 13), (6, 47)]

def bg():
    sp = "".join(f'<i class="spark" style="left:{x}%;top:{y}%"></i>' for x, y in SPARKS)
    return ('<div id="bg" aria-hidden="true"><div class="glow g1"></div><div class="glow g2"></div>'
            f'<div class="glow g3"></div><div class="horizon"></div><div class="grid"></div>{sp}</div>')

def render():
    out = ['<!doctype html><html lang="ru"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
           '<title>Linux: дистрибутивы и работа в терминале</title>',
           '<style>', CSS, '</style></head><body>',
           bg(), '<div id="prog"><i></i></div><main id="deck">']
    for label, body, cls in S:
        out.append(f'<section class="slide {cls}" data-label="{label}">'
                   f'<div class="sc"><div class="wrap">{body}</div></div></section>')
    out.append('</main>')
    out.append('<nav id="nav" aria-label="Навигация по слайдам">'
               f'<button id="b-prev" type="button" aria-label="Шаг назад">{ICON_L}</button>'
               '<span id="ind" aria-live="polite"></span>'
               f'<button id="b-next" type="button" aria-label="Шаг вперёд">{ICON_R}</button>'
               '<span class="nsep"></span>'
               f'<button id="b-rep" type="button" title="Клавиша R">{ICON_REP}<span class="lb">Повторить</span></button>'
               f'<button id="b-ov" type="button" title="Esc">{ICON_GRID}<span class="lb">Содержание</span></button>'
               '</nav>')
    out.append('<div id="ov" hidden><h2>Содер<span class="o">жание</span></h2><div class="ovg"></div></div>')
    out.append('<script>window.__QUIZ__=' + json.dumps(QUIZ, ensure_ascii=False) + ';</script>')
    out.append('<script>' + JS + '</script></body></html>')
    OUT.write_text("".join(out), encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"{len(S)} слайдов, {kb:.1f} КБ")

render()
