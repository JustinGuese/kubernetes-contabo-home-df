from platform import node, platform

from prefect import flow, get_run_logger
from prefect.infrastructure.kubernetes import KubernetesJob

kubernetes_job_block = KubernetesJob.load("testjob")

@flow
def check():
    logger = get_run_logger()
    logger.info(f"Network: {node()}. ✅")
    logger.info(f"Instance: {platform()}. ✅")

if __name__ == "__main__":
    check()