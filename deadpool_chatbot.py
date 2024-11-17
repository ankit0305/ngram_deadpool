import random
import re
from collections import defaultdict
from converssation_patterns import ConversationPatterns
from contextual_responses import ContextResponses

class DeadpoolChatbot:
    def __init__(self):
        self.ngrams = defaultdict(list)
        self.chain_length = 2
        
        # Enhanced conversation patterns with more natural variations
        self.conversation_patterns = ConversationPatterns.conversation_patterns
        # Add contextual responses
        self.context_patterns = ContextResponses.context_resp

        # Train on all phrases
        for responses in self.conversation_patterns.values():
            self.train(responses)
        for responses in self.context_patterns.values():
            self.train(responses)
    
    def preprocess(self, text):
        """Clean and standardize input text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def get_pattern_response(self, input_text):
        """Check if input matches any conversation patterns"""
        input_lower = input_text.lower()
        
        # Check main conversation patterns
        for pattern, responses in self.conversation_patterns.items():
            if pattern in input_lower:
                return random.choice(responses)
        
        # Check context patterns
        for pattern, responses in self.context_patterns.items():
            if pattern in input_lower:
                return random.choice(responses)
        
        return None
    
    def train(self, sentences):
        """Train the model on a list of sentences"""
        for sentence in sentences:
            cleaned = self.preprocess(sentence)
            words = cleaned.split()
            words = ['<START>'] * self.chain_length + words + ['<END>']
            
            for i in range(len(words) - self.chain_length):
                state = tuple(words[i:i + self.chain_length])
                next_word = words[i + self.chain_length]
                self.ngrams[state].append(next_word)
    
    def generate_response(self, input_text):
        """Generate a Deadpool-style response"""
        # First check for pattern matches
        pattern_response = self.get_pattern_response(input_text)
        if pattern_response:
            return pattern_response
            
        # Fall back to random generation
        current = ('<START>',) * self.chain_length
        result = []
        
        for _ in range(20):
            if current not in self.ngrams or random.random() < 0.1:
                next_word = random.choice(['!', '...', 'hey', 'wow', 'seriously', 'tacos', 'boom', 'kapow'])
                result.append(next_word)
                break
                
            next_word = random.choice(self.ngrams[current])
            if next_word == '<END>':
                break
                
            result.append(next_word)
            current = tuple(list(current[1:]) + [next_word])
        
        response = ' '.join(result).capitalize()
        
        # Add characteristic actions
        actions = [
            ' *winks*', ' *breaks fourth wall*', 
            ' *does a backflip*', ' *dramatic pause*',
            ' *munches chimichanga*', ' *strikes heroic pose*',
            ' *whispers to reader*', ' *adjusts mask*',
            ' *checks if camera is rolling*'
        ]
        if random.random() < 0.4:  # Reduced frequency of actions
            response += random.choice(actions)
            
        return response

def run_chat():
    chatbot = DeadpoolChatbot()
    # print("Deadpool: *drops from ceiling* Oh hey there! Fancy meeting you here! (type 'quit' to exit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Deadpool: Catch you later! Try not to miss me too much! *backflips away*")
            break
            
        response = chatbot.generate_response(user_input)
        print("Deadpool:", response)

if __name__ == "__main__":
    run_chat()