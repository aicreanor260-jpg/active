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

# ---------------------------------------------------------------- слайды
S = []

def slide(label, body, cls=""):
    S.append((label, body, cls))

# ---- 01 --------------------------------------------------------------------
slide("Титул", f"""
<div class="tslide">
  <div class="lbl">Linux</div>
  <h1>Операционная система <span class="o">Linux</span></h1>
  <p class="tsub">Дистрибутивы и работа в терминале</p>
  <div class="card" style="margin-top:2rem;max-width:44rem">
    <div class="cbody">
      <b>Дистрибутив</b> — ядро Linux вместе с системными инструментами, библиотеками и прикладными
      программами, собранное и поддерживаемое как единое целое.
    </div>
  </div>
  {TODO}
  <div class="tmeta">
    <span class="tchip">10 дистрибутивов</span>
    <span class="tchip">18 слайдов</span>
    <span class="tchip">живой терминал</span>
  </div>
</div>""", "tslide")

# ---- 02 --------------------------------------------------------------------
slide("Что такое дистрибутив",
      head("Linux", "Что такое", "дистрибутив", "Одна идея — разные возможности") + f"""
<div class="g4">
  {card("Ядро", "Управляет процессором, памятью, устройствами и файловыми системами. "
                "Одно и то же у всех дистрибутивов, отличается только версией.", num="01", step=1)}
  {card("Системные инструменты", "Оболочка, утилиты работы с файлами, менеджер пакетов, система инициализации. "
                                 "То, с чем работает человек в терминале.", num="02", step=2)}
  {card("Библиотеки", "Готовый код, которым пользуются программы: вывод на экран, работа с сетью, шифрование. "
                      "Ставятся вместе с программами.", num="03", step=3)}
  {card("Приложения", "Браузер, редактор, офис, средства разработки. Набор зависит от того, "
                      "для чего собран дистрибутив.", num="04", step=4)}
</div>
{TODO}
{info("Сменить дистрибутив не значит выучить другую систему: ядро, дерево каталогов и команды "
      "остаются теми же. Меняются <b>набор программ</b>, <b>оформление</b> и <b>менеджер пакетов</b>.", step=5)}""")

# ---- 03 --------------------------------------------------------------------
D1 = [
    ("01", "ubuntu", "Ubuntu", "Выпуски выходят каждые полгода, версии с долгой поддержкой (LTS) — раз в два года. "
                               "Большое сообщество и много готовых инструкций.", "user", "Для новичков"),
    ("02", "debian", "Debian", "Основа для Ubuntu и десятков других систем. Пакеты обновляются осторожно, "
                               "упор на предсказуемость и стабильность.", "server", "Для серверов"),
    ("03", "kali", "Kali Linux", "Сборка для анализа защищённости: инструменты исследования сетей и систем "
                                 "уже установлены и настроены.", "shield", "Для безопасности"),
    ("04", "mx", "MX Linux", "Собран на основе Debian, нетребователен к ресурсам, дополнен собственными "
                             "утилитами настройки системы.", "chip", "Для слабых ПК"),
    ("05", "manjaro", "Manjaro", "Построен на Arch Linux, обновления приходят непрерывно "
                                 "(модель rolling release), свежие версии программ.", "rocket", "Для опытных"),
]
D2 = [
    ("06", "mint", "Linux Mint", "Основан на Ubuntu, привычный рабочий стол и набор программ сразу после установки.",
     "user", "Для новичков"),
    ("07", "solus", "Solus", "Самостоятельная система, не производная от других. Собственный менеджер пакетов eopkg.",
     "desk", "Для рабочего стола"),
    ("08", "fedora", "Fedora", "Площадка, где новые решения появляются раньше других: свежее ядро и свежие библиотеки.",
     "code", "Для разработчиков"),
    ("09", "suse", "openSUSE", "Два варианта выпуска: стабильный Leap и непрерывно обновляемый Tumbleweed. "
                               "Конфигуратор YaST.", "server", "Для серверов"),
    ("10", "deepin", "Deepin", "Китайский дистрибутив с собственной графической оболочкой и набором "
                               "фирменных программ.", "desk", "Для рабочего стола"),
]

