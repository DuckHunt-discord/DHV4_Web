import markdown
from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe


def get_tag(name):
    # First, search in tags
    try:
        return Tag.objects.filter(name__iexact=name).get()
    except Tag.DoesNotExist:
        try:
            alias = TagAlias.objects.filer(name__iexact=name).select_related('tag').get()
            return alias.tag
        except TagAlias.DoesNotExist:
            return None


class Tag(models.Model):
    owner = models.ForeignKey('botdata.DiscordUser', related_name='tags', on_delete=models.CASCADE)

    # Statistics
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uses = models.IntegerField(default=0)
    revisions = models.IntegerField(default=0)

    # Tag
    official = models.BooleanField(default=False)
    name = models.CharField(max_length=90, db_index=True, unique=True)
    content = models.TextField()

    @property
    def html(self):
        return mark_safe(markdown.markdown(self.content))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'tag'


class TagAlias(models.Model):
    owner = models.ForeignKey('botdata.DiscordUser', related_name='tags_aliases', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='aliases', on_delete=models.CASCADE)

    uses = models.IntegerField(default=0)

    name = models.CharField(max_length=90, db_index=True, unique=True)

    def __str__(self):
        return f"{self.name} -> {self.tag.name}"

    class Meta:
        db_table = 'tagalias'
