import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

from deprecation import deprecated

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint, UiEndpoint
from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    EntityIncompleteException,
    LOGSException,
)
from LOGS.Auxiliary.MinimalModelGenerator import (
    BridgeMinimalFromDict,
    DatasetTypeMinimalFromDict,
    ExperimentMinimalFromDict,
    FormatMinimalFromDict,
    InstrumentMinimalFromDict,
    MethodMinimalFromDict,
    MinimalFromList,
    SampleMinimalFromDict,
)
from LOGS.Auxiliary.ParameterHelper import ParameterHelper
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.DatasetInfo import DatasetInfo
from LOGS.Entities.DatasetRelations import DatasetRelations
from LOGS.Entities.DatasetRequestParameter import ParsingStates
from LOGS.Entities.DatasetTypeMinimal import DatasetTypeMinimal
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entities.Track import Track
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Entity.SerializeableContent import SerializeableContent
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection, ResponseTypes

if TYPE_CHECKING:
    from LOGS.Entities.BridgeMinimal import BridgeMinimal
    from LOGS.Entities.EquipmentMinimal import EquipmentMinimal
    from LOGS.Entities.ExperimentMinimal import ExperimentMinimal
    from LOGS.Entities.FormatMinimal import FormatMinimal
    from LOGS.Entities.InstrumentMinimal import InstrumentMinimal
    from LOGS.Entities.MethodMinimal import MethodMinimal
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal
    from LOGS.Entities.SampleMinimal import SampleMinimal


class ParsedMetadata(SerializeableContent):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


