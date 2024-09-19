"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _SimpleRoutes:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _SimpleRoutesEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_SimpleRoutes.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    AllNodes: _SimpleRoutes.ValueType  # 0
    AllPrimaries: _SimpleRoutes.ValueType  # 1
    Random: _SimpleRoutes.ValueType  # 2

class SimpleRoutes(_SimpleRoutes, metaclass=_SimpleRoutesEnumTypeWrapper): ...

AllNodes: SimpleRoutes.ValueType  # 0
AllPrimaries: SimpleRoutes.ValueType  # 1
Random: SimpleRoutes.ValueType  # 2
global___SimpleRoutes = SimpleRoutes

class _SlotTypes:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _SlotTypesEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_SlotTypes.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    Primary: _SlotTypes.ValueType  # 0
    Replica: _SlotTypes.ValueType  # 1

class SlotTypes(_SlotTypes, metaclass=_SlotTypesEnumTypeWrapper): ...

Primary: SlotTypes.ValueType  # 0
Replica: SlotTypes.ValueType  # 1
global___SlotTypes = SlotTypes

class _RequestType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _RequestTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RequestType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    InvalidRequest: _RequestType.ValueType  # 0
    """/ Invalid request type"""
    CustomCommand: _RequestType.ValueType  # 1
    """/ An unknown command, where all arguments are defined by the user."""
    Get: _RequestType.ValueType  # 2
    Set: _RequestType.ValueType  # 3
    Ping: _RequestType.ValueType  # 4
    Info: _RequestType.ValueType  # 5
    Del: _RequestType.ValueType  # 6
    Select: _RequestType.ValueType  # 7
    ConfigGet: _RequestType.ValueType  # 8
    ConfigSet: _RequestType.ValueType  # 9
    ConfigResetStat: _RequestType.ValueType  # 10
    ConfigRewrite: _RequestType.ValueType  # 11
    ClientGetName: _RequestType.ValueType  # 12
    ClientGetRedir: _RequestType.ValueType  # 13
    ClientId: _RequestType.ValueType  # 14
    ClientInfo: _RequestType.ValueType  # 15
    ClientKill: _RequestType.ValueType  # 16
    ClientList: _RequestType.ValueType  # 17
    ClientNoEvict: _RequestType.ValueType  # 18
    ClientNoTouch: _RequestType.ValueType  # 19
    ClientPause: _RequestType.ValueType  # 20
    ClientReply: _RequestType.ValueType  # 21
    ClientSetInfo: _RequestType.ValueType  # 22
    ClientSetName: _RequestType.ValueType  # 23
    ClientUnblock: _RequestType.ValueType  # 24
    ClientUnpause: _RequestType.ValueType  # 25
    Expire: _RequestType.ValueType  # 26
    HSet: _RequestType.ValueType  # 27
    HGet: _RequestType.ValueType  # 28
    HDel: _RequestType.ValueType  # 29
    HExists: _RequestType.ValueType  # 30
    MGet: _RequestType.ValueType  # 31
    MSet: _RequestType.ValueType  # 32
    Incr: _RequestType.ValueType  # 33
    IncrBy: _RequestType.ValueType  # 34
    Decr: _RequestType.ValueType  # 35
    IncrByFloat: _RequestType.ValueType  # 36
    DecrBy: _RequestType.ValueType  # 37
    HGetAll: _RequestType.ValueType  # 38
    HMSet: _RequestType.ValueType  # 39
    HMGet: _RequestType.ValueType  # 40
    HIncrBy: _RequestType.ValueType  # 41
    HIncrByFloat: _RequestType.ValueType  # 42
    LPush: _RequestType.ValueType  # 43
    LPop: _RequestType.ValueType  # 44
    RPush: _RequestType.ValueType  # 45
    RPop: _RequestType.ValueType  # 46
    LLen: _RequestType.ValueType  # 47
    LRem: _RequestType.ValueType  # 48
    LRange: _RequestType.ValueType  # 49
    LTrim: _RequestType.ValueType  # 50
    SAdd: _RequestType.ValueType  # 51
    SRem: _RequestType.ValueType  # 52
    SMembers: _RequestType.ValueType  # 53
    SCard: _RequestType.ValueType  # 54
    PExpireAt: _RequestType.ValueType  # 55
    PExpire: _RequestType.ValueType  # 56
    ExpireAt: _RequestType.ValueType  # 57
    Exists: _RequestType.ValueType  # 58
    Unlink: _RequestType.ValueType  # 59
    TTL: _RequestType.ValueType  # 60
    ZAdd: _RequestType.ValueType  # 61
    ZRem: _RequestType.ValueType  # 62
    ZRange: _RequestType.ValueType  # 63
    ZCard: _RequestType.ValueType  # 64
    ZCount: _RequestType.ValueType  # 65
    ZIncrBy: _RequestType.ValueType  # 66
    ZScore: _RequestType.ValueType  # 67
    Type: _RequestType.ValueType  # 68
    HLen: _RequestType.ValueType  # 69
    Echo: _RequestType.ValueType  # 70
    ZPopMin: _RequestType.ValueType  # 71
    Strlen: _RequestType.ValueType  # 72
    LIndex: _RequestType.ValueType  # 73
    ZPopMax: _RequestType.ValueType  # 74
    XRead: _RequestType.ValueType  # 75
    XAdd: _RequestType.ValueType  # 76
    XReadGroup: _RequestType.ValueType  # 77
    XAck: _RequestType.ValueType  # 78
    XTrim: _RequestType.ValueType  # 79
    XGroupCreate: _RequestType.ValueType  # 80
    XGroupDestroy: _RequestType.ValueType  # 81
    HSetNX: _RequestType.ValueType  # 82
    SIsMember: _RequestType.ValueType  # 83
    HVals: _RequestType.ValueType  # 84
    PTTL: _RequestType.ValueType  # 85
    ZRemRangeByRank: _RequestType.ValueType  # 86
    Persist: _RequestType.ValueType  # 87
    ZRemRangeByScore: _RequestType.ValueType  # 88
    Time: _RequestType.ValueType  # 89
    ZRank: _RequestType.ValueType  # 90
    Rename: _RequestType.ValueType  # 91
    DBSize: _RequestType.ValueType  # 92
    BRPop: _RequestType.ValueType  # 93
    HKeys: _RequestType.ValueType  # 94
    SPop: _RequestType.ValueType  # 95
    PfAdd: _RequestType.ValueType  # 96
    PfCount: _RequestType.ValueType  # 97
    PfMerge: _RequestType.ValueType  # 98
    BLPop: _RequestType.ValueType  # 100
    LInsert: _RequestType.ValueType  # 101
    RPushX: _RequestType.ValueType  # 102
    LPushX: _RequestType.ValueType  # 103
    ZMScore: _RequestType.ValueType  # 104
    ZDiff: _RequestType.ValueType  # 105
    ZDiffStore: _RequestType.ValueType  # 106
    SetRange: _RequestType.ValueType  # 107
    ZRemRangeByLex: _RequestType.ValueType  # 108
    ZLexCount: _RequestType.ValueType  # 109
    Append: _RequestType.ValueType  # 110
    SUnionStore: _RequestType.ValueType  # 111
    SDiffStore: _RequestType.ValueType  # 112
    SInter: _RequestType.ValueType  # 113
    SInterStore: _RequestType.ValueType  # 114
    ZRangeStore: _RequestType.ValueType  # 115
    GetRange: _RequestType.ValueType  # 116
    SMove: _RequestType.ValueType  # 117
    SMIsMember: _RequestType.ValueType  # 118
    ZUnionStore: _RequestType.ValueType  # 119
    LastSave: _RequestType.ValueType  # 120
    GeoAdd: _RequestType.ValueType  # 121
    GeoHash: _RequestType.ValueType  # 122
    ObjectEncoding: _RequestType.ValueType  # 123
    SDiff: _RequestType.ValueType  # 124
    ObjectIdleTime: _RequestType.ValueType  # 125
    ObjectRefCount: _RequestType.ValueType  # 126
    Lolwut: _RequestType.ValueType  # 100500
    GeoDist: _RequestType.ValueType  # 127
    GeoPos: _RequestType.ValueType  # 128
    BZPopMax: _RequestType.ValueType  # 129
    ObjectFreq: _RequestType.ValueType  # 130
    RenameNX: _RequestType.ValueType  # 131
    Touch: _RequestType.ValueType  # 132
    ZRevRank: _RequestType.ValueType  # 133
    ZInterStore: _RequestType.ValueType  # 134
    HRandField: _RequestType.ValueType  # 135
    ZUnion: _RequestType.ValueType  # 136
    BZPopMin: _RequestType.ValueType  # 137
    FlushAll: _RequestType.ValueType  # 138
    ZRandMember: _RequestType.ValueType  # 139
    BitCount: _RequestType.ValueType  # 140
    BZMPop: _RequestType.ValueType  # 141
    SetBit: _RequestType.ValueType  # 142
    ZInterCard: _RequestType.ValueType  # 143
    ZMPop: _RequestType.ValueType  # 144
    GetBit: _RequestType.ValueType  # 145
    ZInter: _RequestType.ValueType  # 146
    BitPos: _RequestType.ValueType  # 147
    BitOp: _RequestType.ValueType  # 148
    HStrlen: _RequestType.ValueType  # 149
    FunctionLoad: _RequestType.ValueType  # 150
    FunctionList: _RequestType.ValueType  # 151
    FunctionDelete: _RequestType.ValueType  # 152
    FunctionFlush: _RequestType.ValueType  # 153
    FCall: _RequestType.ValueType  # 154
    LMPop: _RequestType.ValueType  # 155
    ExpireTime: _RequestType.ValueType  # 156
    PExpireTime: _RequestType.ValueType  # 157
    BLMPop: _RequestType.ValueType  # 158
    XLen: _RequestType.ValueType  # 159
    Sort: _RequestType.ValueType  # 160
    FunctionKill: _RequestType.ValueType  # 161
    FunctionStats: _RequestType.ValueType  # 162
    FCallReadOnly: _RequestType.ValueType  # 163
    FlushDB: _RequestType.ValueType  # 164
    LSet: _RequestType.ValueType  # 165
    XDel: _RequestType.ValueType  # 166
    XRange: _RequestType.ValueType  # 167
    LMove: _RequestType.ValueType  # 168
    BLMove: _RequestType.ValueType  # 169
    GetDel: _RequestType.ValueType  # 170
    SRandMember: _RequestType.ValueType  # 171
    BitField: _RequestType.ValueType  # 172
    BitFieldReadOnly: _RequestType.ValueType  # 173
    Move: _RequestType.ValueType  # 174
    SInterCard: _RequestType.ValueType  # 175
    XRevRange: _RequestType.ValueType  # 176
    Copy: _RequestType.ValueType  # 178
    MSetNX: _RequestType.ValueType  # 179
    LPos: _RequestType.ValueType  # 180
    LCS: _RequestType.ValueType  # 181
    GeoSearch: _RequestType.ValueType  # 182
    Watch: _RequestType.ValueType  # 183
    UnWatch: _RequestType.ValueType  # 184
    GeoSearchStore: _RequestType.ValueType  # 185
    SUnion: _RequestType.ValueType  # 186
    Publish: _RequestType.ValueType  # 187
    SPublish: _RequestType.ValueType  # 188
    XGroupCreateConsumer: _RequestType.ValueType  # 189
    XGroupDelConsumer: _RequestType.ValueType  # 190
    RandomKey: _RequestType.ValueType  # 191
    GetEx: _RequestType.ValueType  # 192
    Dump: _RequestType.ValueType  # 193
    Restore: _RequestType.ValueType  # 194
    SortReadOnly: _RequestType.ValueType  # 195
    FunctionDump: _RequestType.ValueType  # 196
    FunctionRestore: _RequestType.ValueType  # 197
    XPending: _RequestType.ValueType  # 198
    XGroupSetId: _RequestType.ValueType  # 199
    SScan: _RequestType.ValueType  # 200
    ZScan: _RequestType.ValueType  # 201
    HScan: _RequestType.ValueType  # 202
    XAutoClaim: _RequestType.ValueType  # 203
    XInfoGroups: _RequestType.ValueType  # 204
    XInfoConsumers: _RequestType.ValueType  # 205
    XInfoStream: _RequestType.ValueType  # 207
    Scan: _RequestType.ValueType  # 206
    Wait: _RequestType.ValueType  # 208
    XClaim: _RequestType.ValueType  # 209
    PubSubChannels: _RequestType.ValueType  # 210
    PubSubNumPat: _RequestType.ValueType  # 211
    PubSubNumSub: _RequestType.ValueType  # 212
    PubSubSChannels: _RequestType.ValueType  # 213
    PubSubSNumSub: _RequestType.ValueType  # 214
    ScriptExists: _RequestType.ValueType  # 215
    ScriptFlush: _RequestType.ValueType  # 216
    ScriptKill: _RequestType.ValueType  # 217
    ScriptShow: _RequestType.ValueType  # 218

