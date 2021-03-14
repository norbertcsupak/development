import time
import os
import sys
from watchdog.observers import  Observer
from watchdog.events import PatternMatchingEventHandler,RegexMatchingEventHandler
from stat import *
import logging

def on_created(event):
	logging.info(f'File created: {event.src_path} -> {os.stat(event.src_path)}')

def on_delete(event):
	logging.info(f'File deleted: {event.src_path}')

def on_moved(event):
    logging.info(f'File moved from {event.src_path} to {event.dest_path} -> {os.stat(event.dest_path)}')


def on_modified(event):
    logging.info(f'Modified: {event.src_path} -> {os.stat(event.src_path)}')

if __name__ == '__main__':

	FORMAT = '%(asctime)-15s %(message)s'
	logging.basicConfig(filename='/tmp/watchdog.log', level=logging.INFO, format=FORMAT)
	logging.info('Started')

	path = sys.argv[1] if len(sys.argv) > 1 else '/home/norbert/Desktop'

	patterns = ['.+']
	ignore_patterns = [f"^{path}\.+"]
	ignore_dirs = False
	case_sensitive = True

	my_event_handler = RegexMatchingEventHandler(patterns,ignore_patterns,ignore_dirs,case_sensitive)
	my_event_handler.on_created = on_created
	my_event_handler.on_deleted = on_delete
	my_event_handler.on_moved = on_moved
	my_event_handler.on_modified = on_modified


	go_recursively = True
	my_observer = Observer()

	my_observer.schedule(my_event_handler, path ,recursive=go_recursively)


	my_observer.start()
	try:
		while True:
			time.sleep(1)
	except  KeyboardInterrupt:
		my_observer.stop()
		my_observer.join()