@Endpoint("datasets")
@UiEndpoint("#data")
class Dataset(
    INamedEntity,
    IProjectBased,
    IOwnedEntity,
    IEntityWithIntId,
    IRelatedEntity[DatasetRelations],
    ITypedEntity,
    ISoftDeletable,
    IUniqueEntity,
    IPermissionedEntity,
):
    _noInfo = True
    _noParameters = True
    _relationType = type(DatasetRelations)

    _legacyId: Optional[str]
    _type: Optional[DatasetTypeMinimal]
    _format: Optional["FormatMinimal"]
    _acquisitionDate: Optional[datetime]
    _path: Optional[str]
    _sourceBaseDirectory: Optional[str]
    _sourceRelativeDirectory: Optional[str]
    _method: Optional["MethodMinimal"]
    _experiment: Optional["ExperimentMinimal"]
    _claimed: Optional[bool]
    _notes: Optional[str]
    _dateAdded: Optional[datetime]
    _isViewableEntity: Optional[bool]
    _other: Optional[str]
    _instrument: Optional["InstrumentMinimal"]
    _sample: Optional["SampleMinimal"]
    _bridge: Optional["BridgeMinimal"]
    _operators: Optional[List["PersonMinimal"]]
    _equipments: Optional[List["EquipmentMinimal"]]
    _projects: Optional[List["ProjectMinimal"]]
    _parsingState: Optional[ParsingStates]
    _parsedMetadata: Optional[ParsedMetadata]
    _parameters: Optional[Dict[str, Any]]
    _formatVersion: Optional[int]
    _parserLogs: Optional[List[ParserLog]]
    _tracks: Optional[List[Track]]
    _datatracks: Optional[List[Datatrack]]
    _tracksHierarchy: Optional[HierarchyNode]
    _files: Optional[List[FileEntry]]
    _parameterHelper: Optional[ParameterHelper]
    _zipSize: Optional[int]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        format: Optional[Union[str, "FormatMinimal"]] = None,
    ):
        self._legacyId = None
        self._type = None
        self._format = None
        self._acquisitionDate = None
        self._path = None
        self._method = None
        self._experiment = None
        self._claimed = None
        self._notes = None
        self._dateAdded = None
        self._isViewableEntity = None
        self._isDeleted = None
        self._other = None
        self._instrument = None
        self._sample = None
        self._bridge = None
        self._operators = None
        self._equipments = None
        self._projects = None
        self._parsingState = None
        self._parsedMetadata = None
        self._parameters = None
        self._formatVersion = None
        self._parserLogs = None
        self._tracks = None
        self._datatracks = None
        self._tracksHierarchy = None
        self._files = None
        self._parameterHelper = None
        self._zipSize = None

        super().__init__(ref=ref, id=id, connection=connection)
        self._noSerialize += [
            "parameters",
            "formatVersion",
            "parserLogs",
            "tracks",
            "datatracks",
            "tracksHierarchy",
        ]

        if isinstance(ref, Dataset):
            self._format = ref._format

        if format:
            self.format = cast(Any, format)

        if files:
            if not self._format or not self._format.id:
                raise LOGSException(
                    "Cannot create %s object from files parameter without a format"
                    % type(self).__name__
                )

            self._files = FileEntry.entriesFromFiles(files)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "parameters" in ref:
                self._parameters = self.checkAndConvertNullable(
                    ref["parameters"], dict, "parameters"
                )
                self._noParameters = False
                self._noParameters = False
            if "formatVersion" in ref:
                self._formatVersion = self.checkAndConvertNullable(
                    ref["formatVersion"], int, "formatVersion"
                )
                self._noInfo = False
            if "parserLogs" in ref:
                self._parserLogs = self.checkListAndConvertNullable(
                    ref["parserLogs"], ParserLog, "parserLogs"
                )
                self._noInfo = False
            if "tracks" in ref:
                self._tracks = self.checkListAndConvertNullable(
                    ref["tracks"], Track, "tracks"
                )
                self._noInfo = False
            if "datatracks" in ref:
                self._datatracks = self.checkListAndConvertNullable(
                    ref["datatracks"], Datatrack, "datatracks"
                )
                self._noInfo = False
            if "tracksHierarchy" in ref:
                self._tracksHierarchy = self.checkAndConvertNullable(
                    ref["tracksHierarchy"], HierarchyNode, "tracksHierarchy"
                )
                self._noInfo = False

        super().fromDict(ref=ref)

    def fetchZipSize(self):
        connection, endpoint, id = self._getConnectionData()

        zip, responseError = connection.getEndpoint(
            endpoint + ["zip_size"], parameters={"ids": [self.id]}
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(zip, dict) and "size" in zip:
            self._zipSize = zip["size"]

    def fetchParameters(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, responseError = connection.getEndpoint(
            endpoint + [id, "parameters"]
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(parameters, dict):
            if "url" in parameters:
                del parameters["url"]
            self._parameters = parameters
        else:
            self._parameters = {}

        self._parameterHelper = ParameterHelper(self._parameters)
        self._noParameters = False

    def fetchInfo(self: "Dataset"):
        connection, endpoint, id = self._getConnectionData()

        data, responseError = connection.getEndpoint(endpoint + [id, "info"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        info = DatasetInfo(data)
        self._formatVersion = info.formatVersion
        self._parserLogs = info.parserLogs
        self._tracks = info.tracks
        self._datatracks = info.datatracks
        self._tracksHierarchy = info.tracksHierarchy
        self._parsingState = info.parsingState

        trackLookup: Dict[str, Datatrack] = {}
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack.connection = self.connection
                datatrack._endpoint = endpoint + [str(id), "datatrack"]
                if datatrack.id:
                    trackLookup[datatrack.id] = datatrack

        if self._tracks:
            for track in self._tracks:
                track.connection = self.connection
                if track._dataIds:
                    track.datatracks = cast(
                        Any,
                        {
                            k: (trackLookup[v] if v in trackLookup else None)
                            for k, v in track._dataIds.items()
                        },
                    )
        self._noInfo = False

    def fetchFull(self):
        self.fetchParameters()
        self.fetchInfo()
        self.fetchZipSize()

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ):
        connection, endpoint, id = self._getConnectionData()

        if not directory:
            directory = os.curdir

        if not fileName:
            fileName = self.name if self.name and self.name != "" else "Dataset"
            fileName += ".zip"

        path = os.path.join(directory, Tools.sanitizeFileName(fileName=fileName))

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, responseError = connection.getEndpoint(
            endpoint + [id, "files", "zip"], responseType=ResponseTypes.RAW
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        with open(path, mode="wb") as localfile:
            localfile.write(cast(bytes, data))

        return path

    def getParameter(self, key, removeUnit=False):
        if not self._parameterHelper:
            self._parameterHelper = ParameterHelper(self.parameters)
        return self._parameterHelper.get(key, removeUnit)

    @property
    def type(self) -> Optional[DatasetTypeMinimal]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = DatasetTypeMinimalFromDict(
            value, "datasetType", connection=self.connection
        )

    @property
    def format(self) -> Optional["FormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = FormatMinimalFromDict(
            value, "format", connection=self.connection
        )

    @property
    def acquisitionDate(self) -> Optional[datetime]:
        return self._acquisitionDate

    @acquisitionDate.setter
    def acquisitionDate(self, value):
        self._acquisitionDate = self.checkAndConvertNullable(
            value, datetime, "acquisitionDate"
        )

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, value):
        self._path = self.checkAndConvertNullable(value, str, "path")

    @property
    def claimed(self) -> Optional[bool]:
        return self._claimed

    @claimed.setter
    def claimed(self, value):
        self._claimed = self.checkAndConvertNullable(value, bool, "claimed")

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def dateAdded(self) -> Optional[datetime]:
        return self._dateAdded

    @dateAdded.setter
    def dateAdded(self, value):
        self._dateAdded = self.checkAndConvertNullable(value, datetime, "dateAdded")

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = self.checkAndConvertNullable(value, bool, "isDeleted")

    @property
    def other(self) -> Optional[str]:
        return self._other

    @other.setter
    def other(self, value):
        self._other = self.checkAndConvertNullable(value, str, "other")

    @property
    def parsingState(self) -> Optional[ParsingStates]:
        return self._parsingState

    @parsingState.setter
    def parsingState(self, value):
        self._parsingState = cast(
            ParsingStates, self.checkAndConvertNullable(value, str, "parsingState")
        )

    @property
    def parsedMetadata(self) -> Optional[ParsedMetadata]:
        return self._parsedMetadata

    @parsedMetadata.setter
    def parsedMetadata(self, value):
        self._parsedMetadata = self.checkAndConvertNullable(
            value, ParsedMetadata, "parsedMetadata"
        )

    @property
    def parameters(self) -> Optional[Dict[str, Any]]:
        if self._noParameters:
            raise EntityIncompleteException(
                self,
                parameterName="parameters",
                functionName=f"{self.fetchParameters.__name__}()",
            )
        return self._parameters

    @property
    def formatVersion(self) -> Optional[int]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="formatVersion",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._formatVersion

    @property
    def parserLogs(self) -> Optional[List[ParserLog]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="parserLogs",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._parserLogs

    @property
    def tracks(self) -> Optional[List[Track]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracks

    @property
    def datatracks(self) -> Optional[List[Datatrack]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="datatracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._datatracks

    @property
    def tracksHierarchy(self) -> Optional[HierarchyNode]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracksHierarchy",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracksHierarchy

    @property
    def zipSize(self) -> Optional[int]:
        if self._zipSize is None:
            raise EntityIncompleteException(
                self,
                parameterName="zipSize",
                functionName=f"{self.fetchZipSize.__name__}()",
            )
        return self._zipSize

    @property
    def bridge(self) -> Optional["BridgeMinimal"]:
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = BridgeMinimalFromDict(
            value, "bridge", connection=self.connection
        )

    @property
    def bridgeId(self) -> Optional[int]:
        return self._bridge.id if self._bridge else None

    @bridgeId.setter
    def bridgeId(self, value):
        self._bridge = BridgeMinimalFromDict(
            value, "bridge", connection=self.connection
        )

    @property
    def equipments(self) -> Optional[List["EquipmentMinimal"]]:
        return self._equipments

    @equipments.setter
    def equipments(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def equipmentIds(self) -> Optional[List[int]]:
        if self._equipments is None:
            return None
        return [e.id for e in self._equipments]

    @equipmentIds.setter
    def equipmentIds(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def method(self) -> Optional["MethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def methodId(self) -> Optional[int]:
        return self._method.id if self._method else None

    @property
    def experiment(self) -> Optional["ExperimentMinimal"]:
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = ExperimentMinimalFromDict(
            value, "experiment", connection=self.connection
        )

    @property
    def sample(self) -> Optional["SampleMinimal"]:
        return self._sample

    @sample.setter
    def sample(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def sampleId(self) -> Optional[int]:
        return self._sample.id if self._sample else None

    @sampleId.setter
    def sampleId(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def operators(self) -> Optional[List["PersonMinimal"]]:
        return self._operators

    @operators.setter
    def operators(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def operatorIds(self) -> Optional[List[int]]:
        if self._operators is None:
            return None
        return [e.id for e in self._operators]

    @operatorIds.setter
    def operatorIds(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def projects(self) -> Optional[List["ProjectMinimal"]]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    @property
    def projectIds(self) -> Optional[List[int]]:
        if self._projects is None:
            return None
        return [e.id for e in self._projects]

    @projectIds.setter
    def projectIds(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    @property
    def instrument(self) -> Optional["InstrumentMinimal"]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )

    @property
    def instrumentId(self) -> Optional[int]:
        return self._instrument.id if self._instrument else None

    @instrumentId.setter
    def instrumentId(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )

    @property
    def legacyId(self) -> Optional[str]:
        return self._legacyId

    @legacyId.setter
    def legacyId(self, value):
        self._legacyId = self.checkAndConvertNullable(value, str, "legacyId")

    @property
    def sourceBaseDirectory(self) -> Optional[str]:
        return self._sourceBaseDirectory

    @sourceBaseDirectory.setter
    def sourceBaseDirectory(self, value):
        self._sourceBaseDirectory = self.checkAndConvertNullable(
            value, str, "sourceBaseDirectory"
        )

    @property
    def sourceRelativeDirectory(self) -> Optional[str]:
        return self._sourceRelativeDirectory

    @sourceRelativeDirectory.setter
    def sourceRelativeDirectory(self, value):
        self._sourceRelativeDirectory = self.checkAndConvertNullable(
            value, str, "sourceRelativeDirectory"
        )

    @property
    @deprecated(details="Please use property 'attachment'")
    def isViewableEntity(self) -> Optional[bool]:
        return self._isViewableEntity

    @isViewableEntity.setter
    @deprecated(details="Please use property 'attachment'")
    def isViewableEntity(self, value):
        self._isViewableEntity = self.checkAndConvertNullable(
            value, bool, "isViewableEntity"
        )
