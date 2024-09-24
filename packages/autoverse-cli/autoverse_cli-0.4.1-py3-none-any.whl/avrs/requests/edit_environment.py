from avrs.requests.request import AvrsApiRequest

class AvrsEditEnvironmentRequests():
    def __init__(self, parser, cfg):
            psr = parser.add_parser('edit-environment', help='Edits the environment')
            sps = psr.add_subparsers(required= True, help='')
            AvrsSetTimeOfDayRequest(sps, cfg)


class AvrsSetTimeOfDayRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'SetTimeOfDay', '')
        psr = parser.add_parser('set-time-of-day', help='sets the current time of day')
        psr.add_argument('tod', type=float, help='The time of day (0-24) to set')
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        self.target_object_id = ''
        return {
            'TimeOfDay': args.tod
        }