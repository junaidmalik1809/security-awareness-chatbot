import json
import random
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

class SecurityChatbot:
    def __init__(self, knowledge_base_path: str):
        print("[INFO] Loading Sentence Transformer model... (this may take a few seconds)")
        # Using a lightweight but strong model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.knowledge = self._load_knowledge(knowledge_base_path)
        self.patterns = []
        self.tags = []
        self.pattern_embeddings = None
        
        self._prepare_data()
        print("[INFO] Chatbot is ready!")

    def _load_knowledge(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _prepare_data(self):
        """Prepare patterns and create embeddings."""
        for tag, data in self.knowledge.items():
            if tag == "default":
                continue
            for pattern in data.get("patterns", []):
                self.patterns.append(pattern)
                self.tags.append(tag)

        # Convert all patterns into embeddings (vectors)
        self.pattern_embeddings = self.model.encode(self.patterns, convert_to_tensor=True)

    def get_response(self, user_input: str) -> str:
        # Convert user input into embedding
        user_embedding = self.model.encode(user_input, convert_to_tensor=True)

        # Calculate cosine similarity with all patterns
        similarities = util.cos_sim(user_embedding, self.pattern_embeddings)[0]

        best_score = torch.max(similarities).item()
        best_idx = torch.argmax(similarities).item()

        # Threshold (you can adjust this)
        if best_score > 0.45:
            tag = self.tags[best_idx]
            responses = self.knowledge[tag]["responses"]
            return random.choice(responses)
        else:
            return random.choice(self.knowledge["default"]["responses"])