import argparse

# region - Set up description / arguments
from app.app import App

parser = argparse.ArgumentParser(description='Process self-admin data')
parser.add_argument('source',
                    metavar='S',
                    type=str,
                    help='The absolute path to the root directory containing dated sub directories.')

args = parser.parse_args()

# endregion

# start the app
if __name__ == '__main__':
    App(args.source).run()
