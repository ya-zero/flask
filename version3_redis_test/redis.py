from redis import Redis
import rq

def redis_send(ipaddr,command):
queue= rq.Queue('microblog',connection=Redis.from_url('redis://'))
job= queue.enqueue('task_ssh.send_command',ipaddr,command)
