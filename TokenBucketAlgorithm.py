import time

class TokenBucket:
    def __init__(self,capacity,rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity
        self.last_refill = time.time()
        
    def allow_request(self):
        current_time = time.time()
        elapsed = current_time - self.last_refill
        self.tokens = min(self.capacity,self.tokens+elapsed*self.rate)
        self.last_refill = current_time
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False