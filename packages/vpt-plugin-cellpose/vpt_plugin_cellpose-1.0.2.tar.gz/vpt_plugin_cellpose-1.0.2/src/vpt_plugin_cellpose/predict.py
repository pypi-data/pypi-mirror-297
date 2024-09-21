import warnings

import numpy as np
from cellpose import models

from vpt_core.io.image import ImageSet
from vpt_plugin_cellpose import CellposeSegProperties, CellposeSegParameters


def run(images: ImageSet, properties: CellposeSegProperties, parameters: CellposeSegParameters) -> np.ndarray:
    warnings.filterwarnings("ignore", message=".*the `scipy.ndimage.filters` namespace is deprecated.*")

    is_valid_channels = parameters.nuclear_channel and parameters.entity_fill_channel
    image = (
        images.as_stack([parameters.nuclear_channel, parameters.entity_fill_channel])
        if is_valid_channels
        else images.as_stack()
    )

    empty_z_levels = set()
    for z_i, z_plane in enumerate(image):
        for channel_i in range(z_plane.shape[-1]):
            if z_plane[..., channel_i].std() < 0.1:
                empty_z_levels.add(z_i)
    if len(empty_z_levels) == image.shape[0]:
        return np.zeros((image.shape[0],) + image.shape[1:-1])

    if properties.custom_weights:
        model = models.CellposeModel(gpu=False, pretrained_model=properties.custom_weights, net_avg=False)
    else:
        model = models.Cellpose(gpu=False, model_type=properties.model, net_avg=False)

    to_segment_z = list(set(range(image.shape[0])).difference(empty_z_levels))
    mask = model.eval(
        image[to_segment_z, ...],
        z_axis=0,
        channel_axis=len(image.shape) - 1,
        diameter=parameters.diameter,
        flow_threshold=parameters.flow_threshold,
        mask_threshold=parameters.mask_threshold,
        resample=False,
        min_size=parameters.minimum_mask_size,
        tile=True,
        do_3D=(properties.model_dimensions == "3D"),
    )[0]
    mask = mask.reshape((len(to_segment_z),) + image.shape[1:-1])
    for i in empty_z_levels:
        mask = np.insert(mask, i, np.zeros(image.shape[1:-1]), axis=0)
    return mask
