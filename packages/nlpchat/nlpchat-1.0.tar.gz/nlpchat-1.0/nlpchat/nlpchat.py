import random
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class NlpChat:
    def __init__(self):
        self.intent_data = {"intents": []}
        self.responses = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.label_encoder = LabelEncoder()
        self.classifier = LogisticRegression()

    def add_intent(self, tag, patterns, responses):
        """
        Add intents easily by specifying a tag, patterns, and responses.
        """
        intent = {
            "tag": tag,
            "patterns": patterns,
            "responses": responses
        }
        self.intent_data["intents"].append(intent)

    def train(self):
        """
        Prepares training data and trains the Logistic Regression classifier.
        """
        patterns = []
        labels = []

        for intent in self.intent_data['intents']:
            self.responses[intent['tag']] = intent['responses']
            for pattern in intent['patterns']:
                patterns.append(pattern)
                labels.append(intent['tag'])

        # Encode labels and split data
        self.encoded_labels = self.label_encoder.fit_transform(labels)
        X_train, _, y_train, _ = train_test_split(patterns, self.encoded_labels, test_size=0.2, random_state=42)

        # Generate sentence embeddings
        X_train_embeddings = self.model.encode(X_train)

        # Train the classifier
        self.classifier.fit(X_train_embeddings, y_train)

    def save_model(self, filepath):
        """
        Save the trained model and label encoder to a file.
        """
        model_data = {
            "classifier": self.classifier,
            "label_encoder": self.label_encoder,
            "responses": self.responses
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filepath):
        """
        Load a saved model and label encoder from a file.
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
            self.classifier = model_data['classifier']
            self.label_encoder = model_data['label_encoder']
            self.responses = model_data['responses']

    def predict_intent(self, text):
        """
        Predicts the intent for the given user input.
        """
        text_embedding = self.model.encode([text])
        predicted_label = self.classifier.predict(text_embedding)
        intent = self.label_encoder.inverse_transform(predicted_label)[0]
        return intent

    def get_response(self, text):
        """
        Returns a response for the given user input based on the predicted intent.
        """
        intent = self.predict_intent(text)
        return random.choice(self.responses[intent])
    
    def get_intent(self, text):
        """
        Returns only the predicted intent for the given user input.
        """
        return self.predict_intent(text)
