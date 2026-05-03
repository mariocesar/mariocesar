---
title: Static Websites Are Usually Enough
description: Notes on why a personal site can stay small, fast, and static for a long time.
summary: A small reminder that static publishing gives personal sites fewer failure modes and more room to breathe.
date: 2026-05-03
updated: 2026-05-03
---

# Static Websites Are Usually Enough

For a personal website, static publishing is a strong default. There is no runtime to babysit, no database to migrate, no admin surface to protect, and no cache layer to explain to your future self.

That does not mean the site has to be primitive. A small static builder can still generate article pages, feeds, sitemaps, metadata, and structured HTML. The difference is that the complexity happens before deploy, not during every request.

The best version of this setup is boring in production and pleasant while writing.

## FAQ

### When is a static site no longer enough?

When the site needs per-user state, private content, server-side search, payments, comments, or form handling that cannot be outsourced cleanly. Until then, static hosting removes more problems than it creates.

### Is a custom static builder overkill?

Sometimes. But a tiny builder can be less work than adapting a large framework. The test is whether the builder stays boring: read content, render templates, write files.

### What should stay dynamic during development?

Preview and rebuild feedback. Production can be static while development still has a watcher, local server, and live reload.

### What is the biggest static-site mistake?

Letting the content model fragment. The homepage, articles, RSS, and sitemap should come from the same source of truth, or publishing becomes chores glued together.
