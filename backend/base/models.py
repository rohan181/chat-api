from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    reply = models.TextField( null=True)
    api = models.TextField( null=True)
    audio = models.FileField(upload_to='note/',null=True)

class video(models.Model):
   file = models.FileField(upload_to='documents/',null=True)
   message = models.TextField(null=True)
   image = models.ImageField(upload_to='images/',null=True)


class UserProfilesModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    nickname = models.CharField(max_length=255, db_index=True)
    telephone = models.CharField(null=True, blank=True, default="", max_length=255)
    password = models.CharField(null=True, blank=True, default="", max_length=255)
    password_update_time = models.DateTimeField(null=True, blank=True)
    birthday = models.DateField()


class AIProfilesModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    birthday = models.DateTimeField(null=True, blank=True)
    ai_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # Calculates AI age
    def get_age(self):
        if self.ai_activated:
            now = timezone.now
            today = date.today()

            one_or_zero = (today.month, today.day) < (self.birthday.month, self.birthday.day)

            year_difference = today.year - self.birthday.year

            age = year_difference - one_or_zero

            return age
        return "Not activated yet."

    def save(self, *args, **kwargs):
        if self.ai_activated:
            if not self.birthday:
                self.birthday = timezone.now()
        super().save(*args, **kwargs)


class UserAI(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    ai = models.ForeignKey(AIProfilesModel, on_delete=models.CASCADE)


class Tag(models.Model):
    tag = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.tag


class AvaterModel(models.Model):
    avater_ai = models.ForeignKey(AIProfilesModel, on_delete=models.CASCADE)
    avater_image = models.ImageField(upload_to="", blank=True, null=True)
    GENDER_CHOICES = (
        ("m", ("Male")),
        ("f", ("Female")),
    )
    gender = models.CharField(max_length=6, db_index=True, choices=GENDER_CHOICES, blank=True, null=True)


class CollectionModel(models.Model):
    """
    Collection class to hold details of collections
    """

    collection_name = models.CharField(null=True, blank=True, default="", max_length=255)
    collection_description = models.TextField()

    def __str__(self):
        return self.collection_name


class SmsModel(models.Model):
    """
    SMS Model to handle SIM verification

    """

    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0, blank=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.telephone


class NotificationModel(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    notification_content = models.TextField()
    notification_read = models.BooleanField(default=0)


class VideoModel(models.Model):
    video = models.FileField(upload_to="")
    video_tags = models.ManyToManyField(Tag, blank=True)
    video_runtime = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    video_short_description = models.CharField(null=True, blank=True, default="", max_length=255)


class TopicModel(models.Model):
    topic_name = models.CharField(null=True, blank=True, default="", max_length=255)
    is_free = models.BooleanField(default=False)
    topic_description = models.TextField()
    topic_tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.topic_name


class LongVideoModel(VideoModel):
    long_video_name = models.CharField(null=True, blank=True, default="", max_length=255)
    activate_time = models.DateTimeField()
    liked_number = models.IntegerField()
    is_long_video = models.BooleanField(default=False)
    source = models.CharField(null=True, blank=True, default="", max_length=255)

    def __str__(self):
        return self.long_video_name

    def video_type(self):
        if self.video_runtime > 360:
            self.is_long_video = True
            return self.is_long_video


class ShortVideoModel(VideoModel):
    short_video_name = models.CharField(null=True, blank=True, default="", max_length=255)
    activate_time = models.DateTimeField()
    liked_number = models.IntegerField()
    is_long_video = models.BooleanField(default=False)
    source = models.CharField(null=True, blank=True, default="", max_length=255)

    def __str__(self):
        return self.short_video_name

    def video_type(self):
        if self.video_runtime < 360:
            self.is_long_video = False
            return self.is_long_video


class FeedsModel(models.Model):
    feed_owner = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    feed_content = models.TextField()
    feed_tags = models.ManyToManyField(Tag, blank=True)


class FeedCommentModel(models.Model):
    feed_component = models.ForeignKey(FeedsModel, on_delete=models.CASCADE, default=1)
    comment_author = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE, default=1)
    comment_content = models.TextField()
    is_parent_comment = models.BooleanField(default=False)


class LettersModel(models.Model):
    letter_owner = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    voice_message = models.FileField(upload_to="")


class LikedVideosModel(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)


class LikedFeedsModel(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    feed = models.ForeignKey(FeedsModel, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)


class UserTopicsModel(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicModel, on_delete=models.CASCADE)
    is_following = models.BooleanField(default=True)


class UserCollectionsModel(models.Model):
    user = models.ForeignKey(UserProfilesModel, on_delete=models.CASCADE)
    collection = models.ForeignKey(CollectionModel, on_delete=models.CASCADE)
    is_following = models.BooleanField(default=True)   