import threading
import random
import time
import queue

# put by producer, got by consumer
producer = queue.Queue(maxsize = 1)

# put by consumer, got by producer

consumer = queue.Queue(maxsize = 1)

print_lock = threading.Lock()

def my_print(msg):
    with print_lock:
        print(msg)

def consumer_thread_proc():
    
    rnd = random.Random()
    rnd.seed()

    time.sleep(1)
    
    my_print('  consumer: signaling producer start')
    consumer.put(1)

    for i in range(3):

        # wait for producer to signal ready.
        my_print('    consumer: waiting')
        val = producer.get()
        producer.task_done()
        my_print('    consumer: wait done {0}'.format(val))

        # signal producer to re-start
        my_print('  consumer: signaling producer start')
        consumer.put(1)

        # simulate time processing
        my_print('consumer: start processing {0}'.format(val))
        time.sleep(1)
        my_print('consumer: processing complete {0}'.format(val))

    # wait for producer to signal ready last time
    my_print('    consumer: waiting')
    val = producer.get()
    producer.task_done()
    my_print('    consumer: wait done {0}'.format(val))

    # signal producer to end
    my_print('      consumer:  signaling producer end')
    consumer.put(None)

    # simulate time processing
    my_print('consumer: start processing {0}'.format(val))
    time.sleep(1)
    my_print('consumer: processing complete {0}'.format(val))

def producer_thread_proc():
    
    rnd = random.Random()
    rnd.seed()
    val = 0

    # simulate other work
    time.sleep(1)

    while True:

        # wait for consumer to signal start.
        my_print('  producer: waiting')
        item = consumer.get()
        my_print('  producer: wait done')
        if item is None:
            my_print('      producer: ending')
            break
        consumer.task_done()

        # simulate time producing
        my_print('producer: start producing {0}'.format(val))
        time.sleep(1)
        my_print('producer: production complete {0}'.format(val))
        producer.put(val)
        val += 1

def main():

    consumer_thread = threading.Thread(target = consumer_thread_proc, args = ())
    producer_thread = threading.Thread(target = producer_thread_proc, args = ())

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()

main()
