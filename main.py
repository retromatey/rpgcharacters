import subprocess


def define_env(env):
    @env.macro
    def run(command: str) -> str:
        """Run a shell command and return its output."""
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
