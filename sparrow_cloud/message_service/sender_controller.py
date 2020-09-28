# -*- coding: utf-8 -*-
import json
import requests
import os
from sparrow_cloud.restclient import requests_client


class TaskSender(object):

    def __init__(self, message_backend_conf):
        if not message_backend_conf:
            raise Exception("message_backend_conf is not properly configured")
        self._message_backend_conf = message_backend_conf

    def base_send_task(self, message_code, args=[], kwargs={}, delay_time=0):
        # {
        #     "code": "new_task",
        #     "args": [1,2,3],
        #     "kwargs": {"key": "value"},
        #     "exchange": "default",
        #     "routing_key": "default",
        #     "delivery_mode": "persistent",
        #     "delay": False,
        #     "delay_time": 1
        # }
        data = {
            "code": message_code,
            "args": args,
            "kwargs": kwargs,
            "delivery_mode": "persistent",
            "delay_time": delay_time
        }
        parent_options = os.environ.get("SPARROW_TASK_PARENT_OPTIONS")
        if parent_options:
            # parent_options = parent_options.replace("'",'"')
            try:
                data['parent_options'] = json.loads(parent_options)
            except:
                pass
            # os.environ.pop("SPARROW_TASK_PARENT_OPTIONS")
        # import pdb; pdb.set_trace()
        backend_service_conf = self._message_backend_conf.get('SERVICE_CONF', None)
        api_path = self._message_backend_conf.get('API_PATH', None)
        result = requests_client.post(backend_service_conf, api_path=api_path, json=data)
        if result.status_code == 200:
            try:
                res = result.json()
                task_id = res.get('task_id')
                return task_id
            except:
                raise Exception(result.text)
        else:
            raise Exception(result.text)

    def send_task(self, message_code, delay_time=0, *args, **kwargs):
        # 发送任务
        # import pdb; pdb.set_trace()
        return self.base_send_task(
            message_code=message_code,
            args=args,
            kwargs=kwargs,
            delay_time=delay_time
        )

    # def send_delayed_task(self, exchange, routing_key, message_code, delay, delay_time, *args, **kwargs):
    #     # 发送延时任务
    #     return self.base_send_task(
    #         exchange=exchange,
    #         routing_key=routing_key,
    #         message_code=message_code,
    #         args=args,
    #         kwargs=kwargs,
    #         delay=delay,
    #         delay_time=delay_time
    #     )


# if __name__ == "__main__":
#     sender = TaskSender("1")
#     sender.send_task("1",2,3, order_id=5, **{"test": "q"})