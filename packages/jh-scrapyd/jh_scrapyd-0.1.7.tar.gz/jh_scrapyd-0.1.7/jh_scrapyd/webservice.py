import traceback
from twisted.python import log
from copy import copy

from scrapyd.jobstorage import job_items_url, job_log_url
from scrapyd.utils import JsonResource
from scrapyd.utils import native_stringify_dict


class WsResource(JsonResource):

    def __init__(self, root):
        JsonResource.__init__(self)
        self.root = root

    def render(self, txrequest):
        try:
            return JsonResource.render(self, txrequest).encode('utf-8')
        except Exception as e:
            if self.root.debug:
                return traceback.format_exc().encode('utf-8')
            log.err()
            r = {"node_name": self.root.nodename, "status": "error", "message": str(e)}
            return self.render_object(r, txrequest).encode('utf-8')


class DaemonStatus(WsResource):

    def render_GET(self, txrequest):
        pending = self.root.poller.get_queues_count()
        running = len(self.root.launcher.processes)
        finished = len(self.root.launcher.finished)

        return {
            "node_name": self.root.nodename,
            "status": "ok",
            "pending": pending,
            "running": running,
            "finished": finished,
        }


class ListJobs(WsResource):

    def render_GET(self, txrequest):
        args = native_stringify_dict(copy(txrequest.args), keys_only=False)
        project = args.get('project', [None])[0]
        spiders = self.root.launcher.processes.values()
        pending = [task for project, queue in self.root.poller.get_queues().items()
                   for task in queue.list() if task['_project'] == project]

        running = [
            {
                "project": s.project,
                "spider": s.spider,
                "id": s.job,
                "pid": s.pid,
                "start_time": str(s.start_time),
            } for s in spiders if project is None or s.project == project
        ]
        finished = [
            {
                "project": s.project,
                "spider": s.spider,
                "id": s.job,
                "start_time": str(s.start_time),
                "end_time": str(s.end_time),
                "log_url": job_log_url(s),
                "items_url": job_items_url(s),
            } for s in self.root.launcher.finished
            if project is None or s.project == project
        ]
        return {"node_name": self.root.nodename, "status": "ok",
                "pending": pending, "running": running, "finished": finished}


class JhCancel(WsResource):
    def render_POST(self, txrequest):
        args = {k: v[0] for k, v in native_stringify_dict(copy(txrequest.args), keys_only=False).items()}
        project = args['project']
        jobid = args['job']
        # 信号参数
        signal = args.get('signal', 'TERM')
        # 进程id
        process_pid = args.get('pid')

        # 队列
        queue = self.root.poller.queues[project]
        if queue.has(jobid):
            # 当前任务为pending，直接清除任务队列数据
            prevstate = "pending"
            queue.cancel(jobid)
        else:
            # 存在running的任务，需要平滑关闭
            prevstate = "running"
            spiders = self.root.launcher.processes
            for index in spiders:
                spider = spiders[index]
                if spider.project == project and spider.job == jobid:
                    # 重启进程
                    self._restart_process(spider, signal, process_pid, index)

        return {"node_name": self.root.nodename, "status": "ok", "prevstate": prevstate}

    def _restart_process(self, spider, signal, process_pid, p_index):
        # 是否成功
        is_ok = False
        try:
            # 优雅终止
            spider.transport.signalProcess(signal)
            is_ok = True
        except Exception as e:
            log.msg(f"Unable to send signal {signal} to spider {spider.spider}: {e}")
            try:
                # 强制重启
                self.root.launcher.restart(p_index)
                is_ok = True
            except Exception as e:
                log.msg(f"Unable to forcefully terminate process {process_pid}: {e}")

        return is_ok
