import argparse
import json
import sys
from pathlib import Path


def parse_options(override_args=None):

    parser = argparse.ArgumentParser(
        prog='cpu_util',
        description='CPU utilization service',
        usage='%(prog)s [options]',
        conflict_handler='resolve',
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Print this help text and exit')

    # region common
    grp_common = parser.add_argument_group('common')
    grp_common.add_argument(
        '--config',
        default='config.json',
        dest='cfg_file',
        help='Full path to configuration file'
    )
    grp_common.add_argument(
        '--cpu-load-limit',
        default=60,
        dest='cpu_load_limit',
        help='CPU load limit for messages'
    )
    # end region

    # region RabbitMQ
    grp_rabbit = parser.add_argument_group('rabbit')
    grp_rabbit.add_argument(
        '--rabbit-host',
        dest='rabbit_host',
        default='127.0.0.1',
        help='RabbitMQ host address'
    )
    grp_rabbit.add_argument(
        '--rabbit-port',
        default=5672,
        dest='rabbit_port',
        help='RabbitMQ port number, default 5672'
    )
    grp_rabbit.add_argument(
        '--rabbit-login',
        dest='rabbit_login',
        default='guest',
        help='RabbitMQ user login'
    )
    grp_rabbit.add_argument(
        '--rabbit-psw',
        dest='rabbit_psw',
        default='guest',
        help='RabbitMQ user password'
    )
    # endregion

    if override_args is not None:
        opts = parser.parse_args(override_args)
    else:
        cmd_line_args = sys.argv[1:]
        cmd_line_opts = parser.parse_args(cmd_line_args)
        cfg_file = Path(cmd_line_opts.cfg_file)

        if cfg_file.exists():
            try:
                with cfg_file.open() as json_file:
                    cfg = [f"--{key}={value}" for (key, value) in json.load(json_file).items()]
            except Exception as e:
                parser.error(f"Can't load json configuration file {cfg_file}: {e}")
        elif any('--config' in p for p in cmd_line_args):
            parser.error(f"Configuration file {cfg_file} does not exist.")
        else:
            cfg = []

        # параметры командной строки имеют приоритет перед конфигурационным файлом
        opts = parser.parse_args(cfg + cmd_line_args)

    return parser, opts
