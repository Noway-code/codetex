import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer,  # Change here
    Seq2SeqTrainingArguments,  # Change here
    DataCollatorForSeq2Seq,
)
from datasets import load_dataset, DatasetDict
import numpy as np
from evaluate import load

bleu = load("bleu")

# Load the dataset directly from a CSV file
dataset = load_dataset('csv', data_files='seq2seq/dataset.csv')

# Ensure the dataset has 'code' and 'equation' columns
print("Dataset columns:", dataset['train'].column_names)

# Split the dataset into train, validation, and test sets
# First, split into train and test sets
dataset = dataset['train'].train_test_split(test_size=0.1)

# Then, split the test set equally into validation and test sets
test_valid = dataset['test'].train_test_split(test_size=0.5)

# Create a DatasetDict to hold the splits
dataset = DatasetDict({
    'train': dataset['train'],
    'validation': test_valid['train'],
    'test': test_valid['test'],
})

# Initialize the tokenizer and model
model_name = "t5-small"  # You can replace this with another model like 't5-base'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenization function using 'text_target' for target sequences
def tokenize_function(examples):
    model_inputs = tokenizer(
        examples['code'],
        max_length=512,
        truncation=True,
        padding=False,  # Padding is handled by the data collator
    )
    labels = tokenizer(
        text_target=examples['equation'],
        max_length=256,
        truncation=True,
        padding=False,
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Apply the tokenization function to the entire dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    # Decode the predictions and labels
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    # Post-process
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [label.strip() for label in decoded_labels]
    decoded_labels = [[label] for label in decoded_labels]  # BLEU expects references as list of lists
    # Compute BLEU score
    result = bleu.compute(predictions=decoded_preds, references=decoded_labels)
    return {"bleu": result["bleu"]}

training_args = Seq2SeqTrainingArguments(  # Change here
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=10,
    logging_dir="./logs",
    logging_steps=10,
    predict_with_generate=True,  # Add this line (if supported)
)

trainer = Seq2SeqTrainer(  # Change here
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    compute_metrics=compute_metrics,
    # If 'predict_with_generate' is not accepted here, ensure it's in 'Seq2SeqTrainingArguments'
)

trainer.train()

trainer.save_model("t5-code-to-math")
tokenizer.save_pretrained("t5-code-to-math")

# Evaluate the model on the test set
results = trainer.evaluate(tokenized_datasets["test"])
print("Evaluation results:", results)

# Prepare the model for inference
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

# Function to generate an equation from a code snippet
def generate_equation(code_snippet):
    with torch.no_grad():
        inputs = tokenizer.encode(
            code_snippet,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(device)
        outputs = model.generate(
            inputs,
            max_length=256,
            num_beams=4,
            early_stopping=True,
        )
        equation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return equation

# Example usage of the inference function
code_example = "def add(a, b):\n    return a + b"
print("Generated Equation:", generate_equation(code_example))
