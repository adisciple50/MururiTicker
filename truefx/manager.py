import cookielib
import urllib
import urllib2
import ssl
import os
import errno
from lxml import html
import url_provider
import zipfile
import glob


class Manager:
    url_provider = url_provider.UrlProvider()
    login_response_cookies = False

    def download_and_merge_to_one_file(self, year, symbol, directory):

        self.download_for_year(year, symbol, directory)
        self.unzip_for_year(year, symbol, directory)

        output_filename = symbol.lower() + '-' + str(year) + '.csv'
        files = self.get_filenames_to_merge(str(year), symbol, directory)

        with open(directory + output_filename, 'w') as outfile:
            for fname in files:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
                    infile.close()
            outfile.close()

        for fname in self.get_filenames_to_delete(year, symbol, directory):
            os.unlink(fname)

    def get_filenames_to_merge(self, year, symbol, directory):
        return glob.glob(directory + symbol.upper() + '-' + str(year) + '-*.csv')

    def get_filenames_to_delete(self, year, symbol, directory):
        return glob.glob(directory + symbol.lower() + '-' + str(year) + '-*.zip') \
               + glob.glob(directory + symbol.upper() + '-' + str(year) + '-*.csv')

    def unzip_for_year(self, year, symbol, directory):

        for month in range(1, 12, 1):
            self.unzip_for_month(year, month, symbol, directory)

    def unzip_for_month(self, year, month, symbol, directory):

        filename = self.get_downloaded_filename(month, symbol, year)

        filename_with_directory = directory + filename

        zip_ref = zipfile.ZipFile(filename_with_directory, 'r')
        zip_ref.extractall(directory)
        zip_ref.close()

    def download_for_year(self, year, symbol, destination_directory):

        for month in range(1, 12, 1):

            try:
                self.download_for_month(year, month, symbol, destination_directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def download_for_month(self, year, month, symbol, destination_directory):

        filename = self.get_downloaded_filename(month, symbol, year)

        filename_with_directory = destination_directory + filename

        if os.path.isfile(destination_directory + filename):
            raise OSError(errno.EEXIST, "File '" + filename_with_directory + "' already exists",
                          filename_with_directory)

        opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.login_response_cookies)
        )

        opener.addheaders += [("Referer", self.url_provider.get_download_referrer_url(year, month))]

        url_to_download = self.url_provider.get_download_url(year, month, symbol)

        print("Downloading '%s' to '%s'" % (url_to_download, filename_with_directory))

        response = opener.open(url_to_download)

        f = open(destination_directory + filename, "wb")
        f.write(response.read())
        f.close()

        return filename_with_directory

    def get_downloaded_filename(self, month, symbol, year):
        return symbol.lower() + "-" + str(year) + "-" + str(month).zfill(2) + ".zip"

    def login_to_true_fx(self, username, password):

        form_data = {
            'USERNAME': username,
            'PASSWORD': password
        }

        form_data_encoded = urllib.urlencode(form_data)
        self.login_response_cookies = cookielib.CookieJar()

        ctx = self.get_ssl_default_context()

        opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(context=ctx, debuglevel=0),
            urllib2.HTTPCookieProcessor(self.login_response_cookies)
        )

        response = opener.open(self.url_provider.get_login_url(), form_data_encoded)

        if self.check_login_from_response(response):
            return True
        else:
            return False

    def get_ssl_default_context(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def check_login_from_response(self, response):
        the_page = response.read()
        tree = html.fromstring(the_page)

        if tree.xpath('count(//*[@id="login-form"])') == 0:
            return True
        else:
            return False
