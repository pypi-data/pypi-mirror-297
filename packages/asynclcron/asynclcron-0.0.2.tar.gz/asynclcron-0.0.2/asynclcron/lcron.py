import heapq
import pytz
import asyncio
import logging
from datetime import datetime
from croniter import croniter


logger = logging.getLogger(__name__)


class CronJob:
    def __init__(self, async_func, cron, args=None, kwargs=None, name=None) -> None:
        self.async_func = async_func
        self.cron = cron
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.name = name

    def __str__(self) -> str:
        return f"job {self.name if self.name else ''} {self.cron}"


class LightweightCron:
    """
    currently this is a static cron schedule
    wait exact time then trigger the earliest job
    """

    def __init__(self, jobs, tz_name=None, log_next_run_datetime=True) -> None:
        self._jobs = jobs
        self._tz_name = tz_name
        self._log_next_run_datetime = log_next_run_datetime
        if not self._jobs:
            raise Exception("jobs are required")

    def _init_jobs(self):
        """
        add jobs to headq
        add idx to break tie for headq
        """
        q = []
        curr_dt = datetime.now(pytz.timezone(self._tz_name)) if self._tz_name else datetime.now()
        for idx, job in enumerate(self._jobs):
            iter = croniter(job.cron, curr_dt)
            next_dt = iter.get_next(datetime)
            if self._log_next_run_datetime:
                logger.info(f"{job}: next run at {next_dt}")
            q.append((next_dt, idx, iter, job, None))
        heapq.heapify(q)

        return q

    async def run(self):
        # init jobs
        q = self._init_jobs()

        while True:
            curr_dt = datetime.now(pytz.timezone(self._tz_name)) if self._tz_name else datetime.now()
            run_dt, idx, iter, job, _ = q[0]
            # logger.info(f"run_dt={run_dt}, curr_dt={curr_dt}, job={job}")
            if run_dt > curr_dt:
                # wait until first job can run
                wait_seconds = (run_dt - curr_dt).total_seconds()
                # logger.info(f"wait {wait_seconds} seconds")
                await asyncio.sleep(wait_seconds)
            else:
                # run job
                task = asyncio.create_task(job.async_func(*job.args, **job.kwargs), name=job.name)

                # add job next
                next_dt = iter.get_next(datetime)
                if self._log_next_run_datetime:
                    logger.info(f"{job}: next run at {next_dt}")
                heapq.heapreplace(q, (next_dt, idx, iter, job, task))

                # let tasks run
                await asyncio.sleep(0)
