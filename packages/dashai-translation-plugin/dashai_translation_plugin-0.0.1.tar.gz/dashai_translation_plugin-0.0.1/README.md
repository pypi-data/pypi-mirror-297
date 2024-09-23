# **Translation Plugin**

## **Components included**

The ML components included in this plugin are the following:

### **Task**

- Translation Task

### **Models**

The translation models come from HuggingFace, and these are:

- Helsinki-NLP/opus-mt-en-es: This model translates from English to Spanish using transformers (more information about the model is available [here](https://huggingface.co/Helsinki-NLP/opus-mt-en-es)).

### **Metrics**

The metrics included in this plugin come from the [*evaluation*](https://pypi.org/project/evaluate/) library, and these are:

- BLEU: measures the precision of n-grams between a machine-generated translation and one or more reference translations, evaluating similarity
- TER: calculates the number of edits (insertions, deletions, substitutions, and reordering) needed to transform a machine-generated translation into the reference translation.

