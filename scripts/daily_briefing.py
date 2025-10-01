#!/usr/bin/env python3
"""
Daily briefing system for Claudipedia project.

Sends an email every morning at 5am with:
- Current project status
- Progress in last 5 days
- Progress in last 24 hours
- Next milestones
- Key metrics

Usage:
    python3 scripts/daily_briefing.py --send

Setup cron job:
    0 5 * * * cd /home/g/dev/claudipedia && python3 scripts/daily_briefing.py --send
"""

import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
import subprocess


class ProjectBriefing:
    """Generate and send project briefing emails."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.status_file = self.project_root / ".claudipedia_status.json"
        self.recipient = "butaeff@gmail.com"
        self.briefing_dir = self.project_root / "docs" / "briefings"

    def load_status(self):
        """Load project status from tracking file."""
        if self.status_file.exists():
            with open(self.status_file) as f:
                return json.load(f)
        return {
            "last_updated": None,
            "phase": "Phase 1: Physics Foundation",
            "completed_steps": [],
            "current_step": "Step 2: Core Data Models",
            "milestones": {
                "Repository Setup": "completed",
                "Core Data Models": "in_progress",
                "Graph Database": "pending",
                "Axiom Seeding": "pending",
                "Decomposition Engine": "pending",
                "Verification Engine": "pending",
                "Gap Detection": "pending",
                "Synthesis Engine": "pending",
                "API Server": "pending",
                "Test Queries": "pending"
            },
            "history": []
        }

    def save_status(self, status):
        """Save project status."""
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)

    def get_git_stats(self):
        """Get git statistics."""
        try:
            os.chdir(self.project_root)

            # Files changed in last 24 hours
            result = subprocess.run(
                ['git', 'log', '--since=24 hours ago', '--stat', '--oneline'],
                capture_output=True, text=True
            )
            last_day = result.stdout if result.returncode == 0 else "No commits"

            # Files changed in last 5 days
            result = subprocess.run(
                ['git', 'log', '--since=5 days ago', '--stat', '--oneline'],
                capture_output=True, text=True
            )
            last_5_days = result.stdout if result.returncode == 0 else "No commits"

            # Total commits
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                capture_output=True, text=True
            )
            total_commits = result.stdout.strip() if result.returncode == 0 else "0"

            return {
                "last_day": last_day,
                "last_5_days": last_5_days,
                "total_commits": total_commits
            }
        except Exception as e:
            return {"error": str(e)}

    def count_lines_of_code(self):
        """Count lines of code in the project."""
        try:
            python_files = list(self.project_root.glob("src/**/*.py"))
            total_lines = 0
            for file in python_files:
                with open(file) as f:
                    total_lines += len(f.readlines())
            return total_lines
        except Exception:
            return 0

    def generate_briefing(self):
        """Generate briefing content."""
        status = self.load_status()
        git_stats = self.get_git_stats()
        loc = self.count_lines_of_code()

        # Calculate progress
        milestones = status.get("milestones", {})
        completed = sum(1 for v in milestones.values() if v == "completed")
        total = len(milestones)
        progress_pct = (completed / total * 100) if total > 0 else 0

        briefing = f"""
# Claudipedia Daily Briefing
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 🎯 Current Status

**Phase:** {status.get('phase', 'Unknown')}
**Current Step:** {status.get('current_step', 'Unknown')}
**Overall Progress:** {progress_pct:.1f}% ({completed}/{total} milestones completed)

---

## 📊 Milestones

"""
        for milestone, state in milestones.items():
            emoji = "✅" if state == "completed" else "🔄" if state == "in_progress" else "⏸️"
            briefing += f"{emoji} **{milestone}**: {state}\n"

        briefing += f"""

---

## 📈 Progress (Last 24 Hours)

{git_stats.get('last_day', 'No activity')}

---

## 📅 Progress (Last 5 Days)

{git_stats.get('last_5_days', 'No activity')}

---

## 💻 Code Metrics

