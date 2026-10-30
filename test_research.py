import asyncio

from agents import create_agent_team


async def run_pipeline(topic, agent_team):
    (
        research_agent,
        content_writer_agent,
        seo_optimizer_agent,
        content_review_agent,
    ) = agent_team

    print("\n" + "=" * 70)
    print("STEP 1: SEO RESEARCH")
    print("=" * 70)

    research_result = await research_agent.run(
        task=f"""
        Research the following topic for an SEO content project:

        TOPIC:
        {topic}

        Perform web research and identify:

        - Current trends
        - Important subtopics
        - Search intent
        - Primary keywords
        - Secondary keywords
        - Long-tail keywords
        - Questions users may search
        - Recent developments
        - Content opportunities
        - Recommended article angles

        Return a structured research report.
        """
    )

    research_report = research_result.messages[-1].content

    print("\n" + "=" * 70)
    print("RESEARCH REPORT")
    print("=" * 70)

    print(research_report)

    print("\n" + "=" * 70)
    print("STEP 2: CONTENT WRITING")
    print("=" * 70)

    writer_result = await content_writer_agent.run(
        task=f"""
        Create an SEO-friendly article based on the following research report.

        TOPIC:
        {topic}

        RESEARCH REPORT:
        {research_report}

        Write the complete article.

        Include:

        - SEO-friendly title
        - Introduction
        - H1/H2/H3 structure
        - Main content
        - Relevant keywords
        - Examples where useful
        - FAQ section where appropriate
        - Conclusion

        Make the article useful, readable and natural.
        """
    )

    article = writer_result.messages[-1].content

    print("\n" + "=" * 70)
    print("STEP 3: SEO OPTIMIZATION")
    print("=" * 70)

    optimizer_result = await seo_optimizer_agent.run(
        task=f"""
        Optimize the following article for SEO.

        ORIGINAL TOPIC:
        {topic}

        RESEARCH REPORT:
        {research_report}

        DRAFT ARTICLE:
        {article}

        Perform a complete SEO audit and then provide the
        optimized article.

        Make sure the optimized article:

        - Satisfies search intent
        - Uses keywords naturally
        - Has a strong SEO title
        - Has a good meta description
        - Has proper H1/H2/H3 structure
        - Is readable
        - Avoids keyword stuffing
        - Provides useful information
        - Contains an appropriate FAQ section
        """
    )
    optimized_content = optimizer_result.messages[-1].content

    print("\n" + "=" * 70)
    print("STEP 4: FINAL CONTENT REVIEW")
    print("=" * 70)

    review_result = await content_review_agent.run(
        task=f"""
        Perform the final review of the following SEO article.

        ORIGINAL TOPIC:
        {topic}

        RESEARCH REPORT:
        {research_report}

        SEO-OPTIMIZED ARTICLE:
        {optimized_content}

        Review the content for:

        - Accuracy
        - Relevance
        - Search intent
        - Readability
        - Grammar
        - Structure
        - Repetition
        - Content quality
        - SEO quality
        - Overall reader experience

        Fix any issues you find.

        Then provide the final publish-ready article.
        """
    )

    final_content = review_result.messages[-1].content

    print("\n" + "=" * 70)
    print("FINAL REVIEW RESULT")
    print("=" * 70)

    print(final_content)


async def main():
    topic = input("Enter a topic for SEO content: ")
    model_client, agent_team = create_agent_team()
    try:
        await run_pipeline(topic, agent_team)
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
