import os
import argparse
import sys

from DarkFream.app import create_app, run_server


def main():
    parser = argparse.ArgumentParser(description="Dark Fream command-line tool")
    subparsers = parser.add_subparsers(dest="command")

    create_app_parser = subparsers.add_parser("createapp", help="Create a new app")
    create_app_parser.add_argument("app_name", help="Name of the app to create")

    run_server_parser = subparsers.add_parser("runserver", help="Run the development server")
    run_server_parser.add_argument("-a", "--address", default="127.0.0.1", help="Server address")
    run_server_parser.add_argument("-p", "--port", default=8000, type=int, help="Server port")

    args = parser.parse_args()

    if args.command == "createapp":
        create_app(args.app_name)
    elif args.command == "runserver":
        run_server(args.address, args.port)
    else:
        print("Unknown command")
        sys.exit(1)

if __name__ == "__main__":
    main()
