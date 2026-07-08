#!/usr/bin/env python3
"""Build Project Garuda public website pages from authorized content."""

from __future__ import annotations

import html
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

WEBSITE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = WEBSITE_ROOT.parent
CONTENT_ROOT = WEBSITE_ROOT / "content"
PAGES_ROOT = WEBSITE_ROOT / "pages"
ASSETS_ROOT = PAGES_ROOT / "assets"
STYLES_SRC = WEBSITE_ROOT / "styles"
MARK_SRC = WEBSITE_ROOT / "brand" / "mark" / "institutional-mark-v1.0.svg"

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Manifesto", "about/manifesto.html"),
    ("Vision", "about/vision.html"),
    ("Principles", "about/principles.html"),
    ("Constitutional Engineering", "constitutional-engineering.html"),
    ("Governance", "institution/governance.html"),
    ("Library", "library/book-one.html"),
    ("Research", "research.html"),
    ("Contact", "contact.html"),
]

PAGE_MAP: dict[str, str] = {
    "content/home.md": "index.html",
    "content/manifesto.md": "about/manifesto.html",
    "content/vision.md": "about/vision.html",
    "content/principles.md": "about/principles.html",
    "content/constitutional-engineering.md": "constitutional-engineering.html",
    "content/invitation.md": "invitation.html",
    "content/research.md": "research.html",
    "content/news.md": "news.html",
    "content/contact.md": "contact.html",
    "content/institution/constitutional-framework.md": "institution/constitutional-framework.html",
    "content/institution/governance.md": "institution/governance.html",
    "content/institution/architecture.md": "institution/architecture.html",
    "content/institution/engineering.md": "institution/engineering.html",
    "content/institution/preservation.md": "institution/preservation.html",
    "content/library/book-one.md": "library/book-one.html",
    "content/library/atlas.md": "library/atlas.html",
    "content/library/companion.md": "library/companion.html",
    "content/library/timeline.md": "library/timeline.html",
    "content/library/selected-texts.md": "library/selected-texts.html",
}

MARK_SVG = MARK_SRC.read_text(encoding="utf-8")


@dataclass
class ParsedPage:
    title: str
    lead: str | None
    body_html: str
    repository_label: str | None
    repository_links: list[tuple[str, str]]
    reading_journey_html: str | None


def asset_prefix(output_path: Path) -> str:
    depth = len(output_path.parent.parts)
    return "../" * depth if depth else ""


def repo_href(content_rel: str, href: str, output_rel: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return href
    source = (CONTENT_ROOT / content_rel).parent
    target = (source / href).resolve()
    try:
        target.relative_to(REPO_ROOT)
    except ValueError:
        return href
    output_dir = (PAGES_ROOT / output_rel).parent
    rel = Path(os.path.relpath(target, output_dir))
    return rel.as_posix()


def site_href(content_rel: str, href: str, output_rel: str) -> str:
    if href.endswith(".md"):
        parent = (WEBSITE_ROOT / content_rel).parent
        if href.startswith("content/"):
            key = href
        else:
            rel = (parent / href).resolve().relative_to(CONTENT_ROOT)
            key = f"content/{rel.as_posix()}"
        mapped = PAGE_MAP.get(key)
        if mapped:
            return Path(os.path.relpath(PAGES_ROOT / mapped, PAGES_ROOT / Path(output_rel).parent)).as_posix()
    return href


def format_prose(text: str, content_rel: str, output_rel: str) -> str:
    linked = convert_links(text, content_rel, output_rel, site=True)
    linked = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: f"<strong>{html.escape(match.group(1))}</strong>",
        linked,
    )
    linked = re.sub(
        r"(?<!\*)\*([^*]+?)\*(?!\*)",
        lambda match: f"<em>{html.escape(match.group(1))}</em>",
        linked,
    )
    linked = re.sub(r"\*\(([^)]+)\)\*", r"<em>(\1)</em>", linked)
    return linked


