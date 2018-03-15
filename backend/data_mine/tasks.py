from celery.schedules import crontab
from backend.celery import app as celery_app
from data_mine.InsertTickers import InsertTickers


@celery_app.task(name="insert_ticker_nightly")
def insert_ticker_nightly():
    ins = InsertTickers()
    ins.run(1, ['AAPL'])


@celery_app.task(name="run_experiment_nightly")
def run_experiment():
    pass


@celery_app.task(name="insert_prediction_nightly")
def insert_prediction():
    pass


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # should use UTC time
    # Call task every 10 seconds.
    sender.add_periodic_task(
        2.0,
        insert_ticker_nightly.s(),
        name="insert_ticker")

    # run experiment nightly
    sender.add_periodic_task(
        crontab(hour=4, minute=4),
        run_experiment.s(),
        name="run_experiment_daily",
    )

    # insert prediction nightly
    sender.add_periodic_task(
        crontab(hour=4, minute=4),
        insert_prediction.s(),
        name="insert_prediction_nightly",
    )

    '''
    # Executes crontab
    sender.add_periodic_task(
        crontab(hour=4, minute=39),
        insert_ticker_nightly.s(),
        name="insert_ticker_nightly"
    )
    '''
