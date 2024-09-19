# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/command_request.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eprotobuf/command_request.proto\x12\x0f\x63ommand_request\"M\n\x0bSlotIdRoute\x12-\n\tslot_type\x18\x01 \x01(\x0e\x32\x1a.command_request.SlotTypes\x12\x0f\n\x07slot_id\x18\x02 \x01(\x05\"O\n\x0cSlotKeyRoute\x12-\n\tslot_type\x18\x01 \x01(\x0e\x32\x1a.command_request.SlotTypes\x12\x10\n\x08slot_key\x18\x02 \x01(\t\",\n\x0e\x42yAddressRoute\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\xf6\x01\n\x06Routes\x12\x36\n\rsimple_routes\x18\x01 \x01(\x0e\x32\x1d.command_request.SimpleRoutesH\x00\x12\x37\n\x0eslot_key_route\x18\x02 \x01(\x0b\x32\x1d.command_request.SlotKeyRouteH\x00\x12\x35\n\rslot_id_route\x18\x03 \x01(\x0b\x32\x1c.command_request.SlotIdRouteH\x00\x12;\n\x10\x62y_address_route\x18\x04 \x01(\x0b\x32\x1f.command_request.ByAddressRouteH\x00\x42\x07\n\x05value\"\xb6\x01\n\x07\x43ommand\x12\x32\n\x0crequest_type\x18\x01 \x01(\x0e\x32\x1c.command_request.RequestType\x12\x38\n\nargs_array\x18\x02 \x01(\x0b\x32\".command_request.Command.ArgsArrayH\x00\x12\x1a\n\x10\x61rgs_vec_pointer\x18\x03 \x01(\x04H\x00\x1a\x19\n\tArgsArray\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\x0c\x42\x06\n\x04\x61rgs\"\x80\x01\n\x18ScriptInvocationPointers\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x19\n\x0ckeys_pointer\x18\x02 \x01(\x04H\x00\x88\x01\x01\x12\x19\n\x0c\x61rgs_pointer\x18\x03 \x01(\x04H\x01\x88\x01\x01\x42\x0f\n\r_keys_pointerB\x0f\n\r_args_pointer\"<\n\x10ScriptInvocation\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04keys\x18\x02 \x03(\x0c\x12\x0c\n\x04\x61rgs\x18\x03 \x03(\x0c\"9\n\x0bTransaction\x12*\n\x08\x63ommands\x18\x01 \x03(\x0b\x32\x18.command_request.Command\"\x93\x01\n\x0b\x43lusterScan\x12\x0e\n\x06\x63ursor\x18\x01 \x01(\t\x12\x1a\n\rmatch_pattern\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x12\x12\n\x05\x63ount\x18\x03 \x01(\x03H\x01\x88\x01\x01\x12\x18\n\x0bobject_type\x18\x04 \x01(\tH\x02\x88\x01\x01\x42\x10\n\x0e_match_patternB\x08\n\x06_countB\x0e\n\x0c_object_type\"\x89\x03\n\x0e\x43ommandRequest\x12\x14\n\x0c\x63\x61llback_idx\x18\x01 \x01(\r\x12\x32\n\x0esingle_command\x18\x02 \x01(\x0b\x32\x18.command_request.CommandH\x00\x12\x33\n\x0btransaction\x18\x03 \x01(\x0b\x32\x1c.command_request.TransactionH\x00\x12>\n\x11script_invocation\x18\x04 \x01(\x0b\x32!.command_request.ScriptInvocationH\x00\x12O\n\x1ascript_invocation_pointers\x18\x05 \x01(\x0b\x32).command_request.ScriptInvocationPointersH\x00\x12\x34\n\x0c\x63luster_scan\x18\x06 \x01(\x0b\x32\x1c.command_request.ClusterScanH\x00\x12&\n\x05route\x18\x07 \x01(\x0b\x32\x17.command_request.RoutesB\t\n\x07\x63ommand*:\n\x0cSimpleRoutes\x12\x0c\n\x08\x41llNodes\x10\x00\x12\x10\n\x0c\x41llPrimaries\x10\x01\x12\n\n\x06Random\x10\x02*%\n\tSlotTypes\x12\x0b\n\x07Primary\x10\x00\x12\x0b\n\x07Replica\x10\x01*\xbe\x18\n\x0bRequestType\x12\x12\n\x0eInvalidRequest\x10\x00\x12\x11\n\rCustomCommand\x10\x01\x12\x07\n\x03Get\x10\x02\x12\x07\n\x03Set\x10\x03\x12\x08\n\x04Ping\x10\x04\x12\x08\n\x04Info\x10\x05\x12\x07\n\x03\x44\x65l\x10\x06\x12\n\n\x06Select\x10\x07\x12\r\n\tConfigGet\x10\x08\x12\r\n\tConfigSet\x10\t\x12\x13\n\x0f\x43onfigResetStat\x10\n\x12\x11\n\rConfigRewrite\x10\x0b\x12\x11\n\rClientGetName\x10\x0c\x12\x12\n\x0e\x43lientGetRedir\x10\r\x12\x0c\n\x08\x43lientId\x10\x0e\x12\x0e\n\nClientInfo\x10\x0f\x12\x0e\n\nClientKill\x10\x10\x12\x0e\n\nClientList\x10\x11\x12\x11\n\rClientNoEvict\x10\x12\x12\x11\n\rClientNoTouch\x10\x13\x12\x0f\n\x0b\x43lientPause\x10\x14\x12\x0f\n\x0b\x43lientReply\x10\x15\x12\x11\n\rClientSetInfo\x10\x16\x12\x11\n\rClientSetName\x10\x17\x12\x11\n\rClientUnblock\x10\x18\x12\x11\n\rClientUnpause\x10\x19\x12\n\n\x06\x45xpire\x10\x1a\x12\x08\n\x04HSet\x10\x1b\x12\x08\n\x04HGet\x10\x1c\x12\x08\n\x04HDel\x10\x1d\x12\x0b\n\x07HExists\x10\x1e\x12\x08\n\x04MGet\x10\x1f\x12\x08\n\x04MSet\x10 \x12\x08\n\x04Incr\x10!\x12\n\n\x06IncrBy\x10\"\x12\x08\n\x04\x44\x65\x63r\x10#\x12\x0f\n\x0bIncrByFloat\x10$\x12\n\n\x06\x44\x65\x63rBy\x10%\x12\x0b\n\x07HGetAll\x10&\x12\t\n\x05HMSet\x10\'\x12\t\n\x05HMGet\x10(\x12\x0b\n\x07HIncrBy\x10)\x12\x10\n\x0cHIncrByFloat\x10*\x12\t\n\x05LPush\x10+\x12\x08\n\x04LPop\x10,\x12\t\n\x05RPush\x10-\x12\x08\n\x04RPop\x10.\x12\x08\n\x04LLen\x10/\x12\x08\n\x04LRem\x10\x30\x12\n\n\x06LRange\x10\x31\x12\t\n\x05LTrim\x10\x32\x12\x08\n\x04SAdd\x10\x33\x12\x08\n\x04SRem\x10\x34\x12\x0c\n\x08SMembers\x10\x35\x12\t\n\x05SCard\x10\x36\x12\r\n\tPExpireAt\x10\x37\x12\x0b\n\x07PExpire\x10\x38\x12\x0c\n\x08\x45xpireAt\x10\x39\x12\n\n\x06\x45xists\x10:\x12\n\n\x06Unlink\x10;\x12\x07\n\x03TTL\x10<\x12\x08\n\x04ZAdd\x10=\x12\x08\n\x04ZRem\x10>\x12\n\n\x06ZRange\x10?\x12\t\n\x05ZCard\x10@\x12\n\n\x06ZCount\x10\x41\x12\x0b\n\x07ZIncrBy\x10\x42\x12\n\n\x06ZScore\x10\x43\x12\x08\n\x04Type\x10\x44\x12\x08\n\x04HLen\x10\x45\x12\x08\n\x04\x45\x63ho\x10\x46\x12\x0b\n\x07ZPopMin\x10G\x12\n\n\x06Strlen\x10H\x12\n\n\x06LIndex\x10I\x12\x0b\n\x07ZPopMax\x10J\x12\t\n\x05XRead\x10K\x12\x08\n\x04XAdd\x10L\x12\x0e\n\nXReadGroup\x10M\x12\x08\n\x04XAck\x10N\x12\t\n\x05XTrim\x10O\x12\x10\n\x0cXGroupCreate\x10P\x12\x11\n\rXGroupDestroy\x10Q\x12\n\n\x06HSetNX\x10R\x12\r\n\tSIsMember\x10S\x12\t\n\x05HVals\x10T\x12\x08\n\x04PTTL\x10U\x12\x13\n\x0fZRemRangeByRank\x10V\x12\x0b\n\x07Persist\x10W\x12\x14\n\x10ZRemRangeByScore\x10X\x12\x08\n\x04Time\x10Y\x12\t\n\x05ZRank\x10Z\x12\n\n\x06Rename\x10[\x12\n\n\x06\x44\x42Size\x10\\\x12\t\n\x05\x42RPop\x10]\x12\t\n\x05HKeys\x10^\x12\x08\n\x04SPop\x10_\x12\t\n\x05PfAdd\x10`\x12\x0b\n\x07PfCount\x10\x61\x12\x0b\n\x07PfMerge\x10\x62\x12\t\n\x05\x42LPop\x10\x64\x12\x0b\n\x07LInsert\x10\x65\x12\n\n\x06RPushX\x10\x66\x12\n\n\x06LPushX\x10g\x12\x0b\n\x07ZMScore\x10h\x12\t\n\x05ZDiff\x10i\x12\x0e\n\nZDiffStore\x10j\x12\x0c\n\x08SetRange\x10k\x12\x12\n\x0eZRemRangeByLex\x10l\x12\r\n\tZLexCount\x10m\x12\n\n\x06\x41ppend\x10n\x12\x0f\n\x0bSUnionStore\x10o\x12\x0e\n\nSDiffStore\x10p\x12\n\n\x06SInter\x10q\x12\x0f\n\x0bSInterStore\x10r\x12\x0f\n\x0bZRangeStore\x10s\x12\x0c\n\x08GetRange\x10t\x12\t\n\x05SMove\x10u\x12\x0e\n\nSMIsMember\x10v\x12\x0f\n\x0bZUnionStore\x10w\x12\x0c\n\x08LastSave\x10x\x12\n\n\x06GeoAdd\x10y\x12\x0b\n\x07GeoHash\x10z\x12\x12\n\x0eObjectEncoding\x10{\x12\t\n\x05SDiff\x10|\x12\x12\n\x0eObjectIdleTime\x10}\x12\x12\n\x0eObjectRefCount\x10~\x12\x0c\n\x06Lolwut\x10\x94\x91\x06\x12\x0b\n\x07GeoDist\x10\x7f\x12\x0b\n\x06GeoPos\x10\x80\x01\x12\r\n\x08\x42ZPopMax\x10\x81\x01\x12\x0f\n\nObjectFreq\x10\x82\x01\x12\r\n\x08RenameNX\x10\x83\x01\x12\n\n\x05Touch\x10\x84\x01\x12\r\n\x08ZRevRank\x10\x85\x01\x12\x10\n\x0bZInterStore\x10\x86\x01\x12\x0f\n\nHRandField\x10\x87\x01\x12\x0b\n\x06ZUnion\x10\x88\x01\x12\r\n\x08\x42ZPopMin\x10\x89\x01\x12\r\n\x08\x46lushAll\x10\x8a\x01\x12\x10\n\x0bZRandMember\x10\x8b\x01\x12\r\n\x08\x42itCount\x10\x8c\x01\x12\x0b\n\x06\x42ZMPop\x10\x8d\x01\x12\x0b\n\x06SetBit\x10\x8e\x01\x12\x0f\n\nZInterCard\x10\x8f\x01\x12\n\n\x05ZMPop\x10\x90\x01\x12\x0b\n\x06GetBit\x10\x91\x01\x12\x0b\n\x06ZInter\x10\x92\x01\x12\x0b\n\x06\x42itPos\x10\x93\x01\x12\n\n\x05\x42itOp\x10\x94\x01\x12\x0c\n\x07HStrlen\x10\x95\x01\x12\x11\n\x0c\x46unctionLoad\x10\x96\x01\x12\x11\n\x0c\x46unctionList\x10\x97\x01\x12\x13\n\x0e\x46unctionDelete\x10\x98\x01\x12\x12\n\rFunctionFlush\x10\x99\x01\x12\n\n\x05\x46\x43\x61ll\x10\x9a\x01\x12\n\n\x05LMPop\x10\x9b\x01\x12\x0f\n\nExpireTime\x10\x9c\x01\x12\x10\n\x0bPExpireTime\x10\x9d\x01\x12\x0b\n\x06\x42LMPop\x10\x9e\x01\x12\t\n\x04XLen\x10\x9f\x01\x12\t\n\x04Sort\x10\xa0\x01\x12\x11\n\x0c\x46unctionKill\x10\xa1\x01\x12\x12\n\rFunctionStats\x10\xa2\x01\x12\x12\n\rFCallReadOnly\x10\xa3\x01\x12\x0c\n\x07\x46lushDB\x10\xa4\x01\x12\t\n\x04LSet\x10\xa5\x01\x12\t\n\x04XDel\x10\xa6\x01\x12\x0b\n\x06XRange\x10\xa7\x01\x12\n\n\x05LMove\x10\xa8\x01\x12\x0b\n\x06\x42LMove\x10\xa9\x01\x12\x0b\n\x06GetDel\x10\xaa\x01\x12\x10\n\x0bSRandMember\x10\xab\x01\x12\r\n\x08\x42itField\x10\xac\x01\x12\x15\n\x10\x42itFieldReadOnly\x10\xad\x01\x12\t\n\x04Move\x10\xae\x01\x12\x0f\n\nSInterCard\x10\xaf\x01\x12\x0e\n\tXRevRange\x10\xb0\x01\x12\t\n\x04\x43opy\x10\xb2\x01\x12\x0b\n\x06MSetNX\x10\xb3\x01\x12\t\n\x04LPos\x10\xb4\x01\x12\x08\n\x03LCS\x10\xb5\x01\x12\x0e\n\tGeoSearch\x10\xb6\x01\x12\n\n\x05Watch\x10\xb7\x01\x12\x0c\n\x07UnWatch\x10\xb8\x01\x12\x13\n\x0eGeoSearchStore\x10\xb9\x01\x12\x0b\n\x06SUnion\x10\xba\x01\x12\x0c\n\x07Publish\x10\xbb\x01\x12\r\n\x08SPublish\x10\xbc\x01\x12\x19\n\x14XGroupCreateConsumer\x10\xbd\x01\x12\x16\n\x11XGroupDelConsumer\x10\xbe\x01\x12\x0e\n\tRandomKey\x10\xbf\x01\x12\n\n\x05GetEx\x10\xc0\x01\x12\t\n\x04\x44ump\x10\xc1\x01\x12\x0c\n\x07Restore\x10\xc2\x01\x12\x11\n\x0cSortReadOnly\x10\xc3\x01\x12\x11\n\x0c\x46unctionDump\x10\xc4\x01\x12\x14\n\x0f\x46unctionRestore\x10\xc5\x01\x12\r\n\x08XPending\x10\xc6\x01\x12\x10\n\x0bXGroupSetId\x10\xc7\x01\x12\n\n\x05SScan\x10\xc8\x01\x12\n\n\x05ZScan\x10\xc9\x01\x12\n\n\x05HScan\x10\xca\x01\x12\x0f\n\nXAutoClaim\x10\xcb\x01\x12\x10\n\x0bXInfoGroups\x10\xcc\x01\x12\x13\n\x0eXInfoConsumers\x10\xcd\x01\x12\x10\n\x0bXInfoStream\x10\xcf\x01\x12\t\n\x04Scan\x10\xce\x01\x12\t\n\x04Wait\x10\xd0\x01\x12\x0b\n\x06XClaim\x10\xd1\x01\x12\x13\n\x0ePubSubChannels\x10\xd2\x01\x12\x11\n\x0cPubSubNumPat\x10\xd3\x01\x12\x11\n\x0cPubSubNumSub\x10\xd4\x01\x12\x14\n\x0fPubSubSChannels\x10\xd5\x01\x12\x12\n\rPubSubSNumSub\x10\xd6\x01\x12\x11\n\x0cScriptExists\x10\xd7\x01\x12\x10\n\x0bScriptFlush\x10\xd8\x01\x12\x0f\n\nScriptKill\x10\xd9\x01\x12\x0f\n\nScriptShow\x10\xda\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.command_request_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SIMPLEROUTES']._serialized_start=1489
  _globals['_SIMPLEROUTES']._serialized_end=1547
  _globals['_SLOTTYPES']._serialized_start=1549
  _globals['_SLOTTYPES']._serialized_end=1586
  _globals['_REQUESTTYPE']._serialized_start=1589
  _globals['_REQUESTTYPE']._serialized_end=4723
  _globals['_SLOTIDROUTE']._serialized_start=51
  _globals['_SLOTIDROUTE']._serialized_end=128
  _globals['_SLOTKEYROUTE']._serialized_start=130
  _globals['_SLOTKEYROUTE']._serialized_end=209
  _globals['_BYADDRESSROUTE']._serialized_start=211
  _globals['_BYADDRESSROUTE']._serialized_end=255
  _globals['_ROUTES']._serialized_start=258
  _globals['_ROUTES']._serialized_end=504
  _globals['_COMMAND']._serialized_start=507
  _globals['_COMMAND']._serialized_end=689
  _globals['_COMMAND_ARGSARRAY']._serialized_start=656
  _globals['_COMMAND_ARGSARRAY']._serialized_end=681
  _globals['_SCRIPTINVOCATIONPOINTERS']._serialized_start=692
  _globals['_SCRIPTINVOCATIONPOINTERS']._serialized_end=820
  _globals['_SCRIPTINVOCATION']._serialized_start=822
  _globals['_SCRIPTINVOCATION']._serialized_end=882
  _globals['_TRANSACTION']._serialized_start=884
  _globals['_TRANSACTION']._serialized_end=941
  _globals['_CLUSTERSCAN']._serialized_start=944
  _globals['_CLUSTERSCAN']._serialized_end=1091
  _globals['_COMMANDREQUEST']._serialized_start=1094
  _globals['_COMMANDREQUEST']._serialized_end=1487
# @@protoc_insertion_point(module_scope)
