from pathlib import Path
from typing import Optional, Mapping, Sequence, Union

from audeep.backend.parsers.base import Parser, _InstanceMetadata


def _get_audio_paths(file: Union[Path, str]) -> Sequence[Path]:
    file = Path(file)
    paths = []
    with open(file) as fid:
        for line in fid:
            p = Path(line.strip())
            paths.append(p if p.is_absolute() else (file.parent / p).resolve())
    return paths


class FileListParser(Parser):
    def __init__(self, basedir: Path):
        super().__init__(basedir)
        self._num_instances_cache = None

    def can_parse(self) -> bool:
        return (self._basedir / 'files.txt').exists()

    @property
    def num_instances(self) -> int:
        if self._num_instances_cache is None:
            self._num_instances_cache = len(_get_audio_paths(
                self._basedir / 'files.txt'))

        # noinspection PyTypeChecker
        return self._num_instances_cache

    @property
    def num_folds(self) -> int:
        return 0

    @property
    def label_map(self) -> Optional[Mapping[str, int]]:
        return None

    def parse(self) -> Sequence[_InstanceMetadata]:
        meta_list = []
        for file in _get_audio_paths(self._basedir / 'files.txt'):
            instance_metadata = _InstanceMetadata(path=file,
                                                  filename=file.stem,
                                                  label_nominal=None,
                                                  label_numeric=None,
                                                  cv_folds=[],
                                                  partition=None)
            meta_list.append(instance_metadata)
        return meta_list
