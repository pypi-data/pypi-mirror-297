from openai import OpenAI
import os
import anthropic
import re


ANTHROPIC_MODEL_NAME = "claude-3-opus-20240229"


class OpenaiAdapter:
    """Openai Adapter"""
    def __init__(self):
        # it will access the API key from os.environ
        self.client = OpenAI()

    def chat(self, messages, temperature=1):
        # Ensure messages is a list of message dictionaries
        formatted_messages = [
            {"role": "system", "content": message} if isinstance(message, str) else message
            for message in messages
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=formatted_messages,
            temperature=temperature,
        )
        return completion.choices[0].message


class AnthropicAdapter:
    """Anthropic Adapter"""
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.grader = Grader()

    def create(self, text):
        message = self.client.messages.create(
            model=ANTHROPIC_MODEL_NAME,
            max_tokens=1000,
            temperature=0.0,
            system="You are a useful assistant.",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return message.content[0].text

    def grade_completion(self, output, golden_answer):
        messages = self.grader.build_grader_prompt(output, golden_answer)
        completion = self.create(messages)
        # Extract just the label from the completion (we don't care about the thinking)
        pattern = r'<correctness>(.*?)</correctness>'
        match = re.search(pattern, completion, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Did not find <correctness></correctness> tags.")


class Grader:
    """Model-based Grading"""
    def __init__(self):
        pass

    def build_grader_prompt(self, answer, rubric):
        """We start by defining a "grader prompt" template."""
        user_content = f"""You will be provided an answer that an assistant gave to a question, and a rubric that instructs you on what makes the answer correct or incorrect.
        
        Here is the answer that the assistant gave to the question.
        <answer>{answer}</answer>
        
        Here is the rubric on what makes the answer correct or incorrect.
        <rubric>{rubric}</rubric>
        
        An answer is correct if it entirely meets the rubric criteria, and is otherwise incorrect. =
        First, think through whether the answer is correct or incorrect based on the rubric inside <thinking></thinking> tags. """
        f"""Then, output either 'correct' if the answer is correct or 'incorrect' if the answer is incorrect inside <correctness></correctness> tags."""

        messages = [{'role': 'user', 'content': user_content}]
        return messages

    def evaluate(self, prompt, completion):
        pass


class TaskOrchestrator:
    """
    The TaskOrchestrator class encapsulates the logic for orchestrating tasks, executing sub-tasks, and refining results.
    It leverages OpenAI for generating task breakdowns and executing sub-tasks, and Anthropic for refining the results
    into a polished final output.
    """
    def __init__(self):
        """
        The constructor initializes the OpenAI and Anthropic API clients with the provided API keys.
        It also sets the models for orchestrator, sub-agent, and refiner tasks and initializes a list
        to keep track of task exchanges.
        """
        self.openai_client = OpenAI()
        self.anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.orchestrator_model = "gpt-3.5-turbo"
        self.sub_agent_model = "gpt-3.5-turbo"
        self.refiner_model = ANTHROPIC_MODEL_NAME
        self.task_exchanges = []

    def call_openai(self, model, messages):
        """
        This method sends a request to the OpenAI API with the specified model and messages, and returns the response content.
        """
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1500
        )
        return response.choices[0].message.content

    def call_anthropic(self, messages):
        """
        This method sends a request to the Anthropic API with the provided messages and returns the response content.
        """
        response = self.anthropic_client.messages.create(
            model=self.refiner_model,
            messages=messages,
            max_tokens=1500
        )
        return response.choices[0].message.content

    def orchestrate_task(self, objective, previous_results=None):
        """
        This method constructs a prompt to break down the main objective into the next sub-task and calls the OpenAI API to get the response.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Objective: {objective}\nPrevious results: {previous_results or 'None'}\nPlease break this down into the next sub-task."}
        ]
        return self.call_openai(self.orchestrator_model, messages)

    def execute_sub_task(self, prompt):
        """This method constructs a prompt for executing a sub-task and calls the OpenAI API to get the response."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        return self.call_openai(self.sub_agent_model, messages)

    def refine_results(self, objective, sub_task_results):
        """
        This method constructs a prompt for refining the sub-task results into a final output and calls the Anthropic API to get the response.
        """
        messages = [
            {"role": "user", "content": f"Objective: {objective}\nSub-task results: {sub_task_results}\nPlease refine these results into a cohesive final output."}
        ]
        return self.call_anthropic(messages)

    def run(self, objective):
        """
        Example objective: "Explain the concept of deep learning."
        """
        previous_results = []
        index = 0
        while True:
            orchestration_result = self.orchestrate_task(objective, previous_results)
            if "The task is complete:" in orchestration_result or index >= 2:
                final_output = orchestration_result.replace("The task is complete:", "").strip()
                break
            else:
                sub_task_prompt = orchestration_result
                sub_task_result = self.execute_sub_task(sub_task_prompt)
                self.task_exchanges.append((sub_task_prompt, sub_task_result))
                previous_results.append(sub_task_result)
                index += 1

        refined_output = self.refine_results(objective, previous_results)
        return refined_output


class LLM:
    def __init__(self, adapter_type):
        if adapter_type == "openai":
            self.adapter = OpenaiAdapter()
        elif adapter_type == "anthropic":
            self.adapter = AnthropicAdapter()
        elif adapter_type == "task_orchestrator":
            self.adapter = TaskOrchestrator()
        else:
            raise ValueError(f"Unsupported adapter type: {adapter_type}")