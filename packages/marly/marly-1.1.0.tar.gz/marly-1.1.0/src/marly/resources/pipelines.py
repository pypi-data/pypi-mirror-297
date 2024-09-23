# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import pipeline_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.pipeline_result import PipelineResult
from ..types.pipeline_response_model import PipelineResponseModel

__all__ = ["PipelinesResource", "AsyncPipelinesResource"]


class PipelinesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PipelinesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/velocitybolt/marly-python#accessing-raw-response-data-eg-headers
        """
        return PipelinesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PipelinesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/velocitybolt/marly-python#with_streaming_response
        """
        return PipelinesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        api_key: str,
        provider_model_name: str,
        provider_type: str,
        workloads: Iterable[pipeline_create_params.Workload],
        additional_params: Dict[str, object] | NotGiven = NOT_GIVEN,
        markdown_mode: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineResponseModel:
        """
        Initiates a pipeline processing job for the given PDF and schemas.

        Args:
          api_key: API key for the AI provider

          provider_model_name: Name of the AI model to use

          provider_type: Type of AI provider (e.g., 'azure', 'openai')

          workloads: Array of workload objects containing PDF content and schemas

          additional_params: Additional parameters specific to the AI provider

          markdown_mode: Flag to enable markdown mode

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/pipelines",
            body=maybe_transform(
                {
                    "api_key": api_key,
                    "provider_model_name": provider_model_name,
                    "provider_type": provider_type,
                    "workloads": workloads,
                    "additional_params": additional_params,
                    "markdown_mode": markdown_mode,
                },
                pipeline_create_params.PipelineCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineResponseModel,
        )

    def retrieve(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineResult:
        """
        Retrieves the results of a pipeline processing job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._get(
            f"/pipelines/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineResult,
        )


class AsyncPipelinesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPipelinesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/velocitybolt/marly-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPipelinesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPipelinesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/velocitybolt/marly-python#with_streaming_response
        """
        return AsyncPipelinesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        api_key: str,
        provider_model_name: str,
        provider_type: str,
        workloads: Iterable[pipeline_create_params.Workload],
        additional_params: Dict[str, object] | NotGiven = NOT_GIVEN,
        markdown_mode: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineResponseModel:
        """
        Initiates a pipeline processing job for the given PDF and schemas.

        Args:
          api_key: API key for the AI provider

          provider_model_name: Name of the AI model to use

          provider_type: Type of AI provider (e.g., 'azure', 'openai')

          workloads: Array of workload objects containing PDF content and schemas

          additional_params: Additional parameters specific to the AI provider

          markdown_mode: Flag to enable markdown mode

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/pipelines",
            body=await async_maybe_transform(
                {
                    "api_key": api_key,
                    "provider_model_name": provider_model_name,
                    "provider_type": provider_type,
                    "workloads": workloads,
                    "additional_params": additional_params,
                    "markdown_mode": markdown_mode,
                },
                pipeline_create_params.PipelineCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineResponseModel,
        )

    async def retrieve(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PipelineResult:
        """
        Retrieves the results of a pipeline processing job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._get(
            f"/pipelines/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PipelineResult,
        )


class PipelinesResourceWithRawResponse:
    def __init__(self, pipelines: PipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = to_raw_response_wrapper(
            pipelines.create,
        )
        self.retrieve = to_raw_response_wrapper(
            pipelines.retrieve,
        )


class AsyncPipelinesResourceWithRawResponse:
    def __init__(self, pipelines: AsyncPipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = async_to_raw_response_wrapper(
            pipelines.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            pipelines.retrieve,
        )


class PipelinesResourceWithStreamingResponse:
    def __init__(self, pipelines: PipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = to_streamed_response_wrapper(
            pipelines.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            pipelines.retrieve,
        )


class AsyncPipelinesResourceWithStreamingResponse:
    def __init__(self, pipelines: AsyncPipelinesResource) -> None:
        self._pipelines = pipelines

        self.create = async_to_streamed_response_wrapper(
            pipelines.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            pipelines.retrieve,
        )
