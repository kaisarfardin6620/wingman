#!/usr/bin/env python3
"""
generate_resume.py
==================
Combines resume_template.md + project_bullets.md to produce RESUME_DRAFT.md.

Usage
-----
    # Basic (uses default paths)
    python resume/generate_resume.py

    # Custom paths
    python resume/generate_resume.py \
        --template  resume/resume_template.md \
        --bullets   resume/project_bullets.md \
        --output    RESUME_DRAFT.md

How it works
------------
1. Reads project_bullets.md and parses every block that starts with
   "## PROJECT: <id>" into a dictionary keyed by <id>.
2. Reads resume_template.md and replaces any marker of the form
   <!-- PROJECT:<id> --> with the formatted bullet list for that project.
3. Appends a "Projects" section with ALL parsed projects if the template
   does not already contain individual project markers.
4. Writes the result to the output file, overwriting any previous version.

Run instructions (from the repo root)
--------------------------------------
    python resume/generate_resume.py
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_project_bullets(bullets_path: Path) -> dict:
    """
    Parse project_bullets.md into a dict:
        { project_id: { "name": str, "url": str, "stack": str, "bullets": [str] } }
    """
    text = bullets_path.read_text(encoding="utf-8")
    projects = {}

    # Split on "## PROJECT: <id>" headers
    blocks = re.split(r"^## PROJECT:\s*(.+)$", text, flags=re.MULTILINE)
    # blocks[0] is the preamble; then pairs of (id, body) follow
    it = iter(blocks[1:])
    for project_id, body in zip(it, it):
        project_id = project_id.strip()
        lines = body.strip().splitlines()

        name = ""
        url = ""
        stack = ""
        bullets: list[str] = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("---"):
                continue
            name_match = re.match(r"\*\*Name:\*\*\s*(.+)", line)
            url_match = re.match(r"\*\*URL:\*\*\s*(.+)", line)
            stack_match = re.match(r"\*\*Stack:\*\*\s*(.+)", line)
            if name_match:
                name = name_match.group(1).strip()
            elif url_match:
                url = url_match.group(1).strip()
            elif stack_match:
                stack = stack_match.group(1).strip()
            elif line.startswith("- "):
                bullets.append(line)

        projects[project_id] = {
            "name": name,
            "url": url,
            "stack": stack,
            "bullets": bullets,
        }

    return projects


def format_project_section(project: dict) -> str:
    """Render a single project as a Markdown sub-section."""
    name = project["name"] or "Project"
    url = project["url"]
    stack = project["stack"]
    bullets = "\n".join(project["bullets"])

    link = f"[{name}]({url})" if url else name
    stack_line = f"*{stack}*\n\n" if stack else ""
    return f"### {link}\n{stack_line}{bullets}\n"


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate(template_path: Path, bullets_path: Path, output_path: Path) -> None:
    projects = parse_project_bullets(bullets_path)

    template = template_path.read_text(encoding="utf-8")

    # Replace inline project markers (<!-- PROJECT:<id> -->) if present
    def replace_marker(match: re.Match) -> str:
        pid = match.group(1).strip()
        if pid in projects:
            return format_project_section(projects[pid])
        return match.group(0)  # leave unknown markers untouched

    result = re.sub(r"<!--\s*PROJECT:(\S+)\s*-->", replace_marker, template)

    # If the template contains a "## Projects" section with no markers,
    # append all projects after that heading.
    if "<!-- PROJECT:" not in template and "<!-- PROJECT:" not in result:
        projects_heading = re.search(
            r"^## Projects\s*$", result, flags=re.MULTILINE
        )
        if projects_heading:
            insert_pos = projects_heading.end()
            sections = "\n\n" + "\n\n".join(
                format_project_section(p) for p in projects.values()
            )
            result = result[:insert_pos] + sections + result[insert_pos:]
        else:
            # Append a full Projects section before the Education section
            # (or at the end if Education is absent)
            edu_match = re.search(r"^## Education", result, flags=re.MULTILINE)
            sections_block = (
                "\n\n## Projects\n\n"
                + "\n\n".join(format_project_section(p) for p in projects.values())
            )
            if edu_match:
                result = (
                    result[: edu_match.start()]
                    + sections_block
                    + "\n\n"
                    + result[edu_match.start():]
                )
            else:
                result = result.rstrip() + sections_block + "\n"

    # Stamp generation date
    today = date.today().isoformat()
    if "*Generated:" not in result:
        result = result.rstrip() + f"\n\n---\n\n*Generated: {today} | [Resume generator](resume/generate_resume.py)*\n"
    else:
        result = re.sub(
            r"\*Generated:.*",
            f"*Generated: {today} | [Resume generator](resume/generate_resume.py)*",
            result,
        )

    output_path.write_text(result, encoding="utf-8")
    print(f"✅  Resume written to: {output_path.resolve()}")
    print(f"   Projects included:  {', '.join(projects.keys())}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    resume_dir = repo_root / "resume"

    parser = argparse.ArgumentParser(
        description="Generate RESUME_DRAFT.md from template + project bullets."
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=resume_dir / "resume_template.md",
        help="Path to resume_template.md (default: resume/resume_template.md)",
    )
    parser.add_argument(
        "--bullets",
        type=Path,
        default=resume_dir / "project_bullets.md",
        help="Path to project_bullets.md (default: resume/project_bullets.md)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "RESUME_DRAFT.md",
        help="Output path (default: RESUME_DRAFT.md in repo root)",
    )
    args = parser.parse_args()

    for p, label in [
        (args.template, "--template"),
        (args.bullets, "--bullets"),
    ]:
        if not p.exists():
            print(f"❌  File not found ({label}): {p}", file=sys.stderr)
            sys.exit(1)

    generate(args.template, args.bullets, args.output)


if __name__ == "__main__":
    main()
