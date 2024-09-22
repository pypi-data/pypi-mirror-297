import json
import time
import asyncio
from typing import Optional, Dict, Any, Union, List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from requests.auth import AuthBase
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import base64
import warnings

class RequestException(Exception):
    """There was an ambiguous exception that occurred while handling your request."""

class HTTPError(RequestException):
    """An HTTP error occurred."""

class ConnectionError(RequestException):
    """A Connection error occurred."""

class Timeout(RequestException):
    """The request timed out."""

class TooManyRedirects(RequestException):
    """Too many redirects."""

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
        self.hooks = {'response': []}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _get_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={self.ua.random}")
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            if self.proxies:
                options.add_argument(f'--proxy-server={self.proxies["http"]}')
            
            if not self.verify:
                options.add_argument('--ignore-certificate-errors')
            
            if self.cert:
                options.add_argument(f'--ssl-client-certificate={self.cert}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver

    def _execute_request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None, 
                         data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
                         cookies: Optional[Dict[str, str]] = None, timeout: Optional[float] = None, 
                         allow_redirects: bool = True, files: Optional[Dict[str, Any]] = None) -> 'Response':
        driver = self._get_driver()
        full_url = url
        if params:
            full_url += '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
        
        all_cookies = {**self.cookies, **(cookies or {})}
        for name, value in all_cookies.items():
            driver.add_cookie({'name': name, 'value': value})

        timeout = timeout or self.default_timeout
        driver.set_page_load_timeout(timeout)

        if self.auth:
            auth_header = self.auth(full_url)
            headers = headers or {}
            headers.update(auth_header)

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

        try:
            if method == 'GET':
                driver.get(full_url)
            else:
                driver.execute_script(f"""
                    var xhr = new XMLHttpRequest();
                    xhr.open('{method}', '{full_url}', false);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.send(JSON.stringify({json.dumps(data)}));
                    return xhr.responseText;
                """)

            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            status_code = driver.execute_script("return navigator.connection.httpStatusCode")
            content = driver.page_source

            response = Response(driver, status_code, content, url=full_url)

            for hook in self.hooks['response']:
                hook(response)

            return response

        except Exception as e:
            if isinstance(e, webdriver.TimeoutException):
                raise Timeout("Request timed out")
            elif isinstance(e, webdriver.WebDriverException):
                raise ConnectionError("Failed to establish a connection")
            else:
                raise RequestException("An error occurred during the request")

    def request(self, method: str, url: str, **kwargs) -> 'Response':
        return self._execute_request(method.upper(), url, **kwargs)

    def get(self, url: str, **kwargs) -> 'Response':
        return self._execute_request('GET', url, **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> 'Response':
        if json:
            kwargs['data'] = json
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
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

    def mount(self, prefix: str, adapter: Any):
        warnings.warn("mount() is not fully implemented in StealthyRequests", UserWarning)

    def register_hook(self, event: str, hook: callable):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(hook)

    async def async_request(self, method: str, url: str, **kwargs) -> 'Response':
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.request, method, url, **kwargs)

class Response:
    def __init__(self, driver, status_code: int, content: str, url: str):
        self.driver = driver
        self.status_code = status_code
        self.content = content.encode('utf-8')
        self.text = content
        self._json = None
        self.url = url
        self.history = []
        self.elapsed = None
        self.encoding = 'utf-8'
        self.reason = None
        self.raw = None

    def json(self):
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

    @property
    def cookies(self):
        return {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}

    @property
    def headers(self):
        return self.driver.execute_script("""
            var req = new XMLHttpRequest();
            req.open('GET', document.location, false);
            req.send(null);
            var headers = {};
            var headerString = req.getAllResponseHeaders();
            var headerPairs = headerString.split('\\r\\n');
            for (var i = 0; i < headerPairs.length; i++) {
                var headerPair = headerPairs[i];
                var index = headerPair.indexOf(': ');
                if (index > 0) {
                    var key = headerPair.substring(0, index);
                    var val = headerPair.substring(index + 2);
                    headers[key] = val;
                }
            }
            return headers;
        """)

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise HTTPError(f"{self.status_code} Client Error: {self.reason} for url: {self.url}")

    def close(self):
        if self.raw:
            self.raw.close()

def session():
    return StealthyRequests()

async def get(url: str, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('GET', url, **kwargs)

async def post(url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
    async with StealthyRequests() as sr:
        return await sr.async_request('POST', url, data=data, json=json, **kwargs)

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
def get(url: str, params=None, **kwargs) -> Response:
    kwargs.setdefault('allow_redirects', True)
    return request('GET', url, params=params, **kwargs)

def post(url: str, data=None, json=None, **kwargs) -> Response:
    return request('POST', url, data=data, json=json, **kwargs)

def put(url: str, data=None, **kwargs) -> Response:
    return request('PUT', url, data=data, **kwargs)

def delete(url: str, **kwargs) -> Response:
    return request('DELETE', url, **kwargs)

def head(url: str, **kwargs) -> Response:
    kwargs.setdefault('allow_redirects', False)
    return request('HEAD', url, **kwargs)

def options(url: str, **kwargs) -> Response:
    kwargs.setdefault('allow_redirects', True)
    return request('OPTIONS', url, **kwargs)

def patch(url: str, data=None, **kwargs) -> Response:
    return request('PATCH', url, data=data, **kwargs)

# Дополнительные функции
def urlparse(url):
    return urlparse(url)

def urljoin(base, url, allow_fragments=True):
    return urljoin(base, url, allow_fragments)

def quote(string, safe='/', encoding=None, errors=None):
    from urllib.parse import quote
    return quote(string, safe, encoding, errors)

def unquote(string, encoding='utf-8', errors='replace'):
    from urllib.parse import unquote
    return unquote(string, encoding, errors)

def dict_from_cookiejar(cj):
    return {cookie.name: cookie.value for cookie in cj}

def add_dict_to_cookiejar(cj, cookie_dict):
    for name, value in cookie_dict.items():
        cj.set_cookie(create_cookie(name, value))

def create_cookie(name, value, **kwargs):
    from http.cookiejar import Cookie
    return Cookie(version=0, name=name, value=value, port=None, port_specified=False,
                  domain='', domain_specified=False, domain_initial_dot=False,
                  path='/', path_specified=True, secure=False, expires=None,
                  discard=True, comment=None, comment_url=None, rest={'HttpOnly': None},
                  rfc2109=False, **kwargs)