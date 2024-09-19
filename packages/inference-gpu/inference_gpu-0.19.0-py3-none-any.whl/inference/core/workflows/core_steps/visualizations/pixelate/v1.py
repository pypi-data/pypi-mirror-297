from typing import Literal, Optional, Type, Union

import supervision as sv
from pydantic import ConfigDict, Field

from inference.core.workflows.core_steps.visualizations.common.base import (
    OUTPUT_IMAGE_KEY,
    VisualizationBlock,
    VisualizationManifest,
)
from inference.core.workflows.execution_engine.entities.base import WorkflowImageData
from inference.core.workflows.execution_engine.entities.types import (
    INTEGER_KIND,
    WorkflowParameterSelector,
)
from inference.core.workflows.prototypes.block import BlockResult, WorkflowBlockManifest

TYPE: str = "roboflow_core/pixelate_visualization@v1"
SHORT_DESCRIPTION = "Pixelates detected objects in an image."
LONG_DESCRIPTION = """
The `PixelateVisualization` block pixelates detected
objects in an image using Supervision's `sv.PixelateAnnotator`.
"""


class PixelateManifest(VisualizationManifest):
    type: Literal[f"{TYPE}", "PixelateVisualization"]
    model_config = ConfigDict(
        json_schema_extra={
            "name": "Pixelate Visualization",
            "version": "v1",
            "short_description": SHORT_DESCRIPTION,
            "long_description": LONG_DESCRIPTION,
            "license": "Apache-2.0",
            "block_type": "visualization",
        }
    )

    pixel_size: Union[int, WorkflowParameterSelector(kind=[INTEGER_KIND])] = Field(  # type: ignore
        description="Size of the pixelation.",
        default=20,
        examples=[20, "$inputs.pixel_size"],
    )

    @classmethod
    def get_execution_engine_compatibility(cls) -> Optional[str]:
        return ">=1.0.0,<2.0.0"


class PixelateVisualizationBlockV1(VisualizationBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.annotatorCache = {}

    @classmethod
    def get_manifest(cls) -> Type[WorkflowBlockManifest]:
        return PixelateManifest

    def getAnnotator(
        self,
        pixel_size: int,
    ) -> sv.annotators.base.BaseAnnotator:
        key = "_".join(map(str, [pixel_size]))

        if key not in self.annotatorCache:
            self.annotatorCache[key] = sv.PixelateAnnotator(pixel_size=pixel_size)
        return self.annotatorCache[key]

    def run(
        self,
        image: WorkflowImageData,
        predictions: sv.Detections,
        copy_image: bool,
        pixel_size: Optional[int],
    ) -> BlockResult:
        annotator = self.getAnnotator(
            pixel_size,
        )

        annotated_image = annotator.annotate(
            scene=image.numpy_image.copy() if copy_image else image.numpy_image,
            detections=predictions,
        )

        output = WorkflowImageData(
            parent_metadata=image.parent_metadata,
            workflow_root_ancestor_metadata=image.workflow_root_ancestor_metadata,
            numpy_image=annotated_image,
        )

        return {OUTPUT_IMAGE_KEY: output}
