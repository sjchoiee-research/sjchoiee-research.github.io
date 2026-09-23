"""Research-led homepage sections. Python standard library only."""
from datetime import date
from html import escape
from itertools import count
import math
import re
_figure_ids = count(1)


def _e(value):
    return escape(str(value if value is not None else ""), quote=True)


def _external(url, label, cls="", aria_label=""):
    aria = f' aria-label="{_e(aria_label)}"' if aria_label else ""
    return (f'<a href="{_e(url)}" class="{_e(cls)}" target="_blank" '
            f'rel="noopener noreferrer"{aria}>{label}</a>')


def _number(value, fallback):
    try:
        number = float(value)
        return number if math.isfinite(number) else fallback
    except (ValueError, TypeError):
        return fallback


def _figure_window(figure, cls="", eager=False):
    """Display an original figure or panel without changing its bitmap."""
    if not figure or not figure.get("src"):
        return ""
    width = max(1, _number(figure.get("width"), 1000))
    height = max(1, _number(figure.get("height"), 700))
    crop = figure.get("crop")
    if isinstance(crop, (list, tuple)) and len(crop) == 4:
        x, y, crop_width, crop_height = [_number(v, 0) for v in crop]
        if crop_width <= 0 or crop_height <= 0:
            x, y, crop_width, crop_height = 0, 0, width, height
    else:
        x, y, crop_width, crop_height = 0, 0, width, height
    description = figure.get("alt") or figure.get("label") or "Research figure"
    clip_id = f'figure-clip-{next(_figure_ids)}'
    # Explicit clipping also excludes adjacent panels in the SVG's letterbox area.
    clip_outline = f'M{x:g},{y:g}h{crop_width:g}v{crop_height:g}h{-crop_width:g}z'
    # Omit panel letters in the display window while retaining the source bitmap.
    for omitted in figure.get("omit_regions", []):
        ox, oy, ow, oh = [_number(v, 0) for v in omitted]
        if ow > 0 and oh > 0:
            clip_outline += f' M{ox:g},{oy:g}h{ow:g}v{oh:g}h{-ow:g}z'
    svg = (f'<svg class="research-panel" xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="{x:g} {y:g} {crop_width:g} {crop_height:g}" '
           f'width="{crop_width:g}" height="{crop_height:g}" role="img" '
           f'aria-label="{_e(description)}">'
           f'<title>{_e(description)}</title>'
           f'<defs><clipPath id="{clip_id}"><path d="{clip_outline}" clip-rule="evenodd"/></clipPath></defs>'
           f'<image href="{_e(figure["src"])}" x="0" y="0" '
           f'width="{width:g}" height="{height:g}" preserveAspectRatio="none" clip-path="url(#{clip_id})"/>'
           '</svg>')
    return _external(figure["src"], svg, "figure-window " + cls,
                     "Open original figure: " + description)


def _authors_markup(authors):
    text = ", ".join(str(a) for a in authors) if isinstance(authors, list) else str(authors or "")
    escaped = _e(text)
    return re.sub(r'(?<!\w)(Sung[- ]Jin Choi|S\.?\s*[-‐‑–]?\s*J\.?\s+Choi|최성진)(?!\w)',
                  r'<strong>\1</strong>', escaped, flags=re.I)


def _date_label(value):
    try:
        parsed = date.fromisoformat(str(value)[:10])
        return f"{parsed.day} {parsed.strftime('%B %Y')}"
    except (ValueError, TypeError):
        return str(value or "Date not recorded")


def hero_visual(C):
    """The right-hand hero figure, centered on actual device research."""
    hero = C.get("hero") or {}
    main = hero.get("main_figure") or {}
    if not main.get("src"):
        return ""
    detail = hero.get("detail_figure") or {}
    additional = hero.get("additional_figure") or {}
    title = hero.get("title") or "From materials to semiconductor devices"
    subtitle = hero.get("subtitle") or ""
    source = hero.get("source_url") or main.get("source_url")
    detail_html = ""
    if detail.get("src"):
        companion = (
            _figure_window(additional, "hero-detail-window")
            if additional.get("src") else
            '<div class="hero-detail-caption"><span class="hero-detail-rule" aria-hidden="true"></span>'
            + f'<p>{_e(detail.get("label") or "A closer look at the fabricated device")}</p></div>'
        )
        detail_html = (
            '<div class="hero-science-detail' + (' has-companion' if additional.get("src") else '') + '">'
            + _figure_window(detail, "hero-detail-window")
            + companion + '</div>'
        )
    source_link = _external(source, 'Paper <span aria-hidden="true">↗</span>',
                            "hero-science-source", "Read the research paper") if source else ""
    return (
        '<figure class="hero-science">'
        '<div class="hero-science-topline"><span>Research in focus</span>'
        '<span class="hero-science-mark" aria-hidden="true">↗</span></div>'
        '<div class="hero-science-main">' + _figure_window(main, "hero-main-window", eager=True) + '</div>'
        + detail_html
        + '<figcaption class="hero-science-caption"><div>'
        + f'<strong>{_e(title)}</strong>'
        + (f'<p>{_e(subtitle)}</p>' if subtitle else "")
        + '</div>' + source_link + '</figcaption></figure>'
    )


