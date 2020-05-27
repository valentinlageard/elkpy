import grpc
import sushi_rpc_pb2 as proto
import sushi_rpc_pb2_grpc
from elkpy import sushi_info_types as info

expected_processor_1 = info.ProcessorInfo()
expected_processor_1.id = 1
expected_processor_1.label = "Test plugin 1"
expected_processor_1.name = "test_plugin_1"
expected_processor_1.parameter_count = 1
expected_processor_1.program_count = 1

expected_processor_1_bypass = True

expected_processor_2 = info.ProcessorInfo()
expected_processor_2.id = 2
expected_processor_2.label = "Test plugin 2"
expected_processor_2.name = "test_plugin_2"
expected_processor_2.parameter_count = 2
expected_processor_2.program_count = 2

expected_processor_2_bypass = False

grpc_proc_1 = proto.ProcessorInfo(
    id = expected_processor_1.id,
    label = expected_processor_1.label,
    name = expected_processor_1.name,
    parameter_count = expected_processor_1.parameter_count,
    program_count = expected_processor_1.program_count
)

grpc_proc_2 = proto.ProcessorInfo(
    id = expected_processor_2.id,
    label = expected_processor_2.label,
    name = expected_processor_2.name,
    parameter_count = expected_processor_2.parameter_count,
    program_count = expected_processor_2.program_count
)

grpc_proc_list = proto.ProcessorInfoList(processors = [grpc_proc_1, grpc_proc_2])

expected_track_1 = info.TrackInfo()
expected_track_1.id = 1
expected_track_1.label = "Test track 1"
expected_track_1.name = "test_plugin_1"
expected_track_1.input_channels = 1
expected_track_1.input_busses = 1
expected_track_1.output_channels = 1
expected_track_1.output_busses = 1
expected_track_1.processors = [1, 2]

expected_track_2 = info.TrackInfo()
expected_track_2.id = 2
expected_track_2.label = "Test track 2"
expected_track_2.name = "test_plugin_2"
expected_track_2.input_channels = 2
expected_track_2.input_busses = 2
expected_track_2.output_channels = 2
expected_track_2.output_busses = 2
expected_track_2.processors = [1, 2]

grpc_track_1 = proto.TrackInfo(
    id = expected_track_1.id,
    label = expected_track_1.label,
    name = expected_track_1.name,
    input_channels = expected_track_1.input_channels,
    input_busses = expected_track_1.input_busses,
    output_channels = expected_track_1.output_channels,
    output_busses = expected_track_1.output_busses,
    processors = [proto.ProcessorIdentifier(id = expected_track_1.processors[0]),
                  proto.ProcessorIdentifier(id = expected_track_1.processors[1])]
)

grpc_track_2 = proto.TrackInfo(
    id = expected_track_2.id,
    label = expected_track_2.label,
    name = expected_track_2.name,
    input_channels = expected_track_2.input_channels,
    input_busses = expected_track_2.input_busses,
    output_channels = expected_track_2.output_channels,
    output_busses = expected_track_2.output_busses,
    processors = [proto.ProcessorIdentifier(id = expected_track_2.processors[0]),
                  proto.ProcessorIdentifier(id = expected_track_2.processors[1])]
)

grpc_track_list = proto.TrackInfoList(tracks = [grpc_track_1, grpc_track_2])

expected_proc_bypass_request = proto.ProcessorBypassStateSetRequest(
    processor = proto.ProcessorIdentifier(id = 1),
    value = True
)

expected_create_track_request = proto.CreateTrackRequest(
    name = "test_track_3",
    channels = 3
)

expected_create_multibus_request = proto.CreateMultibusTrackRequest(
    name = "test_multibus",
    output_busses = 12,
    input_busses = 16
)

expected_create_processor_request = proto.CreateProcessorRequest(
    name = "test_processor_3",
    uid = "sushi.internal.test",
    path = "/test/path",
    type = proto.PluginType(type = 2),
    track = proto.TrackIdentifier(id = 1),
    position = proto.ProcessorPosition(add_to_back = False,
                                       before_processor = proto.ProcessorIdentifier(id = 1))
)

expected_move_processor_request = proto.MoveProcessorRequest(
    processor = proto.ProcessorIdentifier(id = 1),
    source_track = proto.TrackIdentifier(id = 1),
    dest_track = proto.TrackIdentifier(id = 2),
    position = proto.ProcessorPosition(add_to_back = True,
                                       before_processor = proto.ProcessorIdentifier(id = 1))
)

expected_delete_processor_request = proto.DeleteProcessorRequest(
    processor = proto.ProcessorIdentifier(id = 2),
    track = proto.TrackIdentifier(id = 1)
)

class AudioGraphControllerServiceMockup(sushi_rpc_pb2_grpc.AudioGraphControllerServicer):

    def __init__(self):
        super().__init__()
        self.called = False
        self.recent_request = None

    def GetAllProcessors(self, request, context):
        return grpc_proc_list

    def GetAllTracks(self, request, context):
        return grpc_track_list

    def GetTrackId(self, request, context):
        if request.value == expected_track_1.name:
            return proto.TrackIdentifier(id = grpc_track_1.id)
        elif request.value == expected_track_2.name:
            return proto.TrackIdentifier(id = grpc_track_2.id)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track name".format(request.value))

    def GetTrackInfo(self, request, context):
        if request.id == expected_track_1.id:
            return grpc_track_1
        elif request.id == expected_track_2.id:
            return grpc_track_2
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track id".format(request.id))

    def GetTrackProcessors(self, request, context):
        if request.id == 1 or request.id == 2:
            return grpc_proc_list
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a track id".format(request.id))

    def GetProcessorId(self, request, context):
        if request.value == expected_processor_1.name:
            return proto.ProcessorIdentifier(id = grpc_proc_1.id)
        elif request.value == expected_processor_2.name:
            return proto.ProcessorIdentifier(id = grpc_proc_2.id)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor name".format(request.value))

    def GetProcessorInfo(self, request, context):
        if request.id == expected_processor_1.id:
            return grpc_proc_1
        elif request.id == expected_processor_2.id:
            return grpc_proc_2
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor id".format(request.id))

    def GetProcessorBypassState(self, request, context):
        if request.id == expected_processor_1.id:
            return proto.GenericBoolValue(value = expected_processor_1_bypass)
        elif request.id == expected_processor_2.id:
            return proto.GenericBoolValue(value = expected_processor_2_bypass)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "{} is not a processor id".format(request.id))

    def SetProcessorBypassState(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateMultibusTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def CreateProcessorOnTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def MoveProcessorOnTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def DeleteProcessorFromTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def DeleteTrack(self, request, context):
        self.called = True
        self.recent_request = request
        return proto.GenericVoidValue()

    def was_called(self):
        temp = self.called
        self.called = False
        return temp

    def get_recent_request(self):
        temp = self.recent_request
        self.recent_request = None
        return temp
