#!/usr/bin/env python3
"""Convert a multi-structure 3D SDF file to Maestro compressed format.

Run with ``$SCHRODINGER/run``. Structures are streamed; coordinates, titles,
and structure properties are handled by Schrödinger's structure I/O layer.
"""

import argparse
import os
from pathlib import Path
import tempfile


def convert(input_path, output_path, overwrite=False):
    from schrodinger import structure

    source = Path(input_path).expanduser().resolve(strict=True)
    destination = Path(output_path).expanduser().resolve()
    if source.suffix.lower() not in ('.sdf', '.sd'):
        raise ValueError('Input must have .sdf or .sd extension')
    if destination.suffix.lower() != '.maegz':
        raise ValueError('Output must have .maegz extension')
    if source == destination:
        raise ValueError('Input and output paths must differ')
    if not destination.parent.is_dir():
        raise ValueError('Output directory does not exist: ' + str(destination.parent))
    if destination.exists() and not overwrite:
        raise FileExistsError('Output exists; use --overwrite to replace it: '
                              + str(destination))

    fd, temporary_name = tempfile.mkstemp(prefix='.sdf_to_maegz_', suffix='.maegz',
                                          dir=str(destination.parent))
    os.close(fd)
    temporary = Path(temporary_name)
    count = 0
    try:
        with structure.StructureReader(str(source)) as reader, \
                structure.StructureWriter(str(temporary)) as writer:
            for count, st in enumerate(reader, 1):
                writer.append(st)
        if count == 0:
            raise ValueError('Input SDF contains no structures')
        os.replace(str(temporary), str(destination))
    finally:
        if temporary.exists():
            temporary.unlink()
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path,
                        help='Input multi-structure .sdf/.sd file')
    parser.add_argument('--output', required=True, type=Path,
                        help='Output .maegz file')
    parser.add_argument('--overwrite', action='store_true',
                        help='Replace an existing output file')
    args = parser.parse_args()
    try:
        count = convert(args.input, args.output, overwrite=args.overwrite)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print('%d structures written to %s' % (count, args.output))


if __name__ == '__main__':
    main()
