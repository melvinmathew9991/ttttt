import os  
import functools  
import time  
from langchain_community.llms import Ollama  
from langchain_openai import ChatOpenAI  
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  
from langchain.callbacks.manager import CallbackManager  

# Define a cache decorator to cache responses
def cache(func):
    """
    Decorator function to cache the results of expensive function calls.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    cached_results = {}  # Initialize an empty dictionary to store cached results

    @functools.wraps(func)  # Preserve function metadata
    def wrapper(*args, **kwargs):
        """
        Wrapper function to cache results and avoid repeated computation.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            The cached result of the decorated function.
        """
        key = str(args) + str(kwargs)  # Generate a unique key for the function call
        if key not in cached_results:  # Check if the result is already cached
            cached_results[key] = func(*args, **kwargs)  # Cache the result if not already cached
        return cached_results[key]  # Return the cached result

    return wrapper  # Return the decorated function

@cache  # Apply the cache decorator to the function
def initialize_model(model_type):
    """
    Initialize the specified language model and cache the result.

    Args:
        model_type (str): The type of language model to initialize.

    Returns:
        langchain_community.llms.Ollama or langchain_openai.ChatOpenAI: The initialized language model, or None if initialization fails.
    """
    try:
        start_time = time.time() 
        if model_type == "ollama":
            model_name = os.environ.get("OLLAMA_MODEL_NAME", "phi3")  
            model = Ollama(  
                model=model_name,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
        elif model_type == "openai":
            model = ChatOpenAI(  # Initialize ChatOpenAI model with specified parameters
                temperature=0.1,
                convert_system_message_to_human=True
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")  
        
        end_time = time.time()  
        elapsed_time = end_time - start_time  
        print(f"Time taken for {model_type} model initialization:", elapsed_time, "seconds")  

        return model  
    except ValueError as e:
        print("Error occurred during model initialization:", e)  
        return None  
