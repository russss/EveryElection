import csv
import re

import requests
from django.conf import settings

from storage.s3wrapper import S3Wrapper


class ReadFromCSVMixin(object):
    """
    A generic mixin for for a reading from a CSV file in a Django
    management command.

    The CSV file can be a local file, a URL or on an S3 bucket.

    `self.S3_BUCKET_NAME` needs to be set when using S3.
    """
    ENCODING = 'utf-8'
    DELIMITER = ','
    S3_BUCKET_NAME = settings.LGBCE_BUCKET

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-f',
            '--file',
            action='store',
            help='Path to import e.g: /foo/bar/baz.csv',
        )
        group.add_argument(
            '-u',
            '--url',
            action='store',
            help='URL to import e.g: http://foo.bar/baz.csv',
        )
        group.add_argument(
            '-s',
            '--s3',
            action='store',
            help='S3 key to import e.g: foo/bar/baz.csv'
        )

    def read_local_csv(self, filename):
        f = open(filename, 'rt', encoding=self.ENCODING)
        reader = csv.DictReader(f, delimiter=self.DELIMITER)
        return list(reader)

    def read_csv_from_url(self, url):
        r = requests.get(url)

        # if CSV came from google docs
        # manually set the encoding
        gdocs_pattern = r'(.)+docs\.google(.)+\/ccc(.)+'
        if re.match(gdocs_pattern, url):
            r.encoding = self.ENCODING

        csv_reader = csv.DictReader(r.text.splitlines())
        return list(csv_reader)

    def read_csv_from_s3(self, filepath):
        s3 = S3Wrapper(self.S3_BUCKET_NAME)
        f = s3.get_file(filepath)
        return self.read_local_csv(f.name)

    def load_csv_data(self, options):
        if options['file']:
            return self.read_local_csv(options['file'])
        if options['url']:
            return self.read_csv_from_url(options['url'])
        if options['s3']:
            return self.read_csv_from_s3(options['s3'])