def distro_grid(rows, start=1):
    out = ""
    for i, (num, mark, name, desc, ic, tg) in enumerate(rows):
        out += card(name, desc, num=num, logo=MARK[mark], tag=tag(ic, tg), step=start + i)
    return f'<div class="g5">{out}</div>'

slide("Дистрибутивы 01–05",
      head("Linux", "Дистрибутивы", "Linux", "Пять популярных систем и задачи, под которые их выбирают")
      + distro_grid(D1) + TODO)

# ---- 04 --------------------------------------------------------------------
slide("Дистрибутивы 06–10",
      head("Linux", "Дистрибутивы", "Linux", "Продолжение списка: 06—10")
      + distro_grid(D2) + TODO)

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
    <div class="qrow"><span class="qt">Для чего нужна система</span>{opts("use", [("home", "Учёба и дом"), ("server", "Сервер"), ("sec", "Анализ защищённости")])}</div>
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
slide("Терминал: зачем он нужен",
      head("Terminal", "Зачем нужен", "терминал", "Одна строка вместо десятка щелчков мышью")
      + f"""
<div class="two n">
  <div class="vstack">
    {card("", "Терминал — окно, в котором работает <b>командная оболочка</b>. Она читает строку, "
              "запускает программу и показывает её вывод. Всё, что делается мышью в графическом "
              "интерфейсе, здесь делается командой — и наоборот, многое доступно только так.", step=1)}
    {card("Приглашение командной строки",
          '<div class="mono" style="font-size:1.15rem;margin-bottom:.6rem">'
          '<span style="color:var(--ink)">kali@kali</span><span class="tdim">:</span>'
          '<span class="o">~</span><span class="tdim">$</span></div>'
          '<b>kali</b> — имя пользователя, после <b>@</b> — имя компьютера, '
          'после двоеточия — <b>текущий каталог</b> (<span class="mono o">~</span> означает домашний), '
          'символ <b>$</b> — обычный пользователь, <b>#</b> — суперпользователь root.', step=2)}
    {TODO}
  </div>
  <div class="vstack">
    {syn([("Структура:", '<span class="cmd">команда</span> <span class="opt">-флаги</span> <span class="arg">аргументы</span>'),
          ("Пример:", '<span class="cmd">ls</span> <span class="opt">-l</span> <span class="arg">/etc</span>')], step=3)}
    {term([T("whoami", "kali"),
           T("hostname", "kali"),
           T("ls -l /etc/hosts", '-rw-r--r-- 1 root root 221 Oct 10 12:30 hosts')], step=4)}
    {info("Команда — что выполнить, флаги — как именно, аргументы — над чем работать. "
          "Короткие флаги объединяются: <b>-l -h</b> и <b>-lh</b> — одно и то же.", step=5)}
  </div>
</div>""")

# ---- 07 --------------------------------------------------------------------
def nd(name, path, d=True, cls=""):
    return f'<span class="nd {"d" if d else "f"} {cls}" data-p="{path}" tabindex="0">{name}</span>'

