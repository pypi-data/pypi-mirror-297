from IPython import get_ipython

def execute_child_notebooks(notebooks, arguments=None, timeout=300):
    """
    Execute a list of child notebooks and return their results.

    Parameters:
    - notebooks: A list of paths to the notebooks to execute.
    - arguments: A dictionary of arguments to pass to the child notebooks (optional).
    - timeout: Time in seconds to wait for each notebook to finish.

    Returns:
    - A list of results from each child notebook.
    """
    # Check if dbutils is defined; if not, try to retrieve it
    dbutils = globals().get("dbutils") or locals().get("dbutils") or get_ipython().user_ns.get("dbutils")
    if not dbutils:
        raise ValueError("dbutils is not available in the current scope. Make sure to run this function in Databricks.")

    results = []
    for notebook in notebooks:
        try:
            print(f"Running notebook: {notebook}")
            result = dbutils.notebook.run(notebook, timeout_seconds=timeout, arguments=arguments or {})
            results.append(result)
        except Exception as e:
            print(f"Error running notebook {notebook}: {e}")
            results.append(None)
    
    return results
