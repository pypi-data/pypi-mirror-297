"""
Implements a backend that sends the interactions to a REST endpoint
"""

import os
import typing
from uuid import uuid4
from functools import partial
from dataclasses import asdict

import requests
from loguru import logger
from jsonalias import Json
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from aalu.core.schemas import Metadata
from aalu.backends.base import BaseDecorateBackend


class ZipkinBackend(BaseDecorateBackend):
    """
    Implements a backend to send interactions to a Zipkin endpoint
    """

    endpoint: str
    headers: dict[str, str]

    def model_post_init(self, __context: typing.Any) -> None:
        logger.info(f"Sending interactions to {self.endpoint}")
        s = requests.session()
        s.headers = {
            **self.headers,
            "Content-Type": "application/json",
        }

        zipkin_tracer_provider = TracerProvider()
        zipkin_tracer_provider.add_span_processor(
            BatchSpanProcessor(
                ZipkinExporter(
                    endpoint=self.endpoint,
                    session=s,
                )
            )
        )
        trace.set_tracer_provider(zipkin_tracer_provider)
        return super().model_post_init(__context)

    def get_context_manager(
        self,
        metadata: Metadata,
    ):
        """
        Returns the context manager for the target function
        """
        tracer = trace.get_tracer(metadata.namespace)
        return partial(tracer.start_as_current_span, name=metadata.func_lineage)

    def persist(
        self,
        context_manager,
        input_message: Json,
        output_message: Json,
        timestamp: int,
        duration: int,
        metadata: Metadata,
    ) -> None:
        """
        Implements signature to persist interaction
        """
        tags = asdict(
            metadata.to_persistmodel(
                span_id=uuid4().hex,
                timestamp=timestamp,
                duration=duration,
                input_message=input_message,
                output_message=output_message,
            )
        )["tags"]
        for tagname, tagval in tags.items():
            context_manager.set_attribute(tagname, tagval)


AALU_ZIPKIN_BACKEND = (
    ZipkinBackend(
        endpoint=os.environ["AALU_API_ENDPOINT"],
        headers={"Authorization": f"Bearer {os.environ['AALU_API_KEY']}"},
        tags={"AALU_REST_BACKEND"},
    )
    if (os.getenv("AALU_API_ENDPOINT") and os.getenv("AALU_API_KEY"))
    else None
)