def featured_papers(C):
    """All verified selected papers, with text and original figure panels."""
    cards = []
    for paper in C.get("selected", []):
        title = paper.get("title") or paper.get("short_title") or "Selected publication"
        url = paper.get("url") or "publications.html"
        publication_id = paper.get("publication_id")
        role = paper.get("role") or ""
        if isinstance(role, list):
            role = " · ".join(str(item) for item in role)
        figures = [f for f in paper.get("figures", []) if f.get("src")][:2]
        figure_cards = []
        for figure in figures:
            label = figure.get("label") or "Research figure"
            source = figure.get("source_url") or url
            figure_cards.append(
                '<figure class="featured-figure">' + _figure_window(figure)
                + '<figcaption><span>' + _e(label) + '</span>'
                + _external(source, '<span aria-hidden="true">↗</span>', "figure-source",
                            "View the source for " + label)
                + '</figcaption></figure>'
            )
        gallery = ('<div class="featured-figures' + (' is-single' if len(figures) == 1 else '') + (' is-stacked' if paper.get('figure_layout')=='stacked' else '')
                   + '">' + ''.join(figure_cards) + '</div>') if figures else ""
        authors = _authors_markup(paper.get("authors"))
        authors_html = ('<details class="featured-authors"><summary>View authors</summary>'
                        + f'<p>{authors}</p></details>') if authors else ""
        cite_button = (f'<button type="button" data-cite="{_e(publication_id)}" '
                       f'aria-label="Copy citation for {_e(title)}">Cite</button>') if publication_id else ""
        journal = paper.get("journal") or paper.get("journal_abbreviation") or ""
        year = paper.get("year")
        metadata = _e(journal) + (f'<span aria-hidden="true"> · </span><span>{_e(year)}</span>' if year else "")
        cards.append(
            '<article class="featured-paper' + (' has-figures' if gallery else '') + '">'
            '<div class="featured-copy">'
            + (f'<p class="featured-role">{_e(role)}</p>' if role else "")
            + '<h3>' + _external(url, _e(title)) + '</h3>'
            + f'<p class="featured-journal">{metadata}</p>'
            + (f'<p class="featured-summary">{_e(paper["summary"])}</p>' if paper.get("summary") else "")
            + authors_html
            + '<div class="featured-actions">'
            + _external(url, 'DOI <span aria-hidden="true">↗</span>') + cite_button
            + '</div></div>' + gallery + '</article>'
        )
    if not cards:
        return ""
    return (
        '<section class="section featured-section" id="selected-publications" aria-labelledby="featured-heading">'
        '<div class="section-head"><div><div class="section-label">A closer look at our work</div>'
        '<h2 id="featured-heading">Selected publications</h2></div>'
        '<a class="text-link" href="publications.html">All publications '
        '<span class="arrow" aria-hidden="true">↗</span></a></div>'
        '<div class="featured-list">' + ''.join(cards) + '</div></section>'
    )


def scholar_metrics(C):
    """A dated public Scholar snapshot, or the source link when unavailable."""
    metrics = C.get("scholar_metrics") or {}
    profile = metrics.get("profile_url") or C.get("profile", {}).get("scholar_url")
    if not profile:
        return ""
    definitions = [("citations", "Citations"), ("h_index", "h-index"), ("i10_index", "i10-index")]
    valid = all(isinstance(metrics.get(key), (int, float)) and not isinstance(metrics.get(key), bool)
                and math.isfinite(metrics[key]) and metrics[key] >= 0 for key, _ in definitions)
    checked = _date_label(metrics.get("updated_at"))
    if valid:
        links = []
        for key, label in definitions:
            value = f'{int(metrics[key]):,}'
            links.append(_external(profile, f'<strong>{value}</strong><span>{_e(label)}</span>',
                                   "scholar-stat", f"{label}: {value}. View Google Scholar"))
        values = '<div class="scholar-values">' + ''.join(links) + '</div>'
    else:
        values = '<div class="scholar-unavailable">' + _external(
            profile, 'View Google Scholar <span aria-hidden="true">↗</span>') + '</div>'
    return (
        '<section class="scholar-strip" id="scholar-metrics" aria-label="Google Scholar research metrics">'
        '<div class="scholar-label"><span>Research impact · All time</span>'
        + _external(profile, 'Google Scholar <span aria-hidden="true">↗</span>')
        + '</div>' + values + f'<p class="scholar-checked">Checked {_e(checked)}</p></section>'
    )


def hero_options(C):
    """Comparable visual directions, each retaining its original figure source."""
    cards = []
    for index, option in enumerate(C.get("hero_options") or [], start=1):
        figure = option.get("main_figure") or {}
        title = option.get("title") or f"Direction {index}"
        description = option.get("description") or ""
        source = option.get("source_url") or figure.get("source_url")
        number = option.get("id") or f"0{index}"
        cards.append(
            '<article class="hero-choice">'
            + '<div class="hero-choice-number">' + _e(number)
            + ('<span>Recommended</span>' if option.get("recommended") else '') + '</div>'
            + '<div class="hero-choice-image">' + _figure_window(figure) + '</div>'
            + f'<h2>{_e(title)}</h2><p>{_e(description)}</p>'
            + (_external(source, 'Source paper <span aria-hidden="true">↗</span>', "hero-choice-source") if source else '')
            + '</article>'
        )
    return '<div class="hero-choice-gallery">' + ''.join(cards) + '</div>' if cards else ""