slide("Файловая система",
      head("Linux", "Файловая", "система", "Одно дерево от корня, а не отдельные диски с буквами")
      + f"""
<div class="two w">
  <div class="card" data-hook="tree" data-home="/home/kali">
    <div class="tree">
      <div data-step="1">{nd("/", "/")}<span class="tdim">  корень дерева</span></div>
      <div class="lv">
        <div data-step="2">{nd("bin", "/bin")}<span class="tdim">  исполняемые файлы команд</span></div>
        <div data-step="2">{nd("etc", "/etc")}<span class="tdim">  настройки системы</span></div>
        <div data-step="2">{nd("home", "/home")}<span class="tdim">  домашние каталоги пользователей</span></div>
        <div class="lv">
          <div data-step="4">{nd("kali", "/home/kali")}</div>
          <div class="lv">
            <div data-step="5">{nd("Desktop", "/home/kali/Desktop")}</div>
            <div data-step="5">{nd("Documents", "/home/kali/Documents")}</div>
            <div data-step="5">{nd("Downloads", "/home/kali/Downloads")}</div>
            <div data-step="5">{nd("report.txt", "/home/kali/report.txt", d=False)}</div>
          </div>
        </div>
        <div data-step="3">{nd("var", "/var")}<span class="tdim">  журналы и изменяемые данные</span></div>
        <div data-step="3">{nd("usr", "/usr")}<span class="tdim">  программы и их данные</span></div>
        <div data-step="3">{nd("tmp", "/tmp")}<span class="tdim">  временные файлы</span></div>
      </div>
      <div class="pathbar">Путь: <b>/home/kali</b></div>
    </div>
  </div>
  <div class="vstack">
    {card("Абсолютный путь", "Начинается с косой черты и отсчитывается от корня: "
          '<span class="mono o">/home/kali/Documents</span>. Работает откуда угодно.', num="01", step=6)}
    {card("Относительный путь", "Отсчитывается от текущего каталога: "
          '<span class="mono o">Documents/notes.txt</span>. Короче, но зависит от того, где вы находитесь.',
          num="02", step=7)}
    {card("Особые обозначения",
          '<span class="mono o">.</span> — текущий каталог, <span class="mono o">..</span> — родительский, '
          '<span class="mono o">~</span> — домашний каталог пользователя, '
          '<span class="mono o">/</span> — корень.', num="03", step=8)}
    {info("Регистр букв различается: <b>Report.txt</b> и <b>report.txt</b> — два разных файла. "
          "Имена, начинающиеся с точки, считаются скрытыми.", step=9)}
  </div>
</div>""")

# ---- 08 --------------------------------------------------------------------
slide("pwd, ls, cd",
      head("Terminal", "Основные", "команды", "Где я нахожусь, что здесь лежит и как перейти в другой каталог")
      + f"""
<div class="g3" style="margin-bottom:1.1rem">
  {card("pwd", "Печатает абсолютный путь текущего каталога. Первая команда, когда непонятно, где вы оказались.",
        num="01", step=1, big=True)}
  {card("ls", "Показывает содержимое каталога. Без аргументов — текущего, с аргументом — указанного.",
        num="02", step=2, big=True)}
  {card("cd", "Переходит в другой каталог. Без аргументов возвращает в домашний.",
        num="03", step=3, big=True)}
</div>
<div class="two w" data-hook="cwd" data-cwd="/home/kali|/home/kali|/home/kali|/home/kali/Downloads|/home/kali/Downloads|/home/kali">
  {term([T("pwd", "/home/kali"),
         T("ls", lsc([("Desktop", 1), ("Documents", 1), ("Downloads", 1), ("Pictures", 1),
                      ("Templates", 1), ("report.txt", 0)], rows=3)),
         T("cd Downloads", None),
         T("pwd", "/home/kali/Downloads", path="~/Downloads"),
         T("cd ..", None, path="~/Downloads")], step=4)}
  <div class="vstack">
    <div class="card tree" data-step="4">
      <div>{nd("/home", "/home")}</div>
      <div class="lv">
        <div>{nd("kali", "/home/kali", cls="cwd")}</div>
        <div class="lv">
          <div>{nd("Desktop", "/home/kali/Desktop")}</div>
          <div>{nd("Documents", "/home/kali/Documents")}</div>
          <div>{nd("Downloads", "/home/kali/Downloads")}</div>
        </div>
      </div>
    </div>
    {info("Рамкой отмечен текущий каталог: он меняется вместе с командой <b>cd</b>, "
          "а <b>pwd</b> подтверждает новое положение.", step=5)}
  </div>
</div>
{steps(["<b>pwd</b> — узнать, где вы находитесь сейчас.",
        "<b>ls</b> — посмотреть, что лежит рядом.",
        "<b>cd имя</b> — перейти внутрь, <b>cd ..</b> — вернуться на уровень выше."], step=6)}""")

