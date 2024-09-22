import json
import time
import asyncio
from typing import Optional, Dict, Any, Union, List
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from requests.auth import AuthBase
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import base64

class StealthyRequests:
    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.default_timeout = 30
        self.max_redirects = 30
        self.auth = None
        self.cookies = {}
        self.proxies = None
        self.verify = True
        self.cert = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _get_driver(self):
        if self.driver is None:
            options = Chrome().options
            options.add_argument(f"user-agent={self.ua.random}")
            
            if self.proxies:
                options.add_argument(f'--proxy-server={self.proxies["http"]}')
            
            if not self.verify:
                options.add_argument('--ignore-certificate-errors')
            
            if self.cert:
                options.add_argument(f'--ssl-client-certificate={self.cert}')
            
            self.driver = Chrome(options=options)
        return self.driver

    def _execute_request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None, 
                         data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
                         cookies: Optional[Dict[str, str]] = None, timeout: Optional[float] = None, 
                         allow_redirects: bool = True, files: Optional[Dict[str, Any]] = None) -> 'Response':
        driver = self._get_driver()
        full_url = url
        if params:
            full_url += '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
        
        driver.execute_cdp_cmd('Network.enable', {})

        all_cookies = {**self.cookies, **(cookies or {})}
        for name, value in all_cookies.items():
            driver.add_cookie({'name': name, 'value': value})

        timeout = timeout or self.default_timeout
        driver.set_page_load_timeout(timeout)

        if self.auth:
            auth_header = self.auth(full_url)
            headers = headers or {}
            headers.update(auth_header)

        # Handle file uploads
        if files:
            data = data or {}
            for key, file_info in files.items():
                if isinstance(file_info, tuple):
                    filename, fileobj = file_info[:2]
                    content = fileobj.read()
                else:
                    filename = key
                    content = file_info.read()
                data[key] = (filename, base64.b64encode(content).decode('utf-8'))

        request_id = driver.execute_cdp_cmd('Network.sendRequest', {
            'url': full_url,
            'method': method,
            'headers': headers or {'Content-Type': 'application/json'},
            'postData': json.dumps(data) if data else None
        })['requestId']
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                break
            except:
                time.sleep(0.1)
        else:
            raise TimeoutError("Request timed out")

        status_code = response.get('statusCode', 200)

        redirect_count = 0
        while allow_redirects and status_code in (301, 302, 303, 307, 308) and redirect_count < self.max_redirects:
            redirect_url = response.get('headers', {}).get('Location')
            if redirect_url:
                full_url = urljoin(full_url, redirect_url)
                redirect_count += 1
                response = driver.execute_cdp_cmd('Network.sendRequest', {
                    'url': full_url,
                    'method': 'GET',
                    'headers': headers or {'Content-Type': 'application/json'},
                })
                status_code = response.get('statusCode', 200)
            else:
                break

        return Response(driver, status_code, response.get('body', ''))

    def request(self, method: str, url: str, **kwargs) -> 'Response':
        return self._execute_request(method.upper(), url, **kwargs)

    def get(self, url: str, **kwargs) -> 'Response':
        return self._execute_request('GET', url, **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> 'Response':
        return self._execute_request('POST', url, data=data, **kwargs)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> 'Response':
        return self._execute_request('PUT', url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> 'Response':
        return self._execute_request('DELETE', url, **kwargs)

    def head(self, url: str, **kwargs) -> 'Response':
        return self._execute_request('HEAD', url, **kwargs)

    def options(self, url: str, **kwargs) -> 'Response':
        return self._execute_request('OPTIONS', url, **kwargs)

    def patch(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> 'Response':
        return self._execute_request('PATCH', url, data=data, **kwargs)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def set_auth(self, auth: AuthBase):
        self.auth = auth

    def set_timeout(self, timeout: float):
        self.default_timeout = timeout

    def set_max_redirects(self, max_redirects: int):
        self.max_redirects = max_redirects

    def set_cookies(self, cookies: Dict[str, str]):
        self.cookies.update(cookies)

    def set_proxies(self, proxies: Dict[str, str]):
        self.proxies = proxies

    def set_verify(self, verify: bool):
        self.verify = verify

    def set_cert(self, cert: str):
        self.cert = cert

    async def async_request(self, method: str, url: str, **kwargs) -> 'Response':
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.request, method, url, **kwargs)

def session():
    return StealthyRequests()

class Response:
    def __init__(self, driver, status_code: int, content: str):
        self.driver = driver
        self.status_code = status_code
        self.content = content.encode('utf-8')
        self.text = content
        self._json = None

    def json(self):
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

    @property
    def cookies(self):
        return {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}

    @property
    def headers(self):
        return self.driver.execute_script("var req = new XMLHttpRequest(); req.open('GET', document.location, false); req.send(null); return req.getAllResponseHeaders();")

async def get(url: str, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('GET', url, **kwargs)

async def post(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('POST', url, data=data, **kwargs)

async def put(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('PUT', url, data=data, **kwargs)

async def delete(url: str, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('DELETE', url, **kwargs)

async def head(url: str, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('HEAD', url, **kwargs)

async def options(url: str, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('OPTIONS', url, **kwargs)

async def patch(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('PATCH', url, data=data, **kwargs)

def request(method: str, url: str, **kwargs) -> Response:
    with StealthyRequests() as sr:
        return sr.request(method, url, **kwargs)

# Синхронные версии методов
def get(url: str, **kwargs) -> Response:
    return request('GET', url, **kwargs)

def post(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    return request('POST', url, data=data, **kwargs)

def put(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    return request('PUT', url, data=data, **kwargs)

def delete(url: str, **kwargs) -> Response:
    return request('DELETE', url, **kwargs)

def head(url: str, **kwargs) -> Response:
    return request('HEAD', url, **kwargs)

def options(url: str, **kwargs) -> Response:
    return request('OPTIONS', url, **kwargs)

def patch(url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    return request('PATCH', url, data=data, **kwargs)