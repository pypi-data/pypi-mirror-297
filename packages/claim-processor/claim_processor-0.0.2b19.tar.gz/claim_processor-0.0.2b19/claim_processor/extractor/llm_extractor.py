from typing import List
from tqdm import tqdm

from .extractor_base import ExtractorBase
from ..utils import get_model_batch_response, get_llm_full_name
from ..base import RCText, ExtractionResult
from .extractor_prompts import *

# Set up logging
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LLMExtractor(ExtractorBase):
    def __init__(
        self,
        model: str,
        feature_key: str = None,
        api_base: str = None,
        claim_format: str = "triplet",
        batch_size: int = 16,
        model_config: dict()
    ) -> None:
        super().__init__(claim_format)

        self.feature_key = feature_key
        self.model = get_llm_full_name(model)
        self.batch_size = batch_size
        self.api_base = api_base
        self.model_config = model_config
        logger.info(
            f"Initialized LLMExtractor with model: {self.model}, batch_size: {self.batch_size}"
        )

    def extract_subsentence_claims(
        self, batch_responses, batch_questions=None, max_new_tokens=1024
    ):
        """Extract subsentence claims from the response text.
        Parameters
        ----------
        response : List[str]
            List of model response texts.
        question : List[str|None] | None
            List of questions corresponding to each response.
        max_new_tokens : int, optional
            Maximum number of tokens to generate, defaults to 500.
        Returns
        -------
        List[ExtractionResult]
            List of extracted claims for each response.
        """

        prompt_list = []
        result_list = []
        rc_responses = []
        for _i, r in enumerate(batch_responses):
            rc_r = RCText(r)
            indexed_r_text = rc_r.get_indexed_response(condense_newlines=True)
            q = None
            if batch_questions:
                q = batch_questions[_i]
            if q and len(q):
                prompt = LLM_Triplet_To_Claim_PROMPT_Q.format(q=q, r=indexed_r_text)
            else:
                raise NotImplementedError
            prompt_list.append(prompt)
            rc_responses.append(rc_r)

        logger.info(f"Extracting subsentence claims with {len(prompt_list)} prompts")
        for _i in tqdm(range(0, len(prompt_list), self.batch_size)):
            batch_prompts = prompt_list[_i : _i + self.batch_size]

            if self.feature_key:
                llm_responses = get_model_batch_response(
                    feature_key=self.feature_key,
                    prompts=batch_prompts,
                    temperature=0,
                    model=self.model,
                    n_choices=1,
                    max_new_tokens=max_new_tokens,
                    model_config=self.model_config,
                )
            else:
                llm_responses = get_model_batch_response(
                    prompts=batch_prompts,
                    temperature=0,
                    model=self.model,
                    n_choices=1,
                    max_new_tokens=max_new_tokens,
                    model_config=self.model_config,
                )

            if llm_responses and len(llm_responses):
                for _j, res in enumerate(llm_responses):
                    claims = self.parse_claims(
                        res,
                        claim_starting_prefix="### Claims",
                        excluded_content_prefix="### Question",
                        response_sentence_ids=rc_responses[_i + _j].get_sentence_ids(),
                    )
                    result = ExtractionResult(
                        claims=claims,
                        response=rc_responses[_i + _j],
                        extractor_response=res,
                    )
                    result_list.append(result)
            else:
                logger.warning("No LLM responses received")
                return None

        logger.info(
            f"Extracted a total of {sum(len(r.claims) for r in result_list)} claims"
        )
        return result_list

    def extract_claim_triplets(
        self, batch_responses, batch_questions=None, max_new_tokens=1024
    ):
        """Extract KG triplets from the response text.
        Parameters
        ----------
        response : List[str]
            List of model response texts.
        question : List[str|None] | None
            List of questions corresponding to each response.
        max_new_tokens : int, optional
            Maximum number of tokens to generate, defaults to 500.
        Returns
        -------
        List[ExtractionResult]
            List of extracted claims for each response.
        """

        prompt_list = []
        result_list = []

        for _i, r in enumerate(batch_responses):
            q = None
            if batch_questions:
                q = batch_questions[_i]
            if q is None:
                prompt = LLM_TRIPLET_EXTRACTION_PROMPT.format(input_text=r)
            else:
                prompt = LLM_TRIPLET_EXTRACTION_PROMPT_Q.format(q=q, a=r)
            prompt_list.append(prompt)

        logger.info(f"Extracting claim triplets for {len(batch_responses)} responses")

        for _i in tqdm(range(0, len(prompt_list), self.batch_size)):
            batch_prompts = prompt_list[_i : _i + self.batch_size]

            if self.feature_key:
                llm_responses = get_model_batch_response(
                    feature_key=self.feature_key,
                    prompts=batch_prompts,
                    temperature=0,
                    model=self.model,
                    n_choices=1,
                    max_new_tokens=max_new_tokens,
                    api_base=self.api_base,
                    model_config=self.model_config,
                )
            else:
                llm_responses = get_model_batch_response(
                    prompts=batch_prompts,
                    temperature=0,
                    model=self.model,
                    n_choices=1,
                    max_new_tokens=max_new_tokens,
                    api_base=self.api_base,
                    model_config=self.model_config,
                )

            if llm_responses and len(llm_responses):
                for res in llm_responses:
                    claims = self.parse_claims(res, "###")
                    result = ExtractionResult(
                        claims=claims, response=None, extractor_response=res
                    )
                    result_list.append(result)
            else:
                logger.warning("No LLM responses received")
                return None

        logger.info(
            f"Extracted a total of {sum(len(r.claims) for r in result_list)} claim triplets"
        )
        return result_list