# ---- 09 --------------------------------------------------------------------
COLS = [
    ("-", "тип объекта", "«-» обычный файл, «d» каталог, «l» символьная ссылка."),
    ("rw-r--r--", "права доступа", "Три тройки: владелец, группа, остальные. r — чтение, w — запись, x — исполнение."),
    ("1", "число жёстких ссылок", "Сколько имён в файловой системе указывает на эти же данные."),
    ("kali", "владелец", "Пользователь, которому принадлежит файл."),
    ("kali", "группа", "Группа, которой принадлежит файл."),
    ("0", "размер", "Размер в байтах. С флагом -h — в килобайтах и мегабайтах."),
    ("Oct 10 12:30", "время изменения", "Когда содержимое файла менялось в последний раз."),
    ("test.txt", "имя", "Имя файла или каталога."),
]

def cols_line():
    out = ""
    for i, (v, _, _) in enumerate(COLS):
        out += f'<span data-col="{i + 5}">{v}</span>' + (" " if i < len(COLS) - 1 else "")
    return out

LSLH = ("итого 12K\n"
        'drwxr-xr-x 2 kali kali 4,0K Oct 10 12:30 <span class="dir">Documents</span>\n'
        'drwxr-xr-x 2 kali kali 4,0K Oct 10 12:30 <span class="dir">Downloads</span>\n'
        "-rw-r--r-- 1 kali kali 1,2K Oct 10 12:30 report.txt")
LS_DEMO = term([T("ls -a", lsc([(".", 1), ("..", 1), (".bashrc", 0), ("Documents", 1),
                               ("Downloads", 1), ("report.txt", 0)], rows=3)),
                T("ls -lh", LSLH)], step=4)

slide("Флаги ls",
      head("Terminal", "Команда", "ls", "Один и тот же каталог выглядит по-разному в зависимости от флагов")
      + f"""
<div class="g3" style="margin-bottom:1.1rem">
  {card("ls -l", "Подробный список: права, владелец, размер, дата, имя — по одной строке на объект.",
        num="01", step=1, big=True)}
  {card("ls -a", "Показывает скрытые файлы, чьи имена начинаются с точки, вместе с обычными.",
        num="02", step=2, big=True)}
  {card("ls -lh", "То же, что -l, но размеры в понятном виде: 4,0K вместо 4096.",
        num="03", step=3, big=True)}
</div>
<div class="two w">
  {LS_DEMO}
  <div class="card" data-hook="cols">
    <h3 class="mono">Разбор строки ls -l</h3>
    <div class="cols">{cols_line()}</div>
    <div class="exps">
      """ + "".join(
        f'<div class="exp" data-exp="{i + 5}" data-step="{i + 5}">'
        f'<span class="n">{v}</span><b>{name}</b> — {d}</div>'
        for i, (v, name, d) in enumerate(COLS)) + """
    </div>
  </div>
</div>""")

# ---- 10 --------------------------------------------------------------------
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

slide("touch",
      head("Terminal", "Команда", "touch", "Создание пустых файлов и изменение времени доступа")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">touch</span> <span class="opt">[флаги]</span> <span class="arg">имя_файла</span>'),
          ("Пример:", '<span class="cmd">touch</span> <span class="arg">test.txt</span>')], step=1)}
    {TOUCH_DEMO}
    {info("Файл <b>test.txt</b> появляется в выводе <b>ls</b> сразу после выполнения команды. "
          "Флаг <b>-t</b> задаёт время в формате ГГГГММДДччмм — в подробном выводе видно новую дату.", step=3)}
  </div>
  <div class="g2">
    {card("touch test.txt", "Создаёт пустой файл. Если файл уже есть — содержимое не трогает.",
          num="01", step=4, big=True)}
    {card("touch a.txt b.txt c.txt", "Создаёт сразу несколько файлов одной командой.",
          num="02", step=5, big=True)}
    {card("touch -t 202410101230 f", "Задаёт файлу указанное время: год, месяц, день, часы, минуты.",
          num="03", step=6, big=True)}
    {card("touch report.txt", "Для существующего файла обновляет время последнего изменения на текущее.",
          num="04", step=7, big=True)}
  </div>