- **Total Lines of Code:** {loc:,}
- **Total Git Commits:** {git_stats.get('total_commits', '0')}
- **Python Files:** {len(list(self.project_root.glob('src/**/*.py')))}

---

## 🎯 Next Up

Based on the implementation plan, the next milestones are:

1. **Graph Database Interface** (Days 3-4)
   - Neo4j connection
   - CRUD operations for claims, edges, gaps

2. **Seed Physics Axioms** (Day 5)
   - 50 fundamental physics axioms
   - Mathematical constants
   - Physical laws

3. **Decomposition Engine** (Days 6-8)
   - Question parsing
   - Sub-claim generation
   - Recursion to axioms

---

## 📝 Notes for Non-Technical Review

**What We Built Recently:**
- Core data structures (Claim, Edge, Gap, Source models)
- Configuration system for managing settings
- Unit tests to ensure code quality
- Daily briefing system (this email!)

**What This Means:**
- We have the "building blocks" to store knowledge
- Think of Claims as facts in our database
- Edges connect facts together (e.g., "F=ma derives from Newton's laws")
- Gaps identify what we don't know yet

**Technical Debt:** None yet (early stage)

**Blockers:** None

---

## 🚀 Vision Reminder

We're building a first principles truth machine that will:
1. Store all human knowledge as a graph
2. Verify claims against physics axioms
3. Identify gaps in human understanding
4. Generate new research questions
5. Accelerate toward technological singularity

Current focus: Physics foundation (classical mechanics, thermodynamics, electromagnetism)

---

**Questions or concerns?** Reply to this email or check the repo:
https://github.com/g-but/claudipedia

Built with 🤖 by Claude Code
"""

        return briefing

    def send_email(self, subject, body):
        """Send email via SMTP and save to public archive."""
        # NOTE: This requires SMTP configuration
        # For now, just print to console and save to file

        print("=" * 80)
        print(f"SUBJECT: {subject}")
        print("=" * 80)
        print(body)
        print("=" * 80)

        # Save to public docs/briefings directory
        self.briefing_dir.mkdir(parents=True, exist_ok=True)

        filename = f"briefing_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.briefing_dir / filename

        with open(filepath, 'w') as f:
            f.write(body)

        # Update the README index
        self._update_briefings_index(filename)

        print(f"\n✅ Briefing saved to: docs/briefings/{filename}")
        print(f"   View online: https://github.com/g-but/claudipedia/blob/main/docs/briefings/{filename}")
        print("\n⚠️  Email sending not configured yet.")
        print("To enable email delivery, configure SMTP settings in this script.")
        print(f"Recipient: {self.recipient}")

    def _update_briefings_index(self, filename):
        """Update the briefings README with the latest entry."""
        readme_path = self.briefing_dir / "README.md"

        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read()

            # Add entry after "Recent Briefings" section
            date = filename.replace("briefing_", "").replace(".md", "")
            entry = f"\n- [{date}]({filename}) - Automated daily briefing"

            if "(Most recent first)" in content and entry not in content:
                content = content.replace(
                    "(Most recent first)",
                    f"(Most recent first){entry}"
                )

                with open(readme_path, 'w') as f:
                    f.write(content)

    def run(self):
        """Generate and send briefing."""
        briefing = self.generate_briefing()
        subject = f"Claudipedia Daily Briefing - {datetime.now().strftime('%Y-%m-%d')}"
        self.send_email(subject, briefing)


if __name__ == "__main__":
    import sys

    briefing = ProjectBriefing()

    if "--send" in sys.argv:
        briefing.run()
    elif "--update-status" in sys.argv:
        # Update status manually
        status = briefing.load_status()
        status["last_updated"] = datetime.now().isoformat()
        if "--complete" in sys.argv:
            milestone = sys.argv[sys.argv.index("--complete") + 1]
            status["milestones"][milestone] = "completed"
        briefing.save_status(status)
        print(f"✅ Status updated")
    else:
        print("Usage:")
        print("  python3 scripts/daily_briefing.py --send")
        print("  python3 scripts/daily_briefing.py --update-status --complete 'Milestone Name'")
