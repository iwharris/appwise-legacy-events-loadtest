#!/usr/local/bin/python3

import argparse
import random
import threading
from queue import Queue

import boto3

from helpers import data_helper

sqs = boto3.resource('sqs')


def send_event_batch(sqs_queue, events):
    entries = [{
        'Id': event.get('id'),
        # 'MessageGroupId': 'appwise',  # Required if FIFO queue
        'MessageBody': data_helper.object_to_json(event)
    } for event in events]
    # print(entries)

    response = sqs_queue.send_messages(Entries=entries)
    # Print out any failures
    failures = response.get('Failed')
    if failures:
        print(failures)


def build_random_event():
    return {
        'id': data_helper.random_string(),
        'url': data_helper.random_url(),
        'source': 'loadtest',
        'description': data_helper.random_string(60),
        'source_content_type': 'loadtest',
        'utc_last_modified': '2017-09-07T10:27:57Z',
        'user_id': random.choice(range(5)),
        'service_id': random.choice(range(5))
    }


def do_work(q, sqs_queue, thread_id):
    while True:
        num_events = q.get()
        try:
            # print('Thread {}: Sending {} events'.format(thread_id, num_events))
            events = [build_random_event() for _ in range(num_events)]
            send_event_batch(sqs_queue, events)
        finally:
            q.task_done()


def perform_load_test():
    sqs_queue = sqs.get_queue_by_name(QueueName=args.queue_name)

    work_queue = Queue(maxsize=args.num_events)

    # create worker threads
    for i in range(args.num_threads):
        worker = threading.Thread(target=do_work, args=(work_queue, sqs_queue, i))
        worker.setDaemon(True)
        worker.start()

    # populate work queue with jobs
    for x in range(int(args.num_events / args.batch_size)):
        work_queue.put(args.batch_size)
    if args.num_events % args.batch_size:
        work_queue.put(args.num_events % args.batch_size)

    # wait for threads to finish
    try:
        work_queue.join()
    finally:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate fake legacy events for load testing.')
    parser.add_argument('-n', action='store', dest='num_events', type=int, default=10, help='Number of events to generate')
    parser.add_argument('-b', action='store', dest='batch_size', type=int, default=10, help='SQS batch size')
    parser.add_argument('-q', action='store', dest='queue_name', type=str, nargs='+', default='legacy-connector-events-dev', help='SQS queue name')
    parser.add_argument('-t', action='store', dest='num_threads', type=int, default=1, help='Number of threads sending events')
    args = parser.parse_args()

    try:
        perform_load_test()
    except KeyboardInterrupt:
        pass
