"""
    This script implements the Iteration of Thought (IoT) and Generative Iteration of Thought (GIoT) models.
"""

import os
import signal
from typing import Optional
import asyncio
from loguru import logger
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown
from litellm import completion
import requests  # Added for handling URL requests

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"  # Updated to a more recent model
RATE_LIMIT_WAIT_TIME = 10
GLOBAL_TIMEOUT = 300
DOWNLOAD_TIMEOUT = 10

if not API_KEY:
    raise ValueError("OpenAI API key must be set as an environment variable.")

console = Console()


class IterationOfThought:
    """
    Class for performing Iteration of Thought (IoT) and Generative Iteration of Thought (GIoT).
    """

    def __init__(
        self,
        model: str = MODEL,
        max_iterations: int = 5,
        timeout: int = 30,
        temperature: float = 0.5,  # Added temperature parameter
        stream: bool = False,  # Added stream parameter
    ):
        """
        Initialize the IterationOfThought class.

        Args:
            model (str): The model to use for the LLM.
            max_iterations (int): The maximum number of iterations to perform.
            timeout (int): The timeout for each iteration in seconds.
            temperature (float): Sampling temperature for the API response.
            stream (bool): Whether to stream the response.
        """
        self.model = model
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.temperature = temperature
        self.stream = stream  # Store the stream parameter

    async def _call_llm(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_retries: int = 3,
        stream: Optional[bool] = None,
    ) -> str:
        """
        Call the OpenAI API with the given prompt and return the response.

        Args:
            prompt (str): The prompt to send to the API.
            temperature (float): Sampling temperature for the API response.
            max_retries (int): Number of retries in case of failure.
            stream (bool): Whether to stream the response.

        Returns:
            str: The content of the API response.
        """
        # Use the instance's stream if not provided
        stream = stream if stream is not None else self.stream
        for _ in range(max_retries):
            try:
                console.print(f"[bold green]Calling {self.model} API...[/bold green]")
                response = completion(
                    model=self.model,
                    temperature=temperature or self.temperature,
                    messages=[{"role": "user", "content": prompt}],
                    stream=stream,
                )

                if stream:
                    # Handle streaming response
                    full_response = ""
                    console.print(
                        "[bold green]Streaming response...[/bold green]"
                    )  # Indicate streaming
                    async for chunk in response:
                        # Check if the chunk has the expected structure
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            content = chunk["choices"][0]["delta"].get("content", "")
                            if content:  # Only print if content is not empty
                                full_response += content
                                console.print(
                                    content, end=""
                                )  # Ensure immediate output
                    return full_response.strip()
                else:
                    return response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                console.print(f"[red]Error: {e}")
                return ""
        console.print("[red]Failed to get a response from OpenAI API after max retries")
        return ""

    async def inner_dialogue_agent(self, query: str, previous_response: str) -> str:
        """
        Generate a new prompt based on the original query and previous response.

        Args:
            query (str): The original user query.
            previous_response (str): The previous response from the LLM.

        Returns:
            str: The generated prompt for the next iteration.
        """
        prompt = (
            f"Given the original query: '{query}' and the previous response: '{previous_response}', "
            "generate an instructive and context-specific prompt to refine and improve the answer. "
            "Ensure that the new prompt encourages deeper reasoning or addresses any gaps in the previous response."
        )
        return await self._call_llm(prompt)

    async def llm_agent(self, query: str, prompt: str, stream: bool = False) -> str:
        """
        Call the LLM agent with the given query and prompt.

        Args:
            query (str): The user query.
            prompt (str): The prompt to refine the response.
            stream (bool): Whether to stream the response.

        Returns:
            str: The response from the LLM agent.
        """
        full_prompt = f"Query: {query}\nPrompt: {prompt}\nResponse:"
        return await self._call_llm(full_prompt, stream=stream)  # Pass stream argument

    def stopping_criterion(self, response: str) -> bool:
        """
        Determine if the stopping criterion has been met based on the response.

        Args:
            response (str): The response from the LLM.

        Returns:
            bool: True if the stopping criterion is met, False otherwise.
        """
        lower_response = response.lower()
        return any(
            keyword in lower_response
            for keyword in [
                "answer:",
                "final answer:",
                "conclusion:",
                "summary:",
                "the answer is:",
            ]
        )

    async def aiot(self, query: str, stream: bool = False) -> str:
        """
        Execute the AIoT process for the given query.

        Args:
            query (str): The user query to process.
            stream (bool): Whether to stream the response.

        Returns:
            str: The final response after iterations.
        """
        console.print("\n[bold cyan]Starting AIoT...[/bold cyan]")
        current_response = await self.llm_agent(
            query, "Initial Prompt", stream
        )  # Pass stream argument

        for iteration in range(1, self.max_iterations + 1):
            console.print(f"\n[bold]Iteration {iteration}:[/bold]")
            console.print(Panel(current_response, title="LLMA Response", expand=False))

            if self.stopping_criterion(current_response):
                console.print("[green]Stopping criterion met.[/green]")
                break

            new_prompt = await self.inner_dialogue_agent(query, current_response)
            console.print(Panel(new_prompt, title="IDA Generated Prompt", expand=False))
            current_response = await self.llm_agent(
                query, new_prompt, stream
            )  # Pass stream argument
            await asyncio.sleep(self.timeout)

        console.print("[bold cyan]AIoT completed.[/bold cyan]\n")
        return current_response

    async def giot(
        self, query: str, fixed_iterations: int, stream: bool = False
    ) -> str:
        """
        Execute the GIoT process for the given query with a fixed number of iterations.

        Args:
            query (str): The user query to process.
            fixed_iterations (int): The number of iterations to perform.
            stream (bool): Whether to stream the response.

        Returns:
            str: The final response after iterations.
        """
        console.print("\n[bold magenta]Starting GIoT...[/bold magenta]")
        current_response = await self.llm_agent(
            query, "Initial Prompt", stream
        )  # Pass stream argument

        for iteration in range(1, fixed_iterations + 1):
            console.print(f"\n[bold]Iteration {iteration}:[/bold]")
            console.print(Panel(current_response, title="LLMA Response", expand=False))

            new_prompt = await self.inner_dialogue_agent(query, current_response)
            console.print(Panel(new_prompt, title="IDA Generated Prompt", expand=False))
            current_response = await self.llm_agent(
                query, new_prompt, stream
            )  # Pass stream argument
            await asyncio.sleep(self.timeout)

        console.print("[bold magenta]GIoT completed.[/bold magenta]\n")
        return current_response


