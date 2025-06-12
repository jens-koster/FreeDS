from typing import Any, Callable, Dict, List, Optional, Union


class CheckResult:
    """
    Class to hold the result of a check.
    """

    def __init__(self, passed: bool, message: str) -> None:
        self.passed = passed
        self.message = message

    @property
    def symbol(self) -> str:
        return "✅" if self.passed else "❌"

    def __str__(self) -> str:
        return f"{self.symbol} - {self.message}"

    def __repr__(self) -> str:
        return f"{self.symbol} CheckResult(passed={self.passed}, message={self.message})"


class Check:
    """
    Base class for checks.
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        method: Union[Callable[[], List[CheckResult]], Callable[[], CheckResult]],
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.method = method
        self.results: List[CheckResult] = []
        self.executed = False

    def execute(self) -> None:
        """
        Execute the check and store the results.
        :return: None
        """
        try:
            print(f"Executing check: {self.name}")
            results = self.method()
            if isinstance(results, List):
                self.results = results
            else:
                self.results = [results]
        except Exception as e:
            self.results = [ExceptionCheckResult(f"Check '{self.name}' raised an exception.", e)]
        finally:
            self.executed = True

    @property
    def passed(self) -> bool:
        """
        Check if all results passed.
        :return: True if all results passed, False otherwise.
        """
        if not self.executed:
            raise RuntimeError("Check has not been executed yet. Call execute() first.")
        return all(result.passed for result in self.results)

    @property
    def symbol(self) -> str:
        """
        Get the symbol representing the check result.
        :return: "✔" if passed, "✘" if failed.
        """
        if len(self.results) == 1:
            return self.results[0].symbol
        return "✅" if self.passed else "❌"

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class PluginCheckResult(CheckResult):
    """
    The result of a check on a plugin.
    """

    def __init__(self, passed: bool, message: str, plugin_name: str) -> None:
        super().__init__(passed, message)
        self.plugin_name = plugin_name

    def __str__(self) -> str:
        return f"{self.symbol} {self.plugin_name}: {self.message}"


class NotebookCheckResult(CheckResult):
    """
    The result of a notebook based check.
    """

    def __init__(self, passed: bool, message: str, result_data: Dict[str, Any]) -> None:
        super().__init__(passed, message)
        self.area = result_data.get("area")
        self.description = result_data.get("description")
        self.plugin_name = result_data.get("plugin")
        self.result_data = result_data

    def __str__(self) -> str:
        return f"{self.symbol} {self.area} {self.plugin_name if self.plugin_name else ''} {self.description}: {self.message}"


class AllGoodCheckResult(CheckResult):
    """
    Placeholder result for a check where no problems were found and thus would have no results.
    """

    def __init__(self, message: str) -> None:
        super().__init__(True, "All good, " + message)


class ExceptionCheckResult(CheckResult):
    """
    Result for a check that raised an exception.
    """

    def __init__(self, message: str, exception: Exception) -> None:
        super().__init__(False, message)
        self.exception = exception

    @property
    def symbol(self) -> str:
        return "❗️"

    def __str__(self) -> str:
        return f"{self.symbol} Exception: {self.message} - {str(self.exception)}"

    def __repr__(self) -> str:
        return f"ExceptionCheckResult(passed={self.passed}, message={self.message}, exception={str(self.exception)})"


class MisconfiguredCheckResult(PluginCheckResult):
    """
    Result for a check that has a bug in config or return values.
    """

    def __init__(self, message: str, plugin_name: Optional[str] = None) -> None:
        super().__init__(True, "Config Error: " + message, plugin_name=plugin_name or "Unknown Plugin")

    @property
    def symbol(self) -> str:
        return "❗️"


class CheckList:
    """
    Class to hold a list of checks.
    """

    def __init__(self, area: str) -> None:
        self.area = area
        self.checks: List[Check] = []

    def add(
        self, name: str, description: str, method: Union[Callable[[], List[CheckResult]], Callable[[], CheckResult]]
    ) -> None:
        """
        Add a check to the list.
        """
        self.checks.append(
            Check(
                id=self.area + "__" + name.lower().replace(" ", "_"), name=name, description=description, method=method
            )
        )

    def execute(self) -> None:
        """
        Execute all checks in the list.
        :return: List[CheckResult]
        """
        for check in self.checks:
            check.execute()

    @property
    def results(self) -> List[CheckResult]:
        """
        Get the results of all checks in the list.
        :return: List[CheckResult]
        """
        return [result for check in self.checks for result in check.results]
