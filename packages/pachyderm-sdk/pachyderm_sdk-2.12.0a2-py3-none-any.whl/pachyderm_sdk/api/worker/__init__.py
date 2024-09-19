# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: api/worker/worker.proto
# plugin: python-betterproto
# This file has been @generated
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
import grpc

from .. import pps as _pps__


if TYPE_CHECKING:
    import grpc


@dataclass(eq=False, repr=False)
class CancelRequest(betterproto.Message):
    job_id: str = betterproto.string_field(1)
    data_filters: List[str] = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class CancelResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class NextDatumRequest(betterproto.Message):
    """
    Error indicates that the processing of the current datum errored. Datum
    error semantics with datum batching enabled are similar to datum error
    semantics without datum batching enabled in that the datum may be retried,
    recovered, or result with a job failure.
    """

    error: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class NextDatumResponse(betterproto.Message):
    """
    Env is a list of environment variables that should be set for the
    processing of the next datum.
    """

    env: List[str] = betterproto.string_field(1)


class WorkerStub:

    def __init__(self, channel: "grpc.Channel"):
        self.__rpc_status = channel.unary_unary(
            "/pachyderm.worker.Worker/Status",
            request_serializer=betterproto_lib_google_protobuf.Empty.SerializeToString,
            response_deserializer=_pps__.WorkerStatus.FromString,
        )
        self.__rpc_cancel = channel.unary_unary(
            "/pachyderm.worker.Worker/Cancel",
            request_serializer=CancelRequest.SerializeToString,
            response_deserializer=CancelResponse.FromString,
        )
        self.__rpc_next_datum = channel.unary_unary(
            "/pachyderm.worker.Worker/NextDatum",
            request_serializer=NextDatumRequest.SerializeToString,
            response_deserializer=NextDatumResponse.FromString,
        )

    def status(self) -> "_pps__.WorkerStatus":

        request = betterproto_lib_google_protobuf.Empty()

        return self.__rpc_status(request)

    def cancel(
        self, *, job_id: str = "", data_filters: Optional[List[str]] = None
    ) -> "CancelResponse":
        data_filters = data_filters or []

        request = CancelRequest()
        request.job_id = job_id
        request.data_filters = data_filters

        return self.__rpc_cancel(request)

    def next_datum(self, *, error: str = "") -> "NextDatumResponse":

        request = NextDatumRequest()
        request.error = error

        return self.__rpc_next_datum(request)
