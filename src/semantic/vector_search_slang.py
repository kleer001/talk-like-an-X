import json
import pathlib
from typing import Dict, List, Optional
import spacy
from spacy.tokens import Token

class SlangMapper:
    """
    Handles semantic mapping between 'Base English' and Subculture Slang
    using Cosine Similarity via spaCy word vectors.
    """
    def __init__(self, model_name: str = "en_core_web_md", threshold: float = 0.7):
        self.nlp = spacy.load(model_name)
        self.threshold = threshold
        self.anchors: Dict[str, spacy.tokens.Span] = {}
        self.slang_map: Dict[str, str] = {}
        self.augmentation: Dict = {}

    def load_culture(self, file_path: pathlib.Path) -> None:
        """Loads a culture JSON and pre-vectorizes the keys for performance."""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        subs = data.get("substitutions", {})
        # Vectorize keys once (The 'Anchor' words)
        self.anchors = {word: self.nlp(word) for word in subs.keys()}
        self.slang_map = subs
        self.augmentation = data.get("sentence_augmentation", [])

    def _get_best_slang(self, token: Token) -> str:
        """Finds the nearest semantic neighbor above the threshold."""
        if not token.has_vector or not self.anchors:
            return token.text

        # Exact match check (O(1) optimization)
        if token.lemma_.lower() in self.slang_map:
            return self.slang_map[token.lemma_.lower()]

        # Vector search
        best_match = None
        highest_sim = 0.0

        for base_word, vector in self.anchors.items():
            sim = token.similarity(vector)
            if sim > highest_sim:
                highest_sim = sim
                best_match = base_word

        if best_match and highest_sim >= self.threshold:
            return self.slang_map[best_match]

        return token.text

    def translate_sentence(self, sentence: str) -> str:
        """Processes a sentence, protecting functional words and mapping content words."""
        doc = self.nlp(sentence)
        result = []

        for token in doc:
            # POS Filter: Only translate Nouns, Verbs, Adjectives, Adverbs
            if token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}:
                slang_word = self._get_best_slang(token)
                result.append(slang_word)
            else:
                # Returns protected functional word (the, and, in, etc)
                result.append(token.text)

        return self._format_output(" ".join(result))

    def _format_output(self, text: str) -> str:
        """Stub for capitalization, punctuation, and augmentation logic."""
        # Simple implementation: ensures punctuation isn't spaced out
        return text.replace(" .", ".").replace(" ,", ",").strip()

class DialogueEngine:
    """Orchestrates the selection of culture templates."""
    def __init__(self, template_dir: str = "src/cultures/templates/"):
        self.template_path = pathlib.Path(template_dir)
        self.mapper = SlangMapper()

    def get_npc_response(self, base_text: str, culture_name: str) -> str:
        culture_file = self.template_path / f"{culture_name}.json"
        if not culture_file.exists():
            raise FileNotFoundError(f"Culture {culture_name} not found.")
        
        self.mapper.load_culture(culture_file)
        return self.mapper.translate_sentence(base_text)

# Example Usage:
if __name__ == "__main__":
    engine = DialogueEngine()
    
    # NPC wants to say 'I have no currency for this expensive rocket'
    # 'Currency' is not in the JSON, but 'Money' is.
    # 'Rocket' is not in the JSON, but 'Car' or 'Place' might be semantically closer.
    
    raw_speech = "I have no currency for this expensive rocket."
    beatnik_speech = engine.get_npc_response(raw_speech, "beatnik_1950s")
    
    print(f"Base: {raw_speech}")
    print(f"Beatnik: {beatnik_speech}")
