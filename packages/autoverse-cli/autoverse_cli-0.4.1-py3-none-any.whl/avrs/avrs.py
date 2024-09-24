#!/usr/bin/env python3
import argparse
from argparse import RawDescriptionHelpFormatter
from argparse import RawTextHelpFormatter

from avrs.app_version import *
from avrs.cfg import *
from avrs.launcher import *
from avrs.argparse_help import *

from avrs.requests.move_to_landmark import MoveToLandmarkRequest
from avrs.requests.restart import Restart
from avrs.requests.reset_to_track import ResetToTrack
from avrs.requests.teleport import Teleport
#from src.requests.can import Can
from avrs.requests.npc import Npc
from avrs.requests.reserve_mv_slot import ReserveMvSlot
from avrs.requests.vd import Vd
from avrs.requests.input import InputRequest
from avrs.requests.log_path import LogPath
from avrs.requests.demo import AvrsDemoRequest
from avrs.requests.edit_environment import AvrsEditEnvironmentRequests
from avrs.requests.code_booz import *


def get_version():
    return get_app_version()

def main():
    parser = argparse.ArgumentParser(
            prog='avrs', 
            description='Autoverse CLI',
            epilog='',
            formatter_class=RawTextHelpFormatter)

    version_psr = parser.add_argument(
            '--version', 
            help='show the cli version', 
            action='version', 
            version=get_version())

    sps = parser.add_subparsers(required=True, help='sub-command help')

    cfg = load_cfg('avrs')
    check_app_is_latest()

    AvrsLauncher(sps, cfg)


    MoveToLandmarkRequest(sps, cfg)
    Restart(sps, cfg)
    ResetToTrack(sps, cfg)
    #Can(sps, cfg)
    Teleport(sps, cfg)
    Npc(sps, cfg)
    ReserveMvSlot(sps, cfg)
    Vd(sps, cfg)
    #InputRequest(sps, cfg)
    LogPath(sps, cfg)
    AvrsEditEnvironmentRequests(sps, cfg)
    AvrsCodeBoozRequest(sps, cfg)
    AvrsDemoRequest(sps, cfg)

    if os.environ.get('AVRS_GEN_DOCS', '0') == '1':
        generate_argparse_docs(parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()