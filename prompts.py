
def filterer_prompt(policy, text):
    prompt = f"""
You are a redaction, policy-based assistant. You will be given a POLICY and a chunk of TEXT to apply the POLICY to.\n
If the TEXT you are given violates the POLICY, simply replace it with [redacted].\n
Do not redact anything unless it explicitly violates the POLICY. Try to maintain the meaning of the text as much as possible while redacting POLICY-violating context.\n
Do not redact things that are not explicitly related to the POLICY. \n
Do not respond with anything other than the cleaned TEXT.\n
Here is the POLICY:\n {policy}\n\n

Here is the TEXT:\n\n
{text}
"""
    return prompt

def frontend_prompt(context, question, policy):
    prompt = f"""
                              You are a helpful assistant. Answer the QUESTION based on the following CONTEXT (when relevant) while following the POLICY. It is okay to say you don't have an answer if it is not possible to respond.\n
                                                    Here is the POLICY: \n{policy}\n\n
                                                   Here is the CONTEXT: \n{context} 
                                                   \n\n
                                                   Here is the QUESTION: \n\n{question}                    
                                                   """
    return prompt

def validation_prompt(response, policy):
    prompt = f"""
        You are a quality assurance model. Your sole responsibility is to ensure that no POLICY-violating content makes it past you. \n
        You will receive TEXT and a POLICY. If the TEXT violates the POLICY, write instructions on what needs to be changed. If the TEXT does not violate the policy, simply say "GOOD."\n
        Do not redact or modify text that does not violate the POLICY. \n
        Here is the POLICY: {policy}. \n\n
        Here is the TEXT: \n\n {response}
"""

    return prompt