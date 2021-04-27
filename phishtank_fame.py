try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False


try:
    import base64
    HAVE_BASE64 = True
except ImportError:
    HAVE_BASE64 = False


try:
    import xml.etree.ElementTree as ET
    HAVE_XML = True
except ImportError:
    HAVE_XML = False


from fame.common.utils import tempdir
from fame.common.exceptions import ModuleInitializationError, ModuleExecutionError
from fame.core.module import ProcessingModule

class Phishtank_module(ProcessingModule):

    name = "phishtank"
    description = "Get report from Phishtank platform."
    config = [
        {
            'name': 'api_key',
            'type': 'string',
            'description': 'API Key needed to use the Phishtank API',
        },
        {
            'name': 'phishtank_url',
            'type': 'string',
            'description': 'URL needed to use the Phishtank API',
        }
    ]


    def initialize(self):
        if not HAVE_REQUESTS:
            raise ModuleInitializationError(self, 'Missing dependency: requests')

        if not HAVE_BASE64:
            raise ModuleInitializationError(self, 'Missing dependency: base64')

        if not HAVE_XML:
            raise ModuleInitializationError(self, 'Missing dependency: xml')

        return True


    def each_with_type(self, target, file_type):

        # Set root URLs
        self.results = dict()
        try:


        	urlSafeEncodedBytes = base64.urlsafe_b64encode(target.encode("utf-8"))
        	urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
        	url=self.phishtank_url+urlSafeEncodedStr

        	header = {
	        	"format":"json",
	        	"app_key": self.api_key
	        }

			r = requests.post(url=url, headers = header)
			tree=ET.fromstring(r.text)
			for element in tree.findall('results')[0].findall('url0')[0]:
				if element.tag == "in_database" and element.text == "true":
					self.results["results"]='PHISHING'
				elif element.tag == "in_database" and element.text == "false":
					self.results["results"]='NOT FOUND'

			return True
			
		except Exception:
			return False
