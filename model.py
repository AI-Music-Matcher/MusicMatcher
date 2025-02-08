from transformers import pipeline

model  =  pipeline(
    "text-classification",
    model = "j-hartmann/emotion-english-distilroberta-base"
)



def identify_mood(text):
    model = model()
    return model.predict(text)