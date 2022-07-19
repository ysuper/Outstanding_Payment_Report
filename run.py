from app import app
from outstanding_payment_report import DannyReport
from remind_sales_report import SendSalesReport
from multiprocessing import Process
from apscheduler.schedulers.background import BlockingScheduler


class MyProject:

    def run_flask(self):
        # app.run(host='0.0.0.0', port=7711, debug=True)
        app.run(host='0.0.0.0', port=7711, debug=False)

    def run_boss_report(self):
        DannyReport()

    def run_sales_report(self):
        SendSalesReport(official=True)
        # SendSalesReport(official=False)

    def run_scheduler(self):
        sched = BlockingScheduler()
        sched.add_job(self.run_boss_report, 'interval', hours=1)
        sched.add_job(self.run_sales_report,
                      'cron',
                      day_of_week='mon-fri',
                      hour=18,
                      minute=0,
                      second=0,
                      misfire_grace_time=60)
        sched.start()

    def run_all(self):
        p_list = []
        run_list = [
            self.run_flask,
            self.run_scheduler,
            # self.run_boss_report,
            # self.run_sales_report,
        ]
        for i in run_list:
            p_list.append(Process(target=i))
        for p in p_list:
            p.start()
        for p in p_list:
            p.join()


if __name__ == '__main__':
    project = MyProject()
    project.run_all()
    # project.run_flask()
    # project.run_boss_report()
    # project.run_sales_report()
