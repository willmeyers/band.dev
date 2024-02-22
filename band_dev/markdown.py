import yaml
import markdown as md

from django.conf import settings
from pydantic import BaseModel


markdown = md.Markdown(extensions=["full_yaml_metadata"], extension_configs={
        "full_yaml_metadata": {
            "yaml_loader": yaml.SafeLoader,
        },
    },
)