def get_user_query() -> str:
    """
    Get the user query from the console input.

    Returns:
        str: The user query.
    """
    sample_query = (
        "A textile dye containing an extensively conjugated pi-electrons emits light with energy of 2.3393 eV. "
        "What color of light is absorbed by the organic compound? Pick an answer from the following options:\n"
        "A. Red\nB. Yellow\nC. Blue\nD. Violet"
    )

    console.print(
        Panel.fit("Enter your query (or press Enter to use the sample query):")
    )
    user_input = Prompt.ask("Query", default=sample_query, show_default=True)

    if not user_input.strip():
        console.print("[yellow]No input provided. Using sample query.[/yellow]")
        return sample_query

    return user_input


def timeout_handler(signum, frame):
    """
    Handle the timeout signal.

    Args:
        signum (int): The signal number.
        frame (FrameInfo): The frame information.
    """
    raise TimeoutError("Process took too long")


def interrupt_handler(signum, frame):
    """
    Handle the interrupt signal.

    Args:
        signum (int): The signal number.
        frame (FrameInfo): The frame information.
    """
    raise KeyboardInterrupt("User interrupted the process")


async def stream_response(
    iot: IterationOfThought, query: str, method: str, stream: bool
) -> str:
    """
    Asynchronously run the specified IoT method (AIoT or GIoT) and return the result.
    """
    if stream:
        return (
            await iot.aiot(query, stream)
            if method == "AIoT"
            else await iot.giot(query, 3, stream)
        )
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(f"Running {method}...", total=None)
            result = (
                await iot.aiot(query, stream)
                if method == "AIoT"
                else await iot.giot(query, 3, stream)
            )
            progress.update(task, completed=True)
        return result


