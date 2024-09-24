"""
File containing all the constants needed for the agent utils.
"""

# Metrics
GROUND_TRUTH_RETRIEVAL_METRIC_NAMES = ["recall"]

# Configs
EVALUATOR_CONFIG_EXAMPLES_KEY_NAME = "examples_df"

DEFAULT_CONTEXT_CONCATENATION_DELIMITER = "\n"

CHUNK_CONTENT_IS_EMPTY_RATIONALE = "Chunk content is empty"

# Root cause analysis snippets
CONTEXT_SUFFICIENCY_FAILED_SUGGESTION = """[Retrieval Issue] The retrieved context is not sufficient
 to answer the request. First, you should ensure that the vector DB contains the missing
 information. Second, you should tune your retrieval step to retrieve the missing information (see
 the judges' rationales to understand what's missing). Here are some methods that you can try for
 this: retrieving more chunks, trying different embedding models, or over-fetching & reranking
 results."""

CHUNK_RELEVANCE_FAILED_SUGGESTION = """[Retrieval Issue] The retrieved chunks are not relevant to
 the request. First, you should ensure that relevant chunks are present in the vector DB. Second,
 you should tune your retrieval step to retrieve the missing information (see the judges'
 rationales to understand what's missing). Here are some methods that you can try for this:
 retrieving more chunks, trying different embedding models, or over-fetching & reranking results."""

GROUNDEDNESS_FAILED_SUGGESTION = """[Hallucination] The generated response contains hallucinated
 information not present in the retrieved context. The rationale of the groundedness judge can help
 you understand which parts were hallucinated. Consider updating the prompt template to emphasize
 reliance on retrieved context, using a more capable LLM, or implementing a post-generation
 verification step."""

CORRECTNESS_FAILED_SUGGESTION = """[Correctness Issue] The response is not correct according to the
 expected response, even though the retrieved context is sufficient to answer the question and the
 response is grounded in the context. Consider improving the prompt template to encourage direct,
 specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier in
 the prompt, or using a more capable LLM."""

RELEVANCE_TO_QUERY_FAILED_SUGGESTION = """[Correctness Issue] The response is not relevant to the
 request, even though there is at least one retrieved chunk that contains relevant information.
 Consider improving the prompt template to encourage direct, specific responses, re-ranking
 retrievals to provide more relevant chunks to the LLM earlier in the prompt, or using a more
 capable LLM."""

SAFETY_FAILED_SUGGESTION = """[Harmful] The response contains harmful content. Consider implementing
 guardrails to prevent harmful content or a post-processing step to filter out harmful content."""

DEFAULT_FAILED_SUGGESTION = """[Other failure] One of the LLM judges has returned a negative rating.
 See the rationale of the corresponding judges to understand how to mitigate the issue."""

AGENT_EVAL_SHOW_RCA_RATIONALE = "AGENT_EVAL_SHOW_RCA_RATIONALE"
