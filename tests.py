#/usr/bin/env python
# -*- coding: utf-8 -*-
import core, ast

# Tests
class tests():
    def __init__(self):
        self.score = 0.0
        self.out_of = 0.0
    # API Tests
    def api_tests(self):
        print("Beginning API tests...\n")

        print("Testing hash data...")
        self.out_of += 1
        self.hash_data = core.core().get_api_data("hash", "7708cd4a983ca4648ffbf2eaf6860a1725b17ae86f3e6490cf85a7d7b40266c1")
        if ast.literal_eval(self.hash_data) == { "error": "false", "result": { "verified": "true", "address": "XopyTfnfFMLWtjed1JNBn2B72JRrJaqXLD", "username": "JJ12880", "title": "Radium SmartChain Phase 2.3 Client", "txid": "7e5ad1fbad158f20050df11fe59f4fbb9cc50c163883174804dfaa8b7e2eb091", "linuxtime": 1454470814, "date": "2016-02-03T03:40:14Z", "block": 357073 } }:
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing username data...")
        self.out_of += 1
        self.username_data = core.core().get_api_data("username", "JJ12880")
        if ast.literal_eval(self.username_data) == { "verified": "True", "address": "XopyTfnfFMLWtjed1JNBn2B72JRrJaqXLD", "username": "JJ12880", "memo": "xRADON SuperNet Developer" }:
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing address data...")
        self.out_of += 1
        self.address_data = core.core().get_api_data("address", "XopyTfnfFMLWtjed1JNBn2B72JRrJaqXLD")
        if ast.literal_eval(self.address_data) == { "error": "false", "verified": "True", "address": "XopyTfnfFMLWtjed1JNBn2B72JRrJaqXLD", "username": "JJ12880", "memo": "xRADON SuperNet Developer" }:
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")
        print("API tests finished\n")

    # URL Validation Tests
    def url_tests(self):

        print("Testing a standard http url...")
        self.out_of += 1
        if core.core().is_valid_url("http://google.com/"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a standard https url...")
        self.out_of += 1
        if core.core().is_valid_url("https://google.com/"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a standard url without a prefix...")
        self.out_of += 1
        if core.core().is_valid_url("google.com/"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a non-standard TLD...")
        self.out_of += 1
        if core.core().is_valid_url("https://verify.software/"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a malformed http url...")
        self.out_of += 1
        if not core.core().is_valid_url("http://google"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a malformed https url...")
        self.out_of += 1
        if not core.core().is_valid_url("https://google"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a string...")
        self.out_of += 1
        if not core.core().is_valid_url("google"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

    # Unix-time to UTC conversion test
    def utime_tests(self):

        print("Testing conversion from Unix time to UTC...")
        self.out_of += 1
        if core.core().get_utc_from_unix(1454470814) == "2016-02-03 03:40:14":
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

    # File header tests
    def file_header_tests(self):

        print("Testing a standard http HEAD request...")
        self.out_of += 1
        self.file_header_data = core.core().get_file_headers("http://www.projectradium.org/downloads/Radium%20SmartChain%20Phase%202.3.zip")
        if  self.file_header_data['Content-Length'] == '818884' and self.file_header_data['Accept-Ranges'] == 'bytes' and self.file_header_data['server'] == 'Apache' and self.file_header_data['Last-Modified'] == 'Fri, 01 Apr 2016 04:01:26 GMT' and self.file_header_data['Content-Type'] == 'application/zip':
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print('Testing file size limit filter...')
        self.out_of += 1
        if core.core().is_file_under_limit("http://www.projectradium.org/downloads/Radium%20SmartChain%20Phase%202.3.zip"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing file size limit filter...")
        self.out_of += 1
        if not core.core().is_file_under_limit("http://www.projectradium.org/downloads/RadiumQuickDeploy_3.17.16.exe"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing file size limit filter...")
        self.out_of += 1
        if core.core().is_file_under_limit("https://github.com/ProjectRadium/Radium/releases/download/v1.4.2.1/Radium-qt-1.4.2.1.exe"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

    # File content tests
    def file_content_tests(self):

        print("Testing a standard http GET request...")
        self.out_of += 1
        if core.core().get_file_hash("http://www.projectradium.org/downloads/Radium%20SmartChain%20Phase%202.3.zip") == "7708cd4a983ca4648ffbf2eaf6860a1725b17ae86f3e6490cf85a7d7b40266c1":
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing a standard https GET request...")
        self.out_of += 1
        if core.core().get_file_hash("https://github.com/ProjectRadium/Radium/releases/download/v1.4.2.1/Radium-qt-1.4.2.1.exe") == "8f965a198336d63b2de67ea7160112cc9cce131b9206ce8180ea15a4c05120cd":
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

    # Hash data validation tests
    def hash_data_tests(self):

        print("Testing username verification for a given hash...")
        print("NOTE: If this test fails, you may need to change line 70 of core.py from 'True' to 'true'.")
        self.out_of += 1
        if core.core().is_hash_acct_verified("7708cd4a983ca4648ffbf2eaf6860a1725b17ae86f3e6490cf85a7d7b40266c1"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

        print("Testing username verification for a given hash...")
        print("NOTE: If this test fails, you may need to change line 70 of core.py from 'True' to 'true'.")
        self.out_of += 1
        if core.core().is_hash_acct_verified("8f965a198336d63b2de67ea7160112cc9cce131b9206ce8180ea15a4c05120cd"):
            self.score += 1
            print("passed\n")
        else:
            print("failed\n")

    # Run All Tests
    def run_all(self):
        self.api_tests()
        self.url_tests()
        self.utime_tests()
        self.file_header_tests()
        self.file_content_tests()
        self.hash_data_tests()
        print('%s (%s/%s) of tests passed.' % ('{:.1%}'.format(self.score/self.out_of), str(self.score), str(self.out_of)))

# Run Tests
if __name__ == '__main__':
    tests().run_all()