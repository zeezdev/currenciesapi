from datetime import datetime, timedelta

from mongoengine import (
    Document, queryset_manager,
    DateTimeField, FloatField, StringField)


class QuerysetWithoutIdMixin(object):

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.exclude('id')


class Currency(Document, QuerysetWithoutIdMixin):
    name = StringField()
    code = StringField(min_length=1, required=True, unique=True)

    meta = {
        'collection': 'currencies'
    }


class AbstractRate(Document, QuerysetWithoutIdMixin):
    """Abstract class"""
    currency = StringField(required=True)
    value = FloatField(required=True)

    meta = {
        'abstract': True,
        'allow_inheritance': False
    }


class Rate(AbstractRate):
    """Present a current rate of the certain currency"""

    meta = {
        'collection': 'rates',
    }

    @classmethod
    def find(cls, ticker):
        """Find rates for currencies that presented in the ticker"""
        return cls.objects(currency__in=ticker.to_list())


class RateHistory(AbstractRate):
    """Present a current rate of the certain currency in time"""
    ts = DateTimeField(name='ts', default=datetime.now())

    meta = {
        'collection': 'rates_history',
        'indexes': [
            {
                'fields': ['-ts', 'currency'], 'unique': True, 'sparse': False
            }
        ]
    }

    @classmethod
    def find(cls, ts, ticker):
        """We know that a step of historical data is 10min
        so make the window -10..+10 min to find objects with the nearest
        timestamps.
        """
        dt = ts.replace(second=0)
        minutes = int(str(dt.minute)[-1])

        return cls.objects(
            ts__gte=dt + timedelta(minutes=-minutes),
            ts__lt=dt + timedelta(minutes=10-minutes),
            currency__in=set(ticker.to_list())
        )
