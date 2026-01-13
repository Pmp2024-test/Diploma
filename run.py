import sys
import subprocess
import argparse


def run_tests(mode="all", html=False, allure=False):
    """Запуск тестов"""

    pytest_args = [
        "pytest",
        "-v",
        "--strict-markers",
        "--tb=short",
        "--color=yes"
    ]

    # Выбираем тесты
    if mode == "ui":
        pytest_args.extend(["-m", "ui"])
    elif mode == "api":
        pytest_args.extend(["-m", "api"])
    elif mode == "all":
        pass

    # HTML отчет
    if html:
        pytest_args.extend([
            f"--html=reports/report.html",
            "--self-contained-html"
        ])

    # Allure отчет
    if allure:
        pytest_args.extend([
            f"--alluredir={config.config.REPORTS_DIR}/allure-results"
        ])

    print(f"Запуск тестов в режиме: {mode}")
    print(f"Команда: {' '.join(pytest_args)}")

    return subprocess.call(pytest_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=["ui", "api", "all"], default="all")
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--allure", action="store_true")

    args = parser.parse_args()
    sys.exit(run_tests(args.mode, args.html, args.allure))