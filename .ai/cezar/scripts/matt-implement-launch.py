#!/usr/bin/env python3
"""Fill the implementation slots of the Matt flow.

Picks the oldest open GitHub issues that are ready for an agent and launches one
cezar task per issue with the `matt-implement` workflow. Each task is a ROOT task
created through the cockpit API, so it gets a fresh worktree off `main` (not a
child forked off the caller's branch).

An issue is a candidate when it is:
  - open and labelled `ready-for-agent`,
  - not labelled `in-progress` (the claim this script sets on launch),
  - not blocked: every issue in its native GitHub `blocked_by` list is closed,
  - not already referenced as closed-by an open pull request.

Slots: at most MATT_IMPL_SLOTS (default 2) `matt-implement` tasks are active at
once; active = any status other than done/failed/cancelled/stopped.

An `in-progress` issue with no active task and no open PR is reported as STUCK
and is never re-picked automatically (it most likely failed); remove the label
by hand to retry it.

Usage: matt-implement-launch.py [--dry-run] [--slots N]
Needs: gh (authenticated), CEZ_API_URL and CEZ_PROJECT_ID (set inside cezar tasks).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

WORKFLOW = "matt-implement"
READY = "ready-for-agent"
CLAIM = "in-progress"
INACTIVE = {"done", "failed", "cancelled", "canceled", "stopped", "error"}


def gh(*args: str) -> str:
    res = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} failed: {res.stderr.strip()}")
    return res.stdout


def gh_json(*args: str):
    return json.loads(gh(*args) or "null")


def api(method: str, path: str, body: dict | None = None):
    base = os.environ.get("CEZ_API_URL")
    project = os.environ.get("CEZ_PROJECT_ID")
    if not base or not project:
        sys.exit("CEZ_API_URL / CEZ_PROJECT_ID not set: run this inside a cezar task")
    req = urllib.request.Request(
        f"{base}/api/v1/p/{project}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read() or b"null")


def issue_of(task: str) -> int | None:
    m = re.search(r"#(\d+)", task or "")
    return int(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--slots", type=int, default=int(os.environ.get("MATT_IMPL_SLOTS", "2")))
    args = ap.parse_args()

    repo = gh_json("repo", "view", "--json", "nameWithOwner")["nameWithOwner"]

    active = [
        r for r in api("GET", "/runs")
        if r.get("workflow") == WORKFLOW and r.get("status") not in INACTIVE and not r.get("archived")
    ]
    active_issues = {issue_of(r.get("task", "")) for r in active}
    free = max(0, args.slots - len(active))
    print(f"slots: {args.slots}, active {WORKFLOW} tasks: {len(active)} {sorted(i for i in active_issues if i)}, free: {free}")

    # GraphQL rather than `gh pr list --json closingIssuesReferences`: older gh lacks that field.
    owner, name = repo.split("/")
    prs = gh_json(
        "api", "graphql",
        "-f", "query=query($o:String!,$n:String!){repository(owner:$o,name:$n){pullRequests(states:OPEN,first:100)"
              "{nodes{number closingIssuesReferences(first:20){nodes{number}}}}}}",
        "-f", f"o={owner}", "-f", f"n={name}",
    )["data"]["repository"]["pullRequests"]["nodes"]
    claimed_by_pr = {ref["number"] for pr in prs for ref in pr["closingIssuesReferences"]["nodes"]}

    issues = gh_json(
        "issue", "list", "--state", "open", "--label", READY,
        "--json", "number,title,labels,createdAt", "--limit", "200",
    )
    issues.sort(key=lambda i: i["createdAt"])

    candidates, stuck = [], []
    for issue in issues:
        n = issue["number"]
        labels = {l["name"] for l in issue["labels"]}
        if n in claimed_by_pr or n in active_issues:
            continue
        if CLAIM in labels:
            stuck.append(n)
            continue
        blockers = gh_json("api", f"repos/{repo}/issues/{n}/dependencies/blocked_by") or []
        open_blockers = [b["number"] for b in blockers if b.get("state") == "open"]
        if open_blockers:
            continue
        candidates.append(issue)

    if stuck:
        print(f"STUCK (labelled {CLAIM}, no active task, no open PR; remove the label to retry): {stuck}")
    print(f"unblocked candidates, oldest first: {[i['number'] for i in candidates]}")

    picked = candidates[:free]
    if not picked:
        print("nothing to launch")
        return 0

    if not args.dry_run:
        gh("label", "create", CLAIM, "--color", "FBCA04",
           "--description", "Claimed by a running matt-implement session", "--force")

    for issue in picked:
        n, title = issue["number"], issue["title"]
        task = (
            f"#{n} {title}\n\n"
            f"Implement GitHub issue #{n} (https://github.com/{repo}/issues/{n}). "
            "Read the issue, its parent epic and the spec it links before starting.\n\n"
            f"CEZ:ISSUE={n}"
        )
        if args.dry_run:
            print(f"[dry-run] would launch {WORKFLOW} for #{n}: {title}")
            continue
        gh("issue", "edit", str(n), "--add-label", CLAIM)
        run = api("POST", "/runs", {"task": task, "workflow": WORKFLOW, "autonomous": True})
        run_id = (run or {}).get("id") or (run or {}).get("run", {}).get("id")
        print(f"launched {WORKFLOW} for #{n}: {title} -> run {run_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
