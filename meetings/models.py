from django.db import models

class Meeting(models.Model):
    MEETING_TYPES = [
        ('team','Team'),
        ('client','Client'),
        ('interview','Interview'),
        ('standup','Standup')
    ]

    title = models.CharField(max_length=200)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    transcript = models.TextField(blank=True, null=True)
    ai_output = models.JSONField(default=dict)
    meeting_file = models.FileField(upload_to='meetings/', blank=True, null=True)

    #add google meet
    google_meet_link = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title
