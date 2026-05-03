---
title: Store State as a Timestamp, Query It as a Boolean
description: A Django model-field pattern for tracking both whether a state is true and when it became true.
summary: For many business states, a timestamp is the source of truth and a boolean is the query optimization.
date: 2026-05-01
---

# Store State as a Timestamp, Query It as a Boolean

A boolean can tell you that something is true. It cannot tell you when it became true.

That sounds obvious, but a lot of application schemas still start with:

```python
is_active = models.BooleanField(default=False)
```

Then the product asks when the user became active. Or when the order was approved. Or when the invoice was sent. The schema grows a second column:

```python
active_at = models.DateTimeField(null=True, blank=True)
```

Now there are two sources of truth. If `is_active` says true and `active_at` is null, which one wins?

The better model is to store the timestamp and derive the boolean.

That is the idea behind [TimestampStateField](https://gist.github.com/mariocesar/6cfebb877da34c61204ef31888fd0bc0): one Django field declaration creates the timestamp and a generated boolean field.

```python
class User(models.Model):
    active_at = TimestampStateField()
```

Conceptually, this gives you:

- `active_at`: when the state became true.
- `is_active`: whether the timestamp is present.

The timestamp remains the source of truth. The boolean exists because it is ergonomic and indexable:

```python
User.objects.filter(is_active=True)
User.objects.filter(active_at__year=2026)
```

This is one of those patterns that feels too small to name, but it removes a surprising amount of ambiguity.

It also matches how business people talk. "Is this active?" and "When did it become active?" are two views of the same fact. In the database, that fact should not be stored twice by hand.

There are caveats. Generated fields depend on database support and Django version. If the state can turn false and later true again, a single timestamp only stores the current activation moment, not the full history. If you need a history, use an event table.

But for many states in CRUD-heavy systems, this is enough:

- `paid_at` and `is_paid`
- `verified_at` and `is_verified`
- `archived_at` and `is_archived`
- `published_at` and `is_published`

The design rule is simple: store the fact with the most information. Derive the convenience value.
