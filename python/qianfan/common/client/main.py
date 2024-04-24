# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

from typing import Optional

import click
import rich.markup
import typer
from typer.completion import completion_init
from typer.completion import install_callback
from typer.completion import show_callback

import qianfan
from qianfan.common.client.chat import chat_entry
from qianfan.common.client.completion import completion_entry
from qianfan.common.client.dataset import dataset_app
from qianfan.common.client.embedding import embedding_entry
from qianfan.common.client.evaluation import evaluation_app
from qianfan.common.client.plugin import plugin_entry
from qianfan.common.client.trainer import trainer_app
from qianfan.common.client.txt2img import txt2img_entry
from qianfan.common.client.utils import credential_required
from qianfan.common.client.utils import print_error_msg
from qianfan.utils.utils import check_dependency

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
)
app.command(name="chat")(chat_entry)
app.command(name="completion")(completion_entry)
app.command(name="txt2img")(txt2img_entry)
app.command(name="embedding", no_args_is_help=True)(embedding_entry)
app.command(name="plugin")(plugin_entry)
app.add_typer(dataset_app, name="dataset")
app.add_typer(trainer_app, name="trainer")
app.add_typer(evaluation_app, name="evaluation")

_enable_traceback = False


@app.command(name="openai")
@credential_required
def openai(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind."),
    port: int = typer.Option(8001, "--port", "-p", help="Port of the server."),
    detach: bool = typer.Option(
        False,
        "--detach",
        "-d",
        help="Run the server in background.",
    ),
    log_file: Optional[str] = typer.Option(None, help="Log file path."),
) -> None:
    """
    Create an openai wrapper server.
    """
    check_dependency("openai", ["fastapi", "uvicorn"])
    from qianfan.common.client.openai_adapter import entry as openai_entry

    openai_entry(host=host, port=port, detach=detach, log_file=log_file)


@app.command(name="proxy")
@credential_required
def proxy(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind."),
    base_port: int = typer.Option(
        8002, "--port", "-p", help="Port of the base server."
    ),
    console_port: int = typer.Option(
        8003, "--port", "-p", help="Port of the console server."
    ),
    detach: bool = typer.Option(
        False,
        "--detach",
        "-d",
        help="Run the server in background.",
    ),
    log_file: Optional[str] = typer.Option(None, help="Log file path."),
    mock_port: int = typer.Option(
        -1, "--mock-port", "-m", help="Port of the Mock server."
    ),
) -> None:
    """
    Create a proxy server.
    """
    check_dependency("proxy", ["fastapi", "uvicorn"])
    from qianfan.common.client.proxy import entry as proxy_entry

    proxy_entry(
        host=host,
        base_port=base_port,
        console_port=console_port,
        detach=detach,
        log_file=log_file,
        mock_port=mock_port,
    )


def version_callback(value: bool) -> None:
    """
    Print qianfan sdk version
    """
    if value:
        print(qianfan.__version__)
        raise typer.Exit()


def qianfan_config_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> None:
    """
    update qianfan config
    """
    if value is not None and len(value.strip()) > 0:
        config_name = param.name
        if config_name is not None:
            # arguments name should be lowercase of the variable in config
            qianfan_config_name = config_name.upper()
            qianfan.get_config().__setattr__(qianfan_config_name, value)


def main() -> None:
    """
    Main function of qianfan client.
    """
    try:
        completion_init()
        app()
    except Exception as e:
        if _enable_traceback:
            raise
        else:
            print_error_msg(rich.markup.escape(str(e)))


@app.callback()
def entry(
    access_key: Optional[str] = typer.Option(
        None,
        callback=qianfan_config_callback,
        help=(
            "Access key from"
            " [link=https://console.bce.baidu.com/iam/#/iam/accesslist]Qianfan"
            " IAM[/link]."
            " [link=https://cloud.baidu.com/doc/Reference/s/9jwvz2egb]Reference"
            " here[/link]."
        ),
    ),
    secret_key: Optional[str] = typer.Option(
        None,
        callback=qianfan_config_callback,
        help=(
            "Secret key from"
            " [link=https://console.bce.baidu.com/iam/#/iam/accesslist]Qianfan"
            " IAM[/link]."
            " [link=https://cloud.baidu.com/doc/Reference/s/9jwvz2egb]Reference"
            " here[/link]."
        ),
    ),
    ak: Optional[str] = typer.Option(
        None,
        callback=qianfan_config_callback,
        help=(
            "API key of"
            " [link=https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application]Qianfan"
            " App[/link]."
            " [link=https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Slkkydake]Reference"
            " here[/link]."
        ),
    ),
    sk: Optional[str] = typer.Option(
        None,
        callback=qianfan_config_callback,
        help=(
            "Secret key"
            " [link=https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application]Qianfan"
            " App[/link]."
            " [link=https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Slkkydake]Reference"
            " here[/link]."
        ),
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print version.",
    ),
    enable_traceback: bool = typer.Option(
        False, "--enable-traceback", help="Print traceback when exception is thrown."
    ),
    install_completion: bool = typer.Option(
        None,
        "--install-shell-autocomplete",
        is_flag=True,
        callback=install_callback,
        expose_value=False,
        help="Install the auto completion script for the specified shell.",
    ),
    show_completion: bool = typer.Option(
        None,
        "--show-shell-autocomplete",
        is_flag=True,
        callback=show_callback,
        expose_value=False,
        help=(
            "Show the auto completion script for the specified shell, to copy it or"
            " customize the installation."
        ),
    ),
    log_level: str = typer.Option(
        "WARN",
        help="Set log level.",
        click_type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR"]),
    ),
) -> None:
    """
    Qianfan CLI which provides access to various Qianfan services.
    """
    global _enable_traceback
    _enable_traceback = enable_traceback
    qianfan.enable_log(log_level)


if __name__ == "__main__":
    main()
