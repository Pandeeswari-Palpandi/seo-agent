from ddgs import DDGS


def web_search(query: str) -> str:
    """
    Search the web for recent and relevant information about a topic.

    Args:
        query: The search query.

    Returns:
        A formatted list of search results.
    """

    try:
        results = DDGS().text(
            query,
            max_results=8
        )

        if not results:
            return "No search results were found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href", "No URL")
            snippet = result.get("body", "No description")

            formatted_results.append(
                f"""
                    Result {index}:
                    Title: {title}
                    URL: {url}
                    Description: {snippet}
                """
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Web search failed: {str(e)}"
