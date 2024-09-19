# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# NOTE - build a package and uploaded to PyPi
# https://cloud.google.com/composer/docs/composer-2/troubleshooting-triggerer#trigger_class_not_found

import asyncio
from typing import Any, AsyncIterator
from airflow.triggers.base import BaseTrigger, TriggerEvent

from ray.job_submission import JobSubmissionClient, JobStatus

class RayJobTrigger(BaseTrigger):

    def __init__(
        self,
        cluster_resource_name: str,
        ray_address: str,
        job_id: str,
        poke_interval: float = 2.0
    ):
        super().__init__()
        self.cluster_resource_name = cluster_resource_name
        self.ray_address = ray_address
        self.job_id = job_id
        self.poke_interval = poke_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:

        return (
            "vertexai_ray_job_af_trigger.ray_job_trigger.RayJobTrigger", 
            {
                "cluster_resource_name": self.cluster_resource_name,
                "ray_address": self.ray_address,
                "job_id": self.job_id,
                "poke_interval": self.poke_interval,
            },
        )

    # The run method is an async generator that yields TriggerEvents when the desired condition is met
    async def run(self) -> AsyncIterator[TriggerEvent]:
        client = JobSubmissionClient(self.ray_address)
        while True:
            if not client.get_job_status(self.job_id) in (JobStatus.PENDING, JobStatus.RUNNING):
                yield TriggerEvent({"ray_address": self.ray_address, "job_id": self.job_id})
            await asyncio.sleep(self.poke_interval)
        