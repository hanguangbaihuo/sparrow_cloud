from sparrow_cloud.message_service.sender import send_task


# send_task(exchange="topic_1",
#           routing_key="ORDER_PAY_SUC_ONLINE",
#           message_code="ORDER_PAY_SUC_ONLINE",
#           test={'test': "1"},)


def task1(*args, **kwargs):
    print('='*10)




