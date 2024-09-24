import io
import sys
from pathlib import Path

import click

import yaml

from .schemas import Config


# Windows compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8'
    )


def yaml_to_dict(conf_path: Path) -> dict:
    data = {}

    if conf_path.exists():
        with open(conf_path, 'r', encoding='utf-8') as f:
            if _data := yaml.safe_load(f):
                data = _data

    return data


def load_conf(watch_dir: click.Path | None = None) -> Config:
    """
    Parse 3 configs sequentially
    """

    # load default config
    module_path = Path(__file__).resolve()
    module_dir = module_path.parent
    default_conf: dict = yaml_to_dict(module_dir / 'config.yaml')

    # load user home dir config
    home_conf: dict = yaml_to_dict(
        Path.home() / '.config/lintify/config.yaml')

    # load project root dir conf
    project_conf: dict = yaml_to_dict(Path('.lintify.yaml'))

    result = default_conf
    result |= home_conf
    result |= project_conf

    if watch_dir:
        result['watch_dir'] = watch_dir

    conf = Config(**result)
    return conf


if __name__ == '__main__':
    print(load_conf())
