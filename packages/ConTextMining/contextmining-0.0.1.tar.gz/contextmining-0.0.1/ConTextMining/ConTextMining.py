import transformers
import torch
import gc



def instantiate_pipeline_llama(access_token):
    '''
    instantiates pipeline for llama instruction tuned model
    
    Parameters:
    - access_token (str; required): huggingface access token, for more details refer to https://huggingface.co/docs/hub/en/security-tokens
    
    Returns: 
    Object: a text-generation pipeline from model "meta-llama/Meta-Llama-3.1-8B-Instruct"
    '''
    transformers.set_seed(42)
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    
    pipe = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        token=access_token,
        device_map="auto"
    )
    return(pipe)


def instantiate_pipeline_gemma(access_token):
    '''
    instantiates pipeline for gemma instruction tuned model
    
    Parameters:
    - access_token (str; required): huggingface access token, for more details refer to https://huggingface.co/docs/hub/en/security-tokens
    
    Returns: 
    Object: a text-generation pipeline from model "google/gemma-2-2b-it"
    '''
    transformers.set_seed(42)
    model_id = "google/gemma-2-2b-it"
    pipe = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        token=access_token,
        device="cuda"
    )
    return(pipe)


def instantiate_pipeline_phi(access_token):
    
    '''
    instantiates pipeline for phi instruction tuned model
    Parameters:
    - access_token (str; required): huggingface access token, for more details refer to https://huggingface.co/docs/hub/en/security-tokens
    
    Returns: 
    Object: a text-generation pipeline from model "microsoft/Phi-3-mini-4k-instruct"
    '''
    transformers.set_seed(42)
    model_id = "microsoft/Phi-3-mini-4k-instruct"
    pipe = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        token=access_token,
        device_map="auto"
    )
    return(pipe)





def get_labels_llama_and_phi(topic_modeling_keywords, pipe, keywords_examples, labels_examples):
    '''
    generates topic model labels from the provided topic model's keywords (topic_modeling_keywords) with few-shot in-context learning using either llama or phi pre-trained model
    
    Paramters:
    - topic_modeling_keywords (str; required): keywords for the topic model to label
    - pipe (object; required): pipeline of instantiated pre-trained model used
    - keyword_examples (list, required): List of keywords from the few-shot examples
    - labels_examples (list, required): List of labels from the few-shot examples. 
    
    Returns:
    str: Labels of topic models
    '''
    
    # Enhanced prompt structure with clearer instructions
    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant trained to assign a single, most relevant label to a given set of keywords "
            "derived from topic modeling. These labels should be concise and align with the examples provided."
        )},
        {"role": "assistant", "content": "Here are some examples to guide you:"}
    ]
    
    for keywords, labels in zip(keywords_examples, labels_examples):
        messages.append({"role": "assistant", "content": f"Example Keywords: {keywords}"})
        messages.append({"role": "assistant", "content": f"Assigned Label: {labels}"})
    
    # Explicit instruction for labeling
    messages.append({"role": "user", "content": (
        f"Label the following sets of keywords with a single, most relevant label. Do not provide multiple labels.\n{topic_modeling_keywords}"
    )})

    outputs = pipe(
        messages,
        max_new_tokens=256,
        do_sample=False,
        temperature=0.1,
        pad_token_id=pipe.tokenizer.pad_token_id,
        top_k=2,
        eos_token_id=pipe.tokenizer.eos_token_id 
        
    )

    # Clear cache to free up GPU memory
    gc.collect()
    torch.cuda.empty_cache()

    # Return the generated label from the output
    return outputs[0]["generated_text"][-1]["content"]



def get_labels_gemma(topic_modeling_keywords, pipe, keywords_examples, labels_examples):
    '''
    generates topic model labels from the topic model's keywords (topic_modeling_keywords) with few-shot in-context learning using gemma pre-trained model
    
    Parameters:
    - topic_modeling_keywords (str; required): keywords for the topic model to label
    - pipe (object; required): pipeline of instantiated pre-trained model used
    - keyword_examples (list, required): List of keywords from the few-shot examples
    - labels_examples (list, required): List of labels from the few-shot examples. 
    
    Returns:
    str: Labels of topic models
    '''
    messages = [
        {"role": "user", "content": (
            "You are a helpful assistant trained to assign a single, most relevant label to a given set of keywords "
            "derived from topic modeling. These labels should be concise and align with the examples provided. "
        )},
        {"role": "assistant", "content": "Here are some examples to guide you:"}
    ]
    
    # Add example conversation with alternating roles
    for keywords, labels in zip(keywords_examples, labels_examples):
        messages.append({"role": "user", "content": f"Example Keywords: {keywords}"})
        messages.append({"role": "assistant", "content": f"Assigned Label: {labels}"})
    
    # Final task with alternating roles
    messages.append({"role": "user", "content": (
        f"Label the following sets of keywords with a single, most relevant label. Do not provide multiple labels.\n{topic_modeling_keywords}"
    )})
    outputs = pipe(
        messages,
        max_new_tokens=256,
        do_sample=False,
        temperature=0.1,
        pad_token_id=pipe.tokenizer.pad_token_id,
        eos_token_id=pipe.tokenizer.eos_token_id
    )

    # Clear cache to free up GPU memory
    gc.collect()
    torch.cuda.empty_cache()

    # Return the generated label from the output
    return outputs[0]["generated_text"][-1]["content"].strip()



def get_topic_labels(topic_modeling_keywords, keywords_examples, labels_examples, model_id="google/gemma-2-2b-it", access_token=None):
    '''
    Based on the appropriate model (model_id), it generates the instantiates the pipeline of the selected pre-trained model
    and generates the topic labels based on the provided topic model's keywords using few-shot ICL
     Parameters:
    - topic_modeling_keywords (str; required): keywords for the topic model to label
    - keyword_examples (list, required): List of keywords from the few-shot examples
    - labels_examples (list, required): List of labels from the few-shot examples. 
    - model_id (str, required): huggingface model_id of choice. For now, its a choice between ["microsoft/Phi-3-mini-4k-instruct", "meta-llama/Meta-Llama-3.1-8B-Instruct", "google/gemma-2-2b-it"]. Defaults to "google/gemma-2-2b-it"
    - access_token (str, required): str of huggingface access token. 
    '''
    
    # Check if the model_id is valid
    valid_model_ids = ["microsoft/Phi-3-mini-4k-instruct", "meta-llama/Meta-Llama-3.1-8B-Instruct", "google/gemma-2-2b-it"]
    if model_id not in valid_model_ids:
        raise ValueError(f"Invalid model_id '{model_id}'. It must be one of {valid_model_ids}.")
    
    # Check if access_token is provided
    if access_token is None:
        raise ValueError("An access token must be provided.")

    # Proceed with instantiating the pipeline based on model_id
    if model_id == "microsoft/Phi-3-mini-4k-instruct":
        pipe = instantiate_pipeline_phi(access_token)
        labels = get_labels_llama_and_phi(topic_modeling_keywords, pipe, keywords_examples, labels_examples)
    elif model_id == "meta-llama/Meta-Llama-3.1-8B-Instruct":
        pipe = instantiate_pipeline_llama(access_token)
        labels = get_labels_llama_and_phi(topic_modeling_keywords, pipe, keywords_examples, labels_examples)
    elif model_id == "google/gemma-2-2b-it":
        pipe = instantiate_pipeline_gemma(access_token)
        labels = get_labels_gemma(topic_modeling_keywords, pipe, keywords_examples, labels_examples)
    
    return labels
