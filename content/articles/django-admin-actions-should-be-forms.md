---
title: Django Admin Actions Should Be Forms
description: A decorator pattern for giving Django admin actions a confirmation form before mutating objects.
summary: Django admin actions are more useful when they can ask for input, validate it, and then apply the change.
date: 2026-05-02
updated: 2026-05-03
---

# Django Admin Actions Should Be Forms

Django admin actions are great until the action needs one extra value.

Deleting selected objects gets a confirmation page. But a custom action often wants something more specific: choose a category, upload a file, select a date, type a reason, or confirm a business-specific mutation.

That was the problem behind this gist: [Django admin decorator to create a confirmation form action](https://gist.github.com/mariocesar/8adc56de00104e90bac7). It has survived because the shape is right.

The action should look like this:

```python
class PostCategoryForm(forms.Form):
    title = "Update category for the selected posts"
    category = forms.ModelChoiceField(queryset=Category.objects.all())


@action_form(PostCategoryForm)
def change_category(self, request, queryset, form):
    category = form.cleaned_data["category"]
    return queryset.update(category=category)
```

The important detail is that the action receives a validated form. The decorator owns the admin ceremony:

- Show a confirmation template.
- Preserve the selected queryset.
- Bind `POST` and `FILES`.
- Validate the form.
- Call the action only when the form is valid.
- Report the number of changed objects.

That makes the mutation easy to read. It also puts validation where Django developers expect it: in a form.

This pattern is much better than encoding arguments into action names, adding one-off admin views, or doing half-validation inside the action function. Those approaches work for the first special case and become awkward on the third.

The nice thing about the decorator is that it keeps the admin action contract small. A bulk operation is still an action. It just gets a form before it runs.

There are limits. For long-running jobs, the action should enqueue work and return quickly. For destructive actions, the confirmation page should show enough object context to make mistakes unlikely. For permission-sensitive actions, the decorator should not be the only line of defense.

Still, this is the kind of small extension that makes Django admin feel like a production tool instead of a demo backend. You do not need a separate dashboard for every internal workflow. Sometimes you just need a form in front of an action.

## FAQ

### Should every Django admin action use a form?

No. If the action has no choices and no risk, keep it plain. A form is useful when the action needs user input, file upload, validation, or a confirmation step that explains what will happen.

### Why not build a custom admin view instead?

A custom admin view is better for a full workflow. A form-backed action is better for a single bulk operation that still belongs to the selected queryset.

### What is the common footgun?

Losing the selected objects between the first confirmation page and the final POST. The decorator should preserve the selected IDs and treat the form submission as the second half of the same admin action.

### Should long-running actions execute inside the request?

Usually no. Validate the form in the admin action, enqueue a background job, and show the user that the job started. The admin request should not become a worker process.