</div>
{TODO}""")

# ---- 11 --------------------------------------------------------------------
MK_LS1 = lsc([("Documents", 1), ("Downloads", 1), ("report.txt", 0)], rows=1)
MK_LS2 = lsc([("Documents", 1), ("Downloads", 1),
              ("lab1", 1, "vanish", 'data-gone="4"'), ("report.txt", 0)], rows=1)
MK_DEMO = term([T("mkdir lab1", None),
                T("ls", MK_LS2),
                T("mkdir -p lab2/src/bin", None),
                T("ls lab2/src", lsc([("bin", 1)], rows=1)),
                T("rmdir lab1", None)], step=2)

slide("mkdir, rmdir",
      head("Terminal", "Каталоги:", "mkdir и rmdir", "Создание и удаление каталогов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">mkdir</span> <span class="opt">[-p]</span> <span class="arg">имя_каталога</span>'),
          ("Пример:", '<span class="cmd">mkdir</span> <span class="opt">-p</span> <span class="arg">lab2/src/bin</span>')], step=1)}
    {MK_DEMO}
    {info("Без флага <b>-p</b> команда откажется создавать <b>lab2/src/bin</b>, пока нет "
          "промежуточных каталогов. С флагом создаётся вся цепочка сразу.", step=3)}
  </div>
  <div class="vstack">
    {card("mkdir", "Создаёт каталог в текущем или указанном месте. Несколько имён — несколько каталогов.",
          num="01", step=4, big=True)}
    {card("mkdir -p", "Создаёт всю цепочку вложенных каталогов и не ругается, если каталог уже существует.",
          num="02", step=5, big=True)}
    {card("rmdir", "Удаляет <b>только пустой</b> каталог. Если внутри что-то есть — откажется работать.",
          num="03", step=6, big=True)}
  </div>
</div>
{TODO}""")

# ---- 12 --------------------------------------------------------------------
CP_LS = lsc([("Documents", 1), ("backup.txt", 0, "fade nw", 'data-after="1"'),
             ("plan.md", 0, "fade nw", 'data-after="3"'), ("report.txt", 0)], rows=1)
CP_DEMO = term([T("ls", lsc([("Documents", 1), ("report.txt", 0)], rows=1)),
                T("cp report.txt backup.txt", None),
                T("ls", CP_LS),
                T("mv notes.txt plan.md", None),
                T("mv plan.md Documents/", None)], step=2)

slide("cp, mv",
      head("Terminal", "Копирование:", "cp и mv", "Копировать, переместить, переименовать")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">cp</span> <span class="opt">[-r]</span> <span class="arg">источник назначение</span>'),
          ("Пример:", '<span class="cmd">cp</span> <span class="arg">report.txt backup.txt</span>')], step=1)}
    {CP_DEMO}
    {info("Переименования как отдельной команды в Linux нет: <b>mv старое_имя новое_имя</b> "
          "перемещает файл внутри того же каталога, то есть меняет ему имя.", step=3)}
  </div>
  <div class="vstack">
    {card("cp файл копия", "Копирует файл. Исходный остаётся на месте, появляется второй.",
          num="01", step=4, big=True)}
    {card("cp -r каталог копия", "Копирует каталог со всем содержимым. Без <b>-r</b> каталог не копируется.",
          num="02", step=5, big=True)}
    {card("mv файл каталог/", "Перемещает файл. В исходном месте он исчезает.",
          num="03", step=6, big=True)}
    {card("mv старое новое", "Если назначение не каталог, файл получает новое имя.",
          num="04", step=7, big=True)}
  </div>
</div>
{TODO}""")

# ---- 13 --------------------------------------------------------------------
RM_LS = lsc([("Documents", 1), ("backup.txt", 0, "vanish", 'data-gone="1"'),
             ("lab2", 1, "vanish", 'data-gone="3"'), ("report.txt", 0)], rows=1)
RM_DEMO = term([T("ls", RM_LS),
                T("rm backup.txt", None),
                T("rm lab2", 'rm: невозможно удалить \'lab2\': Это каталог'),
                T("rm -r lab2", None),
                T("ls", lsc([("Documents", 1), ("report.txt", 0)], rows=1))], step=2)

slide("rm",
      head("Terminal", "Удаление:", "rm", "Команда без корзины и без вопросов")
      + f"""
