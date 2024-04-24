# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import AsyncIterator, Callable, Optional

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, Response, StreamingResponse

from qianfan.consts import DefaultValue
from qianfan.extensions.proxy.proxy import ClientProxy
from qianfan.utils.utils import get_ip_address

base_app = FastAPI()
console_app = FastAPI()
proxy = ClientProxy()


@base_app.middleware("http")
async def base_iam(request: Request, callback: Callable) -> Response:
    """
    用于向base请求中添加访问令牌。

    Args:
        request (Request): 请求对象。
        callback (Callable): 回调函数。

    Returns:
        Response: 处理后的响应对象。
    """
    resp = await proxy.get_response(request, DefaultValue.BaseURL)

    if isinstance(resp, AsyncIterator):
        return StreamingResponse(resp, media_type="text/event-stream")

    return JSONResponse(resp)


@console_app.middleware("http")
async def console_iam(request: Request, callback: Callable) -> Response:
    """
    用于向console请求中添加访问令牌。

    Args:
        request (Request): 请求对象。
        callback (Callable): 回调函数。

    Returns:
        Response: 处理后的响应对象。
    """
    resp = await proxy.get_response(request, DefaultValue.ConsoleAPIBaseURL)

    if isinstance(resp, AsyncIterator):
        return StreamingResponse(resp, media_type="text/event-stream")

    return JSONResponse(resp)


def entry(
    host: str,
    base_port: int,
    console_port: int,
    log_file: Optional[str],
    mock_port: int,
) -> None:
    import os

    import rich
    import uvicorn
    import uvicorn.config
    from multiprocess import Process
    from rich.markdown import Markdown

    import qianfan
    from qianfan.utils.logging import logger

    qianfan.enable_log("DEBUG")

    proxy.mock_port = mock_port

    log_config = uvicorn.config.LOGGING_CONFIG
    if log_file is not None:
        log_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "filename": log_file,
            "mode": "a",
            "encoding": "utf-8",
        }
        for key in log_config["loggers"]:
            if "handlers" in log_config["loggers"][key]:
                log_config["loggers"][key]["handlers"].append("file")

    messages = ["Proxy server is running at"]
    display_host = host
    if display_host == "0.0.0.0":
        display_host = get_ip_address()
    messages.append(f"- base: http://{display_host}:{base_port}")
    messages.append(f"- console: http://{display_host}:{console_port}")

    rich.print(Markdown("\n".join(messages)))
    rich.print()

    def start_server(app: FastAPI, port: int) -> None:
        uvicorn.run(app, host=host, port=port, log_config=log_config)

    # close stderr output
    logger._logger.removeHandler(logger.handler)
    log_config["loggers"]["uvicorn.access"]["handlers"].remove("access")
    log_config["loggers"]["uvicorn"]["handlers"].remove("default")

    process_base = Process(target=start_server, args=(base_app, base_port))
    process_console = Process(target=start_server, args=(console_app, console_port))
    process_base.start()
    process_console.start()

    rich.print(
        f"Proxy base server is running in background with PID {process_base.pid}."
    )
    rich.print(
        f"Proxy console server is running in background with PID {process_console.pid}."
    )
    os._exit(0)
