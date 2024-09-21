from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional, Union

import torch
from transformers import AutoImageProcessor, AutoModel

from ralfpt.typehints import PilImage


@dataclass
class SaliencyTester(object):
    model_name: str

    _device: Optional[Union[str, torch.device]] = None
    _model: Optional[AutoModel] = None
    _processor: Optional[AutoImageProcessor] = None

    def __post_init__(self) -> None:
        self._device = self._device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self._model = self.load_model(model_name=self.model_name)
        self._processor = self.load_processor(model_name=self.model_name)

    @property
    def device(self) -> Union[str, torch.device]:
        assert self._device is not None
        return self._device

    @property
    def model(self) -> AutoModel:
        assert self._model is not None
        return self._model

    @property
    def processor(self) -> AutoImageProcessor:
        assert self._processor is not None
        return self._processor

    def load_model(
        self,
        model_name: str,
        trust_remote_code: bool = True,
    ) -> AutoModel:
        model = AutoModel.from_pretrained(
            model_name, trust_remote_code=trust_remote_code
        )
        model = model.to(self.device)
        return model

    def load_processor(
        self, model_name: str, trust_remote_code: bool = True
    ) -> AutoImageProcessor:
        processor = AutoImageProcessor.from_pretrained(
            model_name, trust_remote_code=trust_remote_code
        )
        return processor

    @torch.no_grad()
    def __call__(self, image: PilImage) -> PilImage:
        width, height = image.size

        inputs = self.processor(image, return_tensors="pt")  # type: ignore
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outptus = self.model(**inputs)  # type: ignore
        prediction = outptus[0][0]

        return self.processor.postprocess(prediction, width=width, height=height)  # type: ignore


@lru_cache
def get_cached_saliency_tester(model_name: str) -> SaliencyTester:
    return SaliencyTester(model_name=model_name)


def apply_saliency_detection(
    image: PilImage,
    saliency_testers: List[Union[str, SaliencyTester]],
) -> List[PilImage]:
    image = image.convert("RGB") if image.mode != "RGB" else image

    saliency_maps = []
    for saliency_tester in saliency_testers:
        if isinstance(saliency_tester, str):
            saliency_tester = get_cached_saliency_tester(model_name=saliency_tester)

        saliency_map = saliency_tester(image)
        saliency_map = saliency_map.convert("L")
        saliency_maps.append(saliency_map)

    return saliency_maps