<div class="two w">
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">rm</span> <span class="opt">[-r] [-f]</span> <span class="arg">имя</span>'),
          ("Пример:", '<span class="cmd">rm</span> <span class="opt">-r</span> <span class="arg">lab2</span>')], step=1)}
    {RM_DEMO}
    <div class="card warn" data-step="3">
      <div class="chead"><span class="nbox red">!</span><span class="t">Что важно помнить</span></div>
      <div class="cbody">Удалённое командой <b class="red">rm</b> не попадает в корзину и не восстанавливается
      обычными средствами. Особенно опасны шаблоны: <span class="mono red">rm -rf *</span> в неверном каталоге
      уносит всё его содержимое. Перед удалением по шаблону выполните с ним же <b>ls</b> и посмотрите,
      что попадёт под команду.</div>
    </div>
  </div>
  <div class="vstack">
    {card("rm файл", "Удаляет файл. Каталог так удалить нельзя — команда откажется.",
          num="01", step=4, big=True)}
    {card("rm -r каталог", "Удаляет каталог вместе со всем содержимым, рекурсивно.",
          num="02", step=5, big=True)}
    {card("rm -f файл", "Не задаёт вопросов и не жалуется на отсутствующие файлы. "
                        "Сочетание <b>-rf</b> — самое опасное в системе.", num="03", step=6, big=True)}
    {card("rm -i файл", "Наоборот, спрашивает подтверждение на каждый файл.", num="04", step=7, big=True)}
  </div>
</div>
{TODO}""")

# ---- 14 --------------------------------------------------------------------
CAT_OUT = ('Отчёт по лабораторной работе\n'
           'Дата: 10 октября\n'
           'Исполнитель: kali')
VIEW_DEMO = term([T("cat report.txt", CAT_OUT),
                  T("head -2 report.txt", 'Отчёт по лабораторной работе\nДата: 10 октября'),
                  T("tail -1 report.txt", 'Исполнитель: kali'),
                  T("wc -l report.txt", '3 report.txt')], step=1)

slide("cat, less, head, tail",
      head("Terminal", "Просмотр", "файлов", "Четыре способа заглянуть внутрь, не открывая редактор")
      + f"""
<div class="two w">
  <div class="vstack">
    {VIEW_DEMO}
    {info("Для больших файлов <b>cat</b> неудобен: содержимое пролетает мимо экрана. "
          "Тогда используют <b>less</b> — стрелки листают, <b>/</b> ищет, <b>q</b> выходит.", step=2)}
  </div>
  <div class="g2">
    {card("cat", "Выводит файл целиком. Подходит для коротких файлов и конфигураций.", num="01", step=3, big=True)}
    {card("less", "Постраничный просмотр с поиском. Не загружает файл в память целиком.", num="02", step=4, big=True)}
    {card("head -n", "Первые строки файла, по умолчанию десять.", num="03", step=5, big=True)}
    {card("tail -n", "Последние строки. С флагом <b>-f</b> показывает новые строки по мере появления.",
          num="04", step=6, big=True)}
  </div>
</div>
{TODO}""")

# ---- 15 --------------------------------------------------------------------
def bgrp(title, r, w, x):
    def b(letter, weight, on):
        return (f'<button class="bb" type="button" data-w="{weight}" data-l="{letter}" '
                f'aria-pressed="{"true" if on else "false"}">{letter}</button>')
    return (f'<div class="bgrp"><h4>{title}</h4><div class="bbtns">'
            + b("r", 4, r) + b("w", 2, w) + b("x", 1, x)
            + '</div><div class="bval">0</div></div>')

slide("Права доступа",
      head("Linux", "Права", "доступа", "Кто может читать, изменять и запускать файл")
      + f"""
