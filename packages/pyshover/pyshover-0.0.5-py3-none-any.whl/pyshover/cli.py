#!/usr/bin/env python
import argparse
import logging
import sys

from pyshover import Pushover, PushoverException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

log = logging.getLogger("pushover")
log.setLevel(logging.WARNING)
ERR = 1


def main():
    parser = argparse.ArgumentParser(
        description="Send notifications using Pushover API", epilog=""
    )
    parser.add_argument(
        "--app_token",
        help="Pushover app token. If unset, will attempt to use PUSHOVER_APP_TOKEN from environment",
    )
    parser.add_argument(
        "--user_token",
        help="Pushover user token. If unset, will attempt to use PUSHOVER_USER_TOKEN from environment",
    )
    parser.add_argument(
        "--device_token",
        help="Pushover device token. If unset, will attempt to use PUSHOVER_DEVICE_TOKEN from environment",
    )
    parser.add_argument("--verbose", "-v", help="Verbose output", action="store_true")
    parser.add_argument(
        "--title",
        "-t",
        required=True,
        help="Title of the message",
        default=None,
    )
    parser.add_argument(
        "--message",
        "-m",
        required=True,
        help="Message to send",
        default=None,
    )

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    try:
        pushover = Pushover(
            app_token=args.app_token,
            user_token=args.user_token,
            device_token=args.device_token,
            title=args.title,
            message=args.message,
        )

        response = pushover.send()
        log.info(f"Message sent successfully. Response: {response}")

    except PushoverException as e:
        log.error(f"Error sending message: {e}")
        sys.exit(ERR)


if __name__ == "__main__":
    main()
