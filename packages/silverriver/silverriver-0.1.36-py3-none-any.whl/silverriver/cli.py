import argparse
import logging

from silverriver.golden_paths.record_golden_draft import track_interactions_to_file


def main():
    parser = argparse.ArgumentParser(description="SilverRiver CLI")
    parser.add_argument('url', nargs='?', help='The URL of the webpage to navigate to')
    parser.add_argument('--record-trace', action='store_true', help='Record a trace')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('-o', '--output', default='interaction_trace.json', help='The output JSON file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='[%(levelname)s] %(message)s')

    if args.record_trace:
        if not args.url:
            parser.error("The url argument is required when using --record-trace")
        if not (args.url.startswith('http://') or args.url.startswith('https://')):
            parser.error("The url argument must start with http:// or https://")

        track_interactions_to_file(args.url, args.output, args.headless)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
