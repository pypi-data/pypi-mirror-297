__all__ = [
    "World",
]

from collections.abc import Sequence
from ctypes import c_int
from ctypes import c_size_t
from ctypes import c_void_p
from os import PathLike
from typing import Any

from zenkit import Mesh
from zenkit import Write
from zenkit import _native
from zenkit._core import DLL
from zenkit._core import GameVersion
from zenkit._core import PathOrFileLike
from zenkit._native import ZkPointer
from zenkit.vob.virtual_object import VirtualObject
from zenkit.world.bsp_tree import BspTree
from zenkit.world.way_net import WayNet

DLL.ZkWorld_getMesh.restype = ZkPointer
DLL.ZkWorld_getWayNet.restype = ZkPointer
DLL.ZkWorld_getBspTree.restype = ZkPointer
DLL.ZkWorld_getRootObjectCount.restype = c_size_t
DLL.ZkWorld_getRootObject.restype = ZkPointer
DLL.ZkWorld_getNpcSpawnEnabled.restype = c_int
DLL.ZkWorld_getNpcSpawnFlags.restype = c_int
DLL.ZkWorld_getNpcCount.restype = c_size_t


class World:
    __slots__ = ("_handle", "_delete")

    def __init__(self, **kwargs: Any) -> None:
        self._handle = c_void_p(None)

        if "_handle" in kwargs:
            self._handle: c_void_p = kwargs.pop("_handle")
            self._delete: bool = kwargs.pop("_delete", False)

    @staticmethod
    def load(path_or_file_like: PathOrFileLike, version: GameVersion | None = None) -> "World":
        if version is None:
            handle = _native.load("ZkWorld_load", path_or_file_like)
        else:
            handle = _native.load("ZkWorld_loadVersioned", path_or_file_like, version.value)
        return World(_handle=handle, _delete=True)

    @property
    def mesh(self) -> Mesh:
        return Mesh(_handle=DLL.ZkWorld_getMesh(self._handle).value, _delete=False, _keepalive=self)

    @property
    def way_net(self) -> WayNet:
        return WayNet(_handle=DLL.ZkWorld_getWayNet(self._handle).value, _delete=False, _keepalive=self)

    @property
    def bsp_tree(self) -> BspTree:
        return BspTree(_handle=DLL.ZkWorld_getBspTree(self._handle).value, _delete=False, _keepalive=self)

    @property
    def root_objects(self) -> list[VirtualObject]:
        count = DLL.ZkWorld_getRootObjectCount(self._handle)
        items = []

        for i in range(count):
            handle = DLL.ZkWorld_getRootObject(self._handle, i).value
            items.append(VirtualObject.from_native(handle=handle, takeref=True))

        return items

    @root_objects.setter
    def root_objects(self, objs: Sequence[VirtualObject]) -> None:
        DLL.ZkWorld_clearRootObjects(self._handle)

        for obj in objs:
            self.add_root_object(obj)

    def add_root_object(self, obj: VirtualObject) -> None:
        DLL.ZkWorld_addRootObject(self._handle, obj.handle)

    def save(self, path: str | PathLike, version: GameVersion | None = None) -> None:
        w = Write(path)
        DLL.ZkWorld_save(self._handle, w.handle, version)

    def __del__(self) -> None:
        if self._delete:
            DLL.ZkWorld_del(self._handle)
        self._handle = None

    def __repr__(self) -> str:
        return f"<World handle={self._handle}>"

    @property
    def npc_spawn_enabled(self) -> bool:
        return bool(DLL.ZkWorld_getNpcSpawnEnabled(self._handle))

    @npc_spawn_enabled.setter
    def npc_spawn_enabled(self, enable: bool) -> None:
        DLL.ZkWorld_setNpcSpawnEnabled(self._handle, int(enable))

    @property
    def npc_spawn_flags(self) -> int:
        return DLL.ZkWorld_getNpcSpawnFlags(self._handle)

    @npc_spawn_flags.setter
    def npc_spawn_flags(self, flags) -> None:
        DLL.ZkWorld_setNpcSpawnFlags(self._handle, flags)

    @property
    def npcs(self) -> list[VirtualObject]:
        # TODO: Add NPC object type
        count = DLL.ZkWorld_getNpcCount(self._handle)
        items = []

        for i in range(count):
            handle = DLL.ZkWorld_getNpc(self._handle, i).value
            items.append(VirtualObject.from_native(handle=handle, takeref=True))

        return items

    @npcs.setter
    def npcs(self, npcs: Sequence[VirtualObject]) -> None:
        # TODO: Add NPC object type
        DLL.ZkWorld_clearNpcs(self._handle)

        for npc in npcs:
            self.add_npc(npc)

    def add_npc(self, npc: VirtualObject) -> None:
        DLL.ZkWorld_addNpc(self._handle, npc.handle)

    def remove_npc(self, i: int) -> None:
        DLL.ZkWorld_removeNpc(self._handle, i)
