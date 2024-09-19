# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grsim_packet.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import grsim_commands_pb2 as grsim__commands__pb2
import grsim_replacement_pb2 as grsim__replacement__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grsim_packet.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12grsim_packet.proto\x1a\x14grsim_commands.proto\x1a\x17grsim_replacement.proto\"Z\n\x0cgrSim_Packet\x12!\n\x08\x63ommands\x18\x01 \x01(\x0b\x32\x0f.grSim_Commands\x12\'\n\x0breplacement\x18\x02 \x01(\x0b\x32\x12.grSim_Replacement'
  ,
  dependencies=[grsim__commands__pb2.DESCRIPTOR,grsim__replacement__pb2.DESCRIPTOR,])




_GRSIM_PACKET = _descriptor.Descriptor(
  name='grSim_Packet',
  full_name='grSim_Packet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='commands', full_name='grSim_Packet.commands', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='replacement', full_name='grSim_Packet.replacement', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=159,
)

_GRSIM_PACKET.fields_by_name['commands'].message_type = grsim__commands__pb2._GRSIM_COMMANDS
_GRSIM_PACKET.fields_by_name['replacement'].message_type = grsim__replacement__pb2._GRSIM_REPLACEMENT
DESCRIPTOR.message_types_by_name['grSim_Packet'] = _GRSIM_PACKET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

grSim_Packet = _reflection.GeneratedProtocolMessageType('grSim_Packet', (_message.Message,), {
  'DESCRIPTOR' : _GRSIM_PACKET,
  '__module__' : 'grsim_packet_pb2'
  # @@protoc_insertion_point(class_scope:grSim_Packet)
  })
_sym_db.RegisterMessage(grSim_Packet)


# @@protoc_insertion_point(module_scope)
