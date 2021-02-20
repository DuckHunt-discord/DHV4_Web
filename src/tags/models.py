from django.db import models

# Create your models here.


class Tag(models.Model):
    owners = models.ManyToManyField('botdata.DiscordUser', related_name='tags')

    # Statistics
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uses = models.IntegerField(default=0)
    revisions = models.IntegerField(default=0)

    # Tag
    official = models.BooleanField(default=False)
    name = models.CharField(max_length=90, db_index=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.name}"


class TagAlias(models.Model):
    owner = models.ForeignKey('botdata.DiscordUser', related_name='tags_aliases', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='aliases', on_delete=models.CASCADE)

    uses = models.IntegerField(default=0)

    name = models.CharField(max_length=90, db_index=True)

    def __str__(self):
        return f"{self.name} -> {self.tag.name}"

