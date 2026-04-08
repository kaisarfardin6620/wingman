#!/usr/bin/env python3
"""
resume_update.py — Regenerates RESUME_DRAFT.md from resume_template.py

Usage:
    python resume_update.py

Steps to update your resume:
    1. Edit resume_template.py with your personal details.
    2. Run this script.
    3. RESUME_DRAFT.md will be updated automatically.
"""

import importlib.util
import sys
import textwrap
from pathlib import Path

TEMPLATE_FILE = Path(__file__).parent / "resume_template.py"
OUTPUT_FILE = Path(__file__).parent / "RESUME_DRAFT.md"


def load_template():
    spec = importlib.util.spec_from_file_location("resume_template", TEMPLATE_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_header(t):
    lines = [f"# {t.FULL_NAME}", ""]
    if t.EMAIL and "[FILL" not in t.EMAIL:
        lines.append(f"**Email:** {t.EMAIL}")
    else:
        lines.append("**Email:** [YOUR_EMAIL@example.com]")
    if t.PHONE and "[FILL" not in t.PHONE:
        lines.append(f"**Phone:** {t.PHONE}")
    else:
        lines.append("**Phone:** [YOUR_PHONE_NUMBER]")
    if t.LINKEDIN and "[FILL" not in t.LINKEDIN:
        lines.append(f"**LinkedIn:** {t.LINKEDIN}")
    else:
        lines.append("**LinkedIn:** [YOUR_LINKEDIN_URL]")
    lines.append(f"**GitHub:** {t.GITHUB}")
    lines.append(f"**Location:** {t.LOCATION}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_summary(t):
    summary_text = textwrap.dedent(t.SUMMARY).strip()
    return f"## SUMMARY\n\n{summary_text}\n\n---\n\n"


def build_skills(t):
    lines = ["## SKILLS", ""]
    for category, items in t.SKILLS.items():
        lines.append(f"**{category}:** {', '.join(items)}")
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_projects(t):
    lines = ["## PROJECTS", ""]

    for proj in t.FEATURED_PROJECTS:
        lines.append(f"### {proj['name']}")
        lines.append(f"**Tech Stack:** {proj['tech']}")
        lines.append(f"**GitHub:** {proj['github']}")
        lines.append("")
        for bullet in proj["bullets"]:
            lines.append(f"- {bullet}")
        lines.append("")

    if t.ADDITIONAL_PROJECTS:
        lines.append("### Additional Machine Learning and Deep Learning Projects")
        lines.append(f"**GitHub:** {t.GITHUB}")
        lines.append("")
        for item in t.ADDITIONAL_PROJECTS:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_education(t):
    lines = ["## EDUCATION", ""]
    for edu in t.EDUCATION:
        field = edu["field"] if "[FILL" not in edu["field"] else "[Your Field of Study]"
        university = edu["university"] if "[FILL" not in edu["university"] else "[University Name]"
        grad = edu["graduation"] if "[FILL" not in edu["graduation"] else "[Year]"
        status_label = f" *({edu['status']})*" if edu.get("status") else ""

        lines.append(f"**{edu['degree']} — {field}**{status_label}")
        lines.append(f"{university}, {edu['location']}")
        if edu["status"] == "In Progress":
            lines.append(f"Expected Graduation: {grad}")
        else:
            lines.append(f"Graduated: {grad}")
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_experience(t):
    if not t.EXPERIENCE:
        return ""

    # Check if experience is a placeholder (all fields contain [FILL)
    all_placeholder = all(
        "[FILL" in (e.get("title", "") + e.get("company", ""))
        for e in t.EXPERIENCE
    )

    lines = ["## EXPERIENCE", ""]
    for exp in t.EXPERIENCE:
        title = exp.get("title", "[Job Title]")
        company = exp.get("company", "[Company]")
        location = exp.get("location", "[Location]")
        start = exp.get("start", "[Start Date]")
        end = exp.get("end", "[End Date]")

        lines.append(f"**{title}**")
        lines.append(f"{company}, {location}")
        lines.append(f"{start} – {end}")
        lines.append("")
        for bullet in exp.get("bullets", []):
            lines.append(f"- {bullet}")
        lines.append("")

    if all_placeholder:
        lines.append(
            "> Note: Replace the placeholders above with your actual experience, "
            "or remove this section if you have no formal employment yet."
        )
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_footer():
    from datetime import datetime
    month_year = datetime.now().strftime("%B %Y")
    return f"*Last updated: {month_year} | GitHub: kaisarfardin6620*\n"


def main():
    print(f"Loading template from: {TEMPLATE_FILE}")
    t = load_template()

    sections = [
        build_header(t),
        build_summary(t),
        build_skills(t),
        build_projects(t),
        build_education(t),
        build_experience(t),
        build_footer(),
    ]

    content = "".join(sections)

    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"Resume successfully written to: {OUTPUT_FILE}")

    # Quick ATS compliance checks
    warnings = []
    if "[FILL" in content:
        placeholders = [line.strip() for line in content.splitlines() if "[FILL" in line]
        warnings.append("Unfilled placeholders found:")
        for p in placeholders:
            warnings.append(f"  - {p[:80]}")

    if warnings:
        print("\nATS WARNING — unfilled placeholders:")
        for w in warnings:
            print(w)
        print("\nUpdate resume_template.py and re-run this script.")
    else:
        print("\nATS check passed: no unfilled placeholders found.")


if __name__ == "__main__":
    main()
