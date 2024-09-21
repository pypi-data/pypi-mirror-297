import sys
import atexit

MPI = None

def _import_mpi(use_dill=False):
    global MPI
    try:
        from mpi4py import MPI as _MPI
        if use_dill:
            import dill
            _MPI.pickle.__init__(dill.dumps, dill.loads, dill.HIGHEST_PROTOCOL)
        MPI = _MPI
    except:
        raise ImportError("Please install mpi4py")

    return MPI


class MPIPool:
    r"""A processing pool that distributes tasks using MPI.
    With this pool class, the master process distributes tasks to worker
    processes using an MPI communicator.
    

    Parameters
    ----------
    comm : :class:`mpi4py.MPI.Comm`, optional
        An MPI communicator to distribute tasks with. If ``None``, this uses
        ``MPI.COMM_WORLD`` by default.
    use_dill : bool, optional
        If ``True``, use dill for pickling objects. This is useful for
        pickling functions and objects that are not picklable by the default
        pickle module. Default is ``True``.

    Notes
    -----
    This implementation is inspired by @juliohm in `this module
    <https://github.com/juliohm/HUM/blob/master/pyhum/utils.py#L24>`_
    and was adapted from schwimmbad.
    """

    def __init__(self, comm=None, use_dill=True):

        global MPI
        if MPI is None:
            MPI = _import_mpi(use_dill=use_dill)

        self.comm = MPI.COMM_WORLD if comm is None else comm

        self.master = 0
        self.rank = self.comm.Get_rank()

        atexit.register(lambda: MPIPool.close(self))

        if not self.is_master():
            # workers branch here and wait for work
            self.wait()
            sys.exit(0)

        self.workers = set(range(self.comm.size))
        self.workers.discard(self.master)
        self.size = self.comm.Get_size() - 1

        if self.size == 0:
            raise ValueError("Tried to create an MPI pool, but there "
                             "was only one MPI process available. "
                             "Need at least two.")


    def wait(self):
        r"""Tell the workers to wait and listen for the master process. This is
        called automatically when using :meth:`MPIPool.map` and doesn't need to
        be called by the user.
        """
        if self.is_master():
            return

        status = MPI.Status()
        while True:
            task = self.comm.recv(source=self.master, tag=MPI.ANY_TAG, status=status)

            if task is None:
                # Worker told to quit work
                break

            func, arg = task
            result = func(arg)
            # Worker is sending answer with tag
            self.comm.ssend(result, self.master, status.tag)


    def map(self, worker, tasks):
        r"""Evaluate a function or callable on each task in parallel using MPI.
        The callable, ``worker``, is called on each element of the ``tasks``
        iterable. The results are returned in the expected order.
        
        Parameters
        ----------
        worker : callable
            A function or callable object that is executed on each element of
            the specified ``tasks`` iterable. This object must be picklable
            (i.e. it can't be a function scoped within a function or a
            ``lambda`` function). This should accept a single positional
            argument and return a single object.
        tasks : iterable
            A list or iterable of tasks. Each task can be itself an iterable
            (e.g., tuple) of values or data to pass in to the worker function.

        Returns
        -------
        results : list
            A list of results from the output of each ``worker()`` call.
        """

        # If not the master just wait for instructions.
        if not self.is_master():
            self.wait()
            return


        workerset = self.workers.copy()
        tasklist = [(tid, (worker, arg)) for tid, arg in enumerate(tasks)]
        resultlist = [None] * len(tasklist)
        pending = len(tasklist)

        while pending:
            if workerset and tasklist:
                worker = workerset.pop()
                taskid, task = tasklist.pop()
                # "Sent task %s to worker %s with tag %s"
                self.comm.send(task, dest=worker, tag=taskid)

            if tasklist:
                flag = self.comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
                if not flag:
                    continue
            else:
                self.comm.Probe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)

            status = MPI.Status()
            result = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG,
                                    status=status)
            worker = status.source
            taskid = status.tag

            # "Master received from worker %s with tag %s"

            workerset.add(worker)
            resultlist[taskid] = result
            pending -= 1

        return resultlist


    def close(self):
        """ Tell all the workers to quit."""
        if self.is_worker():
            return

        for worker in self.workers:
            self.comm.send(None, worker, 0)


    def is_master(self):
        return self.rank == 0


    def is_worker(self):
        return self.rank != 0


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self.close()