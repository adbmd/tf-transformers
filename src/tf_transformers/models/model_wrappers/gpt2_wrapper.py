import tensorflow as tf
from absl import logging

from tf_transformers.models import GPT2Encoder
from tf_transformers.utils import get_config, validate_model_name

logging.set_verbosity("INFO")
allowed_model_names = ["gpt2", "gpt2_medium"]


def modelWrapper(model_name, **kwargs):
    """Wrapper for Model

    Args:
        model_name ([type]): [description]

    Returns:
        [type]: [description]
    """

    name = "gpt2"

    model_name = model_name.replace("-", "_")  # replace - with _
    validate_model_name(model_name, allowed_model_names)
    config = get_config("tf_transformers.models.model_configs.gpt2", model_name)

    for _kwarg in kwargs:
        if _kwarg in config:
            config["_kwarg"] = kwargs[_kwarg]
            logging.info("Overwride {} with {}".format(_kwarg, kwargs[_kwarg]))

    if "is_training" not in kwargs:
        kwargs["is_training"] = False
        kwargs["pipeline_mode"] = None

    if "mask_mode" not in kwargs:
        # default for gpt2
        kwargs["mask_mode"] = config["mask_mode"]

    checkpoint_dir = None
    if "checkpoint_dir" in kwargs:
        checkpoint_dir = kwargs["checkpoint_dir"]
        kwargs["checkpoint_dir"]
    kwargs["name"] = name
    tf.keras.backend.clear_session()
    model_layer = GPT2Encoder(config, **kwargs)
    model = model_layer.get_model()
    if checkpoint_dir:
        model.load_checkpoint(checkpoint_dir)
    return model_layer, model, config
