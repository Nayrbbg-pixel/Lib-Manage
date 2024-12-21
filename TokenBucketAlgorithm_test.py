import time


class TokenBucket:
    def __init__(self,capacity,rate):
        self.tokens = capacity
        self.capacity = capacity
        self.rate = rate
        self.last_refill = time.time()
        
    def allow_request(self):
        current_time = time.time()
        elapsed = current_time-self.last_refill
        self.tokens = min(self.capacity,self.tokens+elapsed*self.rate)
        self.last_refill = current_time
        if self.tokens >= 1:
            self.tokens -=1
            return True
        return False
    
# User simulation

user= {'username':'Test','id':12,'role':'user'}

# Api 

class TestAPI:
    def __init__(self,username:str,id:int,role:str):
        self.username = username
        self.id = id
        self.role = role
        self.tokenBucket = TokenBucket(10,1)
        
    def middleware(self):
        val = self.tokenBucket.allow_request()
        return val
        
    def api(self):
        val = self.middleware()
        if val:
            print({'msg':f'You are {self.username}, your id is {self.id}, your role is {self.role}'})
        else:
            print('Rate limit reached')
            
# Simulation
test = TestAPI(user['username'],user['id'],user['role'])
for i in range(100):
    if i == 99:
        time.sleep(1)
        test.api()
        break
    test.api()