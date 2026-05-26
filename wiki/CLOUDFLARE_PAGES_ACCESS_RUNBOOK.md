# Cloudflare Pages And Access Runbook

- Status: Draft
- Owner: Team
- Scope: private-wiki-deployment
- Canonical: No
- Last Reviewed: 2026-05-26

## Purpose

Deploy the project wiki as a private website without moving the source of truth
out of GitHub.

The intended shape is:

```text
docs/wiki/*.md
  -> tools/wiki_site/build.py
  -> Cloudflare Workers static assets
  -> Cloudflare Access login
```

GitHub remains the source of truth for Markdown, commits, PRs, and Discussions.

## Repository Build Settings

Cloudflare may show this flow as `Create a Worker` instead of `Create Pages`.
That is okay. This repository includes `wrangler.jsonc`, which tells Cloudflare
to publish the generated static assets from `site/wiki`.

Use these settings when creating the Cloudflare project:

| Setting | Value |
| --- | --- |
| Project name | `phd-wiki` |
| Production branch | `master` |
| Build command | `python tools/wiki_site/build.py --source docs/wiki --output site/wiki --repo-url https://github.com/LiuZesensengsheng/PHDGAME --repo-ref master --discussion-category general` |
| Root directory | repository root |
| Python version | `3.11` |

If Cloudflare does not auto-detect Python 3.11, set an environment variable:

| Variable | Value |
| --- | --- |
| `PYTHON_VERSION` | `3.11` |

Do not leave the build command empty. The repository does not contain prebuilt
HTML; Cloudflare needs to run the build command before it can upload
`site/wiki`.

## Access Policy

Create a Cloudflare Access application for the Pages domain.

Recommended first policy:

| Field | Value |
| --- | --- |
| Action | `Allow` |
| Include | approved email list or approved email domain |
| Login method | One-time PIN or GitHub identity provider |
| Session duration | 1 week |

Do not rely on an unlisted URL as privacy. The site should require Access login
before any HTML, images, or search index can be loaded.

## GitHub Discussions

GitHub Discussions should stay enabled on the private repository.

Each generated page includes a `Discuss this page` link that opens a GitHub
Discussion draft. The discussion is still governed by private-repo permissions.

## Images

Put wiki images under:

```text
docs/wiki/assets/
docs/wiki/<section>/assets/
```

Use ordinary Markdown:

```md
![Alt text](assets/example.png)
```

The builder copies any `assets/` directory under `docs/wiki` into the generated
site.

## Local Verification

```bash
py -3.11 tools/wiki_site/build.py --source docs/wiki --output site/wiki --repo-url https://github.com/LiuZesensengsheng/PHDGAME --repo-ref master --discussion-category general
py -3.11 -m pytest tests/tools/test_wiki_site_build.py -q
```

Open:

```text
site/wiki/index.html
```

## Current Limitations

- Page comments are linked to GitHub Discussions, not embedded in the page.
- Discussion syncing back into `docs/wiki/_discussion_cache/` is a later step.
- Cloudflare Access setup is account-side configuration and is not fully stored
  in this repository.
