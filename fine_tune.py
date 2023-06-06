import openai
import config

# Set your OpenAI API key
openai.api_key = config.API_KEY

# Define your training data, you can edit this if you want
training_data = [
    {"input": "How are you", "output": "im alright"},
    {"input": "Are you retarded", "output": "ask me later"},
    # Add more training examples here
]

# define the fine-tuning configuration
config = {
    "model": "gpt-3.5-turbo",
    "steps": 1000,  # adjust the number of training steps as needed
    "batch_size": 4,  # adjust the batch size based on available resources
    "learning_rate": 1e-5,  # adjust the learning rate as needed
    "max_tokens": 100,
    "overwrite": True,
    "save_checkpoint": True,
    "save_step": 500,  # save a checkpoint every 500 steps
}

# Define the prompt format for training
prompt_format = "Question: {input}\nAnswer: {output}\n"

# Prepare the training data in the required format
formatted_training_data = [prompt_format.format(**example) for example in training_data]

# Fine-tune the model
response = openai.FineTuning.create(
    training_data=formatted_training_data,
    **config
)

# Get the fine-tuned model ID
model_id = response["model"]

# Save the fine-tuned model
openai.Model.save(model_id, "fine_tuned_model")

print("Fine-tuning completed successfully!")
