import json

from celery import shared_task

from afex_logger.log_service import AppLogService


@shared_task
def aggregate_log(log_type, log_data: str):
    from afex_logger.util import LogUtil

    log_util = LogUtil()
    try:
        config_provider = log_util.get_config_provider()

        if config_provider.is_test_mode():
            log_util.debug_print(log_type, "|", log_data)

        data = json.loads(log_data)
        AppLogService().submit_log(log_type, data)
    except Exception as e:
        log_util.report_exception(e)


@shared_task
def submit_log():
    try:
        AppLogService().send_logs()
    except Exception as e:
        from afex_logger.util import LogUtil
        LogUtil().report_exception(e)
