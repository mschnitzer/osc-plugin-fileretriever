import sys
import osc
from osc.core import http_GET

@osc.cmdln.option('--rev', '-r', metavar='Revision', help='revision of the target file')
@osc.cmdln.option('--destination', '-d', metavar='Destination', help='destination where the file should be stored (locally)')
@osc.cmdln.option('--quiet', '-q', action='store_true', metavar='Quiet', help="shut up and don't print anything")

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
    content = http_GET(url).read()

    if opts['destination']:
        destination = opts['destination']

        if os.path.isdir(opts['destination']):
            destination = '%s/%s' % (opts['destination'], package_file)

        target_file = open(destination, 'w+')
        target_file.write(content)
        target_file.close()

    if not opts['quiet']:
        print(content)

# vim: sw=4 et ts=4
