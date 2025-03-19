from collections import Counter

from service import MemoryService
from helper import Logger
from transformers import pipeline
from typing import List
from model import Memory
import spacy


class MediaDescriptionAnalysisService:
    def __init__(self):
        self.memory_service = MemoryService()
        self.logger = Logger(__name__)

        # Initialize Zero-Shot Classification pipeline
        self.category_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

        # Initialize Emotion Analysis pipeline
        self.emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

        # New GoEmotions pipeline
        # self.go_emotions_classifier = pipeline(
        #     "text-classification",
        #     model="monologg/bert-base-cased-goemotions-original",
        #     framework="pt"
        # )

        # Initialize SpaCy for tag extraction
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(self.nlp.Defaults.stop_words)

        # Define the predefined categories
        self.predefined_categories = ["family", "friends", "travel", "work", "achievements", "other"]

    def analyze_memories_by_patient_id(self, patient_id: str) -> None:
        self.logger.info("Analyzing memories for patient ID: %s", patient_id)

        # Fetch all memories for the patient
        memories = self.memory_service.get_memories_by_patient_id(patient_id)

        # Analyze memory categories
        memories = self._analyze_memory_categories(memories)

        # Analyze memory emotions
        memories = self._analyze_memory_emotions(memories)

        # Analyze memories with GoEmotions
        # self.analyze_memories_with_go_emotions(memories)

        # Analyze memory tags
        memories = self._analyze_memory_tags(memories)

        # Update memories in the database
        self.memory_service.update_memories(memories)
        self.logger.info("Memory analysis completed successfully for patient ID: %s", patient_id)

    def _analyze_memory_categories(self, memories: List[Memory]) -> List[Memory]:
        self.logger.info(f"Analyzing memory categories for {len(memories)} memories")
        for memory in memories:
            try:
                self.logger.info(f"Processing memory: {memory.title}")

                # Check description
                description = memory.description if memory.description else None
                if description is None:
                    continue

                # Perform category analysis
                categories = self._get_categories_from_description(description)
                self.logger.info(f"Categories found for memory '{memory.title}': {categories}")

                # Update memory categories
                memory.categories = categories
            except Exception as e:
                self.logger.error(f"Error processing memory '{memory.title}': {e}")
                continue

        return memories

    def _get_categories_from_description(self, description: str) -> List[str]:
        # Perform Zero-Shot Classification
        result = self.category_classifier(description, candidate_labels=self.predefined_categories, multi_label=True)

        # Filter categories with confidence score > 0.5
        categories = [label for label, score in zip(result["labels"], result["scores"]) if score > 0.5]
        return categories

    def _analyze_memory_emotions(self, memories: List[Memory]) -> List[Memory]:
        self.logger.info(f"Analyzing emotions for {len(memories)} memories")
        for memory in memories:
            try:
                self.logger.info(f"Processing memory: {memory.title}")

                # Collect all descriptions: Main + Media
                all_descriptions = self._get_all_descriptions(memory)

                if not all_descriptions:
                    self.logger.info(f"No descriptions found for memory: {memory.title}")
                    continue

                # Perform emotion analysis
                emotions = self._get_emotions_from_descriptions(all_descriptions)
                self.logger.info(f"Emotions found for memory '{memory.title}': {emotions}")

                # Update memory emotions
                memory.emotions = emotions
            except Exception as e:
                self.logger.error(f"Error processing memory '{memory.title}': {e}")
                continue

        return memories

    def _get_emotions_from_descriptions(self, descriptions: List[str]) -> List[str]:
        emotions = []

        for description in descriptions:
            # Truncate the description if it exceeds the maximum token limit
            truncated_description = self._truncate_text(description, tokenizer=self.emotion_classifier.tokenizer)

            # Perform emotion analysis on the truncated description
            try:
                result = self.emotion_classifier(truncated_description)
                emotions.extend([res["label"] for res in result if res["score"] > 0.5])
            except Exception as e:
                self.logger.error(f"Error analyzing description: {e}")
                continue

        # Remove Deduplicate emotions
        unique_emotions = list(set(emotions))

        # Remove 'Neutral' if other emotions are present
        if "neutral" in unique_emotions and len(unique_emotions) > 1:
            unique_emotions.remove("neutral")

        return unique_emotions

    # def analyze_memories_with_go_emotions(self, memories: List[Memory]) -> None:
    #     self.logger.info("Analyzing memories with GoEmotions")
    #
    #     for memory in memories:
    #         try:
    #             self.logger.info(f"Processing memory with GoEmotions: {memory.title}")
    #
    #             # Collect all descriptions: Main + Media
    #             all_descriptions = self._get_all_descriptions(memory)
    #
    #             if not all_descriptions:
    #                 self.logger.info(f"No descriptions found for memory: {memory.title}")
    #                 continue
    #
    #             # Perform emotion analysis using GoEmotions
    #             emotions = self._get_emotions_from_descriptions_with_go_emotions(all_descriptions)
    #             self.logger.info(f"GoEmotions found for memory '{memory.title}': {emotions}")
    #
    #             # Update memory emotions (separately tracked for GoEmotions)
    #             # memory.emotions = emotions
    #         except Exception as e:
    #             self.logger.error(f"Error processing memory '{memory.title}' with GoEmotions: {e}")
    #             continue
    #
    #     # Update memories in the database
    #     self.memory_service.update_memories(memories)
    #     self.logger.info("GoEmotions analysis completed successfully")

    # def _get_emotions_from_descriptions_with_go_emotions(self, descriptions: List[str]) -> List[str]:
    #     emotions = []
    #
    #     for description in descriptions:
    #         # Truncate the description if it exceeds the maximum token limit
    #         truncated_description = self._truncate_text(description, tokenizer=self.go_emotions_classifier.tokenizer)
    #
    #         # Perform emotion analysis on the truncated description
    #         try:
    #             result = self.go_emotions_classifier(truncated_description)
    #             emotions.extend([res["label"] for res in result if res["score"] > 0.5])
    #         except Exception as e:
    #             self.logger.error(f"Error analyzing description with GoEmotions: {e}")
    #             continue
    #
    #     # Deduplicate emotions
    #     unique_emotions = list(set(emotions))
    #
    #     # Remove 'Neutral' if other emotions are present
    #     if "neutral" in unique_emotions and len(unique_emotions) > 1:
    #         unique_emotions.remove("neutral")
    #
    #     return unique_emotions

    @staticmethod
    def _truncate_text(text: str, tokenizer, max_length: int = 512) -> str:
        tokens = tokenizer.encode(text, truncation=True, max_length=max_length)
        return tokenizer.decode(tokens, skip_special_tokens=True)

    def _analyze_memory_tags(self, memories: List[Memory]) -> List[Memory]:
        self.logger.info(f"Analyzing tags for {len(memories)} memories")
        for memory in memories:
            try:
                self.logger.info(f"Processing memory: {memory.title}")

                # Collect all descriptions: Main + Media
                all_descriptions = self._get_all_descriptions(memory)

                if not all_descriptions:
                    self.logger.info(f"No descriptions found for memory: {memory.title}")
                    continue

                # Generate tags
                tags = self._generate_tags_from_descriptions(all_descriptions)
                self.logger.info(f"Tags generated for memory '{memory.title}': {tags}")

                # Update memory tags
                memory.tags = tags
            except Exception as e:
                self.logger.error(f"Error processing memory '{memory.title}': {e}")
                continue

        return memories

    def _generate_tags_from_descriptions(self, descriptions: List[str], top_n: int = 10) -> List[str]:
        """Generate the top N tags from a list of descriptions."""
        combined_text = " ".join(descriptions)

        # Use SpaCy to process the text
        doc = self.nlp(combined_text)

        # Extract entities and noun chunks as tags
        raw_tags = [ent.text for ent in doc.ents] + [chunk.text for chunk in doc.noun_chunks]

        # Normalize and filter tags
        filtered_tags = self._filter_tags(raw_tags)

        # Count the frequency of each tag
        tag_counts = Counter(filtered_tags)

        # Sort and select the top N tags
        best_tags = [tag for tag, _ in tag_counts.most_common(top_n)]
        return best_tags

    def _filter_tags(self, tags: List[str]) -> List[str]:
        filtered_tags = []
        for tag in tags:
            tag = tag.lower().strip()
            tag = tag.replace("'s", "")
            tag = tag.replace("’s", "")
            if tag not in self.stop_words and len(tag) > 1:
                filtered_tags.append(tag)
        return filtered_tags

    @staticmethod
    def _get_all_descriptions(memory: Memory) -> List[str]:
        all_descriptions = [memory.description] if memory.description else []
        if memory.media:
            all_descriptions.extend(
                media.description for media in memory.media if media.description
            )
        return all_descriptions
