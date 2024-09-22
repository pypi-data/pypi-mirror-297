import asyncio
import logging
from typing import Type, Optional
from graphlit import Graphlit
from graphlit_api import exceptions, enums, input_types
from langchain_core.tools import BaseTool, ToolException
from pydantic import Field, BaseModel

logger = logging.getLogger(__name__)

class IngestInput(BaseModel):
    uri: str = Field(description="URI of web page or cloud-hosted file to be ingested into knowledge base")

class IngestTool(BaseTool):
    name = "Ingest"
    description = """Ingests content from URI. Returns Markdown extracted from content.
    Can ingest individual web pages, PDFs, audio recordings, images, and other unstructured data."""
    args_schema: Type[BaseModel] = IngestInput

    graphlit: Graphlit = Field(None, exclude=True)

    workflow_id: Optional[str] = Field(None, exclude=True)
    correlation_id: Optional[str] = Field(None, exclude=True)

    def __init__(self, graphlit: Optional[Graphlit] = None, workflow_id: Optional[str] = None, correlation_id: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.graphlit = graphlit or Graphlit()
        self.workflow_id = workflow_id
        self.correlation_id = correlation_id

    async def _arun(self, uri: str) -> Optional[str]:
        try:
            response = await self.graphlit.client.ingest_uri(
                uri=uri,
                workflow=input_types.EntityReferenceInput(id=self.workflow_id) if self.workflow_id is not None else None,
                is_synchronous=True,
                correlation_id=self.correlation_id
            )

            content_id = response.ingest_uri.id if response.ingest_uri is not None else None

            if content_id is not None:
                response = await self.graphlit.client.get_content(content_id)

                return response.content.markdown if response.content is not None else None
            else:
                return None
        except exceptions.GraphQLClientError as e:
            logger.error(str(e))
            raise ToolException(str(e)) from e

    def _run(self, uri: str) -> Optional[str]:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                future = asyncio.ensure_future(self._arun(uri))
                return loop.run_until_complete(future)
            else:
                return loop.run_until_complete(self._arun(uri))
        except RuntimeError:
            return asyncio.run(self._arun(uri))
