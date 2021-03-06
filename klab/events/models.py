from django.db import models
from django.conf import settings
from smartmin.models import SmartModel

import flickr
from datetime import datetime, timedelta

class Event(SmartModel):
    """
    The blueprint of events
    """
    RECURRENCE_CHOICES = (
        ('W', "Weekly"),
        ('M', "Monthly"),
        )

    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    date = models.DateField(help_text="The date when the event will occur")
    time = models.TimeField(help_text="The start time for the event")
    duration = models.IntegerField(help_text="The duration in minutes of the event")
    title = models.CharField(max_length=64,
                                   help_text="What is the title of this event")
    logo = models.ImageField(upload_to="photos/", help_text="The image representing the event in general (should be square)")
    description = models.TextField(max_length=256,
                                   help_text="More descriptively say about this event")
    venue = models.CharField(max_length=128,
                             help_text="The exact location where event will take place")
    
    recurrence_type = models.CharField(max_length=1, choices=RECURRENCE_CHOICES, null=True, blank=True,
                                   help_text="Does this event accur weekly or monthly")
    dow = models.IntegerField(null=True, blank=True)
    monthly_ordinal = models.IntegerField(null=True, blank=True)
    photo_tag = models.CharField(max_length=64, null=True, blank=True)
    end_date = models.DateField(help_text="Last date of recurrence", null=True, blank=True)
  
    def __unicode__(self):
        return self.title

    def photos(self):
        if self.photo_tag:
            # try to get flickr photos with a given tag
            try:
                return flickr.api.walk(user_id=flickr.user_id, tags=self.photo_tag)
            except:
                # otherwise give back nothing
                return None

    # def datespan(self, startdate, enddate, delta):
    #     while startdate < enddate:
    #         yield startdate
    #         startdate += delta

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         super(Event, self).save(*args, **kwargs)

    #         # get weeks between now unt the end of event
    #         weeks = self.datespan(self.date, self.end_date, timedelta(days=7))

    #         # all event days of the week
    #         start_dates = []

    #         # store event day of the week
    #         event_dow = self.date.weekday()

    #         if self.recurrence_type == 'W':
    #             # got through days of the week
    #             for i in range(1,8):
    #                 # if dow is in a week from now
    #                 if self.dow & (2**i) != 0:
    #                     # then store days until the next events
    #                     days_until = (7 - event_dow + i - 1) % 7
    #                     start_dates.append(self.date + timedelta(days=days_until))
                    
    #             # create event for every week until the end date
    #             for i, week in enumerate(weeks):
    #                 # create event for this dates
    #                 if i != 0:
    #                     Event.objects.create(parent=self, date=week, title=self.title,
    #                                          description=self.description, flickr_tag=self.flickr_tag, end_date=self.end_date,
    #                                          created_by=self.created_by, modified_by=self.modified_by)


    #     else:
    #        super(Event, self).save(*args, **kwargs)
            