async def run_iot(
    iot: IterationOfThought, query: str, method: str, stream: bool = False
) -> str:
    """
    Run the specified IoT method (AIoT or GIoT) and return the result.
    """
    return await stream_response(iot, query, method, stream)


def display_results(aiot_result: Optional[str], giot_result: Optional[str]):
    """
    Display the results of the IoT methods.

    Args:
        aiot_result (Optional[str]): The result of the AIoT method.
        giot_result (Optional[str]): The result of the GIoT method.
    """
    table = Table(title="Results Comparison")
    table.add_column("Method", style="cyan", no_wrap=True)
    table.add_column("Response", style="magenta")

    if aiot_result:
        table.add_row("AIoT", aiot_result)
    if giot_result:
        table.add_row("GIoT", giot_result)

    console.print(table)


@click.command()
def main_sync(
    method: str,
    verbose: bool,
    model: str,
    temperature: float,
    query: Optional[str] = None,
    file: Optional[str] = None,
    output: Optional[str] = None,
    stream: bool = False,
) -> None:
    """
    Synchronous entry point for the IoT application.
    """
    asyncio.run(
        run_main(
            method=method,
            verbose=verbose,
            model=model,
            temperature=temperature,
            query=query,
            file=file,
            output=output,
            stream=stream,
        )
    )


async def run_main(
    method: str,
    verbose: bool,
    model: str,
    temperature: float,
    query: Optional[str],
    file: Optional[str],
    output: Optional[str],
    stream: bool,
) -> None:
    """
    Asynchronous main logic for the IoT application.

    Args:
        method (str): The method to run (AIoT, GIoT, or both).
        verbose (bool): Flag to enable verbose output.
        model (str): The model to use.
        temperature (float): Sampling temperature for the LLM response.
        query (Optional[str]): User query to process.
        file (Optional[str]): File path or URL to read the query from.
        output (Optional[str]): File path to save the response.
        stream (bool): Whether to stream the response.
    """
    if verbose:
        logger.add("debug.log", level="DEBUG")
    else:
        logger.remove()
        logger.add(lambda _: None)

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.signal(signal.SIGINT, interrupt_handler)

    iot = IterationOfThought(
        model=model, max_iterations=5, timeout=2, temperature=temperature, stream=stream
    )
    console.print(
        f"[bold cyan]Using model: {model} with temperature: {temperature}[/bold cyan]"
    )
    console.print("[bold green]Streaming mode is enabled.[/bold green]")

    if file:
        if file.startswith("http://") or file.startswith("https://"):
            response = requests.get(file, timeout=DOWNLOAD_TIMEOUT)
            file_content = response.text.strip()
        else:
            with open(file, "r", encoding="utf-8") as f:
                file_content = f.read().strip()

        if query:
            query = f"{file_content}\n ----------- \n {query}"
        else:
            query = file_content

    query = query or get_user_query()
    console.print(
        Panel(Markdown(f"**Query:** {query}"), title="Input Query", expand=False)
    )

    try:
        signal.alarm(GLOBAL_TIMEOUT)

        aiot_result = None
        giot_result = None

        if method in ["AIoT", "both"]:
            aiot_result = await run_iot(iot, query, "AIoT", stream)

        if method in ["GIoT", "both"]:
            giot_result = await run_iot(iot, query, "GIoT", stream)

        display_results(aiot_result, giot_result)

        signal.alarm(0)
    except TimeoutError:
        console.print("⚠️ [bold red]Process timed out. Please try again.[/bold red]")
    except KeyboardInterrupt:
        console.print("✋ [bold yellow]Process interrupted by user.[/bold yellow]")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        console.print(f"❌ [bold red]An unexpected error occurred: {e}[/bold red]")

    if output and os.path.exists(output):
        overwrite = Prompt.ask("Output file exists. Overwrite? (y/n)", default="n")
        if overwrite.lower() != "y":
            console.print("[yellow]Output file not overwritten.[/yellow]")
            output = None

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(aiot_result or giot_result)


if __name__ == "__main__":
    """
    Main entry point for the IoT application.
    """
    main_sync()


