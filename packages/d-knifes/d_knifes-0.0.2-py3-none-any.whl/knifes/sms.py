from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models
from typing import List
from django.conf import settings
import re
pattern_china_mainland_phone_number = re.compile(r'^1\d{10}$')
exceed_limit_codes = ['LimitExceeded.PhoneNumberDailyLimit', 'LimitExceeded.PhoneNumberOneHourLimit', 'LimitExceeded.PhoneNumberSameContentDailyLimit', 'LimitExceeded.PhoneNumberThirtySecondLimit']
incorrect_number_codes = ['InvalidParameterValue.IncorrectPhoneNumber']


class SmsError(Exception):
    pass


class LimitExceededError(SmsError):
    pass


class IncorrectNumberError(SmsError):
    pass


class SendFailedError(SmsError):
    pass


def send_sms_msg_by_tencent_cloud(sign_name, phone, template_id, template_param_list: List[str] = None):
    if template_param_list is None:
        template_param_list = []
    cred = credential.Credential(settings.TENCENT_CLOUD_SMS_SECRET_ID, settings.TENCENT_CLOUD_SMS_SECRET_KEY)

    client_profile = ClientProfile(httpProfile=HttpProfile(endpoint='sms.tencentcloudapi.com'))
    client = sms_client.SmsClient(cred, "ap-guangzhou", client_profile)
    req = models.SendSmsRequest()

    req.SmsSdkAppId = settings.TENCENT_CLOUD_SMS_APP_ID
    req.SignName = sign_name
    req.PhoneNumberSet = ["+86" + phone]
    req.TemplateId = template_id
    req.TemplateParamSet = template_param_list

    resp = client.SendSms(req)
    code = resp.SendStatusSet[0].Code
    if code in exceed_limit_codes:
        raise LimitExceededError('该手机号短信发送频率太高，请稍后重试~')
    if code in incorrect_number_codes:
        raise IncorrectNumberError('手机号格式错误')
    if code != 'Ok':
        raise SendFailedError('发送失败，请重试！')


def is_china_mainland_phone_number(phone):
    return True if re.match(pattern_china_mainland_phone_number, str(phone)) else False


