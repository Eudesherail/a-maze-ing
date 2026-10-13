"""Read the small KEY=VALUE configuration format."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from mazegen import MazeGenerator
from mazegen.generator import Point


@dataclass
class Config:
    """Validated application settings."""

    width: int
    height: int
    entry: Point
    exit: Point
    output_file: Path
    perfect: bool
    seed: Optional[int] = None


def coordinate(value: str) -> Point:
    """Parse exactly two comma-separated integer coordinates."""
    parts = value.split(',')
    if len(parts) != 2:
        raise ValueError('Coordinates must have the form x,y.')
    return int(parts[0]), int(parts[1])


def read_config(filename: str) -> Config:
    """Read UTF-8 settings; report malformed, duplicate and missing keys."""
    values: dict[str, str] = {}
    required = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}
    with open(filename, encoding='utf-8') as stream:
        for number, line in enumerate(stream, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError(f'Line {number}: expected KEY=VALUE.')
            key, value = (part.strip() for part in line.split('=', 1))
            if key not in required | {'SEED'}:
                raise ValueError(f'Line {number}: unknown key {key!r}.')
            if key in values or not value:
                raise ValueError(
                    f'Line {number}: duplicate key or empty value.')
            values[key] = value
    missing = required - values.keys()
    if missing:
        raise ValueError('Missing keys: ' + ', '.join(sorted(missing)))
    if values['PERFECT'].lower() not in ('true', 'false'):
        raise ValueError('PERFECT must be True or False.')
    config = Config(int(values['WIDTH']), int(values['HEIGHT']),
                    coordinate(values['ENTRY']), coordinate(values['EXIT']),
                    Path(values['OUTPUT_FILE']),
                    values['PERFECT'].lower() == 'true',
                    int(values['SEED']) if 'SEED' in values else None)
    MazeGenerator(config.width, config.height, config.entry, config.exit,
                  config.perfect, config.seed)
    if config.output_file.resolve() == Path(filename).resolve():
        raise ValueError('OUTPUT_FILE must not overwrite the configuration.')
    return config
