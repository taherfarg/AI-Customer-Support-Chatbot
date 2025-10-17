# Data Directory

This directory contains the customer support Q&A dataset.

## Files

- `customer_support_qa_clean.csv` - Cleaned dataset (768K+ rows)
- `explor_the_data_set.ipynb` - Data exploration notebook

## Dataset Structure

```csv
company,input,response,conversation_id
AppleSupport,"How do I reset my password?","To reset your password...",abc123
```

## Usage

The dataset is automatically loaded by `scripts/build_vector_db.py`.

## Custom Data

To use your own data:
1. Format as CSV with columns: `company`, `input`, `response`, `conversation_id`
2. Save as `customer_support_qa_clean.csv`
3. Run: `python scripts/build_vector_db.py`

