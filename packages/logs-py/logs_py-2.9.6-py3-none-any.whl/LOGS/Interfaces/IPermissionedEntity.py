from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional

from LOGS.Auxiliary import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class IPermissionedEntityRequest:
    includePermissions: Optional[bool] = None


class IPermissionedEntity(IEntityInterface):
    _permissions: Optional[Dict[str, bool]] = None

    @property
    def permissions(self) -> Optional[Dict[str, bool]]:
        return self._permissions

    @permissions.setter
    def permissions(self, value):
        self._permissions = Tools.checkAndConvert(
            value, dict, "permissions", allowNone=True
        )