class RequestType(_RequestType, metaclass=_RequestTypeEnumTypeWrapper): ...

InvalidRequest: RequestType.ValueType  # 0
"""/ Invalid request type"""
CustomCommand: RequestType.ValueType  # 1
"""/ An unknown command, where all arguments are defined by the user."""
Get: RequestType.ValueType  # 2
Set: RequestType.ValueType  # 3
Ping: RequestType.ValueType  # 4
Info: RequestType.ValueType  # 5
Del: RequestType.ValueType  # 6
Select: RequestType.ValueType  # 7
ConfigGet: RequestType.ValueType  # 8
ConfigSet: RequestType.ValueType  # 9
ConfigResetStat: RequestType.ValueType  # 10
ConfigRewrite: RequestType.ValueType  # 11
ClientGetName: RequestType.ValueType  # 12
ClientGetRedir: RequestType.ValueType  # 13
ClientId: RequestType.ValueType  # 14
ClientInfo: RequestType.ValueType  # 15
ClientKill: RequestType.ValueType  # 16
ClientList: RequestType.ValueType  # 17
ClientNoEvict: RequestType.ValueType  # 18
ClientNoTouch: RequestType.ValueType  # 19
ClientPause: RequestType.ValueType  # 20
ClientReply: RequestType.ValueType  # 21
ClientSetInfo: RequestType.ValueType  # 22
ClientSetName: RequestType.ValueType  # 23
ClientUnblock: RequestType.ValueType  # 24
ClientUnpause: RequestType.ValueType  # 25
Expire: RequestType.ValueType  # 26
HSet: RequestType.ValueType  # 27
HGet: RequestType.ValueType  # 28
HDel: RequestType.ValueType  # 29
HExists: RequestType.ValueType  # 30
MGet: RequestType.ValueType  # 31
MSet: RequestType.ValueType  # 32
Incr: RequestType.ValueType  # 33
IncrBy: RequestType.ValueType  # 34
Decr: RequestType.ValueType  # 35
IncrByFloat: RequestType.ValueType  # 36
DecrBy: RequestType.ValueType  # 37
HGetAll: RequestType.ValueType  # 38
HMSet: RequestType.ValueType  # 39
HMGet: RequestType.ValueType  # 40
HIncrBy: RequestType.ValueType  # 41
HIncrByFloat: RequestType.ValueType  # 42
LPush: RequestType.ValueType  # 43
LPop: RequestType.ValueType  # 44
RPush: RequestType.ValueType  # 45
RPop: RequestType.ValueType  # 46
LLen: RequestType.ValueType  # 47
LRem: RequestType.ValueType  # 48
LRange: RequestType.ValueType  # 49
LTrim: RequestType.ValueType  # 50
SAdd: RequestType.ValueType  # 51
SRem: RequestType.ValueType  # 52
SMembers: RequestType.ValueType  # 53
SCard: RequestType.ValueType  # 54
PExpireAt: RequestType.ValueType  # 55
PExpire: RequestType.ValueType  # 56
ExpireAt: RequestType.ValueType  # 57
Exists: RequestType.ValueType  # 58
Unlink: RequestType.ValueType  # 59
TTL: RequestType.ValueType  # 60
ZAdd: RequestType.ValueType  # 61
ZRem: RequestType.ValueType  # 62
ZRange: RequestType.ValueType  # 63
ZCard: RequestType.ValueType  # 64
ZCount: RequestType.ValueType  # 65
ZIncrBy: RequestType.ValueType  # 66
ZScore: RequestType.ValueType  # 67
Type: RequestType.ValueType  # 68
HLen: RequestType.ValueType  # 69
Echo: RequestType.ValueType  # 70
ZPopMin: RequestType.ValueType  # 71
Strlen: RequestType.ValueType  # 72
LIndex: RequestType.ValueType  # 73
ZPopMax: RequestType.ValueType  # 74
XRead: RequestType.ValueType  # 75
XAdd: RequestType.ValueType  # 76
XReadGroup: RequestType.ValueType  # 77
XAck: RequestType.ValueType  # 78
XTrim: RequestType.ValueType  # 79
XGroupCreate: RequestType.ValueType  # 80
XGroupDestroy: RequestType.ValueType  # 81
HSetNX: RequestType.ValueType  # 82
SIsMember: RequestType.ValueType  # 83
HVals: RequestType.ValueType  # 84
PTTL: RequestType.ValueType  # 85
ZRemRangeByRank: RequestType.ValueType  # 86
Persist: RequestType.ValueType  # 87
ZRemRangeByScore: RequestType.ValueType  # 88
Time: RequestType.ValueType  # 89
ZRank: RequestType.ValueType  # 90
Rename: RequestType.ValueType  # 91
DBSize: RequestType.ValueType  # 92
BRPop: RequestType.ValueType  # 93
HKeys: RequestType.ValueType  # 94
SPop: RequestType.ValueType  # 95
PfAdd: RequestType.ValueType  # 96
PfCount: RequestType.ValueType  # 97
PfMerge: RequestType.ValueType  # 98
BLPop: RequestType.ValueType  # 100
LInsert: RequestType.ValueType  # 101
RPushX: RequestType.ValueType  # 102
LPushX: RequestType.ValueType  # 103
ZMScore: RequestType.ValueType  # 104
ZDiff: RequestType.ValueType  # 105
ZDiffStore: RequestType.ValueType  # 106
SetRange: RequestType.ValueType  # 107
ZRemRangeByLex: RequestType.ValueType  # 108
ZLexCount: RequestType.ValueType  # 109
Append: RequestType.ValueType  # 110
SUnionStore: RequestType.ValueType  # 111
SDiffStore: RequestType.ValueType  # 112
SInter: RequestType.ValueType  # 113
SInterStore: RequestType.ValueType  # 114
ZRangeStore: RequestType.ValueType  # 115
GetRange: RequestType.ValueType  # 116
SMove: RequestType.ValueType  # 117
SMIsMember: RequestType.ValueType  # 118
ZUnionStore: RequestType.ValueType  # 119
LastSave: RequestType.ValueType  # 120
GeoAdd: RequestType.ValueType  # 121
GeoHash: RequestType.ValueType  # 122
ObjectEncoding: RequestType.ValueType  # 123
SDiff: RequestType.ValueType  # 124
ObjectIdleTime: RequestType.ValueType  # 125
ObjectRefCount: RequestType.ValueType  # 126
Lolwut: RequestType.ValueType  # 100500
GeoDist: RequestType.ValueType  # 127
GeoPos: RequestType.ValueType  # 128
BZPopMax: RequestType.ValueType  # 129
ObjectFreq: RequestType.ValueType  # 130
RenameNX: RequestType.ValueType  # 131
Touch: RequestType.ValueType  # 132
ZRevRank: RequestType.ValueType  # 133
ZInterStore: RequestType.ValueType  # 134
HRandField: RequestType.ValueType  # 135
ZUnion: RequestType.ValueType  # 136
BZPopMin: RequestType.ValueType  # 137
FlushAll: RequestType.ValueType  # 138
ZRandMember: RequestType.ValueType  # 139
BitCount: RequestType.ValueType  # 140
BZMPop: RequestType.ValueType  # 141
SetBit: RequestType.ValueType  # 142
ZInterCard: RequestType.ValueType  # 143
ZMPop: RequestType.ValueType  # 144
GetBit: RequestType.ValueType  # 145
ZInter: RequestType.ValueType  # 146
BitPos: RequestType.ValueType  # 147
BitOp: RequestType.ValueType  # 148
HStrlen: RequestType.ValueType  # 149
FunctionLoad: RequestType.ValueType  # 150
FunctionList: RequestType.ValueType  # 151
FunctionDelete: RequestType.ValueType  # 152
FunctionFlush: RequestType.ValueType  # 153
FCall: RequestType.ValueType  # 154
LMPop: RequestType.ValueType  # 155
ExpireTime: RequestType.ValueType  # 156
PExpireTime: RequestType.ValueType  # 157
BLMPop: RequestType.ValueType  # 158
XLen: RequestType.ValueType  # 159
Sort: RequestType.ValueType  # 160
FunctionKill: RequestType.ValueType  # 161
FunctionStats: RequestType.ValueType  # 162
FCallReadOnly: RequestType.ValueType  # 163
FlushDB: RequestType.ValueType  # 164
LSet: RequestType.ValueType  # 165
XDel: RequestType.ValueType  # 166
XRange: RequestType.ValueType  # 167
LMove: RequestType.ValueType  # 168
BLMove: RequestType.ValueType  # 169
GetDel: RequestType.ValueType  # 170
SRandMember: RequestType.ValueType  # 171
BitField: RequestType.ValueType  # 172
BitFieldReadOnly: RequestType.ValueType  # 173
Move: RequestType.ValueType  # 174
SInterCard: RequestType.ValueType  # 175
XRevRange: RequestType.ValueType  # 176
Copy: RequestType.ValueType  # 178
MSetNX: RequestType.ValueType  # 179
LPos: RequestType.ValueType  # 180
LCS: RequestType.ValueType  # 181
GeoSearch: RequestType.ValueType  # 182
Watch: RequestType.ValueType  # 183
UnWatch: RequestType.ValueType  # 184
GeoSearchStore: RequestType.ValueType  # 185
SUnion: RequestType.ValueType  # 186
Publish: RequestType.ValueType  # 187
SPublish: RequestType.ValueType  # 188
XGroupCreateConsumer: RequestType.ValueType  # 189
XGroupDelConsumer: RequestType.ValueType  # 190
RandomKey: RequestType.ValueType  # 191
GetEx: RequestType.ValueType  # 192
Dump: RequestType.ValueType  # 193
Restore: RequestType.ValueType  # 194
SortReadOnly: RequestType.ValueType  # 195
FunctionDump: RequestType.ValueType  # 196
FunctionRestore: RequestType.ValueType  # 197
XPending: RequestType.ValueType  # 198
XGroupSetId: RequestType.ValueType  # 199
SScan: RequestType.ValueType  # 200
ZScan: RequestType.ValueType  # 201
HScan: RequestType.ValueType  # 202
XAutoClaim: RequestType.ValueType  # 203
XInfoGroups: RequestType.ValueType  # 204
XInfoConsumers: RequestType.ValueType  # 205
XInfoStream: RequestType.ValueType  # 207
Scan: RequestType.ValueType  # 206
Wait: RequestType.ValueType  # 208
XClaim: RequestType.ValueType  # 209
PubSubChannels: RequestType.ValueType  # 210
PubSubNumPat: RequestType.ValueType  # 211
PubSubNumSub: RequestType.ValueType  # 212
PubSubSChannels: RequestType.ValueType  # 213
PubSubSNumSub: RequestType.ValueType  # 214
ScriptExists: RequestType.ValueType  # 215
ScriptFlush: RequestType.ValueType  # 216
ScriptKill: RequestType.ValueType  # 217
ScriptShow: RequestType.ValueType  # 218
global___RequestType = RequestType

