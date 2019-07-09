# -*- coding: utf-8 -*-

from networkapi import settings
from networkapi import celery_app
from networkapi.api_task.classes import BaseTask
import logging


log = logging.getLogger(__name__)


@celery_app.task(bind=True, base=BaseTask, serializer='pickle')
def async_add_flow(self, plugins, user_id, data):
    """ Asynchronous flows insertion into environment equipment """

    for plugin in plugins:
        try:
            if plugin is not None:
                plugin.add_flow(data=data)

        except Exception as err:
            log.error(err)
            continue


@celery_app.task(bind=True, base=BaseTask, serializer='pickle')
def async_flush_environment(self, plugins, user_id, data):
    """ Asynchronous flush and restore of flows of an environment """

    for plugin in plugins:
        if plugin is not None:
            plugin.update_all_flows(data=data)


@celery_app.task(bind=True, base=BaseTask, serializer='pickle')
def async_delete_flow(self, plugins, user_id, flow_id):
    """ Asynchronous delete one flow by id """

    for plugin in plugins:
        if plugin is not None:
            plugin.del_flow(flow_id=flow_id)
