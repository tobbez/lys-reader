import sys
from backend.feedhandler import FeedHandler

def main(args):
    fh = FeedHandler()
    fh.handle_forever()

if __name__ == '__main__':
    main(sys.argv)