# -*- coding:utf-8 -*-
import Queue
import sys
from threading import Thread


# working thread
class Worker(Thread):
    worker_count = 0
    timeout = 1

    def __init__(self, work_queue, result_queue, **kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        """ the get-some-work, do-some-work main loop of worker threads """
        while True:
            try:
                func, args, kwds = self.work_queue.get(timeout=Worker.timeout)
                res = func(*args, **kwds)
                print "worker[%2d]: %s" % (self.id, str(res))
                self.result_queue.put(res)
                # time.sleep(Worker.sleep)
            except Queue.Empty:
                break
            except:
                print 'worker[%2d]' % self.id, sys.exc_info()[:2]
                raise


class WorkerManager:
    def __init__(self, num_of_workers=10, timeout=5):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self.recruit_threads(num_of_workers)

    def recruit_threads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.work_queue, self.result_queue)
            self.workers.append(worker)

    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.work_queue.empty():
                self.workers.append(worker)
        print "All jobs are are completed."

    def add_job(self, func, *args, **kwds):
        self.work_queue.put((func, args, kwds))

    def get_result(self, *args, **kwds):
        return self.work_queue.get(*args, **kwds)