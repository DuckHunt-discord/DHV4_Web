import markdown
from django.core.validators import validate_slug, MinValueValidator
from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe


def get_tag(name):
    # First, search in tags
    try:
        return Tag.objects.filter(name__iexact=name).get()
    except Tag.DoesNotExist:
        try:
            alias = TagAlias.objects.filter(name__iexact=name).select_related('tag').get()
            return alias.tag
        except TagAlias.DoesNotExist:
            return None


class Tag(models.Model):
    owner = models.ForeignKey('botdata.DiscordUser', related_name='tags', on_delete=models.CASCADE)

    # Statistics
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    revisions = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Tag
    official = models.BooleanField(default=False)
    name = models.CharField(max_length=90, db_index=True, unique=True,
                            validators=[validate_slug, ],
                            help_text="Lowercase & without spaces.")

    content = models.TextField()

    @property
    def html(self):
        return mark_safe(markdown.markdown(self.content.replace("\n", "\n\n")))

    @property
    def description(self):
        try:
            return mark_safe(markdown.markdown(self.content.splitlines()[0]))
        except IndexError:
            return ''

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'tag'


class TagAlias(models.Model):
    owner = models.ForeignKey('botdata.DiscordUser', related_name='tags_aliases', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='aliases', on_delete=models.CASCADE)

    uses = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    name = models.CharField(max_length=90, db_index=True, unique=True,
                            validators=[validate_slug, ],
                            help_text="Lowercase & without spaces.")

    def __str__(self):
        return f"{self.name} -> {self.tag.name}"

    class Meta:
        db_table = 'tagalias'