<div class="two w">
  <div class="vstack">
    {card("", 'Первые десять символов вывода <b>ls -l</b> описывают тип объекта и три набора прав: '
              'для владельца, для его группы и для всех остальных. '
              '<span class="mono o" style="font-size:1.25rem;display:inline-block;margin-top:.5rem">'
              '- rw- r-- r--</span>', step=1)}
    <div class="card" data-hook="bits" data-step="2">
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
    {info("Нажимайте буквы: <b>r</b> даёт 4, <b>w</b> — 2, <b>x</b> — 1. Внутри тройки веса складываются, "
          "и три получившиеся цифры образуют число для <b>chmod</b>.", step=3)}
  </div>
  <div class="vstack">
    {syn([("Синтаксис:", '<span class="cmd">chmod</span> <span class="opt">права</span> <span class="arg">имя</span>'),
          ("Пример:", '<span class="cmd">chmod</span> <span class="opt">755</span> <span class="arg">script.sh</span>')], step=4)}
    {card("chmod 644 файл", "Владелец читает и пишет, остальные только читают. Обычный файл с данными.",
          num="01", step=5, big=True)}
    {card("chmod 755 файл", "Плюс право запуска для всех. Так ставят права скриптам и программам.",
          num="02", step=6, big=True)}
    {card("chmod +x файл", "Символьная форма: добавить право запуска, не трогая остальное.",
          num="03", step=7, big=True)}
    {card("chown пользователь:группа", "Меняет владельца и группу файла. Требует прав суперпользователя.",
          num="04", step=8, big=True)}
  </div>
</div>
{TODO}""")

# ---- 16 --------------------------------------------------------------------
MAN_OUT = ('LS(1)                    User Commands                   LS(1)\n\n'
           'NAME\n'
           '       ls - list directory contents\n\n'
           'SYNOPSIS\n'
           '       ls [OPTION]... [FILE]...')
HELP_OUT = ('Usage: mkdir [OPTION]... DIRECTORY...\n'
            '  -p, --parents     no error if existing, make parent directories as needed\n'
            '  -v, --verbose     print a message for each created directory')
MAN_DEMO = term([T("man ls", MAN_OUT), T("mkdir --help", HELP_OUT)], step=1)

slide("man и --help",
      head("Terminal", "Справка:", "man и --help", "Как отвечать на свои вопросы без поиска в интернете")
      + f"""
<div class="two w">
  <div class="vstack">
    {MAN_DEMO}
    {info("В <b>man</b> листают стрелками, ищут по <b>/слово</b>, выходят клавишей <b>q</b>. "
          "Раздел в скобках после имени — <b>LS(1)</b> — означает: пользовательские команды.", step=2)}
  </div>
  <div class="vstack">
    {card("man команда", "Полное руководство: назначение, синтаксис, все флаги, примеры, связанные команды.",
          num="01", step=3, big=True)}
    {card("команда --help", "Короткая справка прямо в терминале. Быстрее, когда нужно вспомнить один флаг.",
          num="02", step=4, big=True)}
    {card("man -k слово", "Поиск по описаниям всех руководств, когда неизвестно имя нужной команды.",
          num="03", step=5, big=True)}
    {card("whatis команда", "Одна строка: что эта команда делает.", num="04", step=6, big=True)}
    {info("Разделы руководств: 1 — команды, 5 — форматы файлов, 8 — команды администратора. "
          "Отсюда запись <b>man 5 passwd</b> — про формат файла, а не про команду.", step=7)}
  </div>
</div>
{TODO}""")

# ---- 17 --------------------------------------------------------------------
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
      <h3>Задания</h3>
      <div class="tasks"></div>
      <button class="btn sreset" type="button" style="margin-top:.9rem">Сбросить</button>
    </div>
    <div class="info"><span class="ic">i</span><p>Поддерживаются <b>pwd</b>, <b>ls</b>, <b>cd</b>,
      <b>touch</b>, <b>mkdir</b>, <b>rm</b>, <b>cp</b>, <b>mv</b>, <b>cat</b>, <b>clear</b>, <b>help</b>.
      Клавиша <b>Tab</b> дополняет имена файлов, стрелки вверх и вниз листают историю команд.
      Задание засчитывается по состоянию файловой системы — способ решения выбираете сами.</p></div>
  </div>
</div>""")

