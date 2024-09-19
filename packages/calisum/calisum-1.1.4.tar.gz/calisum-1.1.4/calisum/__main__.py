""" calisum.__main__: executed when calisum directory is called as script. """
import asyncio
from calisum.cli import main as run_cli

def main():
    asyncio.run(run_cli())

if __name__ == "__main__":
   main()