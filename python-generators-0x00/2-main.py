import sys
from itertools import islice
processing = __import__('1-batch_processing')

try:
    # Limit processed output to 5 rows
    for user in islice(processing.batch_processing(50), 5):
        print(user)
except BrokenPipeError:
    sys.stderr.close()