# ---- 18 --------------------------------------------------------------------
QUIZ = [
    {"q": "Что выведет команда pwd?", "a": 1,
     "o": ["Список файлов текущего каталога", "Абсолютный путь текущего каталога",
           "Имя текущего пользователя", "Размер текущего каталога"],
     "e": "pwd печатает полный путь от корня — например /home/kali/Downloads."},
    {"q": "Какой флаг ls показывает скрытые файлы?", "a": 2,
     "o": ["-l", "-h", "-a", "-r"],
     "e": "Скрытыми считаются файлы, имя которых начинается с точки. Показать их: ls -a."},
    {"q": "Что произойдёт, если выполнить touch для уже существующего файла?", "a": 0,
     "o": ["Обновится время последнего изменения, содержимое останется",
           "Файл будет очищен", "Команда завершится ошибкой", "Будет создана копия файла"],
     "e": "touch не трогает содержимое: для существующего файла команда лишь обновляет отметку времени."},
    {"q": "Как из каталога /home/kali/Downloads вернуться в /home/kali?", "a": 3,
     "o": ["cd /", "cd Downloads", "cd .", "cd .."],
     "e": "Две точки обозначают родительский каталог. Сюда же вернёт cd без аргументов — в домашний каталог."},
    {"q": "Какая команда создаст цепочку каталогов lab/src/bin, если ничего из неё ещё нет?", "a": 1,
     "o": ["mkdir lab/src/bin", "mkdir -p lab/src/bin", "mkdir -r lab/src/bin", "touch -p lab/src/bin"],
     "e": "Флаг -p создаёт все недостающие промежуточные каталоги. Без него команда сообщит об ошибке."},
    {"q": "Чем mv отличается от cp?", "a": 0,
     "o": ["mv перемещает: в исходном месте файл исчезает, cp оставляет оба",
           "mv работает только с каталогами", "cp умеет переименовывать, а mv нет",
           "Разницы нет, это синонимы"],
     "e": "Поэтому mv используют и для переименования: файл «перемещается» в тот же каталог под новым именем."},
    {"q": "Что означает строка прав -rw-r--r--?", "a": 2,
     "o": ["Каталог, доступный всем на запись", "Файл, который может запускать только владелец",
           "Обычный файл: владелец читает и пишет, остальные только читают",
           "Символьная ссылка с полными правами"],
     "e": "Первый символ «-» — обычный файл. Далее rw- у владельца, r-- у группы и r-- у остальных."},
    {"q": "Каким числом задать права rwxr-xr-x в команде chmod?", "a": 1,
     "o": ["644", "755", "777", "700"],
     "e": "rwx = 4+2+1 = 7, r-x = 4+1 = 5, r-x = 5. Получается chmod 755 — обычные права для скриптов."},
]

slide("Проверь себя",
      head("Linux", "Проверь", "себя", "Восемь вопросов по материалу лекции")
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
  --dim:#9b9691;
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
.cbody{color:var(--dim);font-size:.96rem;line-height:1.55}
.cbody b{color:var(--ink);font-weight:600}
.tag{display:inline-flex;align-self:flex-start;align-items:center;gap:.5em;border:1px solid var(--edge);border-radius:8px;
  padding:.4em .7em;font-size:.82rem;color:var(--orange-2);margin-top:auto;margin-block-start:.9rem}
.tag svg{width:1.05em;height:1.05em;fill:none;stroke:var(--orange);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.logo{width:2.6rem;height:2.6rem;flex:none}
.logo svg{width:100%;height:100%;fill:none;stroke:var(--orange);stroke-width:1.4;stroke-linejoin:round}
.circ{display:inline-grid;place-items:center;width:2em;height:2em;flex:none;border:1px solid var(--orange);border-radius:50%;
  background:transparent;color:var(--orange);font-family:var(--mono);font-weight:700;font-size:.9rem}
.steps{display:flex;flex-direction:column;gap:.9rem}
.steps li{display:flex;gap:.9rem;align-items:flex-start;list-style:none;font-size:1rem;line-height:1.55;color:var(--dim)}
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
.info p{color:var(--dim);font-size:.96rem;line-height:1.55}
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
.exps{margin-top:.9rem;min-height:4.2rem}
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
.mini .cbody{font-size:.86rem}
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
.task p{font-size:.92rem;line-height:1.5;color:var(--dim)}
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
.qexp{min-height:3.2rem;margin-top:.8rem;color:var(--dim);font-size:.95rem;line-height:1.55}
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
