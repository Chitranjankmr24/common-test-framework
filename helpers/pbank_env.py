from helpers.pbank_system_properties import SystemProperties
step_seperator = "---------------------------------------------------------------------------------------------------------------------------"
step_deco = "----------------------------------------"

base_url = SystemProperties.PBANK_URL.value()
api_base_url = SystemProperties.PBANK_API_URL.value()
browser = SystemProperties.PBANK_BROWSER.value()
browser_mode = SystemProperties.PBANK_BROWSER_MODE.value()
user_name = SystemProperties.PBANK_UNAME.value()
pwd = SystemProperties.PBANK_PASSWORD.value()
collect_video = SystemProperties.PBANK_COLLECT_VIDEO.value()
registration = SystemProperties.PBANK_REGISTRATION.value()
slack_webhook = SystemProperties.PBANK_SLACK_WEBHOOK.value()



