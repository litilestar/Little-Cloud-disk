

from celery_tasks.main import celery_app
from .utils.yuntongxun.sms import CCP
import logging

logger = logging.getLogger('django')

@celery_app.task(name='send_sms_code')
def send_sms_codes(mobile,sms_code,expires,temp_id):
    # # 发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile ,[sms_code ,expires] ,temp_id)
    except Exception as ret:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, ret))

    else:
        if result == 0:
            logger.info("发送验证码Ok mobile: %s" % mobile)

        else:
            logger.warning("发送验证码短信失败 mobile: %s," % mobile)

