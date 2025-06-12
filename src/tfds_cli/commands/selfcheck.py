from typing import List

import typer

from tfds_cli.selfcheck import (
    directory_checks,
    docker_checks,
    network_checks,
    notebook_checks,
    s3_checks,
)
from tfds_cli.selfcheck.check_classes import (
    CheckList,
    CheckResult,
    ExceptionCheckResult,
)


def selfcheck() -> int:
    """
    Perform all self checks.
    """
    checklists: List[CheckList] = [
        docker_checks.checks(),
        directory_checks.checks(),
        network_checks.checks(),
        s3_checks.checks(),
    ]

    results: List[CheckResult] = []
    for checklist in checklists:
        try:
            checklist.execute()
            results.extend(checklist.results)
        except Exception as e:
            results.append(ExceptionCheckResult(message="A checklist execution raised an exception.", exception=e))

    results.extend(notebook_checks.check_results())
    for result in results:
        typer.echo(result)
    return 0


selfcheck()
