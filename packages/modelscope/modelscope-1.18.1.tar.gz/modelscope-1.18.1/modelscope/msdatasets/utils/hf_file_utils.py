# noqa: isort:skip_file, yapf: disable
# Copyright (c) Alibaba, Inc. and its affiliates.
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.

import json
import os
import re
import shutil
import warnings
import inspect
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests

from datasets import config
from datasets.utils.file_utils import hash_url_to_filename, get_authentication_headers_for_url, ftp_head, fsspec_head, \
    http_head, _raise_if_offline_mode_is_enabled, ftp_get, fsspec_get, http_get
from filelock import FileLock

from modelscope.utils.config_ds import MS_DATASETS_CACHE
from modelscope.utils.logger import get_logger
from modelscope.hub.api import ModelScopeConfig

logger = get_logger()


def get_from_cache_ms(
    url,
    cache_dir=None,
    force_download=False,
    proxies=None,
    etag_timeout=100,
    resume_download=False,
    user_agent=None,
    local_files_only=False,
    use_etag=True,
    max_retries=0,
    token=None,
    use_auth_token='deprecated',
    ignore_url_params=False,
    storage_options=None,
    download_desc=None,
    disable_tqdm=False,
) -> str:
    """
    Given a URL, look for the corresponding file in the local cache.
    If it's not there, download it. Then return the path to the cached file.

    Return:
        Local path (string)

    Raises:
        FileNotFoundError: in case of non-recoverable file
            (non-existent or no cache on disk)
        ConnectionError: in case of unreachable url
            and no cache on disk
    """
    if use_auth_token != 'deprecated':
        warnings.warn(
            "'use_auth_token' was deprecated in favor of 'token' in version 2.14.0 and will be removed in 3.0.0.\n"
            f"You can remove this warning by passing 'token={use_auth_token}' instead.",
            FutureWarning,
        )
        token = use_auth_token
    if cache_dir is None:
        cache_dir = MS_DATASETS_CACHE
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)

    os.makedirs(cache_dir, exist_ok=True)

    if ignore_url_params:
        # strip all query parameters and #fragments from the URL
        cached_url = urljoin(url, urlparse(url).path)
    else:
        cached_url = url  # additional parameters may be added to the given URL

    connected = False
    response = None
    cookies = None
    etag = None
    head_error = None
    scheme = None

    # Try a first time to file the file on the local file system without eTag (None)
    # if we don't ask for 'force_download' then we spare a request
    filename = hash_url_to_filename(cached_url, etag=None)
    cache_path = os.path.join(cache_dir, filename)

    if os.path.exists(cache_path) and not force_download and not use_etag:
        return cache_path

    # Prepare headers for authentication
    headers = get_authentication_headers_for_url(url, token=token)
    if user_agent is not None:
        headers['user-agent'] = user_agent

    # We don't have the file locally or we need an eTag
    if not local_files_only:
        scheme = urlparse(url).scheme
        if scheme == 'ftp':
            connected = ftp_head(url)
        elif scheme not in ('http', 'https'):
            response = fsspec_head(url, storage_options=storage_options)
            # s3fs uses "ETag", gcsfs uses "etag"
            etag = (response.get('ETag', None) or response.get('etag', None)) if use_etag else None
            connected = True
        try:
            cookies = ModelScopeConfig.get_cookies()
            response = http_head(
                url,
                allow_redirects=True,
                proxies=proxies,
                timeout=etag_timeout,
                max_retries=max_retries,
                headers=headers,
                cookies=cookies,
            )
            if response.status_code == 200:  # ok
                etag = response.headers.get('ETag') if use_etag else None
                for k, v in response.cookies.items():
                    # In some edge cases, we need to get a confirmation token
                    if k.startswith('download_warning') and 'drive.google.com' in url:
                        url += '&confirm=' + v
                        cookies = response.cookies
                connected = True
                # Fix Google Drive URL to avoid Virus scan warning
                if 'drive.google.com' in url and 'confirm=' not in url:
                    url += '&confirm=t'
            # In some edge cases, head request returns 400 but the connection is actually ok
            elif (
                (response.status_code == 400 and 'firebasestorage.googleapis.com' in url)
                or (response.status_code == 405 and 'drive.google.com' in url)
                or (
                    response.status_code == 403
                    and (
                        re.match(r'^https?://github.com/.*?/.*?/releases/download/.*?/.*?$', url)
                        or re.match(r'^https://.*?s3.*?amazonaws.com/.*?$', response.url)
                    )
                )
                or (response.status_code == 403 and 'ndownloader.figstatic.com' in url)
            ):
                connected = True
                logger.info(f"Couldn't get ETag version for url {url}")
            elif response.status_code == 401 and config.HF_ENDPOINT in url and token is None:
                raise ConnectionError(
                    f'Unauthorized for URL {url}. '
                    f'Please use the parameter `token=True` after logging in with `huggingface-cli login`'
                )
        except (OSError, requests.exceptions.Timeout) as e:
            # not connected
            head_error = e
            pass

    # connected == False = we don't have a connection, or url doesn't exist, or is otherwise inaccessible.
    # try to get the last downloaded one
    if not connected:
        if os.path.exists(cache_path) and not force_download:
            return cache_path
        if local_files_only:
            raise FileNotFoundError(
                f'Cannot find the requested files in the cached path at {cache_path} and outgoing traffic has been'
                " disabled. To enable file online look-ups, set 'local_files_only' to False."
            )
        elif response is not None and response.status_code == 404:
            raise FileNotFoundError(f"Couldn't find file at {url}")
        _raise_if_offline_mode_is_enabled(f'Tried to reach {url}')
        if head_error is not None:
            raise ConnectionError(f"Couldn't reach {url} ({repr(head_error)})")
        elif response is not None:
            raise ConnectionError(f"Couldn't reach {url} (error {response.status_code})")
        else:
            raise ConnectionError(f"Couldn't reach {url}")

    # Try a second time
    filename = hash_url_to_filename(cached_url, etag)
    cache_path = os.path.join(cache_dir, filename)

    if os.path.exists(cache_path) and not force_download:
        return cache_path

    # From now on, connected is True.
    # Prevent parallel downloads of the same file with a lock.
    lock_path = cache_path + '.lock'
    with FileLock(lock_path):
        # Retry in case previously locked processes just enter after the precedent process releases the lock
        if os.path.exists(cache_path) and not force_download:
            return cache_path

        incomplete_path = cache_path + '.incomplete'

        @contextmanager
        def temp_file_manager(mode='w+b'):
            with open(incomplete_path, mode) as f:
                yield f

        resume_size = 0
        if resume_download:
            temp_file_manager = partial(temp_file_manager, mode='a+b')
            if os.path.exists(incomplete_path):
                resume_size = os.stat(incomplete_path).st_size

        # Download to temporary file, then copy to cache path once finished.
        # Otherwise, you get corrupt cache entries if the download gets interrupted.
        with temp_file_manager() as temp_file:
            logger.info(f'Downloading to {temp_file.name}')

            # GET file object
            if scheme == 'ftp':
                ftp_get(url, temp_file)
            elif scheme not in ('http', 'https'):
                fsspec_get_sig = inspect.signature(fsspec_get)
                if 'disable_tqdm' in fsspec_get_sig.parameters:
                    fsspec_get(url,
                               temp_file,
                               storage_options=storage_options,
                               desc=download_desc,
                               disable_tqdm=disable_tqdm
                               )
                else:
                    fsspec_get(url, temp_file, storage_options=storage_options, desc=download_desc)
            else:
                http_get_sig = inspect.signature(http_get)

                if 'disable_tqdm' in http_get_sig.parameters:
                    http_get(
                        url,
                        temp_file=temp_file,
                        proxies=proxies,
                        resume_size=resume_size,
                        headers=headers,
                        cookies=cookies,
                        max_retries=max_retries,
                        desc=download_desc,
                        disable_tqdm=disable_tqdm,
                    )
                else:
                    http_get(
                        url,
                        temp_file=temp_file,
                        proxies=proxies,
                        resume_size=resume_size,
                        headers=headers,
                        cookies=cookies,
                        max_retries=max_retries,
                        desc=download_desc,
                    )

        logger.info(f'storing {url} in cache at {cache_path}')
        shutil.move(temp_file.name, cache_path)
        umask = os.umask(0o666)
        os.umask(umask)
        os.chmod(cache_path, 0o666 & ~umask)

        logger.info(f'creating metadata file for {cache_path}')
        meta = {'url': url, 'etag': etag}
        meta_path = cache_path + '.json'
        with open(meta_path, 'w', encoding='utf-8') as meta_file:
            json.dump(meta, meta_file)

    return cache_path
