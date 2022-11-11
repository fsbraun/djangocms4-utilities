import sys

from django.conf import settings

from cms.models import PageContent
from cms.models.placeholdermodel import Placeholder
from django.core.management import color_style
from django.core.management.base import OutputWrapper

stdout = OutputWrapper(sys.stdout)
stdout.style = color_style()

def append(messages, new):
    if new not in messages:
        messages.append(new)
    return messages


def check_tree(placeholder, language=None):
    """checks the plugin tree if the placeholder for common inconsistencies and returns a list
    of messages describing the inconsistency. Returns list of messages."""
    messages = []

    if language is None:
        languages = (
            placeholder.cmsplugin_set.order_by("language")
            .values_list("language", flat=True)
            .distinct()
        )
        for language in languages:
            message = check_tree(placeholder, language)
            if message is not None:
                messages += message
        return messages

    # Check 1: Positions are consecutive starting at 1
    position_list = list(placeholder.cmsplugin_set.filter(language=language).values_list("position", flat=True))
    if position_list != list(
        range(1, placeholder.get_last_plugin_position(language) + 1)
    ):
        append(
            messages,
            f"{language}, {placeholder.slot}: Non consecutive position entries: {position_list}"
        )

    # Check 2: Children AFTER parents
    parent_list = list(placeholder.cmsplugin_set.filter(language=language).values_list("parent", flat=True))
    last_plugin = placeholder.get_last_plugin_position(language)
    for parent_id in parent_list:
        if parent_id is not None:
            parent = placeholder.cmsplugin_set.filter(pk=parent_id).first()
            if parent is not None:
                children_positions = placeholder.cmsplugin_set.get(id=parent_id).get_descendants().values_list("position", flat=True)
                if children_positions:
                    if min(children_positions) <= parent.position:
                        append(
                            messages,
                            f"{language}, {placeholder.slot}: Children with positions lower than their parent's (id={parent_id}) position"
                        )
                        if parent.position + len(children_positions) > last_plugin:
                            append(
                                messages,
                                f"---> Moving plugin (id={parent_id}) up in the tree will cause a server error."
                            )
                    elif max(children_positions) - min(children_positions) + 1 > len(
                        children_positions
                    ):
                        append(
                            messages,
                            f"{language}, {placeholder.slot}: Gap in children positions of parent (id={parent_id})"
                        )
    # Check 3: parents belonging to other placeholders
    for plugin in placeholder.cmsplugin_set.filter(language=language):
        if plugin.parent and plugin.parent.placeholder != placeholder:
            append(
                messages,
                f"{language}, {placeholder.slot}: Plugins claim to be children of parents in a different placeholder"
            )

    return messages


def check_placeholders(placeholders=None):
    if placeholders is None:
        placeholders = get_draft_placeholders()
    for placeholder in placeholders:
        messages = check_tree(placeholder)
        if messages:
            for message in messages:
                stdout.write(message, stdout.style.ERROR)
        else:
            stdout.write(f"Placeholder {placeholder.slot} (id={placeholder.id}) ok.", stdout.style.SUCCESS)


def fix_tree(placeholder, language=None):
    """rebuilds the plugin tree for the placeholder. The resulting tree will look like this:
    Parent 1, position 1
        Child 1, position 2
        Parent 2, position 3
            Child 2, position 4
        Child 3, position 5
    Parent 3, position 6
        Child 4 position 7
    Child 5, position 8   # (Parent link to parent plugin in other placeholder removed)
    """
    if language is None:
        languages = (
            placeholder.cmsplugin_set.filter(language=language).order_by("language")
            .values_list("language", flat=True)
            .distinct()
        )
        for language in languages:
            fix_tree(placeholder, language)
        return

    # First cut links to other placeholders
    for plugin in placeholder.cmsplugin_set.filter(language=language).filter(language=language):
        if plugin.parent and plugin.parent.placeholder != placeholder:
            plugin.update(
                parent=None
            )  # At this point the tree is seriously broken: Cut the link

    # Then rebuild tree
    def build_tree(self, parent):
        nonlocal position

        for plugin in self.cmsplugin_set.filter(
            parent=parent, language=language
        ).order_by("position"):
            position += 1
            plugin.update(position=position)
            build_tree(self, plugin)

    position = placeholder.get_last_plugin_position(language)
    build_tree(placeholder, None)

    placeholder._recalculate_plugin_positions(language)


def get_draft_placeholders():
    if "djangocms_versioning" in settings.INSTALLED_APPS:

        placeholder = list(Placeholder.objects.filter(content_type=None))

        from djangocms_versioning.helpers import remove_published_where

        # Get all draft PageContents (Ensure that we don't change any previously published
        # pages, allows us to use compare
        page_contents = PageContent.objects.all()
        page_contents = remove_published_where(page_contents)
        page_contents = page_contents.filter(versions__state="draft")

        for page_content in page_contents:
            placeholder += list(page_content.placeholders.all())

        return placeholder

    return Placeholder.objects.all()