@typing.final
class SlotIdRoute(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SLOT_TYPE_FIELD_NUMBER: builtins.int
    SLOT_ID_FIELD_NUMBER: builtins.int
    slot_type: global___SlotTypes.ValueType
    slot_id: builtins.int
    def __init__(
        self,
        *,
        slot_type: global___SlotTypes.ValueType = ...,
        slot_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["slot_id", b"slot_id", "slot_type", b"slot_type"]) -> None: ...

global___SlotIdRoute = SlotIdRoute

@typing.final
class SlotKeyRoute(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SLOT_TYPE_FIELD_NUMBER: builtins.int
    SLOT_KEY_FIELD_NUMBER: builtins.int
    slot_type: global___SlotTypes.ValueType
    slot_key: builtins.str
    def __init__(
        self,
        *,
        slot_type: global___SlotTypes.ValueType = ...,
        slot_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["slot_key", b"slot_key", "slot_type", b"slot_type"]) -> None: ...

global___SlotKeyRoute = SlotKeyRoute

@typing.final
class ByAddressRoute(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HOST_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    host: builtins.str
    port: builtins.int
    def __init__(
        self,
        *,
        host: builtins.str = ...,
        port: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["host", b"host", "port", b"port"]) -> None: ...

global___ByAddressRoute = ByAddressRoute

@typing.final
class Routes(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SIMPLE_ROUTES_FIELD_NUMBER: builtins.int
    SLOT_KEY_ROUTE_FIELD_NUMBER: builtins.int
    SLOT_ID_ROUTE_FIELD_NUMBER: builtins.int
    BY_ADDRESS_ROUTE_FIELD_NUMBER: builtins.int
    simple_routes: global___SimpleRoutes.ValueType
    @property
    def slot_key_route(self) -> global___SlotKeyRoute: ...
    @property
    def slot_id_route(self) -> global___SlotIdRoute: ...
    @property
    def by_address_route(self) -> global___ByAddressRoute: ...
    def __init__(
        self,
        *,
        simple_routes: global___SimpleRoutes.ValueType = ...,
        slot_key_route: global___SlotKeyRoute | None = ...,
        slot_id_route: global___SlotIdRoute | None = ...,
        by_address_route: global___ByAddressRoute | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["by_address_route", b"by_address_route", "simple_routes", b"simple_routes", "slot_id_route", b"slot_id_route", "slot_key_route", b"slot_key_route", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["by_address_route", b"by_address_route", "simple_routes", b"simple_routes", "slot_id_route", b"slot_id_route", "slot_key_route", b"slot_key_route", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["value", b"value"]) -> typing.Literal["simple_routes", "slot_key_route", "slot_id_route", "by_address_route"] | None: ...

global___Routes = Routes

@typing.final
class Command(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class ArgsArray(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        ARGS_FIELD_NUMBER: builtins.int
        @property
        def args(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
        def __init__(
            self,
            *,
            args: collections.abc.Iterable[builtins.bytes] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["args", b"args"]) -> None: ...

    REQUEST_TYPE_FIELD_NUMBER: builtins.int
    ARGS_ARRAY_FIELD_NUMBER: builtins.int
    ARGS_VEC_POINTER_FIELD_NUMBER: builtins.int
    request_type: global___RequestType.ValueType
    args_vec_pointer: builtins.int
    @property
    def args_array(self) -> global___Command.ArgsArray: ...
    def __init__(
        self,
        *,
        request_type: global___RequestType.ValueType = ...,
        args_array: global___Command.ArgsArray | None = ...,
        args_vec_pointer: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["args", b"args", "args_array", b"args_array", "args_vec_pointer", b"args_vec_pointer"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["args", b"args", "args_array", b"args_array", "args_vec_pointer", b"args_vec_pointer", "request_type", b"request_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["args", b"args"]) -> typing.Literal["args_array", "args_vec_pointer"] | None: ...

global___Command = Command

@typing.final
class ScriptInvocationPointers(google.protobuf.message.Message):
    """Used for script requests with large keys or args vectors"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HASH_FIELD_NUMBER: builtins.int
    KEYS_POINTER_FIELD_NUMBER: builtins.int
    ARGS_POINTER_FIELD_NUMBER: builtins.int
    hash: builtins.str
    keys_pointer: builtins.int
    args_pointer: builtins.int
    def __init__(
        self,
        *,
        hash: builtins.str = ...,
        keys_pointer: builtins.int | None = ...,
        args_pointer: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["_args_pointer", b"_args_pointer", "_keys_pointer", b"_keys_pointer", "args_pointer", b"args_pointer", "keys_pointer", b"keys_pointer"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["_args_pointer", b"_args_pointer", "_keys_pointer", b"_keys_pointer", "args_pointer", b"args_pointer", "hash", b"hash", "keys_pointer", b"keys_pointer"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_args_pointer", b"_args_pointer"]) -> typing.Literal["args_pointer"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_keys_pointer", b"_keys_pointer"]) -> typing.Literal["keys_pointer"] | None: ...

global___ScriptInvocationPointers = ScriptInvocationPointers

@typing.final
class ScriptInvocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HASH_FIELD_NUMBER: builtins.int
    KEYS_FIELD_NUMBER: builtins.int
    ARGS_FIELD_NUMBER: builtins.int
    hash: builtins.str
    @property
    def keys(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
    @property
    def args(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]: ...
    def __init__(
        self,
        *,
        hash: builtins.str = ...,
        keys: collections.abc.Iterable[builtins.bytes] | None = ...,
        args: collections.abc.Iterable[builtins.bytes] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["args", b"args", "hash", b"hash", "keys", b"keys"]) -> None: ...

global___ScriptInvocation = ScriptInvocation

@typing.final
class Transaction(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMANDS_FIELD_NUMBER: builtins.int
    @property
    def commands(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Command]: ...
    def __init__(
        self,
        *,
        commands: collections.abc.Iterable[global___Command] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["commands", b"commands"]) -> None: ...

global___Transaction = Transaction

@typing.final
class ClusterScan(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURSOR_FIELD_NUMBER: builtins.int
    MATCH_PATTERN_FIELD_NUMBER: builtins.int
    COUNT_FIELD_NUMBER: builtins.int
    OBJECT_TYPE_FIELD_NUMBER: builtins.int
    cursor: builtins.str
    match_pattern: builtins.bytes
    count: builtins.int
    object_type: builtins.str
    def __init__(
        self,
        *,
        cursor: builtins.str = ...,
        match_pattern: builtins.bytes | None = ...,
        count: builtins.int | None = ...,
        object_type: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["_count", b"_count", "_match_pattern", b"_match_pattern", "_object_type", b"_object_type", "count", b"count", "match_pattern", b"match_pattern", "object_type", b"object_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["_count", b"_count", "_match_pattern", b"_match_pattern", "_object_type", b"_object_type", "count", b"count", "cursor", b"cursor", "match_pattern", b"match_pattern", "object_type", b"object_type"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_count", b"_count"]) -> typing.Literal["count"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_match_pattern", b"_match_pattern"]) -> typing.Literal["match_pattern"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_object_type", b"_object_type"]) -> typing.Literal["object_type"] | None: ...

global___ClusterScan = ClusterScan

@typing.final
class CommandRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CALLBACK_IDX_FIELD_NUMBER: builtins.int
    SINGLE_COMMAND_FIELD_NUMBER: builtins.int
    TRANSACTION_FIELD_NUMBER: builtins.int
    SCRIPT_INVOCATION_FIELD_NUMBER: builtins.int
    SCRIPT_INVOCATION_POINTERS_FIELD_NUMBER: builtins.int
    CLUSTER_SCAN_FIELD_NUMBER: builtins.int
    ROUTE_FIELD_NUMBER: builtins.int
    callback_idx: builtins.int
    @property
    def single_command(self) -> global___Command: ...
    @property
    def transaction(self) -> global___Transaction: ...
    @property
    def script_invocation(self) -> global___ScriptInvocation: ...
    @property
    def script_invocation_pointers(self) -> global___ScriptInvocationPointers: ...
    @property
    def cluster_scan(self) -> global___ClusterScan: ...
    @property
    def route(self) -> global___Routes: ...
    def __init__(
        self,
        *,
        callback_idx: builtins.int = ...,
        single_command: global___Command | None = ...,
        transaction: global___Transaction | None = ...,
        script_invocation: global___ScriptInvocation | None = ...,
        script_invocation_pointers: global___ScriptInvocationPointers | None = ...,
        cluster_scan: global___ClusterScan | None = ...,
        route: global___Routes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["cluster_scan", b"cluster_scan", "command", b"command", "route", b"route", "script_invocation", b"script_invocation", "script_invocation_pointers", b"script_invocation_pointers", "single_command", b"single_command", "transaction", b"transaction"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["callback_idx", b"callback_idx", "cluster_scan", b"cluster_scan", "command", b"command", "route", b"route", "script_invocation", b"script_invocation", "script_invocation_pointers", b"script_invocation_pointers", "single_command", b"single_command", "transaction", b"transaction"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["command", b"command"]) -> typing.Literal["single_command", "transaction", "script_invocation", "script_invocation_pointers", "cluster_scan"] | None: ...

global___CommandRequest = CommandRequest
