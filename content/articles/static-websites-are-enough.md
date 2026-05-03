---
title: Static Websites Are Usually Enough
description: Notes on why a personal site can stay small, fast, and static for a long time.
summary: A small reminder that static publishing gives personal sites fewer failure modes and more room to breathe.
date: 2026-05-03
---

# Static Websites Are Usually Enough

For a personal website, static publishing is a strong default. There is no runtime to babysit, no database to migrate, no admin surface to protect, and no cache layer to explain to your future self.

That does not mean the site has to be primitive. A small static builder can still generate article pages, feeds, sitemaps, metadata, and structured HTML. The difference is that the complexity happens before deploy, not during every request.

The best version of this setup is boring in production and pleasant while writing.
