import requests
from ..utils import (
    no_results_found,
    failed_to_run,
)


def kickbox_disposible_email(indicator):
    try:
        response = requests.get(
            f"https://open.kickbox.com/v1/disposable/{indicator.indicator}",
        )

        if response.status_code != 200:
            return failed_to_run(
                tool_name="kickbox_disposible_email",
                status_code=response.status_code,
                reason=response.reason,
            )

        if not response.json().get("disposable"):
            return no_results_found("kickbox_disposible_email")

        return (
            # fmt: off
                {
                    "tool": "kickbox_disposible_email",
                    "outcome": {"status": "results_found", "error_message": None, "status_code": response.status_code, "reason": response.reason},
                    "results": response.json().get("disposable", {})
                },
            # fmt: on
        )
    except Exception as error_message:
        return failed_to_run(
            tool_name="kickbox_disposible_email", error_message=error_message
        )