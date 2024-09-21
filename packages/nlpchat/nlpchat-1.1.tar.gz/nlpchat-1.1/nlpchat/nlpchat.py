from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

class NlpChat:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = LogisticRegression()
        self.label_encoder = LabelEncoder()
        self.intents = []

    def add_intent(self, tag, patterns, responses):
        self.intents.append({
            'tag': tag,
            'patterns': patterns,
            'responses': responses
        })

    def train(self):
        sentences = []
        labels = []

        for intent in self.intents:
            for pattern in intent['patterns']:
                sentences.append(pattern)
                labels.append(intent['tag'])

        # Encode the labels
        encoded_labels = self.label_encoder.fit_transform(labels)

        # Convert sentences to embeddings
        sentence_embeddings = self.model.encode(sentences)

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(sentence_embeddings, encoded_labels, test_size=0.2, random_state=42)

        # Initialize and train a Logistic Regression classifier
        self.classifier.fit(X_train, y_train)

        # Test the classifier
        y_pred = self.classifier.predict(X_test)
        accuracy = (y_pred == y_test).mean()
        print(f"Training completed. Test accuracy: {accuracy * 100:.2f}%")

    def get_response(self, user_input):
        # Encode the new sentence
        embedding = self.model.encode([user_input])
        
        # Predict the intent
        predicted_label = self.classifier.predict(embedding)
        predicted_intent = self.label_encoder.inverse_transform(predicted_label)[0]

        # Find the corresponding response
        for intent in self.intents:
            if intent['tag'] == predicted_intent:
                return np.random.choice(intent['responses'])


    def get_intent(self, user_input):
        # Encode the new sentence
        embedding = self.model.encode([user_input])
        
        # Predict the intent
        predicted_label = self.classifier.predict(embedding)
        predicted_intent = self.label_encoder.inverse_transform(predicted_label)[0]
        
        return predicted_intent

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.classifier, self.label_encoder), f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.classifier, self.label_encoder = pickle.load(f)
    

