import time
from uuid import uuid4


class Locking:
    def __init__(self, duration=None):
        self.duration = duration or 60
        self.locks = {}

    def get(self, uid):
        lock = self.locks.get(uid)
        if lock is not None and lock['due'] > time.time():
            return None

        token = uuid4().hex
        self.locks[uid] = {'due': time.time() + self.duration,
                           'token': token}
        return token

    def release(self, uid, token=None):
        lock = self.locks.get(uid)
        if lock is None:
            return True
        if lock['due'] < time.time():
            del self.locks[uid]
            return True
        if lock['token'] == token:
            del self.locks[uid]
            return True
        return False

    def verify(self, uid, token):
        lock = self.locks.get(uid)
        if lock is None:
            return False
        if lock['token'] != token:
            return False
        if lock['due'] < time.time():
            return False
        return True

    # I suggest to clean expired lock in a time period
    # but I skip it for this assessment project
    # def clean(self):
    #     to_del = []
    #     now = time.time()
    #     for uid, item in self.locks:
    #         if item['due'] < now:
    #             to_del.append(uid)
    #     for uid in to_del:
    #         del self.locks[uid]


def test_locking():
    locking = Locking(duration=1)

    assert(locking.release(1) is True)

    t = locking.get(1)
    assert(t is not None)
    bad_t = locking.get(1)
    assert(bad_t is None)
    assert(locking.verify(1, t) is True)
    assert(locking.release(1) is False)
    assert(locking.release(1, t) is True)

    t = locking.get(1)
    assert(t is not None)
    assert(locking.verify(1, t) is True)
    assert(locking.release(1) is False)
    time.sleep(3)
    assert(locking.verify(1, t) is False)
    assert(locking.release(1) is True)

    print('test_locking done')

# test_locking()
