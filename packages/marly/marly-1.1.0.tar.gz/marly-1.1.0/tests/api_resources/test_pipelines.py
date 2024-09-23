# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from marly import Marly, AsyncMarly
from marly.types import PipelineResult, PipelineResponseModel
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPipelines:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Marly) -> None:
        pipeline = client.pipelines.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        )
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Marly) -> None:
        pipeline = client.pipelines.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
            additional_params={"foo": "bar"},
            markdown_mode=True,
        )
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Marly) -> None:
        response = client.pipelines.with_raw_response.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Marly) -> None:
        with client.pipelines.with_streaming_response.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Marly) -> None:
        pipeline = client.pipelines.retrieve(
            "task_id",
        )
        assert_matches_type(PipelineResult, pipeline, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Marly) -> None:
        response = client.pipelines.with_raw_response.retrieve(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineResult, pipeline, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Marly) -> None:
        with client.pipelines.with_streaming_response.retrieve(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineResult, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Marly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.pipelines.with_raw_response.retrieve(
                "",
            )


class TestAsyncPipelines:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.pipelines.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        )
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.pipelines.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
            additional_params={"foo": "bar"},
            markdown_mode=True,
        )
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMarly) -> None:
        response = await async_client.pipelines.with_raw_response.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMarly) -> None:
        async with async_client.pipelines.with_streaming_response.create(
            api_key="api_key",
            provider_model_name="provider_model_name",
            provider_type="provider_type",
            workloads=[
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
                {
                    "pdf_stream": "pdf_stream",
                    "schemas": ["string", "string", "string"],
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineResponseModel, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMarly) -> None:
        pipeline = await async_client.pipelines.retrieve(
            "task_id",
        )
        assert_matches_type(PipelineResult, pipeline, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMarly) -> None:
        response = await async_client.pipelines.with_raw_response.retrieve(
            "task_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineResult, pipeline, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMarly) -> None:
        async with async_client.pipelines.with_streaming_response.retrieve(
            "task_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineResult, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMarly) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.pipelines.with_raw_response.retrieve(
                "",
            )