def extract_repository_links(line: str, content_rel: str, output_rel: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
        links.append((match.group(1), repo_href(content_rel, match.group(2), output_rel)))
    return links


def repository_label_from_line(line: str) -> str:
    label = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", "", line).strip()
    label = label.rstrip(":").strip("*").strip()
    return inline_format(label)


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def convert_links(text: str, content_rel: str, output_rel: str, site: bool = False) -> str:
    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        href = match.group(2)
        if site and href.endswith(".md") and not href.startswith("../") and not href.startswith("docs/"):
            resolved = site_href(content_rel, href, output_rel)
        else:
            resolved = repo_href(content_rel, href, output_rel)
        cls = ""
        if "docs/" in resolved or "packages/" in resolved:
            cls = ' class="repository-link"'
        return f'<a href="{html.escape(resolved, quote=True)}"{cls}>{inline_format(label)}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def is_table_separator(row: list[str]) -> bool:
    return all(re.match(r"^:?-+:?$", cell.strip()) for cell in row)


def parse_table(lines: list[str], start: int, content_rel: str, output_rel: str) -> tuple[str, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and "|" in lines[i]:
        row = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
        rows.append(row)
        i += 1
    if len(rows) < 2:
        return "", start
    header = rows[0]
    body_rows = rows[2:] if is_table_separator(rows[1]) else rows[1:]
    parts = ["<table>", "<thead><tr>"]
    for cell in header:
        parts.append(f"<th>{convert_links(cell, '', output_rel)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in body_rows:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{convert_links(cell, content_rel, output_rel)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts), i


def parse_markdown(content_rel: str, output_rel: str, text: str) -> ParsedPage:
    lines = text.splitlines()
    title = ""
    lead: str | None = None
    body_parts: list[str] = []
    repository_label: str | None = None
    repository_links: list[tuple[str, str]] = []
    reading_journey_html: str | None = None

    lead_consumed = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped and not body_parts:
            i += 1
            continue

        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            i += 1
            continue

        if stripped.startswith("**") and stripped.endswith("**") and not lead and i < 5:
            lead = stripped.strip("*")
            lead_consumed = True
            i += 1
            continue

        if stripped.startswith("**Reading journey:**") or stripped.startswith("Reading journey:"):
            journey = stripped.replace("**Reading journey:**", "Reading journey:").replace("**Next:**", "Next:")
            reading_journey_html = format_prose(journey, content_rel, output_rel)
            i += 1
            continue

        if (
            stripped.startswith("**Repository authority:**")
            or stripped.startswith("**Read the full")
            or ("repository:" in stripped.lower() and "[" in stripped)
        ):
            repository_label = repository_label_from_line(stripped)
            repository_links.extend(extract_repository_links(stripped, content_rel, output_rel))
            i += 1
            while i < len(lines):
                line_stripped = lines[i].strip()
                if not line_stripped:
                    i += 1
                    continue
                if line_stripped.startswith("["):
                    m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", line_stripped)
                    if m:
                        repository_links.append(
                            (m.group(1), repo_href(content_rel, m.group(2), output_rel))
                        )
                    i += 1
                    continue
                if line_stripped.startswith("The repository remains"):
                    i += 1
                    continue
                if line_stripped.startswith("**Next in reading journey:**"):
                    break
                break
            continue

        if stripped.startswith("**Next in reading journey:**"):
            journey = stripped.replace("**Next in reading journey:**", "Next in reading journey:")
            reading_journey_html = format_prose(journey, content_rel, output_rel)
            i += 1
            continue

        if stripped.startswith("**Canonical references:**"):
            repository_label = "Canonical references"
            i += 1
            while i < len(lines) and lines[i].strip().startswith("-"):
                m = re.search(r"\[([^\]]+)\]\(([^)]+)\)", lines[i])
                if m:
                    repository_links.append(
                        (m.group(1), repo_href(content_rel, m.group(2), output_rel))
                    )
                i += 1
            continue

        if stripped == "---":
            body_parts.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|"):
            table_html, i = parse_table(lines, i, content_rel, output_rel)
            if table_html:
                body_parts.append(table_html)
            continue

        if stripped.startswith("## "):
            body_parts.append(f"<h2>{inline_format(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("### "):
            body_parts.append(f"<h3>{inline_format(stripped[4:])}</h3>")
            i += 1
            continue

        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                item = re.sub(r"^\d+\.\s", "", lines[i].strip())
                items.append(f"<li>{format_prose(item, content_rel, output_rel)}</li>")
                i += 1
            body_parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item = lines[i].strip()[2:]
                items.append(f"<li>{convert_links(item, content_rel, output_rel)}</li>")
                i += 1
            body_parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        if stripped:
            body_parts.append(f"<p>{format_prose(stripped, content_rel, output_rel)}</p>")
        i += 1

    return ParsedPage(
        title=title,
        lead=lead,
        body_html="\n".join(body_parts),
        repository_label=repository_label,
        repository_links=repository_links,
        reading_journey_html=reading_journey_html,
    )


def render_page(content_rel: str, output_path: Path, parsed: ParsedPage) -> str:
    prefix = asset_prefix(output_path)
    current = output_path.as_posix()

    nav_items = []
    for label, href in NAV_ITEMS:
        full = prefix + href
        current_attr = ' aria-current="page"' if href == current else ""
        nav_items.append(f'<li><a href="{html.escape(full)}"{current_attr}>{html.escape(label)}</a></li>')

    repo_block = ""
    if parsed.repository_links:
        label = parsed.repository_label or "Read the full text in the repository"
        links = "".join(
            f'<li><a class="repository-link" href="{html.escape(h, quote=True)}">{html.escape(t)}</a></li>'
            for t, h in parsed.repository_links
        )
        repo_block = f"""
<section class="repository-callout" aria-label="Repository source">
  <p class="repository-callout__label">{label}</p>
  <ul class="repository-callout__links">{links}</ul>
</section>"""

    journey_block = ""
    if parsed.reading_journey_html:
        journey_block = f'<nav class="reading-journey" aria-label="Reading journey">{parsed.reading_journey_html}</nav>'

    title_block = parsed.title
    if content_rel == "content/home.md" and parsed.lead:
        title_html = f'<p class="home-proposition">{html.escape(parsed.lead)}</p>'
    else:
        title_html = f'<h1 class="gateway-page__title">{html.escape(title_block)}</h1>'
        if parsed.lead:
            title_html += f'<p class="gateway-page__lead">{html.escape(parsed.lead)}</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(parsed.title)} — Project Garuda</title>
  <link rel="stylesheet" href="{prefix}assets/styles/main.css">
</head>
<body>
  <div class="site">
    <header class="site-header">
      <div class="site-header__inner">
        <a class="site-mark" href="{prefix}index.html" aria-label="Project Garuda home">
          {MARK_SVG}
        </a>
        <nav class="site-nav" aria-label="Site">
          <ul class="site-nav__list">
            {''.join(nav_items)}
          </ul>
        </nav>
      </div>
    </header>
    <main class="site-main" id="main">
      <article class="gateway-page">
        {title_html}
        <div class="page-content">
          {parsed.body_html}
        </div>
        {repo_block}
        {journey_block}
      </article>
    </main>
    <footer class="site-footer">
      <div class="site-footer__mark" aria-hidden="true">{MARK_SVG}</div>
      <p>The repository remains the institution&apos;s canonical source of truth.</p>
      <p>Project Garuda</p>
      <p>The website introduces. The repository governs.</p>
    </footer>
  </div>
</body>
</html>
"""


def copy_assets() -> None:
    styles_dest = ASSETS_ROOT / "styles"
    mark_dest = ASSETS_ROOT / "mark"
    if ASSETS_ROOT.exists():
        shutil.rmtree(ASSETS_ROOT)
    styles_dest.mkdir(parents=True)
    mark_dest.mkdir(parents=True)
    shutil.copy2(STYLES_SRC / "tokens.css", styles_dest / "tokens.css")
    shutil.copy2(STYLES_SRC / "main.css", styles_dest / "main.css")
    shutil.copy2(MARK_SRC, mark_dest / "institutional-mark-v1.0.svg")


def build() -> list[Path]:
    copy_assets()
    built: list[Path] = []
    for content_rel, output_rel in PAGE_MAP.items():
        source = WEBSITE_ROOT / content_rel
        output = PAGES_ROOT / output_rel
        output.parent.mkdir(parents=True, exist_ok=True)
        parsed = parse_markdown(content_rel, output_rel, source.read_text(encoding="utf-8"))
        output.write_text(render_page(content_rel, Path(output_rel), parsed), encoding="utf-8")
        built.append(output)
    return built


def main() -> int:
    built = build()
    print(f"Built {len(built)} pages into {PAGES_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
