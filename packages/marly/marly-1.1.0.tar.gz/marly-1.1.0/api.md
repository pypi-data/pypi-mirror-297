# Pipelines

Types:

```python
from marly.types import PipelineResponseModel, PipelineResult
```

Methods:

- <code title="post /pipelines">client.pipelines.<a href="./src/marly/resources/pipelines.py">create</a>(\*\*<a href="src/marly/types/pipeline_create_params.py">params</a>) -> <a href="./src/marly/types/pipeline_response_model.py">PipelineResponseModel</a></code>
- <code title="get /pipelines/{task_id}">client.pipelines.<a href="./src/marly/resources/pipelines.py">retrieve</a>(task_id) -> <a href="./src/marly/types/pipeline_result.py">PipelineResult</a></code>
