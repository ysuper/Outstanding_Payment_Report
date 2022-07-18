from app import app
from outstanding_payment_report import DannyReport
from multiprocessing import Process


class MyProject:

    def run_flask(self):
        # app.run(host='0.0.0.0', port=7711, debug=True)
        app.run(host='0.0.0.0', port=7711, debug=False)

    def run_report(self):
        DannyReport()

    def run_flask_report(self):
        p1 = Process(target=self.run_flask)
        p2 = Process(target=self.run_report)
        p1.start()
        p2.start()
        p1.join()
        p2.join()


if __name__ == '__main__':
    project = MyProject()
    project.run_flask_report()
    # project.run_flask()
    # project.run_report()
