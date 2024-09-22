from fsspec.implementations.cached import SimpleCacheFileSystem
import os
import time
import bz2
from pathlib import Path

class SimpleCacheFileSystemBZIP(SimpleCacheFileSystem):
    """Caches whole remote files on first access

    This class is intended as a layer over any other file system, and
    will make a local copy of each file accessed, so that all subsequent
    reads are local. This implementation only copies whole files, and
    does not keep any metadata about the download time or file details.
    It is therefore safer to use in multi-threaded/concurrent situations.

    This is the only of the caching filesystems that supports write: you will
    be given a real local open file, and upon close and commit, it will be
    uploaded to the target filesystem; the writability or the target URL is
    not checked until that time.

    """

    protocol = "simplecachebzip"
    #local_file = True
    #transaction_type = WriteCachedTransaction

    def __init__(self, **kwargs):

        kw = kwargs.copy()
        for key in ["cache_check", "expiry_time", "check_files"]:
            kw[key] = False
        super().__init__(**kw)
        for storage in self.storage:
            if not os.path.exists(storage):
                os.makedirs(storage, exist_ok=True)

        def _strip_protocol_hp(path):
            fo = kwargs["fo"]
            return fo

        self._strip_protocol: Callable = _strip_protocol_hp


    def pipe_file(self, path, value=None, **kwargs):
        print(f"YO PIPING FILE {path} value={value}")
        if self._intrans:
            with self.open(path, "wb") as f:
                f.write(value)
        else:
            super().pipe_file(path, value)

    def _open(self, path, mode="rb", **kwargs):
        print(f"YO OPEN")
        super()._open(path, mode, **kwargs)


    def open_many(self, open_files, **kwargs):
        paths = [of.path for of in open_files]
        if "r" in open_files.mode:
            print("R")
            self._mkcache()
        else:
            return [
                LocalTempFile(
                    self.fs,
                    path,
                    mode=open_files.mode,
                    fn=os.path.join(self.storage[-1], self._mapper(path)),
                    **kwargs,
                )
                for path in paths
            ]

        if self.compression:
            raise NotImplementedError
        details = [self._check_file(sp) for sp in paths]
        downpath = [p for p, d in zip(paths, details) if not d]
        downfn0 = [
            os.path.join(self.storage[-1], self._mapper(p))
            for p, d in zip(paths, details)
        ]  # keep these path names for opening later
        downfn = [fn for fn, d in zip(downfn0, details) if not d]
        if downpath:

            # skip if all files are already cached and up to date
            self.fs.get(downpath, downfn)

            # update metadata - only happens when downloads are successful
            newdetail = [
                {
                    "original": path,
                    "fn": self._mapper(path),
                    "blocks": True,
                    "time": time.time(),
                    "uid": self.fs.ukey(path),
                }
                for path in downpath
            ]

            downloaded_filename = downfn0[0]
            for path, detail in zip(downpath, newdetail):
                self._metadata.update_file(path, detail)
            self.save_cache()

            #at this point the file is download decompress it
            decompressed_tmp_file = downloaded_filename + "_decompressed"
            with bz2.BZ2File(downloaded_filename) as bzip_file:
                with open(decompressed_tmp_file , "wb") as target:
                    target.write(bzip_file.read())
                #rename the file
                Path(downloaded_filename).unlink()
            Path(decompressed_tmp_file).rename(downloaded_filename)


            

        def firstpart(fn):
            # helper to adapt both whole-file and simple-cache
            return fn[1] if isinstance(fn, tuple) else fn

        return [
            open(firstpart(fn0) if fn0 else fn1, mode=open_files.mode)
            for fn0, fn1 in zip(details, downfn0)
        ]

