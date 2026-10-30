import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow

from agents import create_agent_team


def create_seo_workflow(
    agents: tuple[
        AssistantAgent,
        AssistantAgent,
        AssistantAgent,
        AssistantAgent,
    ],
):
    (
        research_agent,
        content_writer_agent,
        seo_optimizer_agent,
        content_review_agent,
    ) = agents

    builder = DiGraphBuilder()

    builder.add_node(research_agent)
    builder.add_node(content_writer_agent)
    builder.add_node(seo_optimizer_agent)
    builder.add_node(content_review_agent)

    builder.add_edge(
        research_agent,
        content_writer_agent
    )

    builder.add_edge(
        content_writer_agent,
        seo_optimizer_agent
    )

    builder.add_edge(
        seo_optimizer_agent,
        content_review_agent
    )

    graph = builder.build()

    flow = GraphFlow(
        participants=builder.get_participants(),
        graph=graph,
    )

    return flow


async def run_seo_workflow(topic: str):
    model_client, agents = create_agent_team()
    try:
        flow = create_seo_workflow(agents)

        task = f"""
Create high-quality SEO content for the following topic:

{topic}

Follow this workflow:

1. Research the topic using web search.
2. Identify current trends and relevant keywords.
3. Write a useful SEO-friendly article.
4. Optimize the article for SEO.
5. Perform a final editorial review.
6. Return the final publish-ready article.
"""

        return await flow.run(task=task)
    finally:
        await model_client.close()


def extract_workflow_messages(result):

    messages = []

    for message in result.messages:

        content = getattr(message, "content", None)

        if isinstance(content, str) and content.strip():
            messages.append({
                "source": getattr(
                    message,
                    "source",
                    "unknown"
                ),
                "content": content,
            })

    return messages


def build_structured_result(topic, result):

    messages = extract_workflow_messages(result)

    research = ""
    article = ""
    seo = ""
    review = ""

    for message in messages:

        source = message["source"]
        content = message["content"]

        if source == "seo_research_agent":
            research = content

        elif source == "content_writer_agent":
            article = content

        elif source == "seo_optimizer_agent":
            seo = content

        elif source == "content_review_agent":
            review = content

    return {
        "topic": topic,
        "research": research,
        "article": article,
        "seo": seo,
        "review": review,
        "final_content": review,
    }


async def generate_seo_content(topic):

    result = await run_seo_workflow(topic)

    structured_result = build_structured_result(
        topic,
        result
    )

    return structured_result


def generate_seo_content_sync(topic):

    return asyncio.run(
        generate_seo_content(topic)
    )


if __name__ == "__main__":

    topic = input(
        "Enter a topic for SEO content: "
    )

    result = generate_seo_content_sync(topic)

    print("\n" + "=" * 70)
    print("FINAL SEO CONTENT")
    print("=" * 70)

    print(result["final_content"])
