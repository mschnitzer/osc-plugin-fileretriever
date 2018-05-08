import sys
import osc
from osc.core import http_GET

@osc.cmdln.option('--rev', '-r', metavar='Revision', help='revision of the target file')

def do_get(self, subcmd, opts, *args):
    opts = opts.__dict__
    args = list(args)

    try:
        if len(args) != 2:
            raise ValueError

        project, package = args[0].split('/')
    except ValueError:
        sys.stderr.write("Usage: osc get $project/$package $file\n")
        sys.exit(1)

    package_file = args[1]

    apiurl = self.get_api_url()

    query = []
    if opts['rev']:
        query.append('rev=%s' % opts['rev'])

    url = makeurl(apiurl, ['source', project, package, package_file], query=query)
    print(http_GET(url).read())

# vim: sw=4 et ts=4
