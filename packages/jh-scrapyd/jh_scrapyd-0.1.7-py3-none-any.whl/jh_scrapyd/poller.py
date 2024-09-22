from twisted.internet.defer import DeferredQueue, inlineCallbacks, maybeDeferred, returnValue
from zope.interface import implementer

from scrapyd.interfaces import IPoller
from jh_scrapyd.common import get_spider_queues
from jh_scrapyd import is_unified_queue



@implementer(IPoller)
class QueuePoller(object):

    def __init__(self, config):
        self.config = config
        self.update_projects()
        self.dq = DeferredQueue()

    @inlineCallbacks
    def poll(self):
        if not self.dq.waiting:
            return
        for p, q in self.queues.items():
            c = yield maybeDeferred(q.count)
            if c:
                msg = yield maybeDeferred(q.pop)
                if msg is not None:  # In case of a concurrently accessed queue
                    returnValue(self.dq.put(self._message(msg, p)))

    def next(self):
        return self.dq.get()

    def update_projects(self):
        self.queues = get_spider_queues(self.config)

    def get_queues(self) -> dict:
        """Obtain the actual queue"""
        queues = {}
        i = 0
        for project, queue in self.queues.items():
            if is_unified_queue() and i > 0:
                # When unifying the queue, only one calculation is needed
                break
            queues[project] = queue
            i += 1
        return queues

    def get_queues_count(self) -> int:
        """Obtain the actual number of queue tasks"""
        total = 0
        for project, queue in self.get_queues().items():
            total += queue.count()
        return total

    def _message(self, queue_msg, project):
        d = queue_msg.copy()
        # TODO Unified queue processing
        if not is_unified_queue():
            # Non-uniform queue
            d['_project'] = project
        d['_spider'] = d.pop('name')
        return d
